import subprocess


def notify_message(message):
    subprocess.Popen(['notify-send', message])
    return
