# -*- coding: utf-8 -*-
import os
import json
import codecs
import time
import platform
from Test_scripts import api_param, api_response, getcookie, sendmail, write_database
from Test_scripts import generate_result, response_status, pass_rate

if __name__ == "__main__":
    print u'API遍历测试开始'
    if platform.system() == 'Windows':
        bt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 测试开始时间
        testNo = time.strftime('%Y%m%d%H%M', time.localtime())
        cur_dir = os.getcwd()
        api_json_path = cur_dir + '\\APIcrawler_json_data'
        print 'Now you are in ' + cur_dir
        print 'Your api json data location is ' + api_json_path
        conf = json.loads(codecs.open(cur_dir + '\\Config\\config.json', encoding='utf-8').read())
        api_ver = conf['api_version']
        cookie = getcookie.gecookie(api_ver)
        print 'Current api version is ' + api_ver
        inroad_url = api_param.api_url(api_json_path).api_url()  # 获取api的url的地址
        cn_name = api_param.api_cn_name(api_json_path).api_chinese_name()  # 获取api的中文名字
        api_len = len(inroad_url)  # 获取api的个数
        print 'Now you need test api number is ' + str(api_len)
        headers = {"Referer": "123"}
        res = api_response.api_cor_res(api_json_path).res_results(cookie, api_ver, headers)
        res_code = [res[i].status_code for i in range(api_len)]
        res_time = ['%.1f' % (float(res[i].elapsed.microseconds) / 1000) for i in range(api_len)]
        res_status = response_status.response_status(api_len).res_status(res)
        passrate = pass_rate.passrate(api_len).pass_rate(res_status, res_code)  # 计算成功率
        et = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 测试结束时间
        # 创建temp.html
        generate_result.gen_result(conf, cur_dir, inroad_url, api_len, cn_name, res, res_code, res_time,
                                   res_status).create_html(passrate, bt, et, testNo)
        # 创建temp.csv
        generate_result.gen_result(conf, cur_dir, inroad_url, api_len, cn_name, res, res_code, res_time,
                                   res_status).create_csv()
        time.sleep(5)

        os.chdir(cur_dir)
        print u'尝试将测试结果写入数据库...'
        if write_database.write_db(conf['db_name'], conf['db_host'], conf['db_username'], conf['db_userpasswd'],
                                   testNo).write_db(api_len) == 1:
            print u'尝试发送测试报告...'
            sendmail.send_mail(conf['receiver_list'], conf['mail_subject'], testNo).send_mail()
            print u'测试报告发送成功,API遍历测试完成'
        else:
            print u'写入数据库或者测试报告发送失败,请检查脚本和错误信息'
    else:
        print u"操作系统不是Windows，请更换windows系统尝试"
