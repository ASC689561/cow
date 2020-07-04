import subprocess


def notify_message(message, level='normal'):
    subprocess.Popen(['notify-send', '-u', level, message])
    return


if __name__ == '__main__':
    notify_message('hello')
