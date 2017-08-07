# -*- coding: utf-8 -*-
import json


class response_status:
    def __init__(self, length):
        self.length = length

    def res_status(self, response):
        respon_status = []
        for i in range(self.length):
            try:
                s = json.loads(str(response[i].text))
                respon_status.append(s['status'])
            except Exception:
                respon_status.append('-1')
        return respon_status
