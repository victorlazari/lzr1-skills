#!/usr/bin/env -S node --experimental-strip-types

/**
 * Deliberately local credential helper.
 *
 * This is not a substitute for an operating-system keychain or managed secret
 * store. It exists only for local development where those facilities are not
 * available. Secret values are accepted from stdin, never argv, and are
 * revealed only for one named key behind an explicit --reveal gate.
 */

import * as fs from 'node:fs';
import * as path from 'node:path';

const MAX_FILE_BYTES = 256 * 1024;
const MAX_VALUE_BYTES = 64 * 1024;
const MAX_KEYS = 256;
const KEY_PATTERN = /^[A-Za-z][A-Za-z0-9_.-]{0,127}$/;
const RESERVED_KEYS = new Set(['__proto__', 'constructor', 'prototype']);

type CredentialMap = Record<string, string>;

function fail(message: string, code = 2): never {
  console.error(`Error: ${message}`);
  process.exit(code);
}

function usage(): void {
  console.log(`Usage:
  local-credential-helper.mts save <key> --stdin
  local-credential-helper.mts get <key> [--reveal]
  local-credential-helper.mts list
  local-credential-helper.mts remove <key> --confirm
  local-credential-helper.mts status
  local-credential-helper.mts --help

Commands:
  save     Read one secret value exactly from standard input and store it.
           Interactive TTY input is rejected to avoid visible, echoed secrets.
  get      Report whether a named key exists; --reveal writes only that value
           to stdout, without adding a newline.
  list     List stored key names only. Values are never printed.
  remove   Delete one named key; --confirm is required.
  status   Show store location, key count, and owner-only mode status.

Prefer an OS keychain or managed secret store. This helper stores encrypted-at-
rest data only when the underlying filesystem provides that property.`);
}

function validateKey(key: string): void {
  if (!KEY_PATTERN.test(key) || RESERVED_KEYS.has(key)) {
    fail('key must match [A-Za-z][A-Za-z0-9_.-]{0,127} and must not be a reserved object name');
  }
}

function requireAbsoluteHome(): string {
  const configured = process.env.HOME;
  if (!configured || !path.isAbsolute(configured)) {
    fail('HOME must be set to an absolute directory');
  }
  let stats: fs.Stats;
  try {
    stats = fs.statSync(configured);
  } catch (error) {
    fail(`HOME cannot be accessed: ${(error as Error).message}`);
  }
  if (!stats.isDirectory()) {
    fail('HOME is not a directory');
  }
  try {
    return fs.realpathSync(configured);
  } catch (error) {
    fail(`HOME cannot be resolved: ${(error as Error).message}`);
  }
}

const HOME = requireAbsoluteHome();
const STORE_DIR = path.join(HOME, '.nemoclaw');
const CREDENTIALS_FILE = path.join(STORE_DIR, 'credentials.json');

function assertOwnedByCurrentUser(stats: fs.Stats, label: string): void {
  if (typeof process.getuid === 'function' && stats.uid !== process.getuid()) {
    fail(`${label} is not owned by the current user`);
  }
}

function ensureStoreDirectory(): void {
  if (fs.existsSync(STORE_DIR)) {
    const stats = fs.lstatSync(STORE_DIR);
    if (stats.isSymbolicLink() || !stats.isDirectory()) {
      fail('credential store directory must be a real directory, not a symlink');
    }
    assertOwnedByCurrentUser(stats, 'credential store directory');
    if ((stats.mode & 0o077) !== 0) {
      fs.chmodSync(STORE_DIR, 0o700);
      console.error('Warning: repaired credential store directory mode to 0700.');
    }
  } else {
    fs.mkdirSync(STORE_DIR, { mode: 0o700 });
  }
}

function validateCredentialObject(value: unknown): CredentialMap {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    fail('credential store JSON must contain one object');
  }

  const entries = Object.entries(value as Record<string, unknown>);
  if (entries.length > MAX_KEYS) {
    fail(`credential store exceeds the ${MAX_KEYS}-key limit`);
  }

  const result = Object.create(null) as CredentialMap;
  for (const [key, secret] of entries) {
    validateKey(key);
    if (typeof secret !== 'string') {
      fail(`credential value for ${key} is not a string`);
    }
    if (Buffer.byteLength(secret, 'utf8') > MAX_VALUE_BYTES) {
      fail(`credential value for ${key} exceeds ${MAX_VALUE_BYTES} bytes`);
    }
    result[key] = secret;
  }
  return result;
}

function loadCredentials(): CredentialMap {
  ensureStoreDirectory();
  if (!fs.existsSync(CREDENTIALS_FILE)) {
    return Object.create(null) as CredentialMap;
  }

  const stats = fs.lstatSync(CREDENTIALS_FILE);
  if (stats.isSymbolicLink() || !stats.isFile()) {
    fail('credential store must be a regular file, not a symlink or special file');
  }
  assertOwnedByCurrentUser(stats, 'credential store');
  if (stats.size > MAX_FILE_BYTES) {
    fail(`credential store exceeds the ${MAX_FILE_BYTES}-byte limit`);
  }
  if ((stats.mode & 0o077) !== 0) {
    fs.chmodSync(CREDENTIALS_FILE, 0o600);
    console.error('Warning: repaired credential store mode to 0600.');
  }

  let parsed: unknown;
  try {
    parsed = JSON.parse(fs.readFileSync(CREDENTIALS_FILE, 'utf8'));
  } catch (error) {
    fail(`credential store is not valid UTF-8 JSON: ${(error as Error).message}`);
  }
  return validateCredentialObject(parsed);
}

function writeCredentials(credentials: CredentialMap): void {
  ensureStoreDirectory();
  const checked = validateCredentialObject(credentials);
  const serialized = `${JSON.stringify(checked, null, 2)}\n`;
  if (Buffer.byteLength(serialized, 'utf8') > MAX_FILE_BYTES) {
    fail(`serialized credential store exceeds the ${MAX_FILE_BYTES}-byte limit`);
  }

  if (fs.existsSync(CREDENTIALS_FILE)) {
    const existing = fs.lstatSync(CREDENTIALS_FILE);
    if (existing.isSymbolicLink() || !existing.isFile()) {
      fail('refusing to replace a symlink or special credential-store file');
    }
    assertOwnedByCurrentUser(existing, 'credential store');
  }

  const temporary = path.join(
    STORE_DIR,
    `.credentials.json.tmp-${process.pid}-${Date.now()}-${Math.random().toString(16).slice(2)}`,
  );
  let descriptor: number | undefined;
  try {
    const noFollow = fs.constants.O_NOFOLLOW ?? 0;
    descriptor = fs.openSync(
      temporary,
      fs.constants.O_CREAT | fs.constants.O_EXCL | fs.constants.O_WRONLY | noFollow,
      0o600,
    );
    fs.writeFileSync(descriptor, serialized, { encoding: 'utf8' });
    fs.fsyncSync(descriptor);
    fs.closeSync(descriptor);
    descriptor = undefined;
    fs.chmodSync(temporary, 0o600);
    fs.renameSync(temporary, CREDENTIALS_FILE);
  } catch (error) {
    if (descriptor !== undefined) {
      fs.closeSync(descriptor);
    }
    try {
      fs.unlinkSync(temporary);
    } catch {
      // Best-effort cleanup only; the original error is more useful.
    }
    fail(`could not update credential store atomically: ${(error as Error).message}`);
  }
}

async function readSecretFromStdin(): Promise<string> {
  if (process.stdin.isTTY) {
    fail('save requires non-interactive stdin; pipe the value from a secret manager or environment variable');
  }

  const chunks: Buffer[] = [];
  let size = 0;
  for await (const chunk of process.stdin) {
    const buffer = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
    size += buffer.length;
    if (size > MAX_VALUE_BYTES) {
      fail(`stdin secret exceeds the ${MAX_VALUE_BYTES}-byte limit`);
    }
    chunks.push(buffer);
  }
  if (size === 0) {
    fail('stdin secret is empty');
  }

  const value = Buffer.concat(chunks).toString('utf8');
  if (Buffer.byteLength(value, 'utf8') !== size) {
    fail('stdin secret is not valid UTF-8');
  }
  return value;
}

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
    usage();
    process.exit(args.length === 0 ? 2 : 0);
  }

  switch (args[0]) {
    case 'save': {
      if (args.length !== 3 || args[2] !== '--stdin') {
        fail('save requires exactly: save <key> --stdin');
      }
      const key = args[1];
      validateKey(key);
      const secret = await readSecretFromStdin();
      const credentials = loadCredentials();
      credentials[key] = secret;
      writeCredentials(credentials);
      console.log(`Saved credential key: ${key}`);
      return;
    }
    case 'get': {
      if (args.length < 2 || args.length > 3 || (args.length === 3 && args[2] !== '--reveal')) {
        fail('get requires: get <key> [--reveal]');
      }
      const key = args[1];
      validateKey(key);
      const credentials = loadCredentials();
      if (!Object.prototype.hasOwnProperty.call(credentials, key)) {
        fail(`credential key not found: ${key}`, 1);
      }
      if (args[2] === '--reveal') {
        process.stdout.write(credentials[key]);
      } else {
        console.log(`Credential key is present: ${key}. Use --reveal only for an explicitly authorized consumer.`);
      }
      return;
    }
    case 'list': {
      if (args.length !== 1) {
        fail('list accepts no additional arguments');
      }
      const keys = Object.keys(loadCredentials()).sort();
      for (const key of keys) {
        console.log(key);
      }
      return;
    }
    case 'remove': {
      if (args.length !== 3 || args[2] !== '--confirm') {
        fail('remove requires exactly: remove <key> --confirm');
      }
      const key = args[1];
      validateKey(key);
      const credentials = loadCredentials();
      if (!Object.prototype.hasOwnProperty.call(credentials, key)) {
        fail(`credential key not found: ${key}`, 1);
      }
      delete credentials[key];
      writeCredentials(credentials);
      console.log(`Removed credential key: ${key}`);
      return;
    }
    case 'status': {
      if (args.length !== 1) {
        fail('status accepts no additional arguments');
      }
      const credentials = loadCredentials();
      const exists = fs.existsSync(CREDENTIALS_FILE);
      console.log(`Store: ${CREDENTIALS_FILE}`);
      console.log(`Exists: ${exists ? 'yes' : 'no'}`);
      console.log(`Keys: ${Object.keys(credentials).length}`);
      console.log('Required modes: directory 0700, file 0600 (checked and repaired when possible)');
      return;
    }
    default:
      fail(`unknown command: ${args[0]}`);
  }
}

main().catch((error: unknown) => {
  const message = error instanceof Error ? error.message : String(error);
  console.error(`Error: ${message}`);
  process.exit(1);
});
