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
from bs4 import BeautifulSoup


def fetchLoginPage(session):
    '''
    Get lt verification code
    '''
    header = {
        "Host": "uis.fudan.edu.cn",
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "DNT": "1",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
        "Referer": "http://jwfw.fudan.edu.cn/eams/home.action",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6",
        "Upgrade-Insecure-Requests": "1"
    }
    response = session.get(
        "http://uis.fudan.edu.cn/authserver/login?service=http%3A%2F%2Fjwfw.fudan.edu.cn%2Feams%2Flogin.action", headers=header)
    if response.status_code == 200:
        parsed_text = BeautifulSoup(response.text, 'lxml')
        dynamic_auth = (parsed_text.body.find(
            'input', attrs={'name': 'lt', 'type': 'hidden'}))['value']
        return dynamic_auth
    else:
        raise Exception("Cannot connect to FDU Teaching Affair login page.")


def login(username, password, lt, session):
    '''
    Login to jwfw.fdu
    '''
    form_data = {
        "username": username,
        "password": password,
        "dllt": "userNamePasswordLogin",
        "execution": "e1s1",
        "_eventId": "submit",
        "rmShown": "1",
        "lt": lt
    }
    return None


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

    try:

        da = fetchLoginPage(s)
    except Exception as e:
        print(e)
    #FDUID = input("Input your FDU id:\n")
    #FDUPW = input("Input your password:\n")
    #resp = needCaptcha(FDUID, s)
    # resp_login = login(username=FDUID, password=FDUPW, s)
    # print(resp)
