---
version: 1.0.0
name: higgsfield-connect
description: |
  Install, authenticate, and fully set up the Higgsfield CLI and agent skills
  in one guided flow. Use this skill whenever the user says anything like:
  "set up higgsfield", "connect higgsfield", "install higgsfield", "higgsfield
  setup", "get higgsfield working", "authenticate higgsfield", "higgsfield
  login", "install higgsfield CLI", or any variation of wanting to get the
  Higgsfield toolchain ready to use. Also trigger this skill if the user hits
  a "command not found: higgsfield" error or any auth/token error when trying
  to use higgsfield commands.
---

# Higgsfield CLI Setup

## What this skill does
Installs the Higgsfield CLI, authenticates via browser, and installs the
Higgsfield agent skills — so every higgsfield command works in this session
and future ones.

## Step-by-step

### 1. Install the CLI

Try a global install first:

```bash
npm install -g @higgsfield/cli 2>&1
```

If that fails with `EACCES` (permission denied on `/usr/local`), install to
the user's home prefix instead — no sudo needed:

```bash
npm install -g @higgsfield/cli --prefix ~/.npm-global 2>&1
```

Then make sure the bin is on PATH for this session:

```bash
export PATH="$HOME/.npm-global/bin:$PATH"
```

Verify it worked:

```bash
higgsfield version 2>&1
```

### 2. Authenticate

```bash
higgsfield auth login 2>&1
```

This opens a browser tab. The CLI will print a device URL if the browser
doesn't open automatically — share it with the user so they can visit it
manually. Wait for "Successfully authenticated." before moving on.

### 3. Install the Higgsfield agent skills

The npm cache at `~/.npm` may have permission issues. Use a temp cache:

```bash
npx --cache /tmp/npm-cache skills add higgsfield-ai/skills 2>&1
```

This installs 4 skills: `higgsfield-generate`, `higgsfield-marketplace-cards`,
`higgsfield-product-photoshoot`, and `higgsfield-soul-id`.

### 4. Confirm everything is working

```bash
export PATH="$HOME/.npm-global/bin:$PATH" && higgsfield model list --video 2>&1 | head -5
```

If models are listed, setup is complete.

## Telling the user what's ready

After all three steps succeed, let them know:
- The CLI is installed and authenticated
- The 4 Higgsfield skills are available for generating images, videos,
  product photos, and marketplace cards
- They can now say things like "generate a video from this photo" or
  "create a product shot" and the skills will handle it

## Troubleshooting

| Problem | Fix |
|---|---|
| `command not found: higgsfield` | Re-run `export PATH="$HOME/.npm-global/bin:$PATH"` |
| Auth token expired | Run `higgsfield auth login` again |
| `npx skills` permission error | Use `--cache /tmp/npm-cache` flag |
| `sudo` needed but no terminal | Never use sudo; use `--prefix ~/.npm-global` instead |
