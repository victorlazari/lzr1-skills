#!/usr/bin/env bash
# lzr1-skills installer — macOS + Linux, Bash 3.2+
# Installs the complete, manifest-validated skill catalog to nine supported tools.

set -uo pipefail
umask 077

REPO="victorlazari/lzr1-skills"
BRANCH="main"
ARCHIVE_URL="https://codeload.github.com/${REPO}/tar.gz/refs/heads/${BRANCH}"
VERSION="2.0.0"
EXPECTED_SKILL_COUNT=86
STATE_FILE="${HOME:-}/.lzr1-skills-state"
LOCK_DIR="${HOME:-}/.lzr1-skills-lock"
MANAGED_SOURCE="${REPO}"
RUN_ID="$(date -u +%Y%m%dT%H%M%SZ 2>/dev/null || printf 'run')-$$"

ACTION="install"
DRY_RUN=false
VERBOSE=false
YES_MODE=false
FORCE=false
HAS_TARGET_FLAG=false
SELECT_DETECTED=false
SOURCE_ROOT=""
SOURCE_MODE=""
WORK_ROOT=""
SKILL_NAMES=""
SKILL_COUNT=0
LOCK_HELD=false
BACKUP_NOTICE=""

AUTO_MODE="${LZR1_AUTO:-${LZRI_AUTO:-false}}"
SOURCE_OVERRIDE="${LZR1_SOURCE_DIR:-}"

OPT_CLAUDE_CODE=false
OPT_CLAUDE_DESKTOP=false
OPT_CODEX=false
OPT_OPENCODE=false
OPT_FACTORY=false
OPT_CURSOR=false
OPT_VSCODE=false
OPT_ANTIGRAVITY=false
OPT_AGY=false

FOUND_CLAUDE_CODE=false
FOUND_CLAUDE_DESKTOP=false
FOUND_CODEX=false
FOUND_OPENCODE=false
FOUND_FACTORY=false
FOUND_CURSOR=false
FOUND_VSCODE=false
FOUND_ANTIGRAVITY=false
FOUND_AGY=false

PATH_CLAUDE_CODE="${HOME:-}/.claude"
PATH_CODEX="${HOME:-}/.codex"
PATH_OPENCODE="${HOME:-}/.config/opencode"
PATH_FACTORY="${HOME:-}/.factory"
PATH_CURSOR="${HOME:-}/.cursor"
PATH_VSCODE="${HOME:-}/.vscode"
PATH_ANTIGRAVITY="${HOME:-}/.antigravity-ide"
PATH_AGY="${HOME:-}/.gemini/antigravity-cli"
PATH_CLAUDE_DESKTOP=""
OS_TYPE="unknown"

if [ -t 1 ] && command -v tput >/dev/null 2>&1; then
  RED=$(tput setaf 1 2>/dev/null || printf '')
  GREEN=$(tput setaf 2 2>/dev/null || printf '')
  YELLOW=$(tput setaf 3 2>/dev/null || printf '')
  CYAN=$(tput setaf 6 2>/dev/null || printf '')
  BOLD=$(tput bold 2>/dev/null || printf '')
  DIM=$(tput dim 2>/dev/null || printf '')
  RESET=$(tput sgr0 2>/dev/null || printf '')
else
  RED='' GREEN='' YELLOW='' CYAN='' BOLD='' DIM='' RESET=''
fi

log_info() { printf '%s[INFO]%s %s\n' "${CYAN}" "${RESET}" "$*"; }
log_ok() { printf '%s[OK]%s %s\n' "${GREEN}" "${RESET}" "$*"; }
log_warn() { printf '%s[WARN]%s %s\n' "${YELLOW}" "${RESET}" "$*" >&2; }
log_error() { printf '%s[ERROR]%s %s\n' "${RED}" "${RESET}" "$*" >&2; }
log_verbose() { [ "${VERBOSE}" = true ] && printf '%s       %s%s\n' "${DIM}" "$*" "${RESET}" || true; }

fail() {
  log_error "$*"
  exit 1
}

cleanup() {
  status=$?
  trap - EXIT HUP INT TERM
  if [ "${LOCK_HELD}" = true ] && [ -n "${LOCK_DIR}" ] && [ -d "${LOCK_DIR}" ] && [ ! -L "${LOCK_DIR}" ]; then
    rm -rf -- "${LOCK_DIR}" 2>/dev/null || true
  fi
  if [ -n "${WORK_ROOT}" ] && [ -d "${WORK_ROOT}" ] && [ ! -L "${WORK_ROOT}" ]; then
    case "${WORK_ROOT}" in
      "${TMPDIR:-/tmp}"/lzr1-skills.*) rm -rf -- "${WORK_ROOT}" 2>/dev/null || true ;;
      *) log_warn "Refusing to remove unexpected temporary path: ${WORK_ROOT}" ;;
    esac
  fi
  exit "${status}"
}
trap cleanup EXIT
trap 'exit 130' HUP INT TERM

print_banner() {
  printf '\n%s%sLZR1 Skills%s  installer v%s\n' "${BOLD}" "${CYAN}" "${RESET}" "${VERSION}"
  printf '%s%d manifest-validated skills for nine supported tools%s\n\n' "${DIM}" "${EXPECTED_SKILL_COUNT}" "${RESET}"
}

print_help() {
  print_banner
  cat <<EOF
USAGE
  bash install.sh [command] [target options] [behavior options]
  curl -fsSL https://raw.githubusercontent.com/${REPO}/main/install.sh | bash

COMMANDS
  install             Install the complete skill catalog (default)
  update              Reinstall to explicitly selected or previously saved targets
  remove              Remove only content carrying lzr1 ownership markers
  doctor              Validate source catalog and report managed target coverage
  help                Show this help

TARGET OPTIONS
  --detected           Select all currently detected tools
  --all                Select all nine tools, including undetected tools
  --claude-code        ${PATH_CLAUDE_CODE}/skills/
  --claude-desktop     Platform-specific Claude Desktop skills directory
  --codex              ${PATH_CODEX}/skills/
  --opencode           ${PATH_OPENCODE}/skill/
  --factory            ${PATH_FACTORY}/skills/
  --cursor             ${PATH_CURSOR}/rules/
  --vscode             ${PATH_VSCODE}/lzr1-skills/
  --antigravity        ${PATH_ANTIGRAVITY}/rules/
  --agy                ${PATH_AGY}/skills/

BEHAVIOR OPTIONS
  --dry-run, -n        Validate source and preview destination changes only
  --verbose, -v        Show per-skill activity
  --yes, -y            Non-interactive confirmation mode; does not select targets
  --force              Back up and replace unowned name collisions
  --version            Show installer version
  --help, -h           Show this help

SAFE NON-INTERACTIVE EXAMPLES
  curl -fsSL https://raw.githubusercontent.com/${REPO}/main/install.sh | bash -s -- --detected --yes
  bash install.sh --codex --claude-code --dry-run
  bash install.sh update
  bash install.sh remove --codex

NOTES
  Package-native targets receive each complete skill directory. Flat-rule targets
  receive <skill>.md plus a hidden .lzr1-skill-resources/ package copy with adjusted
  relative links. Existing paths without lzr1 ownership markers are never overwritten
  unless --force is explicit; forced collisions are preserved under .lzr1-backups/.
EOF
}

set_all_targets() {
  OPT_CLAUDE_CODE=true
  OPT_CLAUDE_DESKTOP=true
  OPT_CODEX=true
  OPT_OPENCODE=true
  OPT_FACTORY=true
  OPT_CURSOR=true
  OPT_VSCODE=true
  OPT_ANTIGRAVITY=true
  OPT_AGY=true
  HAS_TARGET_FLAG=true
}

parse_args() {
  while [ "$#" -gt 0 ]; do
    case "$1" in
      install) ACTION="install" ;;
      update|upgrade) ACTION="update" ;;
      remove|uninstall) ACTION="remove" ;;
      doctor) ACTION="doctor" ;;
      help) print_help; exit 0 ;;
      all|--all) set_all_targets ;;
      --detected) SELECT_DETECTED=true; HAS_TARGET_FLAG=true ;;
      --claude-code) OPT_CLAUDE_CODE=true; HAS_TARGET_FLAG=true ;;
      --claude-desktop) OPT_CLAUDE_DESKTOP=true; HAS_TARGET_FLAG=true ;;
      --codex) OPT_CODEX=true; HAS_TARGET_FLAG=true ;;
      --opencode) OPT_OPENCODE=true; HAS_TARGET_FLAG=true ;;
      --factory) OPT_FACTORY=true; HAS_TARGET_FLAG=true ;;
      --cursor) OPT_CURSOR=true; HAS_TARGET_FLAG=true ;;
      --vscode) OPT_VSCODE=true; HAS_TARGET_FLAG=true ;;
      --antigravity) OPT_ANTIGRAVITY=true; HAS_TARGET_FLAG=true ;;
      --agy) OPT_AGY=true; HAS_TARGET_FLAG=true ;;
      --dry-run|-n) DRY_RUN=true ;;
      --verbose|-v) VERBOSE=true ;;
      --yes|-y) YES_MODE=true ;;
      --force) FORCE=true ;;
      --version) printf 'lzr1-skills v%s\n' "${VERSION}"; exit 0 ;;
      --help|-h) print_help; exit 0 ;;
      --) ;;
      *) fail "Unknown argument: $1" ;;
    esac
    shift
  done
}

detect_os_and_tools() {
  case "$(uname -s 2>/dev/null || printf unknown)" in
    Darwin) OS_TYPE="macos" ;;
    Linux) OS_TYPE="linux" ;;
  esac
  if [ "${OS_TYPE}" = "macos" ]; then
    PATH_CLAUDE_DESKTOP="${HOME}/Library/Application Support/Claude"
  else
    PATH_CLAUDE_DESKTOP="${HOME}/.config/claude"
  fi

  [ -d "${PATH_CLAUDE_CODE}" ] && FOUND_CLAUDE_CODE=true
  [ -d "${PATH_CLAUDE_DESKTOP}" ] && FOUND_CLAUDE_DESKTOP=true
  [ -d "${PATH_CODEX}" ] && FOUND_CODEX=true
  [ -d "${PATH_OPENCODE}" ] && FOUND_OPENCODE=true
  [ -d "${PATH_FACTORY}" ] && FOUND_FACTORY=true
  [ -d "${PATH_CURSOR}" ] && FOUND_CURSOR=true
  [ -d "${PATH_VSCODE}" ] && FOUND_VSCODE=true
  [ -d "${PATH_ANTIGRAVITY}" ] && FOUND_ANTIGRAVITY=true
  [ -d "${PATH_AGY}" ] && FOUND_AGY=true
}

select_detected_targets() {
  OPT_CLAUDE_CODE="${FOUND_CLAUDE_CODE}"
  OPT_CLAUDE_DESKTOP="${FOUND_CLAUDE_DESKTOP}"
  OPT_CODEX="${FOUND_CODEX}"
  OPT_OPENCODE="${FOUND_OPENCODE}"
  OPT_FACTORY="${FOUND_FACTORY}"
  OPT_CURSOR="${FOUND_CURSOR}"
  OPT_VSCODE="${FOUND_VSCODE}"
  OPT_ANTIGRAVITY="${FOUND_ANTIGRAVITY}"
  OPT_AGY="${FOUND_AGY}"
}

any_target_selected() {
  [ "${OPT_CLAUDE_CODE}" = true ] && return 0
  [ "${OPT_CLAUDE_DESKTOP}" = true ] && return 0
  [ "${OPT_CODEX}" = true ] && return 0
  [ "${OPT_OPENCODE}" = true ] && return 0
  [ "${OPT_FACTORY}" = true ] && return 0
  [ "${OPT_CURSOR}" = true ] && return 0
  [ "${OPT_VSCODE}" = true ] && return 0
  [ "${OPT_ANTIGRAVITY}" = true ] && return 0
  [ "${OPT_AGY}" = true ] && return 0
  return 1
}

ensure_work_root() {
  [ -n "${WORK_ROOT}" ] && return 0
  command -v mktemp >/dev/null 2>&1 || fail "mktemp is required"
  WORK_ROOT=$(mktemp -d "${TMPDIR:-/tmp}/lzr1-skills.XXXXXXXX") || fail "Unable to create temporary workspace"
  [ -d "${WORK_ROOT}" ] && [ ! -L "${WORK_ROOT}" ] || fail "Unsafe temporary workspace"
}

sha256_file() {
  local file
  file=$1
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "${file}" | awk '{print $1}'
  elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "${file}" | awk '{print $1}'
  else
    printf 'unavailable'
  fi
}

download_file() {
  local url destination
  url=$1
  destination=$2
  case "${url}" in https://*) ;; *) fail "Refusing non-HTTPS download URL" ;; esac
  if command -v curl >/dev/null 2>&1; then
    curl --fail --silent --show-error --location \
      --proto '=https' --tlsv1.2 --retry 3 --connect-timeout 20 --max-time 300 \
      --output "${destination}" "${url}" || return 1
  elif command -v wget >/dev/null 2>&1; then
    wget -q -O "${destination}" "${url}" || return 1
  else
    fail "curl or wget is required in piped mode"
  fi
  [ -s "${destination}" ] || return 1
}

validate_archive_listing() {
  local listing top CR entry component
  listing=$1
  top=""
  CR=$(printf '\r')
  while IFS= read -r entry || [ -n "${entry}" ]; do
    [ -n "${entry}" ] || fail "Archive contains an empty path"
    case "${entry}" in
      /*) fail "Archive contains an absolute path" ;;
      *"${CR}"*) fail "Archive contains a carriage return in a path" ;;
      *\\*) fail "Archive contains a backslash path" ;;
    esac
    case "/${entry}/" in
      *"/../"*|*"/./"*) fail "Archive contains path traversal components" ;;
    esac
    component=${entry%%/*}
    [ -n "${component}" ] || fail "Archive has an invalid top-level path"
    if [ -z "${top}" ]; then
      top=${component}
    elif [ "${component}" != "${top}" ]; then
      fail "Archive contains multiple top-level roots"
    fi
  done < "${listing}"
  [ -n "${top}" ] || fail "Archive listing is empty"
  printf '%s\n' "${top}"
}

initialize_source() {
  local script_path script_dir archive listing extract_dir top
  ensure_work_root

  if [ -n "${SOURCE_OVERRIDE}" ]; then
    [ -d "${SOURCE_OVERRIDE}" ] || fail "LZR1_SOURCE_DIR is not a directory"
    SOURCE_ROOT=$(cd "${SOURCE_OVERRIDE}" 2>/dev/null && pwd -P) || fail "Cannot resolve LZR1_SOURCE_DIR"
    SOURCE_MODE="override"
  else
    script_path=${BASH_SOURCE[0]:-}
    if [ -n "${script_path}" ] && [ -f "${script_path}" ]; then
      script_dir=$(cd "$(dirname -- "${script_path}")" 2>/dev/null && pwd -P) || script_dir=""
    else
      script_dir=""
    fi
    if [ -n "${script_dir}" ] && [ -f "${script_dir}/skills-list.txt" ] && [ -d "${script_dir}/skills" ]; then
      SOURCE_ROOT="${script_dir}"
      SOURCE_MODE="local"
    else
      SOURCE_MODE="archive"
      archive="${WORK_ROOT}/repository.tar.gz"
      listing="${WORK_ROOT}/archive.list"
      extract_dir="${WORK_ROOT}/archive"
      mkdir -p "${extract_dir}" || fail "Cannot create archive extraction directory"
      log_info "Downloading one repository snapshot from GitHub"
      download_file "${ARCHIVE_URL}" "${archive}" || fail "Repository archive download failed"
      command -v tar >/dev/null 2>&1 || fail "tar is required in piped mode"
      tar -tzf "${archive}" > "${listing}" || fail "Repository archive cannot be listed"
      top=$(validate_archive_listing "${listing}")
      tar -xzf "${archive}" -C "${extract_dir}" || fail "Repository archive extraction failed"
      SOURCE_ROOT="${extract_dir}/${top}"
      [ -d "${SOURCE_ROOT}" ] && [ ! -L "${SOURCE_ROOT}" ] || fail "Extracted repository root is unsafe"
      log_info "Downloaded archive SHA-256: $(sha256_file "${archive}")"
    fi
  fi

  [ -f "${SOURCE_ROOT}/skills-list.txt" ] && [ ! -L "${SOURCE_ROOT}/skills-list.txt" ] || fail "Source is missing a regular skills-list.txt"
  [ -d "${SOURCE_ROOT}/skills" ] && [ ! -L "${SOURCE_ROOT}/skills" ] || fail "Source is missing a safe skills directory"
  if find "${SOURCE_ROOT}/skills" -type l -print 2>/dev/null | grep -q .; then
    fail "Source skill packages must not contain symbolic links"
  fi
  validate_manifest
  log_ok "Validated ${SKILL_COUNT} skills from ${SOURCE_MODE} source"
}

validate_manifest() {
  local manifest normalized sorted duplicates inventory CR name path package
  manifest="${SOURCE_ROOT}/skills-list.txt"
  normalized="${WORK_ROOT}/skills.normalized"
  sorted="${WORK_ROOT}/skills.sorted"
  duplicates="${WORK_ROOT}/skills.duplicates"
  inventory="${WORK_ROOT}/skills.inventory"
  : > "${normalized}"
  CR=$(printf '\r')

  while IFS= read -r name || [ -n "${name}" ]; do
    [ -n "${name}" ] || fail "skills-list.txt contains a blank line"
    case "${name}" in
      *"${CR}"*) fail "skills-list.txt must use LF line endings" ;;
      *[!a-z0-9-]*) fail "Invalid skill name in manifest: ${name}" ;;
      -*|*-) fail "Skill names cannot start or end with a hyphen: ${name}" ;;
    esac
    printf '%s\n' "${name}" >> "${normalized}"
  done < "${manifest}"

  LC_ALL=C sort "${normalized}" > "${sorted}"
  cmp -s "${normalized}" "${sorted}" || fail "skills-list.txt must be bytewise sorted"
  uniq -d "${sorted}" > "${duplicates}"
  [ ! -s "${duplicates}" ] || fail "skills-list.txt contains duplicate skill names"

  SKILL_COUNT=$(wc -l < "${normalized}" | tr -d ' ')
  [ "${SKILL_COUNT}" -eq "${EXPECTED_SKILL_COUNT}" ] || fail "Expected ${EXPECTED_SKILL_COUNT} skills, found ${SKILL_COUNT}"

  : > "${inventory}"
  for path in "${SOURCE_ROOT}"/skills/*; do
    [ -d "${path}" ] || continue
    [ ! -L "${path}" ] || fail "Skill directory is a symbolic link: ${path}"
    name=$(basename -- "${path}")
    [ -f "${path}/SKILL.md" ] && [ ! -L "${path}/SKILL.md" ] || fail "Skill package lacks a regular SKILL.md: ${name}"
    printf '%s\n' "${name}" >> "${inventory}"
  done
  LC_ALL=C sort -o "${inventory}" "${inventory}"
  cmp -s "${normalized}" "${inventory}" || fail "skills-list.txt does not exactly match skills/*/SKILL.md"

  while IFS= read -r name; do
    package="${SOURCE_ROOT}/skills/${name}"
    [ -r "${package}/SKILL.md" ] || fail "Skill entrypoint is not readable: ${name}"
  done < "${normalized}"
  SKILL_NAMES=$(cat "${normalized}")
}

acquire_lock() {
  [ "${DRY_RUN}" = true ] && return 0
  [ -n "${HOME:-}" ] && [ "${HOME#/}" != "${HOME}" ] || fail "HOME must be an absolute path"
  if ! mkdir "${LOCK_DIR}" 2>/dev/null; then
    fail "Another installer operation may be active: ${LOCK_DIR}"
  fi
  LOCK_HELD=true
  printf 'pid=%s\nstarted=%s\n' "$$" "${RUN_ID}" > "${LOCK_DIR}/owner"
}

write_marker() {
  local path skill
  path=$1
  skill=$2
  cat > "${path}" <<EOF
schema=1
source=${MANAGED_SOURCE}
skill=${skill}
EOF
}

is_owned_package() {
  local destination skill marker
  destination=$1
  skill=$2
  [ -d "${destination}" ] && [ ! -L "${destination}" ] || return 1
  marker="${destination}/.lzr1-managed"
  [ -f "${marker}" ] && [ ! -L "${marker}" ] || return 1
  grep -Fqx "source=${MANAGED_SOURCE}" "${marker}" && grep -Fqx "skill=${skill}" "${marker}"
}

is_owned_flat() {
  local marker skill
  marker=$1
  skill=$2
  [ -f "${marker}" ] && [ ! -L "${marker}" ] || return 1
  grep -Fqx "source=${MANAGED_SOURCE}" "${marker}" && grep -Fqx "skill=${skill}" "${marker}"
}

is_owned_index() {
  local index mode
  index=$1
  mode=$2
  [ -f "${index}" ] && [ ! -L "${index}" ] || return 1
  grep -Fqx "source=${MANAGED_SOURCE}" "${index}" && grep -Fqx "mode=${mode}" "${index}"
}

path_exists() {
  [ -e "$1" ] || [ -L "$1" ]
}

assert_safe_target() {
  local target relative current old_ifs component
  target=$1
  case "${target}" in
    "${HOME}"/*) ;;
    *) fail "Refusing target outside HOME: ${target}" ;;
  esac
  relative=${target#"${HOME}"/}
  current=${HOME}
  old_ifs=$IFS
  IFS='/'
  for component in ${relative}; do
    [ -n "${component}" ] || continue
    current="${current}/${component}"
    [ ! -L "${current}" ] || { IFS=$old_ifs; fail "Target path contains a symbolic-link component: ${current}"; }
  done
  IFS=$old_ifs
}

preflight_package_target() {
  local target label index name destination
  target=$1
  label=$2
  index="${target}/.lzr1-skills-index"
  if path_exists "${index}" && ! is_owned_index "${index}" package && [ "${FORCE}" != true ]; then
    log_error "${label}: unowned index collision: ${index}"
    return 1
  fi
  while IFS= read -r name; do
    destination="${target}/${name}"
    if path_exists "${destination}" && ! is_owned_package "${destination}" "${name}"; then
      if [ "${FORCE}" != true ]; then
        log_error "${label}: unowned collision: ${destination}; rerun with --force to back it up"
        return 1
      fi
    fi
  done <<EOF
${SKILL_NAMES}
EOF
  return 0
}

preflight_flat_target() {
  local target label marker_root resource_root index name entry resource marker owned
  target=$1
  label=$2
  marker_root="${target}/.lzr1-managed"
  resource_root="${target}/.lzr1-skill-resources"
  index="${target}/.lzr1-skills-index"
  [ ! -L "${marker_root}" ] || { log_error "${label}: marker root is a symbolic link"; return 1; }
  [ ! -L "${resource_root}" ] || { log_error "${label}: resource root is a symbolic link"; return 1; }
  if path_exists "${index}" && ! is_owned_index "${index}" flat && [ "${FORCE}" != true ]; then
    log_error "${label}: unowned index collision: ${index}"
    return 1
  fi
  while IFS= read -r name; do
    entry="${target}/${name}.md"
    resource="${resource_root}/${name}"
    marker="${marker_root}/${name}"
    owned=false
    is_owned_flat "${marker}" "${name}" && owned=true
    if { path_exists "${entry}" || path_exists "${resource}" || path_exists "${marker}"; } && [ "${owned}" != true ] && [ "${FORCE}" != true ]; then
      log_error "${label}: unowned collision for ${name}; rerun with --force to back it up"
      return 1
    fi
  done <<EOF
${SKILL_NAMES}
EOF
  return 0
}

copy_package() {
  local source destination
  source=$1
  destination=$2
  mkdir -p "${destination}" || return 1
  cp -R "${source}/." "${destination}/" || return 1
}

rewrite_flat_entrypoint() {
  local source destination skill directory temporary
  source=$1
  destination=$2
  skill=$3
  cp "${source}" "${destination}" || return 1
  for directory in references scripts templates tests agents assets examples checklists fixtures docs; do
    temporary="${destination}.rewrite"
    sed "s#](${directory}/#](.lzr1-skill-resources/${skill}/${directory}/#g" "${destination}" > "${temporary}" || return 1
    mv "${temporary}" "${destination}" || return 1
  done
}

backup_destination() {
  local old_path target skill component backup_root
  old_path=$1
  target=$2
  skill=$3
  component=$4
  backup_root="${target}/.lzr1-backups/${RUN_ID}/${skill}"
  mkdir -p "${backup_root}" || return 1
  mv "${old_path}" "${backup_root}/${component}" || return 1
  BACKUP_NOTICE="${target}/.lzr1-backups/${RUN_ID}"
}

install_package_skill() {
  local target name source destination stage staged old had_old owned
  target=$1
  name=$2
  source="${SOURCE_ROOT}/skills/${name}"
  destination="${target}/${name}"
  stage=$(mktemp -d "${target}/.lzr1-stage.${name}.XXXXXXXX") || return 1
  staged="${stage}/${name}"
  copy_package "${source}" "${staged}" || { rm -rf -- "${stage}"; return 1; }
  write_marker "${staged}/.lzr1-managed" "${name}" || { rm -rf -- "${stage}"; return 1; }

  old="${target}/.lzr1-old.${RUN_ID}.${name}"
  had_old=false
  owned=false
  if path_exists "${destination}"; then
    had_old=true
    is_owned_package "${destination}" "${name}" && owned=true
    mv "${destination}" "${old}" || { rm -rf -- "${stage}"; return 1; }
  fi

  if ! mv "${staged}" "${destination}"; then
    [ "${had_old}" = true ] && mv "${old}" "${destination}" 2>/dev/null || true
    rm -rf -- "${stage}"
    return 1
  fi
  rm -rf -- "${stage}"

  if [ "${had_old}" = true ]; then
    if [ "${owned}" = true ]; then
      rm -rf -- "${old}" || return 1
    else
      backup_destination "${old}" "${target}" "${name}" package || return 1
    fi
  fi
  return 0
}

restore_flat_old() {
  local old entry resource marker
  old=$1
  entry=$2
  resource=$3
  marker=$4
  path_exists "${entry}" && rm -f -- "${entry}" 2>/dev/null || true
  if path_exists "${resource}"; then
    [ -L "${resource}" ] && rm -f -- "${resource}" || rm -rf -- "${resource}"
  fi
  path_exists "${marker}" && rm -f -- "${marker}" 2>/dev/null || true
  [ -e "${old}/entry.md" ] && mv "${old}/entry.md" "${entry}" 2>/dev/null || true
  [ -e "${old}/resource" ] && mv "${old}/resource" "${resource}" 2>/dev/null || true
  [ -e "${old}/marker" ] && mv "${old}/marker" "${marker}" 2>/dev/null || true
}

install_flat_skill() {
  local target name source marker_root resource_root entry resource marker stage old owned had_old
  target=$1
  name=$2
  source="${SOURCE_ROOT}/skills/${name}"
  marker_root="${target}/.lzr1-managed"
  resource_root="${target}/.lzr1-skill-resources"
  entry="${target}/${name}.md"
  resource="${resource_root}/${name}"
  marker="${marker_root}/${name}"
  stage=$(mktemp -d "${target}/.lzr1-stage.${name}.XXXXXXXX") || return 1
  mkdir -p "${stage}/resource" || { rm -rf -- "${stage}"; return 1; }
  copy_package "${source}" "${stage}/resource" || { rm -rf -- "${stage}"; return 1; }
  rewrite_flat_entrypoint "${source}/SKILL.md" "${stage}/entry.md" "${name}" || { rm -rf -- "${stage}"; return 1; }
  write_marker "${stage}/marker" "${name}" || { rm -rf -- "${stage}"; return 1; }

  old="${target}/.lzr1-old.${RUN_ID}.${name}"
  mkdir -p "${old}" || { rm -rf -- "${stage}"; return 1; }
  owned=false
  is_owned_flat "${marker}" "${name}" && owned=true
  had_old=false
  if path_exists "${entry}"; then mv "${entry}" "${old}/entry.md" || { rm -rf -- "${stage}" "${old}"; return 1; }; had_old=true; fi
  if path_exists "${resource}"; then mv "${resource}" "${old}/resource" || { restore_flat_old "${old}" "${entry}" "${resource}" "${marker}"; rm -rf -- "${stage}" "${old}"; return 1; }; had_old=true; fi
  if path_exists "${marker}"; then mv "${marker}" "${old}/marker" || { restore_flat_old "${old}" "${entry}" "${resource}" "${marker}"; rm -rf -- "${stage}" "${old}"; return 1; }; had_old=true; fi

  if ! mv "${stage}/resource" "${resource}" || ! mv "${stage}/entry.md" "${entry}" || ! mv "${stage}/marker" "${marker}"; then
    restore_flat_old "${old}" "${entry}" "${resource}" "${marker}"
    rm -rf -- "${stage}" "${old}"
    return 1
  fi
  rm -rf -- "${stage}"

  if [ "${had_old}" = true ]; then
    if [ "${owned}" = true ]; then
      rm -rf -- "${old}" || return 1
    else
      backup_destination "${old}" "${target}" "${name}" flat-layout || return 1
    fi
  else
    rm -rf -- "${old}"
  fi
  return 0
}

write_index() {
  local target mode index staged old had_old owned name
  target=$1
  mode=$2
  index="${target}/.lzr1-skills-index"
  staged="${target}/.lzr1-index.${RUN_ID}.tmp"
  {
    printf 'schema=1\nsource=%s\nmode=%s\ncount=%s\n' "${MANAGED_SOURCE}" "${mode}" "${SKILL_COUNT}"
    while IFS= read -r name; do printf 'skill=%s\n' "${name}"; done <<EOF
${SKILL_NAMES}
EOF
  } > "${staged}" || return 1

  old="${target}/.lzr1-index.${RUN_ID}.old"
  had_old=false
  owned=false
  if path_exists "${index}"; then
    had_old=true
    is_owned_index "${index}" "${mode}" && owned=true
    mv "${index}" "${old}" || { rm -f -- "${staged}"; return 1; }
  fi
  if ! mv "${staged}" "${index}"; then
    [ "${had_old}" = true ] && mv "${old}" "${index}" 2>/dev/null || true
    return 1
  fi
  if [ "${had_old}" = true ]; then
    if [ "${owned}" = true ]; then
      rm -f -- "${old}" || return 1
    else
      backup_destination "${old}" "${target}" index index || return 1
    fi
  fi
  return 0
}

install_target() {
  local target label mode installed name
  target=$1
  label=$2
  mode=$3
  assert_safe_target "${target}"

  if [ "${mode}" = package ]; then
    preflight_package_target "${target}" "${label}" || return 1
  else
    preflight_flat_target "${target}" "${label}" || return 1
  fi

  if [ "${DRY_RUN}" = true ]; then
    log_ok "${label}: would install ${SKILL_COUNT} ${mode} skills to ${target}"
    return 0
  fi

  mkdir -p "${target}" || { log_error "${label}: cannot create ${target}"; return 1; }
  [ ! -L "${target}" ] || { log_error "${label}: target became a symbolic link"; return 1; }
  if [ "${mode}" = flat ]; then
    mkdir -p "${target}/.lzr1-managed" "${target}/.lzr1-skill-resources" || return 1
  fi

  installed=0
  while IFS= read -r name; do
    if [ "${mode}" = package ]; then
      install_package_skill "${target}" "${name}" || { log_error "${label}: failed while installing ${name}"; return 1; }
    else
      install_flat_skill "${target}" "${name}" || { log_error "${label}: failed while installing ${name}"; return 1; }
    fi
    installed=$((installed + 1))
    log_verbose "${label}: ${name}"
  done <<EOF
${SKILL_NAMES}
EOF
  write_index "${target}" "${mode}" || { log_error "${label}: failed to write managed index"; return 1; }
  log_ok "${label}: installed ${installed}/${SKILL_COUNT} skills to ${target}"
  return 0
}

remove_path_safely() {
  local path
  path=$1
  if [ -L "${path}" ]; then
    rm -f -- "${path}"
  elif [ -d "${path}" ]; then
    rm -rf -- "${path}"
  else
    rm -f -- "${path}"
  fi
}

managed_names() {
  local target mode index
  target=$1
  mode=$2
  index="${target}/.lzr1-skills-index"
  if is_owned_index "${index}" "${mode}"; then
    sed -n 's/^skill=\([a-z0-9][a-z0-9-]*\)$/\1/p' "${index}"
  else
    printf '%s\n' "${SKILL_NAMES}"
  fi
}

remove_target() {
  local target label mode names removed name destination entry resource marker index
  target=$1
  label=$2
  mode=$3
  assert_safe_target "${target}"
  [ -d "${target}" ] && [ ! -L "${target}" ] || { log_info "${label}: target not present"; return 0; }
  names="${WORK_ROOT}/remove.$$.${mode}.names"
  managed_names "${target}" "${mode}" > "${names}"
  removed=0
  while IFS= read -r name; do
    case "${name}" in *[!a-z0-9-]*|'') log_warn "${label}: ignored invalid index entry"; continue ;; esac
    if [ "${mode}" = package ]; then
      destination="${target}/${name}"
      if is_owned_package "${destination}" "${name}"; then
        if [ "${DRY_RUN}" = true ]; then
          log_verbose "[dry-run] remove ${destination}"
        else
          remove_path_safely "${destination}" || return 1
        fi
        removed=$((removed + 1))
      elif path_exists "${destination}"; then
        log_warn "${label}: leaving unowned path ${destination}"
      fi
    else
      entry="${target}/${name}.md"
      resource="${target}/.lzr1-skill-resources/${name}"
      marker="${target}/.lzr1-managed/${name}"
      if is_owned_flat "${marker}" "${name}"; then
        if [ "${DRY_RUN}" = true ]; then
          log_verbose "[dry-run] remove flat package ${name}"
        else
          remove_path_safely "${entry}" || return 1
          remove_path_safely "${resource}" || return 1
          remove_path_safely "${marker}" || return 1
        fi
        removed=$((removed + 1))
      elif path_exists "${entry}" || path_exists "${resource}" || path_exists "${marker}"; then
        log_warn "${label}: leaving unowned flat content for ${name}"
      fi
    fi
  done < "${names}"

  index="${target}/.lzr1-skills-index"
  if is_owned_index "${index}" "${mode}" && [ "${DRY_RUN}" != true ]; then
    rm -f -- "${index}" || return 1
  fi
  if [ "${mode}" = flat ] && [ "${DRY_RUN}" != true ]; then
    rmdir "${target}/.lzr1-managed" "${target}/.lzr1-skill-resources" 2>/dev/null || true
  fi
  log_ok "${label}: removed ${removed} managed skills"
}

tool_is_selected() {
  case "$1" in
    claude-code) [ "${OPT_CLAUDE_CODE}" = true ] ;;
    claude-desktop) [ "${OPT_CLAUDE_DESKTOP}" = true ] ;;
    codex) [ "${OPT_CODEX}" = true ] ;;
    opencode) [ "${OPT_OPENCODE}" = true ] ;;
    factory) [ "${OPT_FACTORY}" = true ] ;;
    cursor) [ "${OPT_CURSOR}" = true ] ;;
    vscode) [ "${OPT_VSCODE}" = true ] ;;
    antigravity) [ "${OPT_ANTIGRAVITY}" = true ] ;;
    agy) [ "${OPT_AGY}" = true ] ;;
    *) return 1 ;;
  esac
}

emit_selected_tools() {
  [ "${OPT_CLAUDE_CODE}" = true ] && printf 'claude-code\n'
  [ "${OPT_CLAUDE_DESKTOP}" = true ] && printf 'claude-desktop\n'
  [ "${OPT_CODEX}" = true ] && printf 'codex\n'
  [ "${OPT_OPENCODE}" = true ] && printf 'opencode\n'
  [ "${OPT_FACTORY}" = true ] && printf 'factory\n'
  [ "${OPT_CURSOR}" = true ] && printf 'cursor\n'
  [ "${OPT_VSCODE}" = true ] && printf 'vscode\n'
  [ "${OPT_ANTIGRAVITY}" = true ] && printf 'antigravity\n'
  [ "${OPT_AGY}" = true ] && printf 'agy\n'
}

save_state() {
  local candidate normalized tool
  [ "${DRY_RUN}" = true ] && return 0
  [ ! -L "${STATE_FILE}" ] || { log_error "State file must not be a symbolic link"; return 1; }
  candidate=$(mktemp "${STATE_FILE}.candidate.XXXXXXXX") || return 1
  normalized=$(mktemp "${STATE_FILE}.normalized.XXXXXXXX") || { rm -f -- "${candidate}"; return 1; }
  if [ -f "${STATE_FILE}" ]; then
    while IFS= read -r tool; do
      case "${tool}" in
        claude-code|claude-desktop|codex|opencode|factory|cursor|vscode|antigravity|agy) printf '%s\n' "${tool}" ;;
      esac
    done < "${STATE_FILE}" > "${candidate}"
  else
    : > "${candidate}"
  fi
  emit_selected_tools >> "${candidate}"
  LC_ALL=C sort -u "${candidate}" > "${normalized}" || { rm -f -- "${candidate}" "${normalized}"; return 1; }
  chmod 600 "${normalized}" 2>/dev/null || true
  mv "${normalized}" "${STATE_FILE}" || { rm -f -- "${candidate}" "${normalized}"; return 1; }
  rm -f -- "${candidate}"
}

remove_selected_from_state() {
  local temporary tool
  [ "${DRY_RUN}" = true ] && return 0
  [ ! -L "${STATE_FILE}" ] || { log_error "State file must not be a symbolic link"; return 1; }
  [ -f "${STATE_FILE}" ] || return 0
  temporary=$(mktemp "${STATE_FILE}.tmp.XXXXXXXX") || return 1
  while IFS= read -r tool; do
    case "${tool}" in
      claude-code|claude-desktop|codex|opencode|factory|cursor|vscode|antigravity|agy)
        tool_is_selected "${tool}" || printf '%s\n' "${tool}" >> "${temporary}"
        ;;
    esac
  done < "${STATE_FILE}"
  if [ -s "${temporary}" ]; then
    chmod 600 "${temporary}" 2>/dev/null || true
    mv "${temporary}" "${STATE_FILE}" || return 1
  else
    rm -f -- "${temporary}" "${STATE_FILE}" || return 1
  fi
}

load_state() {
  local tool
  [ -f "${STATE_FILE}" ] && [ ! -L "${STATE_FILE}" ] || return 0
  while IFS= read -r tool; do
    case "${tool}" in
      claude-code) OPT_CLAUDE_CODE=true ;;
      claude-desktop) OPT_CLAUDE_DESKTOP=true ;;
      codex) OPT_CODEX=true ;;
      opencode) OPT_OPENCODE=true ;;
      factory) OPT_FACTORY=true ;;
      cursor) OPT_CURSOR=true ;;
      vscode) OPT_VSCODE=true ;;
      antigravity) OPT_ANTIGRAVITY=true ;;
      agy) OPT_AGY=true ;;
      '') ;;
      *) log_warn "Ignoring unknown state entry: ${tool}" ;;
    esac
  done < "${STATE_FILE}"
}

run_selected_install() {
  local failed
  failed=0
  [ "${OPT_CLAUDE_CODE}" = true ] && install_target "${PATH_CLAUDE_CODE}/skills" "Claude Code" package || { [ "${OPT_CLAUDE_CODE}" = true ] && failed=$((failed + 1)) || true; }
  [ "${OPT_CLAUDE_DESKTOP}" = true ] && install_target "${PATH_CLAUDE_DESKTOP}/skills" "Claude Desktop" package || { [ "${OPT_CLAUDE_DESKTOP}" = true ] && failed=$((failed + 1)) || true; }
  [ "${OPT_CODEX}" = true ] && install_target "${PATH_CODEX}/skills" "Codex" package || { [ "${OPT_CODEX}" = true ] && failed=$((failed + 1)) || true; }
  [ "${OPT_OPENCODE}" = true ] && install_target "${PATH_OPENCODE}/skill" "OpenCode" package || { [ "${OPT_OPENCODE}" = true ] && failed=$((failed + 1)) || true; }
  [ "${OPT_FACTORY}" = true ] && install_target "${PATH_FACTORY}/skills" "Factory" package || { [ "${OPT_FACTORY}" = true ] && failed=$((failed + 1)) || true; }
  [ "${OPT_CURSOR}" = true ] && install_target "${PATH_CURSOR}/rules" "Cursor" flat || { [ "${OPT_CURSOR}" = true ] && failed=$((failed + 1)) || true; }
  [ "${OPT_VSCODE}" = true ] && install_target "${PATH_VSCODE}/lzr1-skills" "VS Code" flat || { [ "${OPT_VSCODE}" = true ] && failed=$((failed + 1)) || true; }
  [ "${OPT_ANTIGRAVITY}" = true ] && install_target "${PATH_ANTIGRAVITY}/rules" "Antigravity" flat || { [ "${OPT_ANTIGRAVITY}" = true ] && failed=$((failed + 1)) || true; }
  [ "${OPT_AGY}" = true ] && install_target "${PATH_AGY}/skills" "Antigravity AGY" package || { [ "${OPT_AGY}" = true ] && failed=$((failed + 1)) || true; }
  [ "${failed}" -eq 0 ] || return 1
  save_state || return 1
  [ -n "${BACKUP_NOTICE}" ] && log_warn "Unowned collisions were backed up under ${BACKUP_NOTICE}"
  return 0
}

run_selected_remove() {
  local failed
  failed=0
  [ "${OPT_CLAUDE_CODE}" = true ] && remove_target "${PATH_CLAUDE_CODE}/skills" "Claude Code" package || { [ "${OPT_CLAUDE_CODE}" = true ] && failed=$((failed + 1)) || true; }
  [ "${OPT_CLAUDE_DESKTOP}" = true ] && remove_target "${PATH_CLAUDE_DESKTOP}/skills" "Claude Desktop" package || { [ "${OPT_CLAUDE_DESKTOP}" = true ] && failed=$((failed + 1)) || true; }
  [ "${OPT_CODEX}" = true ] && remove_target "${PATH_CODEX}/skills" "Codex" package || { [ "${OPT_CODEX}" = true ] && failed=$((failed + 1)) || true; }
  [ "${OPT_OPENCODE}" = true ] && remove_target "${PATH_OPENCODE}/skill" "OpenCode" package || { [ "${OPT_OPENCODE}" = true ] && failed=$((failed + 1)) || true; }
  [ "${OPT_FACTORY}" = true ] && remove_target "${PATH_FACTORY}/skills" "Factory" package || { [ "${OPT_FACTORY}" = true ] && failed=$((failed + 1)) || true; }
  [ "${OPT_CURSOR}" = true ] && remove_target "${PATH_CURSOR}/rules" "Cursor" flat || { [ "${OPT_CURSOR}" = true ] && failed=$((failed + 1)) || true; }
  [ "${OPT_VSCODE}" = true ] && remove_target "${PATH_VSCODE}/lzr1-skills" "VS Code" flat || { [ "${OPT_VSCODE}" = true ] && failed=$((failed + 1)) || true; }
  [ "${OPT_ANTIGRAVITY}" = true ] && remove_target "${PATH_ANTIGRAVITY}/rules" "Antigravity" flat || { [ "${OPT_ANTIGRAVITY}" = true ] && failed=$((failed + 1)) || true; }
  [ "${OPT_AGY}" = true ] && remove_target "${PATH_AGY}/skills" "Antigravity AGY" package || { [ "${OPT_AGY}" = true ] && failed=$((failed + 1)) || true; }
  [ "${failed}" -eq 0 ] || return 1
  remove_selected_from_state || return 1
  return 0
}

doctor_target() {
  local label target mode installed name marker
  label=$1
  target=$2
  mode=$3
  installed=0
  if [ -d "${target}" ] && [ ! -L "${target}" ]; then
    while IFS= read -r name; do
      if [ "${mode}" = package ]; then
        is_owned_package "${target}/${name}" "${name}" && [ -f "${target}/${name}/SKILL.md" ] && installed=$((installed + 1))
      else
        marker="${target}/.lzr1-managed/${name}"
        is_owned_flat "${marker}" "${name}" && [ -f "${target}/${name}.md" ] && [ -f "${target}/.lzr1-skill-resources/${name}/SKILL.md" ] && installed=$((installed + 1))
      fi
    done <<EOF
${SKILL_NAMES}
EOF
  fi
  if [ "${installed}" -eq "${SKILL_COUNT}" ]; then
    printf '  [OK]   %-20s %d/%d managed skills\n' "${label}" "${installed}" "${SKILL_COUNT}"
  elif [ "${installed}" -eq 0 ]; then
    printf '  [NONE] %-20s 0/%d managed skills\n' "${label}" "${SKILL_COUNT}"
  else
    printf '  [WARN] %-20s %d/%d managed skills\n' "${label}" "${installed}" "${SKILL_COUNT}"
  fi
}

doctor() {
  printf '\n%sDoctor report%s\n' "${BOLD}" "${RESET}"
  printf '  Source: %s (%s skills)\n' "${SOURCE_MODE}" "${SKILL_COUNT}"
  doctor_target "Claude Code" "${PATH_CLAUDE_CODE}/skills" package
  doctor_target "Claude Desktop" "${PATH_CLAUDE_DESKTOP}/skills" package
  doctor_target "Codex" "${PATH_CODEX}/skills" package
  doctor_target "OpenCode" "${PATH_OPENCODE}/skill" package
  doctor_target "Factory" "${PATH_FACTORY}/skills" package
  doctor_target "Cursor" "${PATH_CURSOR}/rules" flat
  doctor_target "VS Code" "${PATH_VSCODE}/lzr1-skills" flat
  doctor_target "Antigravity" "${PATH_ANTIGRAVITY}/rules" flat
  doctor_target "Antigravity AGY" "${PATH_AGY}/skills" package
  printf '\n'
}

show_menu() {
  local selection old_ifs number action_input
  [ -r /dev/tty ] && [ -w /dev/tty ] || fail "No interactive terminal; pass --detected --yes or explicit target flags"
  print_banner
  printf 'Select targets (comma-separated), d for detected, a for all, or q to quit:\n'
  printf '  1 Claude Code%s\n' "$([ "${FOUND_CLAUDE_CODE}" = true ] && printf ' [detected]' || true)"
  printf '  2 Claude Desktop%s\n' "$([ "${FOUND_CLAUDE_DESKTOP}" = true ] && printf ' [detected]' || true)"
  printf '  3 Codex%s\n' "$([ "${FOUND_CODEX}" = true ] && printf ' [detected]' || true)"
  printf '  4 OpenCode%s\n' "$([ "${FOUND_OPENCODE}" = true ] && printf ' [detected]' || true)"
  printf '  5 Factory%s\n' "$([ "${FOUND_FACTORY}" = true ] && printf ' [detected]' || true)"
  printf '  6 Cursor%s\n' "$([ "${FOUND_CURSOR}" = true ] && printf ' [detected]' || true)"
  printf '  7 VS Code%s\n' "$([ "${FOUND_VSCODE}" = true ] && printf ' [detected]' || true)"
  printf '  8 Antigravity%s\n' "$([ "${FOUND_ANTIGRAVITY}" = true ] && printf ' [detected]' || true)"
  printf '  9 Antigravity AGY%s\n' "$([ "${FOUND_AGY}" = true ] && printf ' [detected]' || true)"
  printf '> '
  IFS= read -r selection < /dev/tty || fail "Unable to read target selection"
  selection=$(printf '%s' "${selection}" | tr '[:upper:]' '[:lower:]' | tr -d ' ')
  case "${selection}" in
    q|quit|exit) exit 0 ;;
    a|all) set_all_targets ;;
    d|detected) select_detected_targets ;;
    *)
      old_ifs=$IFS
      IFS=','
      for number in ${selection}; do
        case "${number}" in
          1) OPT_CLAUDE_CODE=true ;;
          2) OPT_CLAUDE_DESKTOP=true ;;
          3) OPT_CODEX=true ;;
          4) OPT_OPENCODE=true ;;
          5) OPT_FACTORY=true ;;
          6) OPT_CURSOR=true ;;
          7) OPT_VSCODE=true ;;
          8) OPT_ANTIGRAVITY=true ;;
          9) OPT_AGY=true ;;
          *) fail "Unknown target selection: ${number}" ;;
        esac
      done
      IFS=$old_ifs
      ;;
  esac
  any_target_selected || fail "No tools selected"

  if [ "${ACTION}" = install ]; then
    printf 'Action [i]nstall, [u]pdate, [r]emove (default install): '
    IFS= read -r action_input < /dev/tty || true
    action_input=$(printf '%s' "${action_input}" | tr '[:upper:]' '[:lower:]')
    case "${action_input}" in
      u|update) ACTION=update ;;
      r|remove) ACTION=remove ;;
      ''|i|install) ACTION=install ;;
      *) fail "Unknown action selection: ${action_input}" ;;
    esac
  fi
}

main() {
  [ -n "${HOME:-}" ] || fail "HOME is required"
  case "${HOME}" in /*) ;; *) fail "HOME must be an absolute path" ;; esac
  parse_args "$@"
  detect_os_and_tools

  if [ "${SELECT_DETECTED}" = true ]; then
    select_detected_targets
  fi
  case "${AUTO_MODE}" in
    1|true|TRUE|yes|YES)
      if [ "${HAS_TARGET_FLAG}" != true ]; then select_detected_targets; fi
      YES_MODE=true
      ;;
  esac

  if [ "${ACTION}" = update ] && ! any_target_selected; then
    load_state
  fi

  if [ "${ACTION}" = install ] || [ "${ACTION}" = remove ]; then
    if ! any_target_selected; then
      if [ "${YES_MODE}" = true ]; then
        fail "Non-interactive mode requires --detected or explicit target flags"
      fi
      show_menu
    fi
  fi

  if [ "${ACTION}" = update ] && ! any_target_selected; then
    fail "No saved targets found; run install or pass explicit target flags"
  fi

  initialize_source

  case "${ACTION}" in
    doctor)
      doctor
      ;;
    install|update)
      acquire_lock
      run_selected_install || fail "One or more target installations failed"
      log_ok "Installation complete: ${SKILL_COUNT} skills from one validated source snapshot"
      ;;
    remove)
      acquire_lock
      run_selected_remove || fail "One or more target removals failed"
      log_ok "Managed skill removal complete"
      ;;
    *) fail "Unsupported action: ${ACTION}" ;;
  esac
}

main "$@"
