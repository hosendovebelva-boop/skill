---
name: github-note-push
description: Safely publish Obsidian, Markdown, SVG, and image-heavy note repositories to GitHub. Use when Codex needs to inspect a note repo's git state, stage only intended note files, commit and push note updates, or diagnose failures such as wrong remote names, mixed worktrees, stray .DS_Store files, SSH key mismatches, passphrase-protected keys, or "Repository not found" errors.
---

# GitHub Note Push

## Overview

Use this skill for personal knowledge bases and note repos where the working tree often contains a mix of real note edits, scratch files, exported diagrams, and OS junk files.

Prefer local `git` for status, staging, commit, and push. Use GitHub tooling only when repository metadata or pull-request work is needed.

## Core Workflow

### 1. Inspect the repo before touching the index

Start with:

```bash
git status --short --branch
git remote -v
git log --oneline --decorate --max-count=5
```

Treat note repos as mixed worktrees by default. Do not use `git add -A` unless the user clearly wants every change included.

### 2. Separate real note content from trash or drafts

Prefer staging only the files that belong to the intended sync:

- Markdown notes: `*.md`
- Diagrams and exports: `*.svg`
- Referenced assets: images that are actually used by the notes

Leave common junk or scratch files unstaged unless the user explicitly wants them:

- `.DS_Store`
- temporary untitled notes such as `未命名.md`
- duplicate scratch variants such as `*_note.md`
- clipboard dumps or temporary captures that are not referenced anywhere

If unsure whether a note is a real deliverable or a scratch pad, read it before staging.

### 3. Verify the target repository name before pushing

Note repos often differ only by underscore, hyphen, or pluralization. Read the remote carefully:

```bash
git remote -v
```

If the user names a different target repo than the current `origin`, verify the destination before changing it. A fast check is:

```bash
git ls-remote <remote-url>
```

Interpret failures precisely:

- `Repository not found`: the repo path is wrong or the authenticated account lacks access
- `Permission denied (publickey)`: the repo exists, but SSH authentication failed

### 4. Stage intentionally

Use explicit paths:

```bash
git add -- path/to/note.md path/to/diagram.svg
```

Then confirm what is staged:

```bash
git diff --cached --stat
git diff --cached --name-only
```

If the worktree still contains unrelated untracked files, keep them untouched.

### 5. Commit tersely

Use a short imperative message that describes the note topic, for example:

- `Add IOCP note diagrams`
- `Update MFMS server platform notes`
- `Add AMR and IOCP notes`

### 6. Push with the normal path first

Prefer the simple command once the remote and key setup are correct:

```bash
git push origin main
```

Use the current branch instead of `main` when the repo is intentionally on another branch.

## SSH Troubleshooting

### Compare GitHub and local key fingerprints

When GitHub shows one fingerprint and the local machine uses another, compare them directly:

```bash
ssh-keygen -lf ~/.ssh/p340_ed25519.pub
ssh-keygen -lf ~/.ssh/id_ed25519.pub
```

Do not guess which key GitHub is using. Match fingerprints exactly.

### Test authentication directly

Use:

```bash
ssh -T git@github.com
```

If multiple keys exist, force the intended one:

```bash
ssh -o UseKeychain=yes -o AddKeysToAgent=yes -o IdentitiesOnly=yes -i ~/.ssh/p340_ed25519 -T git@github.com
```

If GitHub replies with:

```text
Hi <username>! You've successfully authenticated, but GitHub does not provide shell access.
```

authentication is working.

### Unlock passphrase-protected keys

If the correct key exists in GitHub but the local machine cannot use it, load it into the macOS agent:

```bash
ssh-add --apple-use-keychain ~/.ssh/p340_ed25519
```

### Make future pushes simple

For stable future pushes, prefer a `~/.ssh/config` entry like:

```sshconfig
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/p340_ed25519
  IdentitiesOnly yes
  AddKeysToAgent yes
  UseKeychain yes
```

After this is in place, ordinary `git push origin main` should work without a long custom SSH command.

### Use a one-off forced SSH command only as a fallback

If repo push still does not pick the intended key, use:

```bash
git -c core.sshCommand='ssh -o UseKeychain=yes -o AddKeysToAgent=yes -o IdentitiesOnly=yes -i ~/.ssh/p340_ed25519' push origin main
```

Use this as a recovery step, not the permanent default if `~/.ssh/config` can be fixed cleanly.

## Notes for Codex

- Read the working tree before staging. Note repos are often messy for legitimate reasons.
- Preserve unrelated untracked scratch files unless the user asks to clean them up.
- Mention clearly which files were pushed and which local scratch files were intentionally left untracked.
- When a push fails, diagnose whether the problem is the repo name, the remote URL, or the SSH identity before retrying.
