# coding:utf-8
import pymssql
import csv
import shutil
import os


class write_db:
    def __init__(self, dbname, host, username, password, t):
        self.dbname = dbname
        self.host = host
        self.username = username
        self.password = password
        self.t = t

    def write_db(self, length):
        try:  # 判定是否存在temp.csv，如没有，则抛出异常
            os.chdir('Test_results')
            if os.path.exists(r'temp.html'):
                os.remove('temp.html')
            if os.path.exists(r'temp.csv'):
                os.remove('temp.csv')
            os.chdir(os.path.dirname(os.getcwd()))
            shutil.move('temp.html', 'Test_results')
            shutil.move('temp.csv', 'Test_results')
            os.chdir('Test_results')
            os.rename('temp.csv', 'TestReport_' + self.t + '.csv')
            with open('TestReport_' + self.t + '.csv', 'rb') as csvfile:
                url = []
                cnname = []
                res_code = []
                res_tim = []
                res_status = []
                error_mes = []
                reader = csv.DictReader(csvfile)
                for row in reader:
                    url.append(row['API_URL'])
                    cnname.append(row['API_ChineseName'])
                    res_code.append(row['Response_code'])
                    res_tim.append(row['Response_time'])
                    res_status.append(row['Response_status'])
                    error_mes.append(row['Error_Message'])
            print u'连接数据库'
            conn = pymssql.connect(host=self.host, user=self.username, password=self.password, database=self.dbname)
            cur = conn.cursor()
            print u"开始写入数据库"
            for i in range(length):  # 循环写入数据库
                sql = 'insert into Nobel_Crawler_Test(TestNo, API_URL, API_ChineseName, Response_code, Response_time, ' \
                      'Response_status, Error_Message) values(' + self.t + ',\'' + url[i] + '\',\'' + cnname[
                          i] + '\',' + \
                      res_code[i] + ',\'' + res_tim[i] + '\',' + res_status[i] + ',\'' + error_mes[i] + '\')'
                cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
            print u"写入成功"
            return 1
        except Exception:
            print u"写入失败"
            return 0
