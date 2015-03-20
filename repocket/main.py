#!/usr/bin/python

from click import (
    command,
    option,
    secho,
    echo,
    progressbar,
    prompt,
    confirm,
    style,
)
import os
import yaml
from collections import namedtuple

from pocket import Pocket

from rules import DEFAULT_RULES, compile_rules


PocketItem = namedtuple('PocketItem', ['id', 'url', 'tags', 'title'])


def save_credentials(consumer_key, access_token, path=None):
    if not path:
        path = os.path.join(os.path.expanduser('~'), '.repocket.yml')

    try:
        with open(path, 'r') as fp:
            cfg = yaml.load(fp.read())
    except IOError:
        cfg = {}

    cfg['credentials'] = {
        'consumer_key': str(consumer_key),
        'access_token': str(access_token),
    }

    with open(path, 'w') as fp:
        fp.write(yaml.dump(cfg))

    return True


def get_consumer_key():
    return prompt('Please enter your Pocket consumer key')


def get_access_token(consumer_key):
    request_token = Pocket.get_request_token(
        consumer_key=consumer_key,
        redirect_uri='localhost',
    )
    auth_url = Pocket.get_auth_url(
        code=request_token,
        redirect_uri='localhost',
    )

    echo('Please, open this URL in your browser: {}'.format(auth_url))
    if confirm('Did you went to that link?'):
        echo('Getting credentials...')
        credentials = Pocket.get_credentials(
            consumer_key=consumer_key,
            code=request_token,
        )
        return credentials['access_token']


def load_credentials(path=None):
    if not path:
        path = os.path.join(
            os.path.expanduser('~'),
            '.repocket.yml',
        )

    try:
        with open(path, 'r') as fp:
            cfg = yaml.load(fp.read())
            creds = cfg.get('credentials', {})
            return creds.get('consumer_key'), creds.get('access_token')
    except IOError:
        return None, None


def retrieve_items(pocket, count=10, sort=None, full=True):
    call_args = dict(sort=sort or 'newest')
    if full:
        call_args['detailType'] = 'complete'
    if count:
        call_args['count'] = count

    returned_items = pocket.get(**call_args)[0]['list']

    for item_id, resp_item in returned_items.iteritems():
        yield PocketItem(
            item_id,
            resp_item['resolved_url'],
            resp_item.get('tags', {}).keys(),
            resp_item['resolved_title']
        )


@command()
@option('--count', default=25, help='Number of items to process.')
@option('--dry-run', is_flag=True)
@option('-a', '--process-all', is_flag=True)
def processor(count, process_all, dry_run):
    at_most_count = process_all and 0 or count
    consumer_key, access_token = load_credentials()

    if not consumer_key or not access_token:
        consumer_key = get_consumer_key()
        access_token = get_access_token(consumer_key)
        save_credentials(consumer_key, access_token)

    secho('Your consumer key: ', fg='cyan', nl=False)
    secho(consumer_key)
    secho('Your access token: ', fg='cyan', nl=False)
    secho(access_token)
    echo()

    api_connector = Pocket(consumer_key, access_token)
    rules = compile_rules(DEFAULT_RULES)
    modified_items = []

    with progressbar(
        retrieve_items(api_connector, count=at_most_count),
        label=style('Processing items', fg='cyan'),
    ) as items:
        for item in items:
            suggested_for_item = set()

            for rule in rules:
                tags = rule.suggest_tags(item)
                if tags:
                    suggested_for_item.update(tags)
                new_tags = suggested_for_item - set(item.tags)
                if new_tags:
                    api_connector.tags_add(item.id, ','.join(list(new_tags)))
                    modified_items.append((item, new_tags))

    if modified_items:
        echo()
        for item, suggested_tags in modified_items:
            secho(u'Title:\t', fg='cyan', nl=False)
            echo(item.title)
            secho('URL:\t', fg='cyan', nl=False)
            echo(item.url)
            secho('Added tags:\t', fg='cyan', nl=False)
            echo(', '.join(suggested_tags))
            echo()

        if not dry_run:
            api_connector.commit()
            secho('Changes are sent to server.', fg='green')
        else:
            secho('"Dry run", no changes are sent to server.', fg='yellow')


if __name__ == '__main__':
    processor()
