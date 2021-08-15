"""
# -*- coding: utf-8 -*-
@Time    : 8/9/2021 3:15 PM
@Author  : Harry Lee
@Email   : harrylee@nyu.edu
"""


class FieldItem:
    def __init__(self, field_name, en_name='', cn_name='', type_='', rules=[], range_=[], stats={}):
        self.field_name = field_name
        self.en_name = en_name
        self.cn_name = cn_name
        self.type = type_
        self.rules = rules
        self.range = range_
        self.stats = stats
        self.key = None
        self.editing = False

    def export(self):
        return {
            'key': self.key,
            'field_name': self.field_name,
            'en_name': self.en_name,
            'cn_name': self.cn_name,
            'type': self.type,
            'rules': self.rules,
            'range': self.range,
            'stats': self.stats,
            'editing': self.editing
        }
