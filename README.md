# PhorceBot Framework
A basic framework for a Twitch chat bot based on my own, PhorceBot.

This framework handles all the basics of connecting a bot to Twitch's servers and parsing messages for use in commands and functions. It's open ended, letting you build on top in any way you want. The biggest goal of this framework is to be as simple as possible to set up for people with no/limited python or programming experience, and to be a great place for them to start learning these things.

_Important_: This framework does not currently include any form of rate limiting. This is a vulnerability, and if abused, puts you at risk of receiving a temporary ban (30 minutes) from Twitch's chat servers. There are many ways to implement rate limiting, so I wanted to leave that up to the individual. Read more here: https://dev.twitch.tv/docs/irc/guide/

### Setup
Edit Credentials.py to include your information. The admin account will always be seen as a moderator by the bot. This should be your main Twitch account. After Credentials.py is set up, simply run Run.py to launch the bot.

Get your bot's oauth token here: https://twitchapps.com/tmi/

### Editing
You can add, edit, and remove whatever code you want in Run.py. There are sections in there for Classes and Variables, Functions, and Chat Commands. Read the comments in Run.py to get a feel for how things work.

Every time a chat line comes into the bot, it splits the line up into multiple digestible variables inside the "chat" class. You can use these variables in any way you want, such as checking if a user is a moderator or subscriber, or printing out their username.
```py
chat.username           # Username of the person that sent the message (Usernames are all lowercase)
chat.displayname        # Display name of the person that sent the message (Includes casing)
chat.moderator          # Moderator status (True or False)
chat.subscriber         # Subscriber status (True or False)
chat.message            # The chat message in all lowercase
chat.message_raw        # The chat message including casing
chat.flags              # Command flags, eg. !command flag
```
Here are some example commands to show you how easy it is to get things rolling:
```py
if "!test" in chat.message:
  say("Testing!")
  
if "!mod" in chat.message and chat.moderator == True:
  say("This is a mod only command!")
  
if "!roll" in chat.message:
  dice = randint(1, 6)
  say(dice)
```
