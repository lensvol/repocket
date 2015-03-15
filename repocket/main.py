#!/usr/bin/python

import sys
import click
import os
import yaml

from pocket import Pocket


def save_credentials(consumer_key, access_token, path=None):
    if not path:
        path = os.path.join(
            os.path.expanduser('~'),
            '.repocket.yml',
        )

    try:
        with open(path, 'r') as fp:
            cfg = yaml.load(fp.read())
    except IOError:
        cfg = {}

    cfg['credentials'] = {
        'consumer_key': consumer_key,
        'access_token': access_token,
    }

    with open(path, 'w') as fp:
        fp.write(yaml.dump(cfg))

    return True


def get_consumer_key():
    return click.prompt('Please enter your Pocket consumer key')


def get_access_token(consumer_key):
    request_token = Pocket.get_request_token(
        consumer_key=consumer_key,
        redirect_uri='localhost',
    )
    auth_url = Pocket.get_auth_url(
        code=request_token,
        redirect_uri='localhost',
    )

    click.echo('Please, open this URL in your browser: {}'.format(auth_url))
    if click.confirm('Did you went to that link?'):
        click.echo('Getting credentials...')
        credentials = Pocket.get_credentials(
            consumer_key=consumer_key,
            code=request_token,
        )
        return credentials['access_token']


if __name__ == '__main__':
    consumer_key = get_consumer_key()
    access_token = get_access_token(consumer_key)

    save_credentials(consumer_key, access_token)

    click.echo('Your consumer key: {}'.format(consumer_key))
    click.echo('Your access token: {}'.format(access_token))
