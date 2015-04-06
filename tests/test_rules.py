# -*- coding: utf-8 -*-

import pytest

from repocket.rules import compile_rules, Rule
from repocket.main import PocketItem


def test_single_rule():
    item1 = PocketItem(1, 'http://google.com', [], 'Google')
    item2 = PocketItem(1, 'http://github.com', [], 'Github')
    rule = Rule('.*google\.com', ['google'])

    assert rule.suggest_tags(item1) == set(['google'])
    assert rule.suggest_tags(item2) == set()
