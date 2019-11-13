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
import re
from fdulogin import FDU_User
import autologin
from bs4 import BeautifulSoup
from FDU_headers import HEADER_CAPTCHA, HEADER_LOGIN, HEADER_LT
from utils import parseCookie, saveHtml


class TableManager():

    def __init__(self, session, cookies):
        self.__session = session
        self.__cookies = cookies
        self._fetchTablePage()
        self.__query_form = {}

    def _fetchTablePage(self):
        header = HEADER_LOGIN
        get_url = "http://jwfw.fudan.edu.cn/eams/courseTableForStd.action"

        resp = self.__session.get(
            get_url, headers=header, cookies=self.__cookies)
        self._set_cookies(resp)
        print(resp)
        self._get_ids(resp)
        saveHtml("Table", resp.text, resp.status_code)

    def _set_cookies(self, resp):
        has_cookies = resp.cookies.get_dict()
        self.__cookies.update(has_cookies)
        set_cookies = parseCookie(resp.headers['Set-Cookie'])
        print(has_cookies)
        print(set_cookies)
        self.__cookies.update(set_cookies)

    def _get_ids(self, resp):
        parsed_text = BeautifulSoup(resp.text, 'lxml')
        ids = parsed_text.find_all('script')
        ids = re.search(r'"ids","[0-9]*"', str(ids)).group(0)
        ids = re.sub('"', '', ids).split(',')
        self.__query_form['ids'] = ids[1]


if __name__ == "__main__":
    user = FDU_User(autologin.id(), autologin.pw())
    session, cookies = user.finish_login()

    tm = TableManager(session, cookies)
