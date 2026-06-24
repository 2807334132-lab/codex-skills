---
name: codex-skills-sync
description: Set up, repair, or explain long-term synchronization for personal Codex skills using a GitHub repository. Use when the user wants to sync skills across computers, initialize the .codex/skills folder as a Git repository, push skills to GitHub, clone skills on another machine, create a semi-automatic sync script, add a desktop shortcut, or troubleshoot Git/GitHub authentication and push/pull issues for Codex skills.
---

# Codex Skills Sync

## Overview

Use this skill to make a user's personal Codex skills portable across machines. Prefer a private GitHub repository and a semi-automatic sync script over fully automatic background commits.

Keep system-managed skills out of the sync repository. In most Codex installs, personal skills live under:

```text
Windows: C:\Users\<user>\.codex\skills
macOS/Linux: ~/.codex/skills
```

## Workflow

1. Locate the skills folder.
2. Inspect existing skill folders and Git state.
3. Install or locate Git if needed.
4. Initialize the skills folder as a Git repo on `main`.
5. Add ignore rules for system, cache, and local-secret files.
6. Commit personal skills.
7. Connect a private GitHub remote.
8. Push `main`.
9. Create a semi-automatic sync script and optional desktop shortcut.
10. Give recovery instructions for the second computer.

Use GitHub CLI when available. If GitHub CLI login fails or network access is blocked, ask the user to create an empty private GitHub repository in the browser, then add that URL as `origin`.

## Repository Setup

Before initializing, list top-level directories and identify personal skills. Exclude `.system/` and any plugin/cache/system directories. Do not sync the entire `.codex` folder.

Recommended `.gitignore`:

```gitignore
.system/
__pycache__/
*.pyc
.env
Thumbs.db
.DS_Store
```

Recommended `.gitattributes`:

```gitattributes
* text=auto eol=lf
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.webp binary
*.ico binary
```

Initialize and commit:

```powershell
$skills = "$env:USERPROFILE\.codex\skills"
git -C $skills init -b main
git -C $skills add .gitignore .gitattributes <personal-skill-folder> ...
git -C $skills commit -m "Initial skills sync"
```

If `git` is not on PATH on Windows, look for:

```text
C:\Program Files\Git\cmd\git.exe
C:\Users\<user>\AppData\Local\Microsoft\WinGet\Packages\Git.MinGit_Microsoft.Winget.Source_8wekyb3d8bbwe\cmd\git.exe
```

## GitHub Remote

Prefer a private repository named `codex-skills`.

If creating in the GitHub web UI, tell the user:

- Visibility: private
- README: off
- `.gitignore`: none
- License: none

Then connect and push:

```powershell
git -C $skills remote add origin https://github.com/<owner>/codex-skills.git
git -C $skills push -u origin main
```

If the repository already has files, use caution. Pull with rebase only after confirming the user wants to merge histories.

## Semi-Automatic Sync Script

Create `sync-skills.ps1` and `sync-skills.bat` in the skills repository. Use the bundled template at `scripts/sync-skills.ps1` when useful.

The sync script should:

1. Find Git.
2. `pull --rebase --autostash`.
3. `git add -A`.
4. Commit only when staged changes exist.
5. Push.
6. Pause at the end so double-click users can read the result.

Avoid fully automatic scheduled commits unless the user explicitly asks. They can create surprise conflicts across computers.

For a Windows desktop shortcut, create a `.lnk` pointing to:

```text
C:\Users\<user>\.codex\skills\sync-skills.bat
```

## Second Computer

On the second computer, install Git, back up any existing personal skills, then clone the private repo into the Codex skills folder. If the folder already exists and contains local skills, do not overwrite it blindly; merge or back it up first.

Fresh setup:

```powershell
git clone https://github.com/<owner>/codex-skills.git "$env:USERPROFILE\.codex\skills"
```

Existing folder setup:

```powershell
cd "$env:USERPROFILE\.codex\skills"
git init -b main
git remote add origin https://github.com/<owner>/codex-skills.git
git pull origin main
```

After syncing, restart Codex or start a new thread so skill discovery reloads.

## Troubleshooting

- If GitHub CLI web auth times out, use browser-created repository plus HTTPS remote.
- If push asks for credentials, authenticate GitHub CLI or Git Credential Manager.
- If pull reports conflicts, stop and ask the user before resolving. Preserve both machines' skill changes where possible.
- If `.system/` appears staged, remove it from the index and ensure `.gitignore` excludes it.
- If generated caches are staged, remove them with `git rm --cached` and add ignore rules.
