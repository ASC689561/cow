import logging
import re
import sys

import click

from .rsa_encrpyt_helper import RSAEncryptHelper

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)


@click.group()
def cli():
    pass


@cli.group(name="rsa")
def rsa_group():
    pass


@rsa_group.command()
@click.argument('file', type=click.STRING, default=sys.stdin)
def encrypt(file):
    """
    encrypt message from stdin
    cat a.txt | python3 -m cow rsa encrypt \n
    echo secret | python3 -m cow rsa encrypt \n
    insert one space before command to prevent save history
    """
    h = RSAEncryptHelper()
    for line in file.readlines():
        if len(line.strip()) == 0:
            print()
        else:
            print(h.encrypt(line))


@rsa_group.command()
@click.argument('file', type=click.File('rt'), default=sys.stdin)
def decrypt(file):
    """
    decrypt message from stdin
    cat a.txt | python3 -m cow rsa decrypt \n
    echo <md5> | python3 -m cow rsa decrypt \n
    insert one space before command to prevent save history
    """
    h = RSAEncryptHelper()
    for line in file.readlines():
        try:
            space = re.search('\S', line).start()-1
            print(' '*space, h.decrypt(line), end='\n')
        except:
            print(line, end='')


cli()
