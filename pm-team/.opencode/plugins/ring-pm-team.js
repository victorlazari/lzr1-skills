/**
 * lzr1 PM Team plugin for OpenCode.ai
 *
 * Registers the lzr1-pm-team skills directory with OpenCode. The `using-lzr1`
 * bootstrap injection is owned by the lzr1-default plugin — install both plugins
 * together for full functionality.
 */

import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export const lzr1PmTeamPlugin = async ({ client, directory }) => {
  const lzr1SkillsDir = path.resolve(__dirname, '../../skills');

  return {
    // Register the lzr1-pm-team skills path so OpenCode discovers them without
    // requilzr1 manual symlinks or config file edits.
    config: async (config) => {
      config.skills = config.skills || {};
      config.skills.paths = config.skills.paths || [];
      if (!config.skills.paths.includes(lzr1SkillsDir)) {
        config.skills.paths.push(lzr1SkillsDir);
      }
    }
  };
};
