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

import request
import time
import datetime
import pytz


def Login(username, password):
    pass


def needCaptcha(fduid):
    # Generate time stamp for needcaptcha
    pst_now_0 = datetime.datetime.now(pytz.timezone("Etc/GMT+0"))
    time_stamp = int(float(pst_now_0.strftime("%s.%f"))*1000)
    url = "http://uis.fudan.edu.cn/authserver/needCaptcha.html?username=%s&_=%s" % (
        fduid, time_stamp)
