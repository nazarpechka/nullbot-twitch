import sys
import ssl
import socket

from nullbot import log

# this module contains connecting to server through irc functions
# do not change it unless you know what are you doing


class irc:

    def __init__(self, config):
        """Initializes bot instance"""
        # importing whole config from passed config
        self.server_address = config['server_address']
        self.connection_port = config['connection_port']
        self.ssl = config['ssl']
        self.channels = config['channels']
        self.nickname = config['nickname']
        self.password = config['password']

        # creating socket connection
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.ssl:
            self.irc = ssl.wrap_socket(self.irc)

    def initialize(self):
        """Connects to twitch IRC"""
        self.connect()
        for channel in self.channels:
            self.join_channel(channel)

    def connect(self):
        """Connects to server and authorises user"""
        try:
            # attempt connecting to server
            self.irc.connect((self.server_address, self.connection_port))
        except ConnectionRefusedError:
            # connecting to server failed
            log('failed connecting to {}, exit...'.format(self.server_address), 2)
            sys.exit()
        else:
            # connecting to server successful
            log('connected to {}'.format(self.server_address))

        # attempt to authorise
        self.send('USER {}\r\n'.format(self.nickname))
        self.send('PASS {}\r\n'.format(self.password))
        self.send('NICK {}\r\n'.format(self.nickname))

        if 'failed' in self.receive():
            # authorisation failed
            log('failed to authorise with {} and {}, exit...'.format(self.nickname, self.password), 2)
            sys.exit()
        else:
            # authorisation successful
            log('authorised with {} and {}'.format(self.nickname, self.password))

    def send(self, message):
        """Sends any message to IRC server"""
        self.irc.send(message.encode('utf-8'))

    def send_message(self, message, channel):
        """Sends any message specifically to twitch chat"""
        self.send('PRIVMSG {} :{}\n'.format(channel, message))
        log('{}'.format(message), 1, channel)

    def receive(self):
        """Receives all new messages from IRC server"""
        try:
            response = self.irc.recv(4096).decode().split('\n')
            # we get byte string, decode it and split to strings
        except ConnectionResetError:
            log('failed to receive response from server (check your SSL settings), exit...', 2)
            sys.exit()

        for string in response:
            if 'PING' in string:
                self.send('PONG {}\r\n'.format(string[5:]))
                # once in few minutes server wants us to answer with PONG to know that we are still online
            if 'PRIVMSG' in string:
                yield string
                # this response is usual twitch chat message

    def get_message(self):
        """Receives new messages specifically from twitch chat"""
        for response in self.receive():
            channel = response[response.find('PRIVMSG ') + 8:response.find(' :')]
            nickname = response[1:response.find('!')]
            message = response[response.find('PRIVMSG ' + channel + ' :') + len(channel) + 10:-1]
            log(message, 0, channel, nickname)
            yield message, channel, nickname
            # we pass each message with nickname to main function

    def join_channel(self, channel):
        """Joins IRC channel"""
        self.send('JOIN {}\r\n'.format(channel))
        log('joined {}'.format(channel), 1)

    def leave_channel(self, channel):
        """Leaves IRC channel"""
        self.send('PART {}\r\n'.format(channel))
        log('left {}'.format(channel), 1)

    # additional features, only if bot is moderator
    def clear_chat(self, channel):
        """Clears twitch chat"""
        self.send('CLEARCHAT {}'.format(channel))

    def ban(self, nickname):
        """Bans specific twitch user"""
        self.irc.send('.ban {}'.format(nickname))
