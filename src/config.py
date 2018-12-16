config = {

    'server_address': 'irc.chat.twitch.tv',
    # twitch server address (do not change unless you know what this is

    'connection_port': 6697,
    # twitch server connection port (do not change unless you know what this is)

    'ssl': True,
    # change this to disable SSL connection (make sure to change port above to 6667)

    'channels': ['#channel1', '#channel2', '#channel3'],
    # your channel name (in stream url twitch.tv/XXXX its #XXXX)

    'nickname': 'nickname',
    # your twitch bot's nickname (the one you use to log in on twitch.tv)

    'password': 'oauth:key'
    # your twitch bot's oauth key (you can get it here http://www.twitchapps.com/tmi/)

}
