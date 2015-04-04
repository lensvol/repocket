# -*- coding: utf-8 -*-

import json

import pytest
from mock import MagicMock

from repocket.main import PocketItem, retrieve_items

TEST_RESPONSE_HEADERS = {
    'status': '200 OK',
    'expires': 'Thu, 19 Nov 1981 08:52:00 GMT',
    'pragma': 'no-cache',
    'x-source': 'Pocket',
    'transfer-encoding':'chunked',
    'set-cookie': 'PHPSESSID=d0etpgedka41uoe642l2qc32s0; path=/',
    'x-limit-key-remaining': '9997',
    'x-limit-key-limit': '10000',
    'server': 'Apache',
    'cache-control': 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0',
    'connection': 'keep-alive',
    'x-limit-user-limit': '500',
    'x-limit-key-reset': '3556',
    'date': 'Sat, 04 Apr 2015 05:31:02 GMT',
    'p3p': 'policyref="/w3c/p3p.xml", CP="ALL CURa ADMa DEVa OUR IND UNI COM NAV INT STA PRE"',
    'content-type': 'application/json',
    'x-limit-user-reset': '3556',
    'x-limit-user-remaining': '497',
}
TEST_RESPONSE_DATA = {
    'status': '1',
    'list': {
        '1': {
            "status": "0",
            "is_index": "0",
            "sort_id": 22,
            "time_updated": "1427796327",
            "time_favorited": "0",
            "time_read": "0",
            "excerpt": "Small excerpt",
            "image": {
                "item_id": "883282590",
                "src": "https://google.com/",
                "height": "0",
                "width": "566"
            },
            "has_image": "1",
            "favorite": "0",
            "has_video": "0",
            "word_count": "889",
            "images": {
                "1": {
                    "src": "https://google.com/1.png",
                    "credit": "",
                    "height": "0",
                    "image_id": "1",
                    "item_id": "883282590",
                    "caption": "",
                    "width": "566"
                },
            },
            "given_title": "Monkey Patching in Go",
            "resolved_url": "https://google.com/",
            "is_article": "1",
            "item_id": "883282590",
            "time_added": "1427796327",
            "resolved_id": "883282590",
            "given_url": "https://com.google/",
            "resolved_title": "Google Home Page",
            "tags": {
                "google": '1',
            },
        }
    }
}

@pytest.fixture
def pocket_mock(request):
    fake_pocket = MagicMock()
    fake_pocket.get.return_value = (
        TEST_RESPONSE_DATA,
        TEST_RESPONSE_HEADERS,
    )
    return fake_pocket


def test_retrieve_items(pocket_mock):
    items = list(retrieve_items(pocket_mock))
    assert len(items) == 1
    assert items[0] == PocketItem(
        '1', 'https://google.com/',
        ['google'], 'Google Home Page',
    )
