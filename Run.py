import string, socket, sys, time, re
from Credentials import cred

print("========================")
print("PhorceBot 4.0 by Vespher")
print("========================")

# =====================
# Classes and Variables
# =====================

# The chat class stores information about incoming chat messages
class chat:
    username = ""                   # Username in all lowercase
    displayname = ""                # Case sensitive username
    moderator = False               # Moderator status. True or False.
    subscriber = False              # Subscriber status. True or False.
    message = ""                    # Chat message
    message_lowercase = ""          # Chat message in all lowercase
    flag = ""                       # A command flag

# =========
# Functions
# =========

# Sends a message to TMI
def irc(message):
    s.send(message + "\r\n")
    print("# " + message)

# Sends a message to Twitch Chat
def say(message):
    s.send("PRIVMSG #" + cred.CHAN + " :" + message + "\r\n")
    print(">>> PhorceBot: " + message)

# =============
# Chat Commands
# =============

def commands(chat):

    # All chat commands go here. Make a command using an if statement.
    # Example: If "!test" in chat.message: say("Testing!")
    # You can use anything in the chat class when making commands!

    # Test command
    if "!test" in chat.message:
        say("Testing!")

    # Checks if you're a mod. Keep in mind that you are not a mod in your own channel. If you are the bot admin, it will think you are a mod.
    if "!mod" in chat.message and chat.moderator == True:
        say("You are a mod!")
    elif "!mod" in chat.message and chat.moderator == False:
        say("You are not a mod.")

    # Admin only quit command. Terminates the bot. You probably shouldn't remove this.
    if "!quit" in chat.message and chat.username == cred.ADMIN:
        say("Quitting.")
        return False

    # End of commands. Return "True" to keep the bot running.
    return True

# ---You shouldn't need to edit anything below this line unless you know what you're doing.---

# ================
# Begin connection
# ================

# Create and open a socket connecting to Twitch IRC
s = socket.socket()
s.connect((cred.HOST, cred.PORT))

# Authenticate
irc("PASS " + cred.OAUTH + "\r\n")
irc("NICK " + cred.USER + "\r\n")

# Join channel
irc("JOIN #" + cred.CHAN + "\r\n")
print("Joined #" + cred.CHAN)

# Send CAP requests
irc("CAP REQ :twitch.tv/membership\r\n")
irc("CAP REQ :twitch.tv/tags\r\n")
irc("CAP REQ :twitch.tv/commands\r\n")

# Parse messages incoming from socket
incoming = ""
receiving = True  # Set receiving to False to terminate the while loop and close the bot
while receiving:
    incoming = s.recv(1024)
    temp = str.split(incoming, "\n")
    incoming = temp.pop()

    for line in temp:

        if line: # Makes sure line isn't false, empty, or null

            # Responds to TMI's pings
            if "PRIVMSG" not in line and "PING :tmi.twitch.tv" in line:
                irc("PONG :tmi.twitch.tv")

            # Checks for Twitch chat messages
            elif "PRIVMSG" in line:

                # Chat message regex. This code splits the chat message into digestible variables inside the chat class.
                meta = re.search(".*display-name=(\w*);.*mod=(\w*);.*subscriber=(\w*);.*PRIVMSG #" + cred.CHAN + " :(.*)", line)
                chat.displayname = meta.group(1)
                chat.username = meta.group(1).lower()
                chat.moderator = meta.group(2)
                chat.subscriber = meta.group(3)
                chat.message_lowercase = meta.group(4).lower()
                chat.message = meta.group(4)

                meta2 = re.search(".*PRIVMSG #" + cred.CHAN + " :!\w* (.*)", line)
                if meta2:
                    chat.flag = meta2.group(1)
                else:
                    chat.flag = ""

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
                if chat.username == cred.ADMIN:
                    chat.moderator = True

                print(chat.displayname + ": " + chat.message)  # Prints the chat line to the console

                receiving = commands(chat)  # Checks the chat message for commands. If a command returns "False", the bot terminates.

# If receiving is false, the while loop will end and the script continues here.
print("No longer receiving messages.")
sys.exit("Exiting.")
