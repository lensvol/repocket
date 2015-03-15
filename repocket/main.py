#!/usr/bin/python

import sys
import click

from pocket import Pocket


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

    click.echo('Your consumer key: {}'.format(consumer_key))
    click.echo('Your access token: {}'.format(access_token))
