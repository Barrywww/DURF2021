"""
# -*- coding: utf-8 -*-
@Time    : 8/9/2021 2:27 PM
@Author  : Harry Lee
@Email   : harrylee@nyu.edu
"""
from my_memory_translate import get_cn


def camel2en(camel):
    en = []
    if camel.upper() == camel:
        return camel.lower()
    for each in camel:
        if ord(each) in range(ord('a'), ord('z') + 1):
            en.append(each)
        elif ord(each) in range(ord('A'), ord('Z') + 1) or ord(each) in range(ord('0'), ord('9') + 1):
            if len(en) > 0 and en[-1] != ' ':
                en.append(' ')
            en.append(chr(ord(each) + 32))
        elif each == '_':
            if len(en) > 0 and en[-1] != ' ':
                en.append(' ')
    en = ''.join(en)
    return en


def translate(en, dictionary={}):
    if en in dictionary:
        return dictionary[en]
    return get_cn(en)


def field2cn(field, dictionary={}):
    en = camel2en(field)
    result = translate(en, dictionary)
    return result, en


if __name__ == '__main__':
    for each in ['isuSize']:
        print(field2cn(each))
