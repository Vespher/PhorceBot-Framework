import re
from Credentials import cred

def messageParse(line, chat):
    chatHeaders, chatMessage = line.split("PRIVMSG #" + cred.CHAN + " :", 1)

    meta = re.search(".*display-name=(\w*);.*mod=(\w*);.*subscriber=(\w*);.*", line)
    chat.displayname = meta.group(1)
    chat.username = meta.group(1).lower()
    chat.moderator = meta.group(2)
    chat.subscriber = meta.group(3)

    meta2 = re.search("!\w* (.*)", chatMessage)
    if meta2:
      chat.flag = meta2.group(1)
    else:
      chat.flag = ""

    chat.message = chatMessage.lower()
    chat.message_raw = chatMessage

    # Sets chat.moderator to be True/False instead of 1/0
    if chat.moderator == "1":
        chat.moderator = True
    else:
        chat.moderator = False

    # Sets chat.subscriber to be True/False instead of 1/0
    if chat.subscriber == "1":
        chat.subscriber = True
    else:
        chat.subscriber = False

    # Sets the admin to always be interpreted as a moderator
    if chat.username == cred.ADMIN or "broadcaster/1" in chatHeaders:
        chat.moderator = True

    return chat
