#!/usr/bin/env bash
# lzr1-skills installer — macOS + Linux, Bash 3.2+
# Supports: Claude Code, Claude Desktop, Codex, OpenCode, Factory,
#           Cursor, VS Code, Antigravity, Antigravity AGY

# ── Strict mode (compatible) ──────────────────────────────────────────────────
set -uo pipefail

# ── Constants ─────────────────────────────────────────────────────────────────
REPO="victorlazari/lzr1-skills"
RAW_BASE="https://raw.githubusercontent.com/${REPO}/main"
SKILLS_MANIFEST_URL="${RAW_BASE}/skills-list.txt"
VERSION="1.0.0"
STATE_FILE="${HOME}/.lzr1-skills-state"

# ── Colors ────────────────────────────────────────────────────────────────────
if [ -t 1 ] && command -v tput >/dev/null 2>&1; then
  RED=$(tput setaf 1)
  GREEN=$(tput setaf 2)
  YELLOW=$(tput setaf 3)
  BLUE=$(tput setaf 4)
  CYAN=$(tput setaf 6)
  MAGENTA=$(tput setaf 5)
  WHITE=$(tput setaf 7)
  BOLD=$(tput bold)
  DIM=$(tput dim 2>/dev/null || printf '')
  RESET=$(tput sgr0)
else
  RED='' GREEN='' YELLOW='' BLUE='' CYAN='' MAGENTA='' WHITE='' BOLD='' DIM='' RESET=''
fi

# ── Flags ─────────────────────────────────────────────────────────────────────
ACTION="install"
CURL_MODE=false
DRY_RUN=false
VERBOSE=false
YES_MODE=false
AUTO_MODE="${LZRI_AUTO:-false}"

# Tool flags (set to true when --flag or --all is used)
OPT_CLAUDE_CODE=false
OPT_CLAUDE_DESKTOP=false
OPT_CODEX=false
OPT_OPENCODE=false
OPT_FACTORY=false
OPT_CURSOR=false
OPT_VSCODE=false
OPT_ANTIGRAVITY=false
OPT_AGY=false

# ── Logging helpers ───────────────────────────────────────────────────────────
log_info()    { printf "%s  %s%s%s\n" "${CYAN}→${RESET}" "${BOLD}" "$*" "${RESET}"; }
log_success() { printf "%s  %s%s%s\n" "${GREEN}✓${RESET}" "${BOLD}" "$*" "${RESET}"; }
log_warn()    { printf "%s  %s%s%s\n" "${YELLOW}⚠${RESET}" "${YELLOW}" "$*" "${RESET}"; }
log_error()   { printf "%s  %s%s%s\n" "${RED}✗${RESET}" "${RED}" "$*" "${RESET}" >&2; }
log_dim()     { printf "   %s%s%s\n" "${DIM}" "$*" "${RESET}"; }

# ── Banner ────────────────────────────────────────────────────────────────────
print_banner() {
  printf "\n"
  printf "%s%s" "${CYAN}${BOLD}" ""
  printf '  ██╗     ███████╗██████╗  ██╗    ███████╗██╗  ██╗██╗██╗     ██╗     ███████╗\n'
  printf '  ██║     ╚════██║██╔══██╗ ╚═╝    ██╔════╝██║ ██╔╝██║██║     ██║     ██╔════╝\n'
  printf '  ██║         ██╔╝██████╔╝        ███████╗█████╔╝ ██║██║     ██║     ███████╗\n'
  printf '  ██║        ██╔╝ ██╔══██╗        ╚════██║██╔═██╗ ██║██║     ██║     ╚════██║\n'
  printf '  ███████╗   ██║  ██║  ██║        ███████║██║  ██╗██║███████╗███████╗███████║\n'
  printf '  ╚══════╝   ╚═╝  ╚═╝  ╚═╝        ╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚══════╝\n'
  printf '%s\n' "${RESET}"
  printf "  %s%sAI Skills for your favorite coding tools%s  %sv%s%s\n\n" \
    "${DIM}" "${WHITE}" "${RESET}" "${DIM}" "${VERSION}" "${RESET}"
  printf "  %s%shttps://github.com/%s%s\n\n" "${DIM}" "${BLUE}" "${REPO}" "${RESET}"
}

# ── OS Detection ──────────────────────────────────────────────────────────────
OS_TYPE=""
ARCH=""

detect_os() {
  case "$(uname -s)" in
    Darwin) OS_TYPE="macos" ;;
    Linux)  OS_TYPE="linux" ;;
    *)      OS_TYPE="unknown" ;;
  esac

  case "$(uname -m)" in
    arm64|aarch64) ARCH="arm64" ;;
    x86_64|amd64)  ARCH="x86_64" ;;
    *)             ARCH="unknown" ;;
  esac
}

# ── Tool Detection ────────────────────────────────────────────────────────────
FOUND_CLAUDE_CODE=false
FOUND_CLAUDE_DESKTOP=false
FOUND_CODEX=false
FOUND_OPENCODE=false
FOUND_FACTORY=false
FOUND_CURSOR=false
FOUND_VSCODE=false
FOUND_ANTIGRAVITY=false
FOUND_AGY=false

# Paths
PATH_CLAUDE_CODE="${HOME}/.claude"
PATH_CODEX="${HOME}/.codex"
PATH_OPENCODE="${HOME}/.config/opencode"
PATH_FACTORY="${HOME}/.factory"
PATH_CURSOR="${HOME}/.cursor"
PATH_VSCODE="${HOME}/.vscode"
PATH_ANTIGRAVITY="${HOME}/.antigravity-ide"
PATH_AGY=""  # set in detect_tools based on OS

detect_tools() {
  detect_os

  [ -d "${PATH_CLAUDE_CODE}" ] && FOUND_CLAUDE_CODE=true

  if [ "${OS_TYPE}" = "macos" ]; then
    PATH_CLAUDE_DESKTOP="${HOME}/Library/Application Support/Claude"
    PATH_AGY="${HOME}/Library/Application Support/Antigravity"
  else
    PATH_CLAUDE_DESKTOP="${HOME}/.config/claude"
    PATH_AGY="${HOME}/.config/antigravity"
  fi
  [ -d "${PATH_CLAUDE_DESKTOP}" ] && FOUND_CLAUDE_DESKTOP=true

  [ -d "${PATH_CODEX}" ]        && FOUND_CODEX=true
  [ -d "${PATH_OPENCODE}" ]     && FOUND_OPENCODE=true
  [ -d "${PATH_FACTORY}" ]      && FOUND_FACTORY=true
  [ -d "${PATH_CURSOR}" ]       && FOUND_CURSOR=true
  [ -d "${PATH_VSCODE}" ]       && FOUND_VSCODE=true
  [ -d "${PATH_ANTIGRAVITY}" ]  && FOUND_ANTIGRAVITY=true
  [ -d "${PATH_AGY}" ]          && FOUND_AGY=true
}

# ── Skills source ─────────────────────────────────────────────────────────────
# List of skill names (populated by load_skill_names)
SKILL_NAMES=""

load_skill_names() {
  if [ "${CURL_MODE}" = true ]; then
    # Fetch manifest from GitHub
    if command -v curl >/dev/null 2>&1; then
      SKILL_NAMES=$(curl -fsSL "${SKILLS_MANIFEST_URL}" 2>/dev/null) || true
    elif command -v wget >/dev/null 2>&1; then
      SKILL_NAMES=$(wget -qO- "${SKILLS_MANIFEST_URL}" 2>/dev/null) || true
    fi
    if [ -z "${SKILL_NAMES}" ]; then
      # Fallback: hardcoded list
      SKILL_NAMES="ai-ml-engineering
content-communications
cron-master
customer-support
data-analytics
design-ux
devops-infrastructure
executive-leadership
finance
gcalendar
google-workspace-bot-integration
hr-people
it-administration
legal-compliance
legendary-readme
marketing
meeting-engineering
one-page
operations
product-management
prompt-master
quality-assurance
research-development
sales
security-engineering
security-review
software-engineering
supply-chain
tomate-pos80
trivy-scanner
vonage-voice
web-presentation-creator"
    fi
  else
    # Local mode: discover from skills/ dir
    local script_dir
    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    if [ -d "${script_dir}/skills" ]; then
      SKILL_NAMES=$(find "${script_dir}/skills" -name "SKILL.md" | \
        sed 's|.*/skills/||' | sed 's|/SKILL.md||' | sort)
    fi
  fi
}

# Get source path for a skill (SKILL.md)
get_skill_source() {
  local skill_name="$1"
  if [ "${CURL_MODE}" = true ]; then
    echo "${RAW_BASE}/skills/${skill_name}/SKILL.md"
  else
    local script_dir
    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    echo "${script_dir}/skills/${skill_name}/SKILL.md"
  fi
}

# ── Spinner ───────────────────────────────────────────────────────────────────
SPINNER_PID=""

spinner_start() {
  local msg="$1"
  printf "   %s%s%s " "${CYAN}" "${msg}" "${RESET}"
  (
    while true; do
      for c in '⠋' '⠙' '⠹' '⠸' '⠼' '⠴' '⠦' '⠧' '⠇' '⠏'; do
        printf "\r   %s%s%s %s" "${CYAN}" "${msg}" "${RESET}" "${c}"
        sleep 0.1
      done
    done
  ) &
  SPINNER_PID=$!
}

spinner_stop() {
  if [ -n "${SPINNER_PID}" ]; then
    kill "${SPINNER_PID}" 2>/dev/null || true
    wait "${SPINNER_PID}" 2>/dev/null || true
    SPINNER_PID=""
    printf "\r"
  fi
}

# ── Core install primitive ────────────────────────────────────────────────────
# install_skill_to_dir <skill_name> <target_dir> [subdir]
# subdir=true  → target_dir/<name>/SKILL.md  (Codex, Claude Code style)
# subdir=false → target_dir/<name>.md        (Cursor, flat style)
install_skill_to_dir() {
  local skill_name="$1"
  local target_dir="$2"
  local use_subdir="${3:-false}"

  local source
  source="$(get_skill_source "${skill_name}")"
  local dest
  if [ "${use_subdir}" = true ]; then
    dest="${target_dir}/${skill_name}/SKILL.md"
    mkdir -p "${target_dir}/${skill_name}"
  else
    dest="${target_dir}/${skill_name}.md"
    mkdir -p "${target_dir}"
  fi

  if [ "${DRY_RUN}" = true ]; then
    log_dim "[dry-run] would install ${skill_name} → ${dest}"
    return 0
  fi

  if [ "${CURL_MODE}" = true ]; then
    if command -v curl >/dev/null 2>&1; then
      curl -fsSL "${source}" -o "${dest}" 2>/dev/null || {
        log_warn "Failed to download ${skill_name}"
        return 1
      }
    elif command -v wget >/dev/null 2>&1; then
      wget -qO "${dest}" "${source}" 2>/dev/null || {
        log_warn "Failed to download ${skill_name}"
        return 1
      }
    else
      log_error "Neither curl nor wget found. Cannot download skills."
      return 1
    fi
  else
    if [ ! -f "${source}" ]; then
      log_warn "Source not found: ${source}"
      return 1
    fi
    cp "${source}" "${dest}" || {
      log_warn "Failed to copy ${skill_name}"
      return 1
    }
  fi

  [ "${VERBOSE}" = true ] && log_dim "  ✓ ${skill_name} → ${dest}"
  return 0
}

# Install all skills to a target directory
# install_all_skills_to <target_dir> <label> [subdir]
install_all_skills_to() {
  local target_dir="$1"
  local tool_label="$2"
  local use_subdir="${3:-false}"
  local count=0
  local failed=0

  mkdir -p "${target_dir}"
  spinner_start "Installing skills for ${tool_label}"

  local name
  while IFS= read -r name; do
    [ -z "${name}" ] && continue
    if install_skill_to_dir "${name}" "${target_dir}" "${use_subdir}" 2>/dev/null; then
      count=$((count + 1))
    else
      failed=$((failed + 1))
    fi
  done <<EOF
${SKILL_NAMES}
EOF

  spinner_stop
  if [ "${failed}" -eq 0 ]; then
    log_success "${tool_label}: ${count} skills → ${target_dir}"
  else
    log_warn "${tool_label}: ${count} skills OK, ${failed} failed → ${target_dir}"
  fi
}

# Remove all lzr1 skills from a directory
# remove_skills_from <target_dir> <label> [subdir]
remove_skills_from() {
  local target_dir="$1"
  local tool_label="$2"
  local use_subdir="${3:-false}"
  local count=0

  if [ ! -d "${target_dir}" ]; then
    log_dim "${tool_label}: directory not found, skipping"
    return 0
  fi

  local name
  while IFS= read -r name; do
    [ -z "${name}" ] && continue
    if [ "${use_subdir}" = true ]; then
      local dest="${target_dir}/${name}"
      if [ -d "${dest}" ]; then
        if [ "${DRY_RUN}" = true ]; then
          log_dim "[dry-run] would remove ${dest}/"
        else
          rm -rf "${dest}"
        fi
        count=$((count + 1))
      fi
    else
      local dest="${target_dir}/${name}.md"
      if [ -f "${dest}" ]; then
        if [ "${DRY_RUN}" = true ]; then
          log_dim "[dry-run] would remove ${dest}"
        else
          rm -f "${dest}"
        fi
        count=$((count + 1))
      fi
    fi
  done <<EOF
${SKILL_NAMES}
EOF

  log_success "${tool_label}: removed ${count} skills from ${target_dir}"
}

# ── Per-tool installers ───────────────────────────────────────────────────────
install_claude_code() {
  install_all_skills_to "${PATH_CLAUDE_CODE}/skills" "Claude Code" true
}

install_claude_desktop() {
  install_all_skills_to "${PATH_CLAUDE_DESKTOP}/skills" "Claude Desktop" true
}

install_codex() {
  # Clean up any stale flat .md files from older installer versions
  local name
  while IFS= read -r name; do
    [ -z "${name}" ] && continue
    rm -f "${PATH_CODEX}/skills/${name}.md" 2>/dev/null || true
  done <<EOF
${SKILL_NAMES}
EOF
  install_all_skills_to "${PATH_CODEX}/skills" "Codex" true
}

install_opencode() {
  install_all_skills_to "${PATH_OPENCODE}/skills" "OpenCode" true
}

install_factory() {
  install_all_skills_to "${PATH_FACTORY}/skills" "Factory" true
}

install_cursor() {
  install_all_skills_to "${PATH_CURSOR}/rules" "Cursor"
}

install_vscode() {
  install_all_skills_to "${PATH_VSCODE}/lzr1-skills" "VS Code"
}

install_antigravity() {
  install_all_skills_to "${PATH_ANTIGRAVITY}/rules" "Antigravity"
}

install_agy() {
  install_all_skills_to "${PATH_AGY}/skills" "Antigravity AGY" true
}

# ── Per-tool removers ─────────────────────────────────────────────────────────
remove_claude_code()    { remove_skills_from "${PATH_CLAUDE_CODE}/skills" "Claude Code" true; }
remove_claude_desktop() { remove_skills_from "${PATH_CLAUDE_DESKTOP}/skills" "Claude Desktop" true; }
remove_codex()          { remove_skills_from "${PATH_CODEX}/skills" "Codex" true; }
remove_opencode()       { remove_skills_from "${PATH_OPENCODE}/skills" "OpenCode" true; }
remove_factory()        { remove_skills_from "${PATH_FACTORY}/skills" "Factory" true; }
remove_cursor()         { remove_skills_from "${PATH_CURSOR}/rules" "Cursor"; }
remove_vscode()         { remove_skills_from "${PATH_VSCODE}/lzr1-skills" "VS Code"; }
remove_antigravity()    { remove_skills_from "${PATH_ANTIGRAVITY}/rules" "Antigravity"; }
remove_agy()            { remove_skills_from "${PATH_AGY}/skills" "Antigravity AGY" true; }

# ── State file ────────────────────────────────────────────────────────────────
save_state() {
  local tools=""
  [ "${OPT_CLAUDE_CODE}" = true ]    && tools="${tools}claude-code\n"
  [ "${OPT_CLAUDE_DESKTOP}" = true ] && tools="${tools}claude-desktop\n"
  [ "${OPT_CODEX}" = true ]          && tools="${tools}codex\n"
  [ "${OPT_OPENCODE}" = true ]       && tools="${tools}opencode\n"
  [ "${OPT_FACTORY}" = true ]        && tools="${tools}factory\n"
  [ "${OPT_CURSOR}" = true ]         && tools="${tools}cursor\n"
  [ "${OPT_VSCODE}" = true ]         && tools="${tools}vscode\n"
  [ "${OPT_ANTIGRAVITY}" = true ]    && tools="${tools}antigravity\n"
  [ "${OPT_AGY}" = true ]            && tools="${tools}agy\n"
  printf "%b" "${tools}" > "${STATE_FILE}" 2>/dev/null || true
}

load_state() {
  [ ! -f "${STATE_FILE}" ] && return 0
  while IFS= read -r tool; do
    case "${tool}" in
      claude-code)    OPT_CLAUDE_CODE=true ;;
      claude-desktop) OPT_CLAUDE_DESKTOP=true ;;
      codex)          OPT_CODEX=true ;;
      opencode)       OPT_OPENCODE=true ;;
      factory)        OPT_FACTORY=true ;;
      cursor)         OPT_CURSOR=true ;;
      vscode)         OPT_VSCODE=true ;;
      antigravity)    OPT_ANTIGRAVITY=true ;;
      agy)            OPT_AGY=true ;;
    esac
  done < "${STATE_FILE}"
}

# ── Doctor ────────────────────────────────────────────────────────────────────
doctor() {
  printf "\n%s%s  Doctor Report%s\n\n" "${BOLD}" "${CYAN}" "${RESET}"

  local tool_name target_dir installed total
  # check_tool_install <label> <dir> [subdir]
  check_tool_install() {
    tool_name="$1"; target_dir="$2"
    local chk_subdir="${3:-false}"
    installed=0; total=0
    if [ -d "${target_dir}" ]; then
      local name
      while IFS= read -r name; do
        [ -z "${name}" ] && continue
        total=$((total + 1))
        if [ "${chk_subdir}" = true ]; then
          [ -f "${target_dir}/${name}/SKILL.md" ] && installed=$((installed + 1))
        else
          [ -f "${target_dir}/${name}.md" ] && installed=$((installed + 1))
        fi
      done <<EOF
${SKILL_NAMES}
EOF
      if [ "${installed}" -eq "${total}" ]; then
        printf "  %s✓%s  %-20s %s%d/%d skills%s\n" \
          "${GREEN}" "${RESET}" "${tool_name}" "${DIM}" "${installed}" "${total}" "${RESET}"
      else
        printf "  %s⚠%s  %-20s %s%d/%d skills%s\n" \
          "${YELLOW}" "${RESET}" "${tool_name}" "${YELLOW}" "${installed}" "${total}" "${RESET}"
      fi
    else
      printf "  %s○%s  %-20s %snot installed%s\n" \
        "${DIM}" "${RESET}" "${tool_name}" "${DIM}" "${RESET}"
    fi
  }

  check_tool_install "Claude Code"      "${PATH_CLAUDE_CODE}/skills"     true
  check_tool_install "Claude Desktop"   "${PATH_CLAUDE_DESKTOP}/skills"  true
  check_tool_install "Codex"            "${PATH_CODEX}/skills"            true
  check_tool_install "OpenCode"         "${PATH_OPENCODE}/skills"         true
  check_tool_install "Factory"          "${PATH_FACTORY}/skills"          true
  check_tool_install "Cursor"           "${PATH_CURSOR}/rules"
  check_tool_install "VS Code"          "${PATH_VSCODE}/lzr1-skills"
  check_tool_install "Antigravity"      "${PATH_ANTIGRAVITY}/rules"
  check_tool_install "Antigravity AGY"  "${PATH_AGY}/skills"              true
  printf "\n"
}

# ── Execute installs based on selected opts ───────────────────────────────────
do_install() {
  load_skill_names

  printf "\n%s%s  Installing lzr1-skills...%s\n\n" "${BOLD}" "${CYAN}" "${RESET}"

  [ "${OPT_CLAUDE_CODE}" = true ]    && install_claude_code
  [ "${OPT_CLAUDE_DESKTOP}" = true ] && install_claude_desktop
  [ "${OPT_CODEX}" = true ]          && install_codex
  [ "${OPT_OPENCODE}" = true ]       && install_opencode
  [ "${OPT_FACTORY}" = true ]        && install_factory
  [ "${OPT_CURSOR}" = true ]         && install_cursor
  [ "${OPT_VSCODE}" = true ]         && install_vscode
  [ "${OPT_ANTIGRAVITY}" = true ]    && install_antigravity
  [ "${OPT_AGY}" = true ]            && install_agy

  save_state
  print_summary
}

do_update() {
  load_state
  if ! any_tool_selected; then
    log_warn "No previously installed tools found. Run install first."
    return 1
  fi
  log_info "Updating previously installed tools..."
  do_install
}

do_remove() {
  load_state
  load_skill_names

  printf "\n%s%s  Removing lzr1-skills...%s\n\n" "${BOLD}" "${RED}" "${RESET}"

  [ "${OPT_CLAUDE_CODE}" = true ]    && remove_claude_code
  [ "${OPT_CLAUDE_DESKTOP}" = true ] && remove_claude_desktop
  [ "${OPT_CODEX}" = true ]          && remove_codex
  [ "${OPT_OPENCODE}" = true ]       && remove_opencode
  [ "${OPT_FACTORY}" = true ]        && remove_factory
  [ "${OPT_CURSOR}" = true ]         && remove_cursor
  [ "${OPT_VSCODE}" = true ]         && remove_vscode
  [ "${OPT_ANTIGRAVITY}" = true ]    && remove_antigravity
  [ "${OPT_AGY}" = true ]            && remove_agy

  # Clear state
  rm -f "${STATE_FILE}" 2>/dev/null || true
  printf "\n%s✓%s  Done. All selected skills removed.\n\n" "${GREEN}" "${RESET}"
}

any_tool_selected() {
  [ "${OPT_CLAUDE_CODE}" = true ]    && return 0
  [ "${OPT_CLAUDE_DESKTOP}" = true ] && return 0
  [ "${OPT_CODEX}" = true ]          && return 0
  [ "${OPT_OPENCODE}" = true ]       && return 0
  [ "${OPT_FACTORY}" = true ]        && return 0
  [ "${OPT_CURSOR}" = true ]         && return 0
  [ "${OPT_VSCODE}" = true ]         && return 0
  [ "${OPT_ANTIGRAVITY}" = true ]    && return 0
  [ "${OPT_AGY}" = true ]            && return 0
  return 1
}

# ── Summary table ─────────────────────────────────────────────────────────────
print_summary() {
  local skill_count
  skill_count=$(printf "%s" "${SKILL_NAMES}" | grep -c . 2>/dev/null || echo "32")

  printf "\n"
  printf "  %s%s┌────────────────────────────────────────────────────┐%s\n" "${DIM}" "${CYAN}" "${RESET}"
  printf "  %s%s│%s%s  Installation Summary%s%s                              │%s\n" \
    "${DIM}" "${CYAN}" "${RESET}" "${BOLD}" "${RESET}" "${DIM}${CYAN}" "${RESET}"
  printf "  %s%s├────────────────────────────────────────────────────┤%s\n" "${DIM}" "${CYAN}" "${RESET}"

  print_summary_row() {
    local label="$1" flag="$2" path="$3"
    if [ "${flag}" = true ]; then
      printf "  %s%s│%s  %s%-18s%s  %s→%s  %s%-24s%s%s│%s\n" \
        "${DIM}" "${CYAN}" "${RESET}" \
        "${GREEN}" "${label}" "${RESET}" \
        "${DIM}" "${RESET}" \
        "${DIM}" "${path}" "${RESET}" \
        "${DIM}${CYAN}" "${RESET}"
    fi
  }

  print_summary_row "Claude Code"     "${OPT_CLAUDE_CODE}"    "~/.claude/skills/"
  print_summary_row "Claude Desktop"  "${OPT_CLAUDE_DESKTOP}" "…/Claude/skills/"
  print_summary_row "Codex"           "${OPT_CODEX}"          "~/.codex/skills/"
  print_summary_row "OpenCode"        "${OPT_OPENCODE}"        "…/opencode/skills/"
  print_summary_row "Factory"         "${OPT_FACTORY}"        "~/.factory/skills/"
  print_summary_row "Cursor"          "${OPT_CURSOR}"         "~/.cursor/rules/"
  print_summary_row "VS Code"         "${OPT_VSCODE}"         "~/.vscode/lzr1-skills/"
  print_summary_row "Antigravity"     "${OPT_ANTIGRAVITY}"    "~/.antigravity-ide/rules/"
  print_summary_row "Antigravity AGY" "${OPT_AGY}"            "…/Antigravity/skills/"

  printf "  %s%s├────────────────────────────────────────────────────┤%s\n" "${DIM}" "${CYAN}" "${RESET}"
  printf "  %s%s│%s  %s%d skills installed%s%s                                  │%s\n" \
    "${DIM}" "${CYAN}" "${RESET}" "${BOLD}${GREEN}" "${skill_count}" "${RESET}" "${DIM}${CYAN}" "${RESET}"
  printf "  %s%s└────────────────────────────────────────────────────┘%s\n" "${DIM}" "${CYAN}" "${RESET}"
  printf "\n"
  printf "  %sTo update later:%s\n" "${DIM}" "${RESET}"
  printf "  %scurl -fsSL https://raw.githubusercontent.com/%s/main/install.sh | bash -s -- update%s\n\n" \
    "${CYAN}" "${REPO}" "${RESET}"
}

# ── Interactive Menu ──────────────────────────────────────────────────────────
show_menu() {
  print_banner

  # Build menu rows
  menu_row() {
    local num="$1" label="$2" found="$3"
    if [ "${found}" = true ]; then
      printf "    %s%s%d%s  %s%-22s%s  %s✓ detected%s\n" \
        "${BOLD}" "${CYAN}" "${num}" "${RESET}" \
        "${WHITE}" "${label}" "${RESET}" \
        "${GREEN}" "${RESET}"
    else
      printf "    %s%s%d%s  %s%-22s%s  %s○ not found%s\n" \
        "${BOLD}" "${CYAN}" "${num}" "${RESET}" \
        "${DIM}" "${label}" "${RESET}" \
        "${DIM}" "${RESET}"
    fi
  }

  printf "  %s%sAvailable targets:%s\n\n" "${BOLD}" "${WHITE}" "${RESET}"
  menu_row 1 "Claude Code"     "${FOUND_CLAUDE_CODE}"
  menu_row 2 "Claude Desktop"  "${FOUND_CLAUDE_DESKTOP}"
  menu_row 3 "Codex"           "${FOUND_CODEX}"
  menu_row 4 "OpenCode"        "${FOUND_OPENCODE}"
  menu_row 5 "Factory"         "${FOUND_FACTORY}"
  menu_row 6 "Cursor"          "${FOUND_CURSOR}"
  menu_row 7 "VS Code"         "${FOUND_VSCODE}"
  menu_row 8 "Antigravity"     "${FOUND_ANTIGRAVITY}"
  menu_row 9 "Antigravity AGY" "${FOUND_AGY}"
  printf "\n"
  printf "  %s%sa%s  All tools\n" "${BOLD}" "${MAGENTA}" "${RESET}"
  printf "  %s%sd%s  Detected tools only\n" "${BOLD}" "${CYAN}" "${RESET}"
  printf "  %s%sq%s  Quit\n\n" "${BOLD}" "${DIM}" "${RESET}"

  # Tool selection
  printf "  %sSelect tools%s (comma-separated, e.g. %s1,3%s or %sa%s): " \
    "${BOLD}" "${RESET}" "${CYAN}" "${RESET}" "${MAGENTA}" "${RESET}"

  local selection=""
  read -r selection </dev/tty || true
  selection=$(printf "%s" "${selection}" | tr '[:upper:]' '[:lower:]' | tr -d ' ')

  case "${selection}" in
    q|quit|exit) printf "\n  Goodbye!\n\n"; exit 0 ;;
    a|all)
      OPT_CLAUDE_CODE=true; OPT_CLAUDE_DESKTOP=true; OPT_CODEX=true
      OPT_OPENCODE=true; OPT_FACTORY=true; OPT_CURSOR=true
      OPT_VSCODE=true; OPT_ANTIGRAVITY=true; OPT_AGY=true
      ;;
    d|detected)
      OPT_CLAUDE_CODE="${FOUND_CLAUDE_CODE}"
      OPT_CLAUDE_DESKTOP="${FOUND_CLAUDE_DESKTOP}"
      OPT_CODEX="${FOUND_CODEX}"
      OPT_OPENCODE="${FOUND_OPENCODE}"
      OPT_FACTORY="${FOUND_FACTORY}"
      OPT_CURSOR="${FOUND_CURSOR}"
      OPT_VSCODE="${FOUND_VSCODE}"
      OPT_ANTIGRAVITY="${FOUND_ANTIGRAVITY}"
      OPT_AGY="${FOUND_AGY}"
      ;;
    *)
      # Parse comma-separated numbers
      local IFS=','
      for num in ${selection}; do
        case "${num}" in
          1) OPT_CLAUDE_CODE=true ;;
          2) OPT_CLAUDE_DESKTOP=true ;;
          3) OPT_CODEX=true ;;
          4) OPT_OPENCODE=true ;;
          5) OPT_FACTORY=true ;;
          6) OPT_CURSOR=true ;;
          7) OPT_VSCODE=true ;;
          8) OPT_ANTIGRAVITY=true ;;
          9) OPT_AGY=true ;;
          *) log_warn "Unknown option: ${num}" ;;
        esac
      done
      ;;
  esac
  unset IFS

  if ! any_tool_selected; then
    log_error "No tools selected. Exiting."
    exit 1
  fi

  # Action selection
  printf "\n  %sAction%s [%sI%s]nstall  [%sU%s]pdate  [%sR%s]emove  (default: Install): " \
    "${BOLD}" "${RESET}" \
    "${GREEN}" "${RESET}" \
    "${CYAN}" "${RESET}" \
    "${RED}" "${RESET}"

  local action_input=""
  read -r action_input </dev/tty || true
  action_input=$(printf "%s" "${action_input}" | tr '[:upper:]' '[:lower:]')

  case "${action_input}" in
    u|update)  ACTION="update" ;;
    r|remove)  ACTION="remove" ;;
    *)         ACTION="install" ;;
  esac

  printf "\n"
  case "${ACTION}" in
    install) do_install ;;
    update)  do_install ;;
    remove)  do_remove ;;
  esac
}

# ── Auto mode (curl/--yes --all) ──────────────────────────────────────────────
auto_install() {
  print_banner
  log_info "Auto-installing to all detected tools..."
  printf "\n"

  OPT_CLAUDE_CODE="${FOUND_CLAUDE_CODE}"
  OPT_CLAUDE_DESKTOP="${FOUND_CLAUDE_DESKTOP}"
  OPT_CODEX="${FOUND_CODEX}"
  OPT_OPENCODE="${FOUND_OPENCODE}"
  OPT_FACTORY="${FOUND_FACTORY}"
  OPT_CURSOR="${FOUND_CURSOR}"
  OPT_VSCODE="${FOUND_VSCODE}"
  OPT_ANTIGRAVITY="${FOUND_ANTIGRAVITY}"
  OPT_AGY="${FOUND_AGY}"

  if ! any_tool_selected; then
    log_warn "No tools detected automatically."
    log_info "Try running the installer interactively to install to a specific tool:"
    printf "  %sbash install.sh%s\n\n" "${CYAN}" "${RESET}"
    exit 0
  fi

  do_install
}

# ── Help ──────────────────────────────────────────────────────────────────────
print_help() {
  print_banner
  cat <<EOF
  ${BOLD}USAGE${RESET}
    bash install.sh [command] [options]
    curl -fsSL https://raw.githubusercontent.com/${REPO}/main/install.sh | bash

  ${BOLD}COMMANDS${RESET}
    install         Install skills (default)
    update          Re-download and reinstall to previously selected tools
    remove          Remove installed skills
    doctor          Check installation health
    help            Show this help

  ${BOLD}TOOL FLAGS${RESET}
    --claude-code     Install to Claude Code (~/.claude/skills/)
    --claude-desktop  Install to Claude Desktop
    --codex           Install to Codex (~/.codex/skills/)
    --opencode        Install to OpenCode (~/.config/opencode/skills/)
    --factory         Install to Factory (~/.factory/skills/)
    --cursor          Install to Cursor (~/.cursor/rules/)
    --vscode          Install to VS Code (~/.vscode/lzr1-skills/)
    --antigravity     Install to Antigravity (~/.antigravity/skills/)
    --agy             Install to Antigravity AGY (~/.agy/skills/)
    --all             Install to all tools

  ${BOLD}OPTIONS${RESET}
    --dry-run, -n     Show what would be done without doing it
    --verbose, -v     Show per-file output
    --yes, -y         Skip prompts (auto-confirm)
    --version         Show version
    --help, -h        Show this help

  ${BOLD}EXAMPLES${RESET}
    # Interactive menu
    bash install.sh

    # Install to specific tools
    bash install.sh --claude-code --cursor

    # Update all previously installed tools
    curl -fsSL https://raw.githubusercontent.com/${REPO}/main/install.sh | bash -s -- update

    # Auto-install to all detected tools
    LZRI_AUTO=1 bash install.sh

    # Dry run
    bash install.sh --all --dry-run

EOF
}

# ── Argument parsing ──────────────────────────────────────────────────────────
HAS_TOOL_FLAG=false

parse_args() {
  while [ "$#" -gt 0 ]; do
    case "$1" in
      install)         ACTION="install" ;;
      update|upgrade)  ACTION="update" ;;
      remove|uninstall) ACTION="remove" ;;
      doctor)          ACTION="doctor" ;;
      all)             ACTION="install"
                       OPT_CLAUDE_CODE=true; OPT_CLAUDE_DESKTOP=true
                       OPT_CODEX=true; OPT_OPENCODE=true; OPT_FACTORY=true
                       OPT_CURSOR=true; OPT_VSCODE=true
                       OPT_ANTIGRAVITY=true; OPT_AGY=true
                       HAS_TOOL_FLAG=true ;;
      --all)           OPT_CLAUDE_CODE=true; OPT_CLAUDE_DESKTOP=true
                       OPT_CODEX=true; OPT_OPENCODE=true; OPT_FACTORY=true
                       OPT_CURSOR=true; OPT_VSCODE=true
                       OPT_ANTIGRAVITY=true; OPT_AGY=true
                       HAS_TOOL_FLAG=true ;;
      --claude-code)    OPT_CLAUDE_CODE=true;    HAS_TOOL_FLAG=true ;;
      --claude-desktop) OPT_CLAUDE_DESKTOP=true; HAS_TOOL_FLAG=true ;;
      --codex)          OPT_CODEX=true;          HAS_TOOL_FLAG=true ;;
      --opencode)       OPT_OPENCODE=true;        HAS_TOOL_FLAG=true ;;
      --factory)        OPT_FACTORY=true;         HAS_TOOL_FLAG=true ;;
      --cursor)         OPT_CURSOR=true;          HAS_TOOL_FLAG=true ;;
      --vscode)         OPT_VSCODE=true;          HAS_TOOL_FLAG=true ;;
      --antigravity)    OPT_ANTIGRAVITY=true;     HAS_TOOL_FLAG=true ;;
      --agy)            OPT_AGY=true;             HAS_TOOL_FLAG=true ;;
      --dry-run|-n)     DRY_RUN=true ;;
      --verbose|-v)     VERBOSE=true ;;
      --yes|-y)         YES_MODE=true ;;
      --version)        printf "lzr1-skills v%s\n" "${VERSION}"; exit 0 ;;
      --help|-h|help)   print_help; exit 0 ;;
      *)                log_warn "Unknown argument: $1" ;;
    esac
    shift
  done
}

# ── Curl mode detection ───────────────────────────────────────────────────────
detect_curl_mode() {
  # Running via curl if the skills/ directory doesn't exist next to the script
  local script_dir
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]:-install.sh}")" 2>/dev/null && pwd)" || script_dir="."
  if [ ! -d "${script_dir}/skills" ]; then
    CURL_MODE=true
  fi
}

# ── Main ──────────────────────────────────────────────────────────────────────
main() {
  parse_args "$@"
  detect_curl_mode
  detect_tools

  # Handle auto mode
  if [ "${AUTO_MODE}" = "1" ] || [ "${AUTO_MODE}" = "true" ]; then
    auto_install
    return 0
  fi

  # --yes --all means non-interactive full auto
  if [ "${YES_MODE}" = true ] && [ "${HAS_TOOL_FLAG}" = true ]; then
    load_skill_names
    do_install
    return 0
  fi

  case "${ACTION}" in
    doctor)
      load_skill_names
      doctor
      ;;
    update)
      do_update
      ;;
    remove)
      if [ "${HAS_TOOL_FLAG}" = true ]; then
        load_skill_names
        do_remove
      else
        # Interactive remove
        show_menu
      fi
      ;;
    install)
      if [ "${HAS_TOOL_FLAG}" = true ]; then
        load_skill_names
        do_install
      else
        show_menu
      fi
      ;;
    *)
      show_menu
      ;;
  esac
}

main "$@"
