# The cred class stores credentials used to connect and authenticate on Twitch's chat servers.

class cred:

    # Bot account oauth token
    OAUTH = "oauth:abc123"

    # Bot account username
    USER = "bot_username"

    # The channel you want the bot to connect to
    CHAN = "channel_name"

    # The name of the account that administrates this bot
    ADMIN = "admin_name"

    # Twitch IRC Connection Info. Don't edit this.
    HOST = "irc.twitch.tv"
    PORT = 6667
