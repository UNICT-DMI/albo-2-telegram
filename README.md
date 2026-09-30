# albo-2-telegram

[Live Demo](https://t.me/albo_unict)

### Installation

Clone this repo with:

```
$ git clone https://github.com/UNICT-DMI/albo-2-telegram.git
```

Requires Python 3.15 or newer.

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then install project dependencies with:

```
$ uv sync
```

uv downloads Python 3.15 itself if it's missing.

### Usage

Create a duplicate file of `settings.yaml.dist` named `settings.yaml`:

```
$ cp settings.yaml.dist settings.yaml
```

Edit the values inside the configuration file as you see fit, specifically:

```
token: "" <string containing the bot's unique identifier>
chat_id: 123456 <chat_id of the channel in which the bot will post its messagges>
chat_id_dev: <list of chat_ids with devs to receive technical exception regarding the bot>
  - 123456
  - 123456
  - ... 
```

Create a new file named `last_id.txt` containing the current last ID in [albo](https://ws1.unict.it/albo/):

```
$ echo 510 > data/last_id.txt
```

Run `uv run albo.py` from the project directory every X minutes to check (the script reads `settings.yaml`, `data/` and `departments_regex.yaml` via relative paths). `uv run` syncs the environment with `uv.lock` before each run, so no manual `uv sync` is needed after a pull.

In a crontab, `PATH` often lacks `~/.local/bin`, so you may need the full path to `uv` (see `which uv`):

```
*/5 * * * * cd /path/to/albo-2-telegram && /home/user/.local/bin/uv run albo.py
```

### AI agents

Agent instructions live in [AGENTS.md](AGENTS.md); [.agents/docs/onboarding.md](.agents/docs/onboarding.md) explains the layout and how to hook up your agent.

### Credits

- Stefano Borzì (Helias)
- Luca Greco
