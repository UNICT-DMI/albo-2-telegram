# Agent setup

Agent instructions are agent-neutral, so each contributor can use any coding agent.

## Layout

- `AGENTS.md`: canonical instructions (commands, constraints) and the index of the docs below.
  Keep it lean: anything else becomes a doc in `.agents/docs/`, linked from `AGENTS.md` as a plain
  markdown link with a one-line "read when…" hook, never an `@` import (some agents load imports
  at startup, defeating on-demand loading).
- `CLAUDE.md`: just `@AGENTS.md`, since Claude Code reads `CLAUDE.md`, not `AGENTS.md`.
  Claude-only instructions may follow the import.
- `.agents/docs/`: agent docs, read on demand.
- `.agents/skills/<name>/`: shared skills, each linked into every agent's skills dir that doesn't
  read `.agents/skills` natively, via a committed relative symlink (e.g.
  `.claude/skills/<name>` → `../../.agents/skills/<name>`).
- `.agents/plans/`: personal planning docs, gitignored.

## Hooking up an agent

- Claude Code: works as is, via `CLAUDE.md`.
- Agents that read `AGENTS.md` natively: nothing to do.
- Any other agent: point its entry file at `AGENTS.md` with its include syntax (no include
  syntax: copy the content and keep it in sync), or re-run `/agentify-project` to research and
  wire it.

## Windows

Skill symlinks need Developer Mode (or admin) and `git clone -c core.symlinks=true`; otherwise
they check out as plain text files.
