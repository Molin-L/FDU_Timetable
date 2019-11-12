# !/usr/bin/env python
# --------------------------------------------------------------
# File:          fetchdata.py
# Project:       FDU_Timetable
# Created:       Tuesday, 12th November 2019 2:36:48 pm
# @Author:       Molin Liu, MSc in Data Science
# Contact:          molin@live.cn
# Last Modified: Tuesday, 12th November 2019 2:36:58 pm
# Copyright  © Rockface 2019 - 2020
# --------------------------------------------------------------

import requests
import time
import datetime
import pytz


def Login(username, password):
    pass


def needCaptcha(fduid, session):
    '''
    Generate time stamp for needcaptcha
    Auth will be expired 1 day 
    '''

    header = {
        "Host": "uis.fudan.edu.cn",
        "Connection": "keep-alive",
        "Accept": "text/plain, */*; q=0.01",
        "DNT": "1",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
        "Referer": "http://uis.fudan.edu.cn/authserver/login?service=http%3A%2F%2Fjwfw.fudan.edu.cn%2Feams%2Flogin.action",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6"
    }
    pst_now_0 = datetime.datetime.now(pytz.timezone("Etc/GMT+0"))
    time_stamp = int(float(pst_now_0.strftime("%s.%f"))*1000)
    url = "http://uis.fudan.edu.cn/authserver/needCaptcha.html?username=%s&_=%s" % (
        fduid, time_stamp)
    response = session.get(url, headers=header)
    return response


if __name__ == "__main__":
    s = requests.Session()
    resp = needCaptcha("15301020060", s)
    print(resp)
