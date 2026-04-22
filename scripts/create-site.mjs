#!/usr/bin/env node
/**
 * create-site.mjs
 *
 * Fork the site-template into sites/<domain>/ and stamp per-site values.
 *
 * Usage:
 *   node scripts/create-site.mjs --name acme --domain acme.com \
 *     --niche health --description "Short description"
 *
 * Design notes:
 * - Uses Node 22 built-ins only (util.parseArgs, fs/promises). No deps.
 * - Copies the template verbatim, then does targeted token rewrites in
 *   site.config.ts, package.json, and wrangler.toml.
 * - Skips git history (`.git/`) and transient folders (node_modules, dist,
 *   .astro) when copying.
 * - By default leaves the new site inside the monorepo (pnpm-workspace
 *   matches `sites/*`). Pass --separate-git to also `git init` inside the
 *   site directory — useful when you intend to extract the site later to
 *   its own GitHub repo. The monorepo's own git tracks it either way.
 */

import { parseArgs } from 'node:util';
import { cp, readFile, writeFile, stat, mkdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execSync } from 'node:child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const ROOT = resolve(__dirname, '..');
const TEMPLATE = join(ROOT, 'packages', 'site-template');

const { values } = parseArgs({
  options: {
    name: { type: 'string' },
    domain: { type: 'string' },
    niche: { type: 'string' },
    description: { type: 'string' },
    'separate-git': { type: 'boolean', default: false },
    force: { type: 'boolean', default: false },
    help: { type: 'boolean', short: 'h', default: false },
  },
});

function usage() {
  console.log(`
Usage: node scripts/create-site.mjs --name <slug> --domain <domain> --niche <niche> [--description "..."] [--separate-git] [--force]

Flags:
  --name          short slug, used as human site name fallback
  --domain        bare domain, e.g. acme.com (becomes sites/<domain>/)
  --niche         free-form niche tag (stored in description fallback)
  --description   optional 1-line description
  --separate-git  also run \`git init\` inside the new site directory
  --force         overwrite existing sites/<domain>/
`.trim());
}

if (values.help || !values.name || !values.domain || !values.niche) {
  usage();
  process.exit(values.help ? 0 : 1);
}

const name = String(values.name);
const domain = String(values.domain);
const niche = String(values.niche);
const description = values.description
  ? String(values.description)
  : `${name} — ${niche} resources, guides, and tools.`;

const target = join(ROOT, 'sites', domain);

if (existsSync(target) && !values.force) {
  console.error(`Target already exists: ${target} (use --force to overwrite)`);
  process.exit(1);
}

if (!existsSync(TEMPLATE)) {
  console.error(`Template not found at ${TEMPLATE}`);
  process.exit(1);
}

console.log(`Creating site at ${target} ...`);

await mkdir(dirname(target), { recursive: true });

// Filter out anything that shouldn't ride along.
const SKIP = new Set(['node_modules', 'dist', '.astro', '.wrangler', '.git']);

await cp(TEMPLATE, target, {
  recursive: true,
  force: values.force,
  filter: (src) => {
    const base = src.split('/').pop();
    return !SKIP.has(base ?? '');
  },
});

// --- Token rewrites -----------------------------------------------------
async function rewrite(file, replacer) {
  const full = join(target, file);
  if (!existsSync(full)) return;
  const content = await readFile(full, 'utf8');
  const next = replacer(content);
  if (next !== content) await writeFile(full, next);
}

const projectName = domain.replace(/\./g, '-');

await rewrite('src/config/site.config.ts', (c) =>
  c
    .replaceAll('__SITE_NAME__', name)
    .replaceAll('__SITE_DOMAIN__', domain)
    .replaceAll('__SITE_DESCRIPTION__', description),
);

await rewrite('wrangler.toml', (c) => c.replaceAll('__PROJECT_NAME__', projectName));

await rewrite('package.json', (c) => {
  const pkg = JSON.parse(c);
  pkg.name = `@site/${projectName}`;
  pkg.private = true;
  pkg.description = description;
  return JSON.stringify(pkg, null, 2) + '\n';
});

// Drop a minimal README specific to the new site.
await writeFile(
  join(target, 'README.md'),
  `# ${name}\n\n${description}\n\nGenerated from \`packages/site-template\` via \`scripts/create-site.mjs\`.\n\nLocal dev:\n\n    pnpm install\n    pnpm dev\n\nDeploy: push to \`main\` (requires Cloudflare secrets on the GitHub repo — see the template README).\n`,
);

if (values['separate-git']) {
  try {
    execSync('git init -q', { cwd: target, stdio: 'inherit' });
    console.log('Initialized separate git repo inside the new site.');
  } catch (err) {
    console.warn('git init failed (continuing):', err?.message ?? err);
  }
}

console.log(`\n✓ Created ${target}\n`);
console.log('Next steps:');
console.log(`  cd sites/${domain}`);
console.log('  pnpm install');
console.log('  pnpm dev\n');
