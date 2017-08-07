# -*- coding: utf-8 -*-
class passrate:
    def __init__(self, length):
        self.length = length

    def pass_rate(self, status, response_code):
        success_api = 0
        fail_api = 0
        for i in range(self.length):
            if response_code[i] == 200 and status[i] == 1:
                success_api += 1
            else:
                fail_api += 1
        return [success_api, fail_api, '%.2f%%' % ((float(success_api) / self.length) * 100)]
