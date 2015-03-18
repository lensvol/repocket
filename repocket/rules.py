# -*- coding: utf-8 -*-

import re


DEFAULT_RULES = [
    {
        'rule': '.*github\.com.*',
        'tags': ('programming', 'github'),
    },
    {
        'rule': '.*blog\.*',
        'tags': ('blog',),
    },
]


class Rule(object):
    rule_expr = None

    def __init__(self, expr, tags):
        self.rule_expr = re.compile(expr)
        self.tags = tags

    def suggest_tags(self, item):
        if self.rule_expr.match(item.url):
            return self.tags


def compile_rules(ruleset):
    rules = []

    for definition in ruleset:
        r = Rule(definition['rule'], definition['tags'])
        rules.append(r)

    return rules
