#!/usr/bin/env -S npx tsx

import * as fs from 'fs';
import * as path from 'path';

const CREDENTIALS_FILE = path.join(process.env.HOME || '', '.nemoclaw_credentials.json');

function saveCredentials(credentials: Record<string, string>) {
  fs.writeFileSync(CREDENTIALS_FILE, JSON.stringify(credentials, null, 2), { mode: 0o600 });
  console.log('Credentials saved securely.');
}

function loadCredentials(): Record<string, string> {
  if (fs.existsSync(CREDENTIALS_FILE)) {
    const data = fs.readFileSync(CREDENTIALS_FILE, 'utf-8');
    return JSON.parse(data);
  }
  return {};
}

const args = process.argv.slice(2);
if (args[0] === '--help') {
  console.log('Usage: local-credential-helper.mts [save|load] [key=value...]');
  process.exit(0);
}

if (args[0] === 'save') {
  const creds = loadCredentials();
  for (let i = 1; i < args.length; i++) {
    const [key, value] = args[i].split('=');
    if (key && value) {
      creds[key] = value;
    }
  }
  saveCredentials(creds);
} else if (args[0] === 'load') {
  console.log(JSON.stringify(loadCredentials(), null, 2));
} else {
  console.error('Invalid command. Use --help for usage.');
  process.exit(1);
}
