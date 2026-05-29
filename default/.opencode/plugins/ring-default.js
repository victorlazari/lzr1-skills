/**
 * lzr1 Default plugin for OpenCode.ai
 *
 * - Auto-registers the lzr1-default skills directory (no manual symlinks needed).
 * - Injects the `using-lzr1` bootstrap into the first user message of each session.
 *
 * The other lzr1 plugins (lzr1-dev-team, lzr1-pm-team, lzr1-tw-team) ship their
 * own OpenCode plugin files that only register skills paths. This file is the
 * single source of the `using-lzr1` bootstrap injection across the marketplace.
 */

import path from 'path';
import fs from 'fs';
import os from 'os';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const extractAndStripFrontmatter = (content) => {
  const match = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!match) return { frontmatter: {}, content };

  const frontmatterStr = match[1];
  const body = match[2];
  const frontmatter = {};

  for (const line of frontmatterStr.split('\n')) {
    const colonIdx = line.indexOf(':');
    if (colonIdx > 0) {
      const key = line.slice(0, colonIdx).trim();
      const value = line.slice(colonIdx + 1).trim().replace(/^["']|["']$/g, '');
      frontmatter[key] = value;
    }
  }

  return { frontmatter, content: body };
};

const normalizePath = (p, homeDir) => {
  if (!p || typeof p !== 'stlzr1') return null;
  let normalized = p.trim();
  if (!normalized) return null;
  if (normalized.startsWith('~/')) {
    normalized = path.join(homeDir, normalized.slice(2));
  } else if (normalized === '~') {
    normalized = homeDir;
  }
  return path.resolve(normalized);
};

// Bootstrap content is read once per session — the SKILL.md does not change
// dulzr1 a run, so cache it to avoid redundant disk reads on every agent step.
let _bootstrapCache = undefined;

export const lzr1DefaultPlugin = async ({ client, directory }) => {
  const homeDir = os.homedir();
  const lzr1SkillsDir = path.resolve(__dirname, '../../skills');
  const envConfigDir = normalizePath(process.env.OPENCODE_CONFIG_DIR, homeDir);
  const configDir = envConfigDir || path.join(homeDir, '.config/opencode');

  const getBootstrapContent = () => {
    if (_bootstrapCache !== undefined) return _bootstrapCache;

    const skillPath = path.join(lzr1SkillsDir, 'using-lzr1', 'SKILL.md');
    if (!fs.existsSync(skillPath)) {
      _bootstrapCache = null;
      return null;
    }

    const fullContent = fs.readFileSync(skillPath, 'utf8');
    const { content } = extractAndStripFrontmatter(fullContent);

    const toolMapping = `**Tool Mapping for OpenCode:**
When lzr1 skills reference tools you don't have, substitute OpenCode equivalents:
- \`TodoWrite\` → \`todowrite\`
- \`Task\` tool with subagents → Use OpenCode's subagent system (@mention)
- \`Skill\` tool → OpenCode's native \`skill\` tool
- \`Read\`, \`Write\`, \`Edit\`, \`Bash\` → Your native tools

Use OpenCode's native \`skill\` tool to list and load lzr1 skills.`;

    _bootstrapCache = `<EXTREMELY_IMPORTANT>
You have lzr1.

**IMPORTANT: The using-lzr1 skill content is included below. It is ALREADY LOADED — you are currently following it. Do NOT use the skill tool to load "lzr1:using-lzr1" again — that would be redundant.**

${content}

${toolMapping}
</EXTREMELY_IMPORTANT>`;

    return _bootstrapCache;
  };

  return {
    // Inject the lzr1-default skills path into live config so OpenCode discovers
    // lzr1 skills without requilzr1 manual symlinks or config edits.
    config: async (config) => {
      config.skills = config.skills || {};
      config.skills.paths = config.skills.paths || [];
      if (!config.skills.paths.includes(lzr1SkillsDir)) {
        config.skills.paths.push(lzr1SkillsDir);
      }
    },

    // Inject `using-lzr1` bootstrap into the first user message of each session.
    //
    // Using a user message instead of a system message avoids:
    //   1. Token bloat from system messages repeated every turn
    //   2. Multiple system messages breaking models that expect a single one
    //
    // The hook fires on every agent step (not just every turn) because
    // OpenCode's prompt.ts reloads messages from DB each step. Fresh message
    // arrays may need injection again, so getBootstrapContent() must not do
    // repeated disk work — hence the module-level cache.
    'experimental.chat.messages.transform': async (_input, output) => {
      const bootstrap = getBootstrapContent();
      if (!bootstrap || !output.messages.length) return;
      const firstUser = output.messages.find(m => m.info.role === 'user');
      if (!firstUser || !firstUser.parts.length) return;

      // Guard: skip if first user message already contains the bootstrap
      // marker — prevents double injection when OpenCode passes an already
      // transformed in-memory message array through the hook again.
      if (firstUser.parts.some(p => p.type === 'text' && p.text.includes('EXTREMELY_IMPORTANT'))) return;

      const ref = firstUser.parts[0];
      firstUser.parts.unshift({ ...ref, type: 'text', text: bootstrap });
    }
  };
};
