# PhorceBot Framework
A basic framework for a Twitch chat bot based on my own Twitch chat bot, PhorceBot.

This framework handles all the basics of connecting a bot to Twitch's servers and parsing messages for use in commands and functions. It's open ended, letting you build on top in any way you want.

_Important_: This framework does not currently include any form of rate limiting. This is a vulnerability, and if abused, puts you at risk of receiving a temporary ban (30 minutes) from Twitch's chat servers. Read more here: https://dev.twitch.tv/docs/irc/guide/

### Setup
Edit Credentials.py to include your information. The admin account will always be seen as a moderator by the bot. This should be your main Twitch account.After Credentials.py is set up, simply run Run.py to launch the bot.

Get your bot's oauth token here: https://twitchapps.com/tmi/

### Editing
You can add, edit, and remove whatever code you want in Run.py. There are sections in there for Classes and Variables, Functions, and Chat Commands.
