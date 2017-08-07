# -*- coding: utf-8 -*-
from api_param import api_cor_params as correct
from api_param import api_err_params as error
from more_itertools import chunked
import requests
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class api_cor_res(correct):
    def res_results(self, cookie, api_version, headers):
        """
        发送正确参数的请求
        :param cookie: value参数为cookie的值
        :param api_version: apiversion
        :return: 返回response
        """
        response_result = []
        api_param = self.api_correct_params()
        api_url = self.api_url()
        for i in range(len(self.api_url())):
            results = requests.post("http://192.168.31.99:7385/" + api_url[i],
                                    params={"APIVersion": api_version},
                                    data=api_param[i],
                                    cookies=cookie,
                                    headers=headers
                                    )
            response_result.append(results)
        return response_result


class api_err_res(error):
    def res_results(self, cookie, api_version, error_list, headers):
        """
        发送带有错误参数的请求
        :param cookie: value参数为cookie的值
        :param api_version: apiversion
        :param error_list: 自定义的错误参数类型
        :return: 返回response的status_code,text
        """
        response_result = []
        api_url = self.api_url()
        p_e = self.api_error_params(error_list)
        for i in range(len(p_e[0])):
            result = []
            for j in range(len(p_e[0][i])):
                _KEY = list(chunked(p_e[0][i][j], len(p_e[0][i])))
                _VALUE = list(chunked(p_e[1][i][j], len(p_e[0][i])))
                _result_min = []
                for k in range(len(error_list)):
                    results = requests.post("http://192.168.31.99:7385/" + api_url[i],
                                            params={"APIVersion": api_version},
                                            data=dict(zip(_KEY[k], _VALUE[k])), cookies=cookie, headers=headers)
                    _result_min.append(results)
                result.append(_result_min)
            response_result.append(result)
        return response_result
