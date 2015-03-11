#!/usr/bin/python

import sys
import click

from pocket import Pocket


def first_time_setup(consumer_key):
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


if len(sys.argv) == 2:
    CONSUMER_KEY = sys.argv[1]

    token = first_time_setup(CONSUMER_KEY)
    click.echo('Your access token: {}'.format(token))
else:
    click.echo('Usage: python repocket/main.py <CONSUMER_KEY>')
