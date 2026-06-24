---
name: capture-complex-task-as-skill
description: Turn a completed complex Codex task into a reusable local skill for this user. Use when the user asks to summarize, remember, codify, save, or convert a completed workflow into a skill, and for this user's stated preference to organize completed complex tasks into skills after the work is done.
---

# Capture Complex Task As Skill

## Goal

After a complex task is completed, preserve the reusable procedure as a concise skill in `C:\Users\TANB\.codex\skills` so future Codex runs can rediscover and apply it.

## Decide Whether To Create A Skill

Create or update a skill when the completed task has at least one of these traits:

- It involved multiple tools or a fragile sequence of steps.
- It is likely to recur for the user.
- It required environment-specific knowledge, validation steps, or non-obvious troubleshooting.
- The user explicitly asks to make, update, summarize, remember, or organize it as a skill.

Skip skill creation for one-off trivial tasks, broad chat answers, or workflows already covered by an existing suitable skill.

## Workflow

1. Name the skill with lowercase hyphen-case, preferably verb-led and under 64 characters.
2. Check whether a matching skill already exists in `C:\Users\TANB\.codex\skills`; update it instead of creating a duplicate.
3. Use the skill-creator workflow and initialize new skills with:

```powershell
python "C:\Users\TANB\.codex\skills\.system\skill-creator\scripts\init_skill.py" <skill-name> --path "C:\Users\TANB\.codex\skills" --interface display_name="<Display Name>" --interface short_description="<Short description>" --interface default_prompt="<Default prompt>"
```

4. Write `SKILL.md` with only the reusable, non-obvious procedure. Include:

- Clear trigger description in YAML frontmatter.
- A short workflow.
- Tool commands or scripts only when they reduce future uncertainty.
- Validation steps.
- User-facing reporting expectations.

5. Avoid copying transient logs, private tokens, cookies, one-time URLs, or unnecessary narrative.
6. Run validation:

```powershell
python "C:\Users\TANB\.codex\skills\.system\skill-creator\scripts\quick_validate.py" "C:\Users\TANB\.codex\skills\<skill-name>"
```

7. Tell the user which skill was created or updated and where it lives.

## Style

Keep skills lean. Prefer reusable procedure over story. Write instructions for a future Codex instance that already knows how to reason, but needs the user's preferred workflow and local details.
