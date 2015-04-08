# -*- coding: utf-8 -*-

import pytest

from repocket.rules import compile_rules, Rule
from repocket.main import PocketItem


def test_single_rule():
    item1 = PocketItem(1, 'http://google.com', [], 'Google')
    item2 = PocketItem(2, 'http://github.com', [], 'Github')
    rule = Rule('.*google\.com', ['google'])

    assert rule.suggest_tags(item1) == set(['google'])
    assert rule.suggest_tags(item2) == set()


def test_tag_creation():
    items = [
        PocketItem(1, 'http://google.com', [], 'Google'),
        PocketItem(2, 'http://github.com/lensvol/repocket', [], 'Specific github'),
        PocketItem(3, 'http://github.com/', [], 'Github'),
    ]

    rule = Rule('.*github\.com/([a-z0-9]+)/.*', ['github', '{0}'])
    results = [rule.suggest_tags(item) for item in items]
    assert results == [set(), set(['github', 'lensvol']), set()]
