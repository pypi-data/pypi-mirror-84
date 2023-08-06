# Twitch Plays hackRU
twitch_plays_hackru is a Python library for twitch chatters to be able to vote on commands in a game.

## Installation

```pip3 install twitch_plays_hackru.```

## Usage

### Importing the classes:
```python
from twitch_plays_hackru import TwitchPlaysOnline, TwitchPlaysOffline
```

### Initializing the TwitchPlaysOnline or TwitchPlaysOffline object: 
```python
twitch_options = {
    "PASS": "oauth:YOUR_OATH_CODE_HERE",
    "BOT": "TwitchPlaysBot",
    "CHANNEL": "YOUR_CHANNEL_NAME_HERE",
    "OWNER": "YOUR_CHANNEL_NAME_HERE",
    "OPTIONS": ["1","2","3","hi","bye"],
    "VOTE_INTERVAL": 5
}
tPlays = TwitchPlaysOnline(**twitch_options)
# or
tPlays = TwitchPlaysOnline(
    PASS="oauth:YOUR_OATH_CODE_HERE",
    BOT="TwitchPlaysBot",
    CHANNEL="YOUR_CHANNEL_NAME_HERE",
    OWNER="YOUR_CHANNEL_NAME_HERE",
    OPTIONS=["1","2","3","hi","bye"],
    VOTE_INTERVAL=5)
```

The object will take in **7 parameters**:\
only VOTE_INTERVAL and OPTIONS are needed for the offline version
SERVER: the server that the bot will be interacting with. In this case it will always be "irc.twitch.tv" (the default)\
PORT: the port you would like use. defaults to 6667\
PASS: the OAuth code for the twitch channel you would like this bot to listen on. Use [twitchapp.com/tmi/](https://twitchapps.com/tmi/) to generate the OAuth code for your twitch channel.\
BOT: the nickname of the bot.\
CHANNEL: the name of the channel you would like this bot to listen on.\
OWNER: the username of the owner of the channel you would like this bot to listen on.\
OPTIONS = []: an array of options that you would like the bot to keep track of.
VOTE_INTERVAL: how often you want to count up the votes. defaults to every 5 seconds

### Chatters voting:
The initialization of the bot will also startup the bot. This means that the bot will send a "Hello World" message in the chat and then begin to listen to all of the chat responses.\
Chatters will preface their vote option by using **play_**
. For example, a vote for **hi** from the code above must be typed **play_hi**. It is not case sensitive.

## Functions:
### vote_results():
```python
result = tPlays.vote_results()
```
vote_results() returns the majority vote since the last count. if a count has not been completed it will return null
the whole idea behind this library is that vote_results acts like pygame.key.get_pressed() which makes
it easy to develop a game with

## License
[GNU](https://choosealicense.com/licenses/agpl-3.0/)
