"""
# -*- coding: utf-8 -*-
@Time    : 8/9/2021 10:30 PM
@Author  : Harry Lee
@Email   : harrylee@nyu.edu
"""


def match_rules(cn, field, en, rules):
    try:
        result = []
        for rule in rules:
            if type(cn) == type([]):
                for each_cn in cn:
                    if each_cn in rule or en in rule.lower() or field in rule.lower():
                        if rule not in result:
                            result.append(rule)
            elif type(cn) == type(''):
                if cn in rule or en in rule.lower() or field in rule.lower():
                    if rule not in result:
                        result.append(rule)
        return result
    except Exception as e:
        print(e)

