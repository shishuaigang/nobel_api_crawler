# -*- coding: utf-8 -*-
import os
import codecs
import json
import sys
import copy
from more_itertools import chunked

reload(sys)
sys.setdefaultencoding('utf8')


class api_num:
    def __init__(self, path):
        self.path = path

    @property
    def json_data(self):
        for files in os.walk(self.path):
            json_file = files[2]
        return json_file

    def read_section(self):  # 返回每个section下value的值
        os.chdir(self.path)
        re = []
        temp = [(json.loads(codecs.open(self.json_data[i], encoding='utf-8').read()))["section"]
                for i in range(len(self.json_data))]  # 结构[[{},{},{}],[{}]]
        for i in range(len(self.json_data)):
            result = []
            for j in range(len(temp[i])):
                result.append(temp[i][j]['value'])  # i=0时，result的第一个元素插入了temp[i]下面的所有value的值
            re.append(result)
        return re

    def every_json_api_number(self):  # 每个json文件下有多少个API，存入list
        # 返回格式[[15], [27, 6, 4, 3, 6, 5, 3, 8, 4, 3, 18, 6, 6], [63], [38]]
        os.chdir(self.path)
        l = self.read_section()
        re = []
        for i in range(len(self.json_data)):
            result = []
            for j in range(len(l[i])):
                result.append(len(json.loads(codecs.open(self.json_data[i], encoding='utf-8').read())[l[i][j]]))
            re.append(result)
        return re


class api_url(api_num):
    def api_url(self):
        num = self.every_json_api_number()
        array_name = self.read_section()
        url = []
        for m in range(len(self.json_data)):
            f = codecs.open(self.json_data[m], encoding='utf-8')
            dict_json = json.loads(f.read())
            if "NoNeed" not in dict_json.keys() or dict_json["NoNeed"] == str(0):
                for n in range(len(num[m])):  # num[m]是一个list
                    for k in range(num[m][n]):
                        if "NoNeed" not in dict_json[array_name[m][n]][k] or dict_json[array_name[m][n]][k][
                            "NoNeed"] == str(0):
                            url.append(dict_json[array_name[m][n]][k]["url"])
        return url


class api_cn_name(api_num):
    def api_chinese_name(self):
        num = self.every_json_api_number()
        array_name = self.read_section()
        api_chinese_name = []
        for m in range(len(self.json_data)):
            f = codecs.open(self.json_data[m], encoding='utf-8')
            dict_json = json.loads(f.read())
            if "NoNeed" not in dict_json.keys() or dict_json["NoNeed"] == str(0):
                for n in range(len(num[m])):
                    for k in range(num[m][n]):
                        if "NoNeed" not in dict_json[array_name[m][n]][k] or dict_json[array_name[m][n]][k][
                                "NoNeed"] == str(0):
                            api_chinese_name.append(dict_json[array_name[m][n]][k]["summary"])  # api的中文名字
        return api_chinese_name


class api_cor_params(api_url):
    def api_details(self):
        num = self.every_json_api_number()
        array_name = self.read_section()
        param_all_details = []
        for m in range(len(self.json_data)):
            f = codecs.open(self.json_data[m], encoding='utf-8')
            dict_json = json.loads(f.read())
            if "NoNeed" not in dict_json.keys() or dict_json["NoNeed"] == str(0):
                for n in range(len(num[m])):
                    for k in range(num[m][n]):
                        if "NoNeed" not in dict_json[array_name[m][n]][k] or dict_json[array_name[m][n]][k][
                            "NoNeed"] == str(0):
                            param_all_details.append(dict_json[array_name[m][n]][k]["params"])
        return param_all_details

    def api_correct_params(self):
        params = []
        api_param_details = self.api_details()
        for i in range(len(self.api_url())):
            params_keys = []
            params_values = []
            for j in range(len(api_param_details[i].keys())):
                params_keys.append(api_param_details[i].keys()[j])
                params_values.append(str(api_param_details[i].values()[j]["default"]))
            params.append(dict(zip(params_keys, params_values)))
        return params


class api_err_params(api_cor_params):
    def api_error_params(self, error_list):
        p_c = self.api_correct_params()
        total_keys = []
        total_values = []
        error_keys = []
        error_values = []
        for i in range(len(p_c)):
            total_keys.append((copy.deepcopy(p_c[i].keys())) * len(error_list) * len(p_c[i].keys()))
            total_values.append((copy.deepcopy(p_c[i].values())) * len(error_list) * len(p_c[i].keys()))
            KEY = list(chunked(total_keys[i], (len(p_c[i].keys()) * len(error_list))))
            VALUE = list(chunked(total_values[i], (len(p_c[i].keys()) * len(error_list))))
            error_keys.append(copy.deepcopy(KEY))
            error_values.append(copy.deepcopy(VALUE))
            for j in range(len(p_c[i].keys())):
                for k in range(len(error_list)):
                    error_values[i][j][len(p_c[i].keys()) * k + j] = error_list[k]
        return [error_keys, error_values]
