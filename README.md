# albo-2-telegram

[Live Demo](https://t.me/albo_unict)

### Installation

Clone this repo with:

```
$ git clone https://github.com/UNICT-DMI/albo-2-telegram.git
```

Install project dependecies with:

```
$ pip3 install -r requirements.txt
```

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

Create a new directory called `data`:
```
$ mkdir data
```

Create a new file named `last_id.txt` containing the current last ID in [albo](https://ws1.unict.it/albo/):

```
$ echo 510 > data/last_id.txt
```

Run `python3 albo.py` every X minutes to check

### Credits

- Stefano Borzì (Helias)
- Luca Greco
