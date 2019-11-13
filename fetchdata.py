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
import os
import fdulogin
import autologin
from bs4 import BeautifulSoup

if __name__ == "__main__":
    s = requests.Session()

    try:
        da = fdulogin.fetchLoginPage(s)
        '''
        Login required
        '''
        # Uncomment the following line when you use this script.
        #FDUID = input("Input your FDU id:\n")
        #FDUPW = input("Input your password:\n")

        # Test Only
        FDUID = autologin.id()
        FDUPW = autologin.pw()
        # End TestOnly
        resp = fdulogin.needCaptcha(FDUID, s)
        if resp.status_code == 200:
            resp_login = fdulogin.login(
                username=FDUID, password=FDUPW, lt=da, session=s)
            print(resp_login)
            fdulogin.saveHtml(resp_login.text, resp_login.status_code)
            if resp_login.status_code == 302:
                print(resp_login.text)
    except Exception as e:
        print(e)

    #
    #
    # print(resp)
