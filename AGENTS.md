# albo-2-telegram

Script that posts new announcements from UNICT's [albo](http://albo.unict.it/) to a Telegram
channel, run periodically (cron). Python 3.15 (`lazy` imports), managed with uv.

## Commands

Run from the repo root: the script reads `settings.yaml`, `data/` and `departments_regex.yaml` via
relative paths.

- Install: `uv sync`
- Run: `uv run albo.py`. Needs `settings.yaml` (from `settings.yaml.dist`) and
  `data/last_id.txt`, see README. With a real `settings.yaml` it posts to the live channel: never
  run it just to test.
- No tests, linter or CI.

## Docs

- [Onboarding](.agents/docs/onboarding.md): read when hooking up an agent, or adding agent docs or
  skills.

## Planning

Planning docs (plans, designs, investigations) go in `.agents/plans/<task-slug>/` (gitignored).
