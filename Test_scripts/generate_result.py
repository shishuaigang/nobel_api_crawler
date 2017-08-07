# -*- coding: utf-8 -*-
import json
import csv


class gen_result:
    def __init__(self, conf, path, inroad_url, api_len, cn_name, response, response_code, response_time,
                 response_staus):
        """
        初始化
        :param conf: config.json
        :param path: script directory
        :param inroad_url: inroad api url
        :param api_len: api length
        :param cn_name: api chinese name
        :param response: api response
        :param response_code: api response_code
        :param response_time: api response_time
        :param response_staus: api response_staus
        """
        self.conf = conf
        self.path = path
        self.url = inroad_url
        self.api_len = api_len
        self.cn_name = cn_name
        self.res = response
        self.res_code = response_code
        self.res_time = response_time
        self.res_status = response_staus

    # 生成temp.html
    def create_html(self, passrate, begintime, endtime, testNo):
        f = open(self.path + r'\\temp.html', 'wb')
        message = """
            <html>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            <head>
            <title>Nobel API扫描</title>
            <style type="text/css">
                tr:hover {
                        background: yellowgreen;
                        color: black;
                        }
                tr:hover td{background:none;}
                tr:hover th{background:none;}
            </style>
            </head>
            <body bgcolor="#F7F7F7">
            <h1 style="margin-left:12.5%;">Nobel_API_Scan</h1>
            <h2 align="center" style="color:darkblue">Summary</h2>
             """
        f.write(message)
        f.close()
        fx = open(self.path + r'\\temp.html', 'a')
        fx.write('')
        fx.write(
            '<table style="margin-left:12.5%;" width="75%" align="left-side" border="1" cellspacing="0" height="280">')
        fx.write('<tr>')
        fx.write('<th align="center" bgcolor="#D0D0D0">测试编号</th>')
        fx.write('<td align="center" bgcolor="#D0D0D0">' + testNo + '</td>')
        fx.write('</tr>')
        fx.write('<tr>')
        fx.write('<th align="center">开始时间</th>')
        fx.write('<td align="center">' + begintime + '</td>')
        fx.write('</tr>')
        fx.write('<tr>')
        fx.write('<th align="center"  bgcolor="#D0D0D0">结束时间</th>')
        fx.write('<td align="center"  bgcolor="#D0D0D0">' + endtime + '</td>')
        fx.write('</tr>')
        fx.write('<tr>')
        fx.write('<th align="center">总数</th>')
        fx.write('<td align="center">' + str(self.api_len) + '</td>')
        fx.write('</tr>')
        fx.write('<tr>')
        fx.write('<th align="center"  bgcolor="#D0D0D0">成功</th>')
        fx.write('<td align="center"  bgcolor="#D0D0D0">' + str(passrate[0]) + '</td>')
        fx.write('</tr>')
        fx.write('<tr>')
        fx.write('<th align="center">失败</th>')
        fx.write('<td align="center"><font color=red>' + str(passrate[1]) + '</font></td>')
        fx.write('</tr>')
        fx.write('<th align="center"  bgcolor="#D0D0D0">成功率</th>')
        fx.write('<td align="center"  bgcolor="#D0D0D0">' + str(passrate[2]) + '</td>')
        fx.write('</tr>')
        fx.close()
        f1 = open(self.path + r'\\temp.html', 'a')
        f1.write('</table>')
        f1.write(
            '<h2 align="center" style="color:darkblue">Details</h2>')
        f1.write('<table width="75%" align="center" style="TABLE-LAYOUT:fixed" border="1" cellspacing="0">')
        f1.write('<tr>')
        f1.write('<td align="center" width="3%" bgcolor="#A4D3EE">序号</td>')
        f1.write('<td align="center" width="20%" bgcolor="#A4D3EE">API_URL</td>')
        f1.write('<td align="center" width="20%" bgcolor="#A4D3EE">API_Chinese_Name</td>')
        f1.write('<td align="center" width="10%" bgcolor="#A4D3EE">Res_Time</td>')
        f1.write('<td align="center" width="7%" bgcolor="#A4D3EE">Res_Code</td>')
        f1.write('<td align="center" width="5%" bgcolor="#A4D3EE">Status</td>')
        f1.write(
            '<td width="15%" style="WORD-WRAP: break-word;word-break:break-all" align="center" bgcolor="#A4D3EE">Error_Message</td>')
        f1.write('<td align="center" width="15%" bgcolor="#A4D3EE">趋势</td>')
        f1.write('</tr>')
        for i in range(self.api_len):
            if i % 2 == 0:
                f1.write('<tr bgcolor=white>')
                f1.write('<td align="center">' + str(i + 1) + '</td>')
                f1.write(
                    '<td align="center" style="WORD-WRAP: break-word;word-break:break-all"><a href="http://192.168.31.199:5000/detail?begintime=20170701&endtime=20190630&apiname=' +
                    self.url[i] + '">' + self.url[i] + '</a></td>')
                f1.write('<td align="center">' + self.cn_name[i] + '</td>')
                f1.write('<td align="center">' + str(self.res_time[i]) + 'ms</td>')
                # response code为200且status为1，code和status颜色为绿色
                if self.res_code[i] == 200 and self.res_status[i] == 1:
                    f1.write('<td align="center" bgcolor="#C1FFC1">' + str(200) + '</td>')
                    f1.write('<td align="center" bgcolor="#C1FFC1">' + str(1) + '</td>')
                    f1.write('<td></td>')
                    f1.write('<td align="left"><div style="width:' + str(
                        float(self.res_time[i]) / 5) + 'px;height:15px;background:darkblue;"></div></td>')
                    # response code为200且status为0，code颜色为绿色，status为红色，填入error message
                elif self.res_code[i] == 200 and self.res_status[i] == 0:
                    f1.write('<td align="center" bgcolor="#C1FFC1">' + str(200) + '</td>')
                    f1.write('<td align="center" bgcolor="red">' + str(0) + '</td>')
                    f1.write(
                        '<td style="word-break:keep-all;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;" align="center">' +
                        (json.loads(str(self.res[i].text)))['error']['message'] + '</td>')
                    f1.write('<td align="left"><div style="width:' + str(
                        float(self.res_time[i]) / 2) + 'px;height:15px;background:darkblue;"></div></td>')
                    # response code为500，颜色为紫色，填入Response code : 500, Sever Error
                elif self.res_code[i] == 500:
                    f1.write('<td align="center" bgcolor="purple">' + str(500) + '</td>')
                    f1.write('<td align="center" bgcolor="purple">''</td>')
                    f1.write(
                        '<td style="word-break:keep-all;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;" align="center">Response code : 500, Sever Error</td>')
                    f1.write('<td align="left"><div style="width:' + str(
                        float(self.res_time[i]) / 2) + 'px;height:15px;background:darkblue;"></div></td>')
                else:
                    f1.write('<td align="center" bgcolor="red">' + str(self.res_code[i]) + '</td>')
                    f1.write('<td align="center" bgcolor="red">''</td>')
                    f1.write(
                        '<td style="word-break:keep-all;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;" align="center">' +
                        self.res[i].text + '</td>')
                    f1.write('<td align="left"><div style="width:' + str(
                        float(self.res_time[i]) / 2) + 'px;height:15px;background:darkblue;"></div></td>')
                f1.write('</tr>')
            else:
                f1.write('<tr bgcolor="#D0D0D0">')
                f1.write('<td align="center">' + str(i + 1) + '</td>')
                f1.write(
                    '<td align="center" style="WORD-WRAP: break-word;word-break:break-all"><a href="http://192.168.31.199:5000/detail?begintime=20170701&endtime=20190630&apiname=' +
                    self.url[i] + '">' + self.url[i] + '</td>')
                f1.write('<td align="center">' + self.cn_name[i] + '</td>')
                f1.write('<td align="center">' + str(self.res_time[i]) + 'ms</td>')
                # response code为200且status为1，code和status颜色为绿色，error message N/A
                if self.res_code[i] == 200 and self.res_status[i] == 1:
                    f1.write('<td align="center" bgcolor="#C1FFC1">' + str(200) + '</td>')
                    f1.write('<td align="center" bgcolor="#C1FFC1">' + str(1) + '</td>')
                    f1.write('<td></td>')
                    f1.write('<td align="left"><div style="width:' + str(
                        float(self.res_time[i]) / 2) + 'px;height:15px;background:darkblue;"></div></td>')
                    # response code为200且status为0，code颜色为绿色，status为红色，填入error message
                elif self.res_code[i] == 200 and self.res_status[i] == 0:
                    f1.write('<td align="center" bgcolor="#C1FFC1">' + str(200) + '</td>')
                    f1.write('<td align="center" bgcolor="red">' + str(0) + '</td>')
                    f1.write(
                        '<td style="word-break:keep-all;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;" align="center">' +
                        (json.loads(str(self.res[i].text)))['error']['message'] + '</td>')
                    f1.write('<td align="left"><div style="width:' + str(
                        float(self.res_time[i]) / 2) + 'px;height:15px;background:darkblue;"></div></td>')
                    # response code为500，颜色为红色，填入Response code : 500, Sever Error
                elif self.res_code[i] == 500:
                    f1.write('<td align="center" bgcolor="purple">' + str(500) + '</td>')
                    f1.write('<td align="center" bgcolor="purple">''</td>')
                    f1.write(
                        '<td style="word-break:keep-all;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;" align="center">Response code : 500, Sever Error</td>')
                    f1.write('<td align="left"><div style="width:' + str(
                        float(self.res_time[i]) / 2) + 'px;height:15px;background:darkblue;"></div></td>')
                else:
                    f1.write('<td align="center" bgcolor="red">' + str(self.res_code[i]) + '</td>')
                    f1.write('<td align="center" bgcolor="red">''</td>')
                    f1.write(
                        '<td style="word-break:keep-all;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;" align="center">' +
                        self.res[i].text + '</td>')
                    f1.write('<td align="left"><div style="width:' + str(
                        float(self.res_time[i]) / 2) + 'px;height:15px;background:darkblue;"></div></td>')
                f1.write('</tr>')
        f1.write('</table>')
        f1.write('</body>')
        f1.write('</html>')
        f1.close()

    def create_csv(self):
        with open(self.path + r'\\temp.csv', 'wb') as csvfile:
            a = csv.writer(csvfile, dialect='excel')
            a.writerow(
                ['API_URL', 'API_ChineseName', 'Response_code', 'Response_time', 'Response_status', 'Error_Message'])
            for i in range(self.api_len):
                if self.res_code[i] == 200 and self.res_status[i] == 1:
                    a.writerow([str(self.url[i]), str(self.cn_name[i]).replace('\'', '#'), str(self.res_code[i]),
                                str(self.res_time[i]), str(self.res_status[i]), 'N/A'])
                elif self.res_code[i] == 200 and self.res_status[i] == 0:
                    a.writerow([str(self.url[i]), str(self.cn_name[i]).replace('\'', '#'), str(self.res_code[i]),
                                str(self.res_time[i]), str(self.res_status[i]),
                                str((json.loads(str(self.res[i].text)))['error']['message']).replace('\'', '#')])
                else:
                    a.writerow([str(self.url[i]), str(self.cn_name[i]).replace('\'', '#'), str(self.res_code[i]),
                                str(self.res_time[i]), str(self.res_status[i]), 'Please check the testreport'])
