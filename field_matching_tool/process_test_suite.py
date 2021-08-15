"""
# -*- coding: utf-8 -*-
@Time    : 8/7/2021 6:00 PM
@Author  : Harry Lee
@Email   : harrylee@nyu.edu
"""
import json
from datetime import datetime

import DateSense

class Log:
    def __init__(self, test_suite_paths):
        self.stats = {}
        self.test_suite_paths = test_suite_paths
        self.count(test_suite_paths)
        self.fields = list(self.stats.keys())
        self.predictions = {}
        for field in self.fields:
            self.predictions[field] = self.pred_type(self.stats[field])

    def walk_json(self, obj, stats={}, key=''):
        """
        Used to go over the json file
        :param obj: the object to be walked over
        :param stats: the processed results
        :param key: the key which refers to this object (root object do not have keys)
        :return: the final statistic result of the file
        """
        if type(obj) == type(list()):
            for each in obj:
                stats = self.walk_json(each, stats, key)
        elif type(obj) == type(dict()):
            for key in obj.keys():
                stats = self.walk_json(obj[key], stats, key)
        else:
            if key in stats:
                if obj in stats[key]:
                    stats[key][obj] += 1
                else:
                    stats[key][obj] = 1
            else:
                stats[key] = {}
                stats[key][obj] = 1
        return stats

    def count(self, paths: list):
        """
        Walk over multiple json files and get the statistics of fields
        :param paths: a list of paths of json test suite files
        :return: the integrated statistics of fields
        """
        log = {}
        for path in paths:
            with open(path, encoding='utf-8') as f:
                suite = json.load(f)
                log = self.walk_json(suite, log)
        self.stats = log
        return log

    def pred_type(self, stats: dict, field=''):
        """
        Predict the type of the field according to the inputs in this filed
        变量名类型识别规则：
            1.	识别是否全为空值，是则识别为“其它”
            2.	识别是否为Float，并获得最大最小值
            3.	识别是否为Int，并获得最大最小值
            4.	由DateSense识别是否为日期， 并获得最大日期和最小日期；
            5.	识别文本的重复率，如果排除空字符串后有重复的文本，则识别为“枚举值”，否则识别为“文本”
        :param stats: one stats info in self.stats
        :return: the type of the field (String, Date, Time, )
            type: 其它、枚举值、整型、浮点数、日期
            range: range(xx), for 整型、浮点数、日期
            values: list(), for 枚举值
            stats: original stats info
        """
        keys = list(stats.keys())
        # 其它
        if len(keys) == 1 and keys[0] == '':
            return {'type': '其它', 'stats': stats, 'range': ''}
        # 整型
        is_integer = True
        integers = []
        try:
            for each in keys:
                if each == '':
                    continue
                if str(int(each)) != each:
                    is_integer = False
                integers.append(int(each))
            if is_integer:
                return {'type': '整型', 'range': 'range({0}, {1})'.format(min(integers), max(integers))}
        except ValueError:
            pass
        # 浮点数
        is_float = True
        floats = []
        try:
            for each in keys:
                if each == '':
                    continue
                if str(float(each)) != each and str(int(each)) != each:
                    is_float = False
                floats.append(float(each))
            if is_float:
                return {'type': '浮点型', 'range': 'range({0}, {1})'.format(min(floats), max(floats))}
        except ValueError:
            pass
        # 日期
        date_format = str(DateSense.detect_format(keys))
        if date_format == "%Y-%m-%d %H:%M:%S.%w":
            date_format = '%Y-%m-%d %H:%M:%S.%f'  # to handle exceptions such as '2017-12-29 00:00:00.000'
        if date_format != '':
            dates = []
            for each in keys:
                if each != '':
                    dates.append(datetime.strptime(each, date_format))
            max_date = datetime.strftime(max(dates), date_format)
            min_date = datetime.strftime(min(dates), date_format)
            if date_format == "%Y-%m-%d %H:%M:%S.%w":
                max_date = max_date.split('.')
                max_date[-1] = int(int(max_date[-1]) / 1000)
                min_date = min_date.split('.')
                min_date[-1] = int(int(min_date[-1]) / 1000)
            return {'type': '日期', 'range': 'range({0}, {1})'.format(min_date, max_date)}

        # 枚举值/文本
        for key in keys:
            if stats[key] > 1:
                return {'type': '枚举值', 'range': keys}
        return {'type': '文本', 'range': ''}


if __name__ == '__main__':
    import os
    root_path = './test_data/manual/fx/'
    paths = []
    for path in os.listdir(root_path):
        paths.append(root_path + path)
    log = Log(paths)
    print()
