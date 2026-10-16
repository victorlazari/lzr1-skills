#!/usr/bin/env bash
# Offline tests for the verified archive download in install.sh (piped mode).
# A fake curl on PATH serves fixtures keyed by URL suffix; no network is used.

set -euo pipefail
umask 077

ROOT=$(CDPATH='' cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)
INSTALLER=$ROOT/install.sh
BUILD=$ROOT/scripts/build-release.sh
WORK=$(mktemp -d "${TMPDIR:-/tmp}/lzr1-download-test.XXXXXXXX")
cleanup() {
  rm -rf -- "$WORK"
}
trap cleanup EXIT HUP INT TERM

fail() {
  printf 'FAIL: %s\n' "$*" >&2
  exit 1
}

[[ -f $INSTALLER && -f $BUILD ]] || fail "missing install.sh or scripts/build-release.sh"

VERSION=$(sed -n 's/^VERSION="\([^"]*\)".*/\1/p' "$INSTALLER" | head -n 1)
[[ -n $VERSION ]] || fail "cannot read installer VERSION"
TAG=v$VERSION

# Temp git repo with the current tracked tree (working-tree content), tagged.
REPO=$WORK/repo
mkdir -p "$REPO"
(
  cd "$ROOT"
  git ls-files -z --cached | while IFS= read -r -d '' f; do
    [[ -f $f ]] || continue
    mkdir -p "$REPO/$(dirname -- "$f")"
    cp -p -- "$f" "$REPO/$f"
  done
)
(
  cd "$REPO"
  git init -q .
  git config user.email t@example.invalid
  git config user.name test
  git config commit.gpgsign false
  git add -A
  git commit -q -m fixture
  git tag "$TAG"
)

GOOD=$WORK/good
(cd "$REPO" && bash "$BUILD" "$TAG" "$GOOD") >"$WORK/build.log" 2>&1 \
  || { cat "$WORK/build.log" >&2; fail "build-release failed"; }

# Fake codeload snapshot: same tree under a branch-style top directory.
SNAP=$WORK/snap
mkdir -p "$SNAP"
(cd "$REPO" && git archive --format=tar.gz --prefix="lzr1-skills-main/" -o "$SNAP/codeload.tar.gz" "$TAG")

FAKEBIN=$WORK/fakebin
mkdir -p "$FAKEBIN"
cat >"$FAKEBIN/curl" <<'CURL'
#!/usr/bin/env bash
# Fake curl: parses --output and the https URL argument; serves $FAKE_FIXTURE.
out=""
url=""
wout=""
fail_flag=""
while [ $# -gt 0 ]; do
  case "$1" in
    --output) out=$2; shift ;;
    --write-out) wout=$2; shift ;;
    --fail) fail_flag=1 ;;
    https://*) url=$1 ;;
  esac
  shift
done
printf '%s\n' "$url" >>"$FAKE_FIXTURE/requests.log"
case "$url" in
  https://api.github.com/*/releases/latest)
    if [ -n "${FAKE_API_EXIT:-}" ]; then exit "$FAKE_API_EXIT"; fi
    printf '%s' "${FAKE_API_STATUS:-404}"
    exit 0
    ;;
esac
if [ -n "$wout" ] && [ -n "${FAKE_SUMS_EXIT:-}" ]; then exit "$FAKE_SUMS_EXIT"; fi
if [ -n "$wout" ] && [ -n "${FAKE_SUMS_STATUS:-}" ]; then printf '%s' "$FAKE_SUMS_STATUS"; exit 0; fi
case "$url" in
  */SHA256SUMS) src=$FAKE_FIXTURE/SHA256SUMS ;;
  */lzr1-skills.tar.gz) src=$FAKE_FIXTURE/lzr1-skills.tar.gz ;;
  */refs/heads/*) src=$FAKE_FIXTURE/codeload.tar.gz ;;
  *) exit 22 ;;
esac
if [ ! -f "$src" ]; then
  if [ -n "$wout" ]; then printf '404'; exit 0; fi
  exit 22
fi
cp "$src" "$out"
[ -z "$wout" ] || printf '200'
CURL
chmod 755 "$FAKEBIN/curl"

# tar wrapper: records every invocation, then runs the real tar.
REALTAR=$(command -v tar)
cat >"$FAKEBIN/tar" <<TAR
#!/usr/bin/env bash
printf '%s\\n' "\$*" >>"\${TAR_LOG:-/dev/null}"
exec "$REALTAR" "\$@"
TAR
chmod 755 "$FAKEBIN/tar"

# Stub wget (only used with curl hidden): serves the same fixtures as the fake curl.
WGETBIN=$WORK/wgetbin
mkdir -p "$WGETBIN"
cp "$FAKEBIN/tar" "$WGETBIN/tar"
cat >"$WGETBIN/wget" <<'WGET'
#!/usr/bin/env bash
printf '%s\n' "$*" >>"$FAKE_FIXTURE/wget.log"
if [ "${1:-}" = "--help" ]; then
  if [ "${FAKE_WGET_HELP:-full}" = full ]; then
    printf 'GNU Wget\n  --https-only\n  --secure-protocol=PR\n'
  else
    printf 'BusyBox wget\n  -q  quiet\n  -O  output\n'
  fi
  exit 0
fi
out=""; url=""; hdr=""
while [ $# -gt 0 ]; do
  case "$1" in
    -O) out=$2; shift ;;
    -S) hdr=1 ;;
    https://*) url=$1 ;;
  esac
  shift
done
printf '%s\n' "$url" >>"$FAKE_FIXTURE/requests.log"
status() { [ -z "$hdr" ] || printf '  HTTP/1.1 %s X\n' "$1" >&2; }
case "$url" in
  https://api.github.com/*/releases/latest)
    if [ -n "${FAKE_API_EXIT:-}" ]; then exit "$FAKE_API_EXIT"; fi
    c=${FAKE_API_STATUS:-404}
    status "$c"; : >"$out"
    case "$c" in 2*) exit 0 ;; *) exit 8 ;; esac
    ;;
esac
if [ -n "${FAKE_SUMS_STATUS:-}" ] && [ "${url%/SHA256SUMS}" != "$url" ]; then
  status "$FAKE_SUMS_STATUS"; : >"$out"
  case "$FAKE_SUMS_STATUS" in 2*) exit 0 ;; *) exit 8 ;; esac
fi
case "$url" in
  */SHA256SUMS) src=$FAKE_FIXTURE/SHA256SUMS ;;
  */lzr1-skills.tar.gz) src=$FAKE_FIXTURE/lzr1-skills.tar.gz ;;
  */refs/heads/*) src=$FAKE_FIXTURE/codeload.tar.gz ;;
  *) status 404; exit 8 ;;
esac
if [ ! -f "$src" ]; then status 404; : >"$out"; exit 8; fi
status 200
cp "$src" "$out"
WGET
chmod 755 "$WGETBIN/wget"

# NOCURL: every system tool except curl and wget (to force the wget code path).
NOCURL=$WORK/nocurl
mkdir -p "$NOCURL"
for d in /usr/bin /bin; do
  for f in "$d"/*; do
    b=${f##*/}
    case $b in curl|wget) continue ;; esac
    [[ -e $NOCURL/$b ]] || ln -s "$f" "$NOCURL/$b" 2>/dev/null || true
  done
done

CASE_N=0
HOME_DIR=""
FIX=""
LOG=""

# new_case <fixture-source-dir>: fresh HOME and a private copy of the fixtures.
new_case() {
  CASE_N=$((CASE_N + 1))
  HOME_DIR=$WORK/home$CASE_N
  FIX=$WORK/fix$CASE_N
  LOG=$WORK/out$CASE_N.log
  mkdir -p "$HOME_DIR" "$FIX"
  if [[ -n ${1:-} ]]; then cp -p "$1"/* "$FIX"/; fi
}

# run_installer <installer args...>: piped mode, isolated HOME, fake curl first.
run_installer() {
  set +e
  TAR_LOG=$WORK/tar$CASE_N.log
  : >"$TAR_LOG"
  cat "$INSTALLER" | env HOME="$HOME_DIR" FAKE_FIXTURE="$FIX" FAKE_SUMS_STATUS="${FAKE_SUMS_STATUS:-}" FAKE_SUMS_EXIT="${FAKE_SUMS_EXIT:-}" \
    FAKE_API_STATUS="${FAKE_API_STATUS:-}" FAKE_API_EXIT="${FAKE_API_EXIT:-}" FAKE_WGET_HELP="${FAKE_WGET_HELP:-full}" TAR_LOG="$TAR_LOG" \
    PATH="${INST_PATH:-$FAKEBIN:$PATH}" \
    bash -s -- "$@" >"$LOG" 2>&1
  RC=$?
  set -e
}

expect_ok() {
  [[ $RC -eq 0 ]] || { cat "$LOG" >&2; fail "case $CASE_N: expected success, got exit $RC"; }
}

expect_fail_with() {
  local msg=$1
  [[ $RC -ne 0 ]] || { cat "$LOG" >&2; fail "case $CASE_N: expected failure"; }
  grep -F -- "$msg" "$LOG" >/dev/null || { cat "$LOG" >&2; fail "case $CASE_N: missing message: $msg"; }
  [[ ! -e $HOME_DIR/.codex ]] || fail "case $CASE_N: nothing should be installed, found $HOME_DIR/.codex"
}

expect_log() {
  grep -F -- "$1" "$LOG" >/dev/null || { cat "$LOG" >&2; fail "case $CASE_N: missing log text: $1"; }
}

expect_installed() {
  [[ -d $HOME_DIR/.codex/skills ]] || { cat "$LOG" >&2; fail "case $CASE_N: skills not installed"; }
}

# 1. Latest release, verified.
new_case "$GOOD"
run_installer --codex --yes
expect_ok
expect_log "from release source (ref: latest), verified: yes"
expect_log "Release archive checksum verified"
expect_installed
grep -F "/releases/latest/download/SHA256SUMS" "$FIX/requests.log" >/dev/null || fail "case 1: wrong SHA256SUMS URL"
printf 'PASS: latest release verified install\n'

# 1b. Pinned tag, verified.
new_case "$GOOD"
run_installer --ref "$TAG" --codex --yes
expect_ok
expect_log "from release source (ref: $TAG), verified: yes"
expect_installed
grep -F "/releases/download/$TAG/lzr1-skills.tar.gz" "$FIX/requests.log" >/dev/null || fail "case 1b: wrong tag URL"
printf 'PASS: pinned tag verified install\n'

# 2. Tarball corrupted, checksum unchanged.
new_case "$GOOD"
python3 -I - "$FIX/lzr1-skills.tar.gz" <<'PY'
import sys
p = sys.argv[1]
b = bytearray(open(p, "rb").read())
b[-5] ^= 0xFF
open(p, "wb").write(bytes(b))
PY
run_installer --codex --yes
expect_fail_with "Release archive checksum mismatch; refusing to extract"
expect_log "Expected SHA-256:"
expect_log "Actual SHA-256:"
printf 'PASS: corrupted tarball refused\n'

# 3. SHA256SUMS without the tarball line.
new_case "$GOOD"
printf '%s  other.tar.gz\n' e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 >"$FIX/SHA256SUMS"
run_installer --codex --yes
expect_fail_with "SHA256SUMS has no entry for lzr1-skills.tar.gz"
printf 'PASS: SHA256SUMS without tarball entry refused\n'

# 4. SHA256SUMS missing on latest: WARN and fall back to codeload main.
new_case "$SNAP"
run_installer --codex --yes
expect_ok
expect_log "No published (non-draft, non-prerelease) release was found; installing the unverified main snapshot"
expect_log "from branch source (ref: main), verified: no"
expect_installed
grep -F "codeload.github.com" "$FIX/requests.log" >/dev/null || fail "case 4: codeload not used"
grep -F "https://api.github.com/repos/" "$FIX/requests.log" | grep -F "/releases/latest" >/dev/null || fail "case 4: releases API not consulted"
printf 'PASS: no release falls back to unverified main\n'

# 5. Explicit tag whose assets are missing: no fallback.
new_case "$SNAP"
run_installer --ref v9.9.9 --codex --yes
expect_fail_with "Release v9.9.9 not found or its checksums could not be downloaded"
if grep -F "codeload.github.com" "$FIX/requests.log" >/dev/null; then fail "case 5: must not fall back to codeload"; fi
printf 'PASS: missing explicit tag fails without fallback\n'

# 6. --ref main: unverified snapshot with WARN.
new_case "$SNAP"
run_installer --ref main --codex --yes
expect_ok
expect_log "Installing an unverified snapshot of main; use a release tag for checksum verification"
expect_log "from branch source (ref: main), verified: no"
expect_installed
printf 'PASS: --ref main installs unverified snapshot\n'

# 7. Invalid refs.
new_case "$GOOD"
run_installer --ref 'a b' --codex --yes
expect_fail_with "Invalid ref: only A-Z a-z 0-9 . _ / - are allowed"
[[ ! -e $FIX/requests.log ]] || fail "case 7: nothing should be downloaded"
new_case "$GOOD"
run_installer --ref '' --codex --yes
expect_fail_with "--ref value must not be empty"
printf 'PASS: invalid refs rejected\n'

# 8. Hard failures on latest SHA256SUMS: no fallback, nothing installed.
for st in 500 503 403 429 401; do
  new_case "$SNAP"
  cp "$GOOD"/* "$FIX"/
  FAKE_SUMS_STATUS=$st run_installer --codex --yes
  expect_fail_with "HTTP status $st"
  expect_log "--ref main"
  if grep -F "codeload.github.com" "$FIX/requests.log" >/dev/null; then fail "case 8 ($st): must not fall back"; fi
done
for ex in 28 6; do
  new_case "$SNAP"
  FAKE_SUMS_EXIT=$ex run_installer --codex --yes
  expect_fail_with "curl exit $ex"
  expect_log "--ref main"
  if grep -F "codeload.github.com" "$FIX/requests.log" >/dev/null; then fail "case 8 (exit $ex): must not fall back"; fi
done
# 404 explicitly with a published release asset set still falls back with WARN.
new_case "$SNAP"
FAKE_SUMS_STATUS=404 run_installer --codex --yes
expect_ok
expect_log "No published (non-draft, non-prerelease) release was found"
# Empty 200 body is a hard failure.
new_case "$GOOD"
: >"$FIX/SHA256SUMS"
run_installer --codex --yes
expect_fail_with "empty body"
printf 'PASS: only HTTP 404 falls back\n'

# 9. Checksum parsing variants.
HASH=$(awk '{print $1}' "$GOOD/SHA256SUMS")
sums_case() { # <content> <expect: ok|msg>
  new_case "$GOOD"
  printf '%b' "$1" >"$FIX/SHA256SUMS"
  run_installer --codex --yes
  if [[ $2 == ok ]]; then expect_ok; expect_installed; else expect_fail_with "$2"; fi
}
UP=$(printf '%s' "$HASH" | tr 'a-f' 'A-F')
sums_case "$HASH  lzr1-skills.tar.gz\r\n" ok
sums_case "$HASH  ./lzr1-skills.tar.gz\n" ok
sums_case "$HASH *lzr1-skills.tar.gz\n" ok
sums_case "$UP  lzr1-skills.tar.gz\n" ok
sums_case "${HASH#?}  lzr1-skills.tar.gz\n" "not a valid SHA-256"
sums_case "${HASH%?}g  lzr1-skills.tar.gz\n" "not a valid SHA-256"
sums_case "$HASH  lzr1-skills.tar.gz\n$HASH  ./lzr1-skills.tar.gz\n" "multiple entries"
printf 'PASS: checksum parsing\n'

# 10. Snapshot with a symlink member is refused before extraction.
new_case "$SNAP"
SYM=$WORK/symsnap
rm -rf "$SYM"; mkdir -p "$SYM"
tar -xzf "$SNAP/codeload.tar.gz" -C "$SYM"
ln -s /etc/passwd "$SYM/lzr1-skills-main/evil-link"
(cd "$SYM" && tar -czf "$FIX/codeload.tar.gz" lzr1-skills-main)
run_installer --ref main --codex --yes
expect_fail_with "non-regular member"
printf 'PASS: symlink snapshot refused\n'

# 11. --ref ignored warning for LZR1_SOURCE_DIR.
new_case "$GOOD"
set +e
LZR1_SOURCE_DIR="$ROOT" HOME="$HOME_DIR" bash "$INSTALLER" --ref v1.0.0 --codex --yes --dry-run >"$LOG" 2>&1
RC=$?
set -e
expect_ok
expect_log "Ignoring --ref"
printf 'PASS: ignored ref warns\n'

# 12. 404 on SHA256SUMS needs a second signal: the releases API must also say 404.
new_case "$SNAP"
FAKE_SUMS_STATUS=404 FAKE_API_STATUS=404 run_installer --codex --yes
expect_ok
expect_log "No published (non-draft, non-prerelease) release was found; installing the unverified main snapshot"
new_case "$SNAP"
FAKE_SUMS_STATUS=404 FAKE_API_STATUS=200 run_installer --codex --yes
expect_fail_with "a release exists but SHA256SUMS is missing: refusing to install unverified; use --ref main to override"
if grep -F "codeload.github.com" "$FIX/requests.log" >/dev/null; then fail "case 12 (api 200): must not fall back"; fi
for st in 500 403 301; do
  new_case "$SNAP"
  FAKE_SUMS_STATUS=404 FAKE_API_STATUS=$st run_installer --codex --yes
  expect_fail_with "--ref main"
  expect_log "HTTP status $st"
  if grep -F "codeload.github.com" "$FIX/requests.log" >/dev/null; then fail "case 12 (api $st): must not fall back"; fi
done
new_case "$SNAP"
FAKE_SUMS_STATUS=404 FAKE_API_EXIT=28 run_installer --codex --yes
expect_fail_with "curl exit 28"
if grep -F "codeload.github.com" "$FIX/requests.log" >/dev/null; then fail "case 12 (api transport): must not fall back"; fi
printf 'PASS: 404 downgrade needs the releases API to also say 404\n'

# Archive helpers (python tarfile) for the hostile and benign tarball cases.
MK=$WORK/mk.py
cat >"$MK" <<'PY'
import io, os, sys, tarfile
mode, src, out, pwn = sys.argv[1:5]
base = {}
with tarfile.open(src) as t:
    for m in t.getmembers():
        if m.isfile():
            base[m.name] = t.extractfile(m).read()
        # directories are implied
prefix = "lzr1-skills-main/"
def add(t, name, data=b"x\n", typ=tarfile.REGTYPE, link=""):
    ti = tarfile.TarInfo(name)
    ti.type = typ
    ti.mode = 0o644
    if typ == tarfile.REGTYPE:
        ti.size = len(data)
        t.addfile(ti, io.BytesIO(data))
    else:
        ti.linkname = link
        t.addfile(ti)
with tarfile.open(out, "w:gz", format=tarfile.GNU_FORMAT) as t:
    if mode == "abs":
        add(t, pwn)
    elif mode == "dotdot":
        add(t, prefix + "../escape.txt")
    elif mode == "tworoots":
        add(t, prefix + "skills-list.txt")
        add(t, "other-root/x.txt")
    elif mode == "rootfile":
        for n, d in base.items():
            add(t, n[len(prefix):], d)
    elif mode in ("symlink", "hardlink", "benign"):
        for n, d in base.items():
            add(t, n, d)
        first = [n for n in base if n.startswith(prefix + "skills/")][0]
        skilldir = first.rsplit("/", 1)[0] + "/"
        if mode == "symlink":
            add(t, skilldir + "evil-link", typ=tarfile.SYMTYPE, link="/etc/passwd")
        elif mode == "hardlink":
            add(t, skilldir + "evil-hard", typ=tarfile.LNKTYPE, link=first)
        else:
            add(t, skilldir + "l file with spaces.txt")
            add(t, skilldir + "lib dir/l again.txt")
            add(t, skilldir + "x-ray notes.txt")
PY

tarball_case() { # <mode> <path: release|branch> ; builds fixture and runs
  local mode=$1 path=$2 args
  PWN=$WORK/pwned-$mode-$path
  new_case "$GOOD"
  rm -f "$FIX/codeload.tar.gz"
  if [[ $path == release ]]; then
    python3 -I "$MK" "$mode" "$SNAP/codeload.tar.gz" "$FIX/lzr1-skills.tar.gz" "$PWN"
    sum=$( (command -v sha256sum >/dev/null && sha256sum "$FIX/lzr1-skills.tar.gz") || shasum -a 256 "$FIX/lzr1-skills.tar.gz")
    printf '%s  lzr1-skills.tar.gz\n' "${sum%% *}" >"$FIX/SHA256SUMS"
    args=(--codex --yes)
  else
    python3 -I "$MK" "$mode" "$SNAP/codeload.tar.gz" "$FIX/codeload.tar.gz" "$PWN"
    args=(--ref main --codex --yes)
  fi
  run_installer "${args[@]}"
}

expect_no_extraction() {
  grep -F -- "-xzf" "$TAR_LOG" >/dev/null && { cat "$LOG" "$TAR_LOG" >&2; fail "case $CASE_N: tar extraction ran"; }
  [[ ! -e $PWN ]] || fail "case $CASE_N: absolute-path member was written"
  return 0
}

# 13. Hostile listings fail before ANY extraction (verified release path and unverified branch path).
for path in release branch; do
  for pair in "abs:Archive contains an absolute path" \
              "dotdot:Archive contains path traversal components" \
              "tworoots:Archive contains multiple top-level roots" \
              "rootfile:Archive has an invalid top-level path"; do
    mode=${pair%%:*}; msg=${pair#*:}
    tarball_case "$mode" "$path"
    expect_fail_with "$msg"
    expect_no_extraction
  done
done
printf 'PASS: hostile archive listings refused before extraction (release and branch)\n'

# 14. Member types: symlink and hardlink refused before extraction; spaces and a leading l accepted.
for path in release branch; do
  for mode in symlink hardlink; do
    tarball_case "$mode" "$path"
    expect_fail_with "non-regular member"
    expect_no_extraction
  done
  tarball_case benign "$path"
  expect_ok
  expect_installed
done
printf 'PASS: link members refused, benign names accepted (%s)\n' "$(tar --version 2>&1 | head -n 1)"

# 15. wget path (curl hidden).
new_case "$GOOD"
INST_PATH="$WGETBIN:$NOCURL" FAKE_WGET_HELP=lacking run_installer --codex --yes
expect_fail_with "lacks --https-only"
if grep -E 'https://' "$FIX/wget.log" >/dev/null 2>&1; then cat "$FIX/wget.log" >&2; fail "case 15: wget must not download without TLS options"; fi
[[ ! -e $FIX/requests.log ]] || fail "case 15: nothing should be requested"
new_case "$GOOD"
INST_PATH="$WGETBIN:$NOCURL" FAKE_WGET_HELP=lacking run_installer --ref main --codex --yes
expect_fail_with "lacks --https-only"
[[ ! -e $FIX/requests.log ]] || fail "case 15: branch path must not request anything"
new_case "$GOOD"
INST_PATH="$WGETBIN:$NOCURL" run_installer --codex --yes
expect_ok
expect_log "Release archive checksum verified"
grep -E -- '--tries=3' "$FIX/wget.log" >/dev/null || fail "case 15: wget lacks --tries=3"
grep -E -- '--timeout=[0-9]+' "$FIX/wget.log" >/dev/null || fail "case 15: wget lacks --timeout"
grep -F -- '--https-only' "$FIX/wget.log" >/dev/null || fail "case 15: wget lacks --https-only"
new_case "$SNAP"
INST_PATH="$WGETBIN:$NOCURL" FAKE_SUMS_STATUS=404 FAKE_API_STATUS=200 run_installer --codex --yes
expect_fail_with "a release exists but SHA256SUMS is missing"
new_case "$SNAP"
INST_PATH="$WGETBIN:$NOCURL" FAKE_SUMS_STATUS=404 FAKE_API_STATUS=404 run_installer --codex --yes
expect_ok
expect_log "No published (non-draft, non-prerelease) release was found"
printf 'PASS: wget path is fail-closed with retry limits\n'

printf 'All installer download tests passed\n'
