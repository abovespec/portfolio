---
title: "How to Format JSON in VS Code: Shortcuts, Settings, and Extensions"
description: "Format JSON in VS Code with a keyboard shortcut, format-on-save, Prettier, and schema validation. Step-by-step guide with exact settings.json snippets."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["vscode", "json", "formatting", "prettier", "developer tools"]
draft: false
---

VS Code has built-in JSON formatting that works without any extensions. Add Prettier or a JSON schema and you get validation, auto-fix, and team-consistent style. This guide covers every approach from the fastest (one keystroke) to the most thorough (workspace schema validation).

## 1. Format with a keyboard shortcut

Open any `.json` file in VS Code and press:

- **Windows / Linux:** `Shift+Alt+F`
- **Mac:** `Shift+Option+F`

VS Code will format the entire file using its built-in JSON language server. If the file has a syntax error, VS Code shows a warning before formatting.

To format a *selection* rather than the whole file:

1. Select the text you want to format
2. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)
3. Run **Format Selection**

## 2. Format on save

Enable automatic formatting every time you save a `.json` file by adding this to your `settings.json`:

```json
{
  "[json]": {
    "editor.formatOnSave": true
  }
}
```

To open `settings.json`:
- Command Palette → **Preferences: Open User Settings (JSON)**

For `jsonc` files (JSON with comments — used by VS Code's own config files):

```json
{
  "[json]": {
    "editor.formatOnSave": true
  },
  "[jsonc]": {
    "editor.formatOnSave": true
  }
}
```

## 3. Control indentation (2 vs 4 spaces vs tabs)

VS Code uses 2-space indentation for JSON by default. To change it:

```json
{
  "[json]": {
    "editor.tabSize": 4,
    "editor.insertSpaces": true
  }
}
```

For tabs:

```json
{
  "[json]": {
    "editor.insertSpaces": false
  }
}
```

You can also change this per-file using the status bar at the bottom of the editor (click the "Spaces: 2" indicator to switch).

## 4. Use Prettier for consistent team formatting

Prettier is the most widely used code formatter for web projects. It enforces a consistent JSON style across your team and integrates with VS Code's format-on-save.

**Install Prettier:**

```bash
npm install --save-dev prettier
```

**Install the VS Code extension:**

Search for "Prettier - Code formatter" in the Extensions panel, or install from the CLI:

```bash
code --install-extension esbenp.prettier-vscode
```

**Set Prettier as the default JSON formatter:**

```json
{
  "[json]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  },
  "[jsonc]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  }
}
```

**Configure Prettier** (create `.prettierrc` in your project root):

```json
{
  "printWidth": 80,
  "tabWidth": 2,
  "useTabs": false,
  "trailingComma": "none"
}
```

Note: Prettier enforces 2-space indentation for JSON and removes trailing commas. These are not configurable — Prettier takes an opinionated stance.

## 5. JSON Schema validation

VS Code can validate your JSON against a schema and show inline errors for missing required fields, wrong types, or unknown keys. This is powered by the built-in JSON language server.

### Built-in schema associations

VS Code automatically associates schemas for many well-known config files:
- `package.json` — npm package schema
- `tsconfig.json` — TypeScript compiler schema
- `.eslintrc.json` — ESLint config schema
- `.prettierrc` — Prettier config schema

### Associate a custom schema

In `settings.json`:

```json
{
  "json.schemas": [
    {
      "fileMatch": ["**/my-config.json"],
      "url": "https://example.com/schemas/my-config-schema.json"
    },
    {
      "fileMatch": ["**/local-config.json"],
      "url": "./schemas/local-config-schema.json"
    }
  ]
}
```

You can also reference schemas from the [JSON Schema Store](https://www.schemastore.org/json/) — a community repository with hundreds of schemas for popular config files.

### Inline `$schema` reference

Add a `$schema` key to the JSON file itself and VS Code picks it up automatically:

```json
{
  "$schema": "https://json.schemastore.org/github-action.json",
  "name": "My Workflow",
  ...
}
```

## 6. Sort JSON keys

VS Code doesn't have a built-in key-sort command, but you can use the **Sort JSON objects** extension (search "Sort JSON"), or do it programmatically:

```bash
# Using Node.js
node -e "
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('input.json', 'utf8'));
const sorted = JSON.parse(JSON.stringify(data, Object.keys(data).sort()));
fs.writeFileSync('output.json', JSON.stringify(sorted, null, 2));
"
```

Or paste the JSON into our [online JSON formatter](/) above, which sorts keys on request.

## 7. Format JSON embedded in other files

If you're editing a `.js` or `.ts` file and want to format a JSON string literal:

1. Extract the JSON to a temporary `.json` file
2. Format it there
3. Copy back

Alternatively, use the **Prettify JSON** or **JSON Tools** VS Code extensions, which add commands to format JSON within string literals.

## 8. Validate JSON from the terminal

To validate and format from the command line without leaving VS Code's integrated terminal:

```bash
# Using Python (no install needed)
python -m json.tool input.json

# Using Node.js
node -e "JSON.parse(require('fs').readFileSync('input.json','utf8')); console.log('Valid')"

# Using npx's prettier
npx prettier --write "**/*.json"
```

## Recommended `settings.json` snippet

Copy this into your user `settings.json` for a solid JSON editing setup:

```json
{
  "[json]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true,
    "editor.tabSize": 2
  },
  "[jsonc]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  },
  "json.validate.enable": true,
  "json.schemaDownload.enable": true
}
```

## Quick reference

| Task | Action |
|------|--------|
| Format file | `Shift+Alt+F` (Win/Linux) / `Shift+Option+F` (Mac) |
| Format selection | Select text → Command Palette → Format Selection |
| Format on save | `"editor.formatOnSave": true` in `[json]` block |
| Change indent | `"editor.tabSize": 4` in `[json]` block |
| Use Prettier | Install extension + set `"editor.defaultFormatter"` |
| Schema validation | `"json.schemas"` array in user/workspace settings |

## References

- [VS Code — JSON editing guide](https://code.visualstudio.com/docs/languages/json)
- [Prettier — JSON formatting](https://prettier.io/docs/en/options.html)
- [JSON Schema Store](https://www.schemastore.org/json/)
- [VS Code keyboard shortcuts (PDF)](https://code.visualstudio.com/shortcuts/keyboard-shortcuts-windows.pdf)
