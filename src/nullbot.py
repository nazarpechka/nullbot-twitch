import time

from irc import *
from config import *
from commands import *


def log(message='nullbot', state=1, channel='#nullbot', nickname='nullbot'):
    if state == 0: color = '\033[94m'  # normal state
    elif state == 1: color = '\033[93m'  # warning state
    else: color = '\033[91m'  # error state
    end_color = '\033[0m'
    current_time = time.strftime('%H:%M:%S')

    print('[{}]{}[{}][{}]{} {}'.format(current_time, color, channel, nickname, end_color, message))


def stop(nullsock):
    log('stopping nullbot...')

    nullsock.leave_channel()
    nullsock.irc.close()

    log('closed socket')
    log('bye-bye :3')
    sys.exit()


def nullbot():
    log("nullbot is starting... please, report problems on github", 1)

    nullsock = irc(config)
    nullsock.initialize()

    # main thread
    while True:
        for message, channel, nickname in nullsock.get_message():

            if '!help' in message:
                nullsock.send_message(help(nickname), channel)
                # example command, function must be defined in commands.py
                # in this example function is help, and it takes user nickname
            if '!stop' in message:
                nullsock.send_message('turning off...', channel)
                stop(nullsock)
                # service command which turns of nullbot
                # you may change or disable it


if __name__ == '__main__':
    nullbot()

