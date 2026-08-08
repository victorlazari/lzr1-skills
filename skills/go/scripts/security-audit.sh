#!/usr/bin/env bash
# Read-only Go project security checks with explicit tool-install consent.

set -euo pipefail

readonly VERIFIED_GOVULNCHECK_VERSION="v1.6.0" # Verified 2026-08-07 via pkg.go.dev.
DRY_RUN=0
TARGET_DIR="."
INSTALL_VERSION=""
TEMP_BIN_DIR=""

show_help() {
    cat <<EOF
Usage: $0 [options] [target_dir]

Options:
  -h, --help                         Show this help message
  --dry-run                          Preview exact checks without running them
  --install-govulncheck VERSION      Explicitly authorize a temporary, exact-version
                                     install when govulncheck is unavailable
                                     (current verified example: ${VERIFIED_GOVULNCHECK_VERSION})

Arguments:
  target_dir                         Go module directory (default: current directory)

The optional install uses GOTOOLCHAIN=local and a temporary GOBIN. It never uses
@latest or writes a binary into the user's normal bin directory. Go may still
populate its module cache and govulncheck may query the Go vulnerability database.
EOF
}

cleanup() {
    if [[ -n "$TEMP_BIN_DIR" && -d "$TEMP_BIN_DIR" ]]; then
        rm -rf -- "$TEMP_BIN_DIR"
    fi
}
trap cleanup EXIT HUP INT TERM

positionals=0
while (($# > 0)); do
    case "$1" in
        -h|--help)
            show_help
            exit 0
            ;;
        --dry-run)
            DRY_RUN=1
            shift
            ;;
        --install-govulncheck)
            if (($# < 2)); then
                echo "Error: --install-govulncheck requires an exact version." >&2
                exit 2
            fi
            INSTALL_VERSION="$2"
            shift 2
            ;;
        --install-govulncheck=*)
            INSTALL_VERSION="${1#*=}"
            shift
            ;;
        --)
            shift
            if (($# > 1)); then
                echo "Error: only one target_dir is supported." >&2
                exit 2
            fi
            if (($# == 1)); then
                TARGET_DIR="$1"
                positionals=1
                shift
            fi
            ;;
        -*)
            echo "Error: unknown option: $1" >&2
            exit 2
            ;;
        *)
            if ((positionals > 0)); then
                echo "Error: only one target_dir is supported." >&2
                exit 2
            fi
            TARGET_DIR="$1"
            positionals=1
            shift
            ;;
    esac
done

if [[ -n "$INSTALL_VERSION" && ! "$INSTALL_VERSION" =~ ^v[0-9]+\.[0-9]+\.[0-9]+([.-][0-9A-Za-z.-]+)?$ ]]; then
    echo "Error: install version must be an exact Go semantic version such as ${VERIFIED_GOVULNCHECK_VERSION}." >&2
    exit 2
fi
if [[ ! -d "$TARGET_DIR" ]]; then
    echo "Error: target directory does not exist: $TARGET_DIR" >&2
    exit 2
fi
if ! command -v go >/dev/null 2>&1; then
    echo "Error: go is required." >&2
    exit 2
fi

TARGET_DIR="$(cd -- "$TARGET_DIR" && pwd -P)"
if [[ ! -f "$TARGET_DIR/go.mod" ]]; then
    echo "Error: no go.mod found in target module: $TARGET_DIR" >&2
    exit 2
fi

GOVULNCHECK_BIN=""
if command -v govulncheck >/dev/null 2>&1; then
    GOVULNCHECK_BIN="$(command -v govulncheck)"
elif [[ -z "$INSTALL_VERSION" ]]; then
    if ((DRY_RUN)); then
        GOVULNCHECK_BIN="govulncheck"
    else
        echo "Error: govulncheck is unavailable." >&2
        echo "Install it separately, or explicitly authorize an exact temporary install:" >&2
        echo "  $0 --install-govulncheck ${VERIFIED_GOVULNCHECK_VERSION} '$TARGET_DIR'" >&2
        exit 2
    fi
fi

if ((DRY_RUN)); then
    echo "[Dry Run] Target: $TARGET_DIR"
    echo "[Dry Run] Would execute in target: go test -race ./..."
    if [[ -n "$INSTALL_VERSION" && -z "$GOVULNCHECK_BIN" ]]; then
        echo "[Dry Run] Would temporarily execute: GOTOOLCHAIN=local GOBIN=<temporary> go install golang.org/x/vuln/cmd/govulncheck@${INSTALL_VERSION}"
        echo "[Dry Run] Would execute: <temporary>/govulncheck ./..."
    else
        echo "[Dry Run] Would execute: ${GOVULNCHECK_BIN:-govulncheck} ./..."
    fi
    exit 0
fi

if [[ -z "$GOVULNCHECK_BIN" ]]; then
    TEMP_BIN_DIR="$(mktemp -d "${TMPDIR:-/tmp}/go-security-audit.XXXXXXXX")"
    chmod 0700 "$TEMP_BIN_DIR"
    echo "Installing govulncheck ${INSTALL_VERSION} into an ephemeral directory..."
    GOTOOLCHAIN=local GOBIN="$TEMP_BIN_DIR" go install "golang.org/x/vuln/cmd/govulncheck@${INSTALL_VERSION}"
    GOVULNCHECK_BIN="$TEMP_BIN_DIR/govulncheck"
    if [[ ! -x "$GOVULNCHECK_BIN" ]]; then
        echo "Error: the exact-version installation did not produce an executable." >&2
        exit 2
    fi
fi

echo "Starting security audit for Go module: $TARGET_DIR"
printf 'govulncheck binary: %s\n' "$GOVULNCHECK_BIN"
"$GOVULNCHECK_BIN" -version || {
    echo "Error: unable to inventory govulncheck version." >&2
    exit 2
}

failures=0
(
    cd -- "$TARGET_DIR"
    echo "Running race detector..."
    if ! go test -race ./...; then
        echo "FAIL: race detector or project tests failed." >&2
        failures=$((failures + 1))
    fi

    echo "Running govulncheck..."
    if ! "$GOVULNCHECK_BIN" ./...; then
        echo "FAIL: govulncheck reported vulnerabilities or could not complete." >&2
        failures=$((failures + 1))
    fi

    if ((failures > 0)); then
        echo "Security audit failed in ${failures} stage(s)." >&2
        exit 1
    fi
)

echo "Security audit completed with all requested stages passing."
