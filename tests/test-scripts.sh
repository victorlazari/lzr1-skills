#!/usr/bin/env bash
# Validates the scripts REGISTERED in tests/script-coverage.tsv: each exists,
# has the right mode and passes a syntax check; `help` rows really answer
# --help with exit 0; `behavior` rows name an existing test file. It does not
# prove an unregistered script is covered (scripts/lint_catalog.py does that),
# and a `static` row for a script that answers --help is allowed.
# Never runs scripts against the real HOME or repo cwd.
# Set LZR1_REGISTRY to test against an alternate registry file.

set -euo pipefail
umask 077

ROOT=$(CDPATH='' cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)
REGISTRY=${LZR1_REGISTRY:-$ROOT/tests/script-coverage.tsv}
WORK=$(mktemp -d "${TMPDIR:-/tmp}/lzr1-scripts-test.XXXXXXXX")
cleanup() {
  rm -rf -- "$WORK"
}
trap cleanup EXIT HUP INT TERM

fail() {
  printf 'FAIL: %s\n' "$*" >&2
  exit 1
}

[[ -f $REGISTRY ]] || fail "registry missing: $REGISTRY"

mkdir -p "$WORK/home" "$WORK/tmp" "$WORK/pycache"

# Bounded, hermetic --help run. Prints captured output; exit status is the
# script's (124 on timeout). No timeout(1) on macOS, so python3 -I does it.
run_help() {
  python3 -I -c '
import os, subprocess, sys
script, work = sys.argv[1], sys.argv[2]
cwd = os.path.join(work, "cwd")
os.makedirs(cwd, exist_ok=True)
env = {"HOME": os.path.join(work, "home"), "TMPDIR": os.path.join(work, "tmp"),
       "PATH": os.environ.get("LZR1_SAFE_PATH", "/usr/local/bin:/usr/bin:/bin")}
try:
    with open(os.devnull, "rb") as dn:
        r = subprocess.run([script, "--help"], cwd=cwd, env=env, stdin=dn,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           timeout=15)
except subprocess.TimeoutExpired as e:
    sys.stdout.buffer.write(e.stdout or b"")
    print("timed out after 15s")
    sys.exit(124)
sys.stdout.buffer.write(r.stdout)
sys.exit(r.returncode)
' "$1" "$WORK"
}

have_node=0
safe_path=/usr/local/bin:/usr/bin:/bin
if command -v node >/dev/null 2>&1; then
  have_node=1
  safe_path="$safe_path:$(dirname -- "$(command -v node)")"
fi
export LZR1_SAFE_PATH=$safe_path
node_skips=0
n_static=0
n_help=0
n_behavior=0
first=1

# Tab is IFS whitespace, so read would collapse empty columns; split by hand.
while IFS= read -r line || [[ -n $line ]]; do
  if [[ $first -eq 1 ]]; then first=0; continue; fi
  [[ -n $line ]] || continue
  path=${line%%$'\t'*}; rest=${line#*$'\t'}
  level=${rest%%$'\t'*}; rest=${rest#*$'\t'}
  reason=${rest%%$'\t'*}; test=${rest#*$'\t'}
  case $test in *$'\t'*) fail "$path: registry row has more than 4 columns" ;; esac
  : "$reason"
  file="$ROOT/$path"
  [[ -f $file && ! -L $file ]] || fail "$path: not a regular file"

  first_two=$(head -c 2 -- "$file" || true)
  case $path in
    skills/*/scripts/*.sh | skills/*/scripts/*.py) want_exec=1 ;;
    *) want_exec=0 ;;
  esac
  [[ $first_two == '#!' ]] && want_exec=1
  if [[ $want_exec -eq 1 && ! -x $file ]]; then
    fail "$path: must be executable"
  fi

  case $path in
    *.sh)
      bash -n "$file" || fail "$path: bash -n failed"
      ;;
    *.py)
      python3 -I -X pycache_prefix="$WORK/pycache" -m py_compile "$file" \
        || fail "$path: py_compile failed"
      ;;
    *.js)
      if [[ $have_node -eq 1 ]]; then
        node --check "$file" || fail "$path: node --check failed"
      else
        node_skips=$((node_skips + 1))
      fi
      ;;
  esac

  case $level in
    static)
      n_static=$((n_static + 1))
      ;;
    help)
      n_help=$((n_help + 1))
      case $path in
        *.js) if [[ $have_node -eq 0 ]]; then continue; fi ;;
      esac
      rc=0
      out=$(run_help "$file" 2>&1) || rc=$?
      [[ $rc -eq 0 ]] || fail "$path: --help exited $rc. Output: $out"
      [[ -n $out ]] || fail "$path: --help printed nothing"
      ;;
    behavior)
      n_behavior=$((n_behavior + 1))
      [[ -f $ROOT/$test ]] || fail "$path: named test file missing: $test"
      ;;
    *)
      fail "$path: unknown level '$level'"
      ;;
  esac
done < "$REGISTRY"

[[ $have_node -eq 1 || $node_skips -eq 0 ]] || printf 'NOTE: node not found; skipped node --check and --help for .js scripts\n'
printf 'PASS: static rows syntax/mode checked (%s)\n' "$n_static"
printf 'PASS: help rows ran --help (%s)\n' "$n_help"
printf 'PASS: behavior rows name an existing test file (%s)\n' "$n_behavior"
printf 'scripts: %s static, %s help, %s behavior\n' "$n_static" "$n_help" "$n_behavior"
