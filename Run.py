import string, socket, sys, time, re
from Credentials import cred
from Parsing import messageParse

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
    message_raw = ""                # Chat message in all lowercase
    flag = ""                       # A command flag

# Random Variables
debugMode = False


# =========
# Functions
# =========

# Sends a message to TMI
def irc(message):
    s.send(bytes(message + "\r\n","UTF-8"))

# Sends a message to Twitch Chat
def say(message):
    s.send(bytes("PRIVMSG #" + cred.CHAN + " :" + message + "\r\n","UTF-8"))
    print(">>> PhorceBot: " + message)

# =============
# Chat Commands
# =============

def commands(chat):

    # All chat commands go here. Make a command using an if statement.
    # Example: If "!test" in chat.message: say("Testing!")
    # You can use anything in the chat class when making commands!

    # Admin only quit command. Terminates the bot. You probably shouldn't remove this.
    if "!quit" in chat.message and chat.username == cred.ADMIN:
        say("Quitting.")
        return False

    # Toggle debug mode
    if "!debug" in chat.message and chat.username == cred.ADMIN:
        say("Debug mode toggled")
        global debugMode
        debugMode = not debugMode

    # Check chat class
    if "!check" in chat.message and debugMode == True:
        say("Display name: " + chat.displayname + " | Username: " + chat.username + " | Mod: " + str(chat.moderator) + " | Sub: " + str(chat.subscriber))

    # Test command
    if "!test" in chat.message:
        say("Testing!")

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
irc("PASS " + cred.OAUTH)
irc("NICK " + cred.USER)

# Join channel
irc("JOIN #" + cred.CHAN)
print("Joined #" + cred.CHAN)

# Send CAP requests
irc("CAP REQ :twitch.tv/membership")
irc("CAP REQ :twitch.tv/tags")
irc("CAP REQ :twitch.tv/commands")

# Parse messages incoming from socket
incoming = ""
receiving = True  # Set receiving to False to terminate the while loop and close the bot
while receiving:
    incoming = s.recv(4096).decode("UTF-8")

    chatLine = str.split(incoming, "\r\n")
    incoming = chatLine.pop() # Removes the old incoming message that was stored to clear RAM. Don't change this!!!

    for line in chatLine:

        if line: # Makes sure line isn't false, empty, or null

            # Responds to TMI's pings
            if "PRIVMSG" not in line and "PING :tmi.twitch.tv" in line:
                irc("PONG :tmi.twitch.tv")

            # Checks for Twitch chat messages
            elif "PRIVMSG" in line:

                try:
                    messageParse(line, chat)

                    if debugMode == True:
                        print(str(chatLine))
                    else:
                        print(chat.displayname + ": " + chat.message_raw)  # Prints the chat line to the console

                    receiving = commands(chat)  # Checks the chat message for commands. If a command returns "False", the bot terminates.
                except Exception as e:
                    print("$ Message processing failed: " + str(chatLine))
                    print(e)

# If receiving is false, the while loop will end and the script continues here.
print("No longer receiving messages.")
sys.exit("Exiting.")
