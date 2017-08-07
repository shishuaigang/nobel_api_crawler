# -*- coding: utf-8 -*-
class response_status:
    def __init__(self, length):
        self.length = length

    def res_status(self, response):
        respon_status = []
        for i in range(self.length):
            if '"status":1' in response[i].text:
                respon_status.append(1)
            elif '"status":0' in response[i].text:
                respon_status.append(0)
            else:
                respon_status.append(-1)  # 如果返回code是500，就没有status这个值返回，程序会出错，所以使用-1
        return respon_status
