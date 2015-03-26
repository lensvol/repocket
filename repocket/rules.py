# -*- coding: utf-8 -*-

import re


DEFAULT_RULES = [
    {
        'rule': '.*github\.com/([a-z0-9]+)/.*',
        'tags': ['programming', 'github', '{0}'],
    },
    {
        'rule': '.*blog\.*',
        'tags': ['blog'],
    },
]


class Rule(object):
    rule_expr = None

    def __init__(self, expr, tags):
        self.rule_expr = re.compile(expr)
        self.tags = tags

    def suggest_tags(self, item):
        m = self.rule_expr.match(item.url)
        if m:
            result = set()
            for t in self.tags:
                try:
                    tag = t.format(*m.groups())
                except IndexError:
                    tag = ''

                if not tag:
                    continue
                result.add(tag)

            return result


def compile_rules(ruleset):
    rules = []

    for definition in ruleset:
        r = Rule(definition['rule'], definition['tags'])
        rules.append(r)

    return rules
