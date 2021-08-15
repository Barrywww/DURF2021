"""
# -*- coding: utf-8 -*-
@Time    : 8/6/2021 6:00 PM
@Author  : Harry Lee
@Email   : harrylee@nyu.edu
"""

import pandas as pd


class UDD:
    def __init__(self, dict_path=[], cn_list=[], en_list=[]):
        self.dict_path = dict_path
        self.cn_list = cn_list
        self.en_list = en_list
        self.original_dict = {}
        self.process_all()

    def process_file(self):
        """
        :param dict_path: the Excel path of the dictionary
        :param original_dict: if there's original caches, then update the dictionary
        :return: updated dictionary
        """
        for path in self.dict_path:
            dict_sheet = pd.read_excel(path)
            for i in range(len(dict_sheet)):
                ori_cn = dict_sheet['中文名称'][i]
                ori_en = dict_sheet['英文名称'][i].lower()
                if ori_en in self.original_dict:
                    if ori_cn not in self.original_dict[ori_en]:
                        self.original_dict[ori_en].append(ori_cn)
                else:
                    self.original_dict[ori_en] = [ori_cn]
        return self.original_dict

    def process_string(self):
        """
        The function requires "cn_list" and "en_list" to have the same length
        :param cn_list: Chinese term name list
        :param en_list: English field name list
        :param original_dict: if there's original caches, then update the dictionary
        :return: updated dictionary
        """
        assert len(self.cn_list) == len(self.en_list), "Lengths of cn_list and en_list do not match."
        for i in range(len(self.cn_list)):
            ori_cn = self.cn_list[i]
            ori_en = self.en_list[i].lower()
            if ori_en in self.original_dict:
                if ori_cn not in self.original_dict[ori_en]:
                    self.original_dict[ori_en].append(ori_cn)
            else:
                self.original_dict[ori_en] = [ori_cn]
        return self.original_dict

    def process_all(self):
        """
        Process excel files and strings
        :return: updated dictionary
        """
        self.process_file()
        self.process_string()
        return self.original_dict

if __name__ == '__main__':
    dictionary = UDD(['./test_data/CFETS_dict.xlsx'], ['发行量', '哈瑞', '你'], ['isu Size', 'Harry', 'You'])
    print(dictionary.process_all())
