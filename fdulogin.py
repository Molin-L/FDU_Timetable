# !/usr/bin/env python
# --------------------------------------------------------------
# File:          fdulogin.py
# Project:       FDU_Timetable
# Created:       Tuesday, 12th November 2019 9:32:46 pm
# @Author:       Molin Liu, MSc in Data Science
# Contact:          molin@live.cn
# Last Modified: Tuesday, 12th November 2019 9:32:51 pm
# Copyright  © Rockface 2019 - 2020     © Recallu 2019 - 2020
# --------------------------------------------------------------

'''
复旦大学统一身份认证登录
'''

import requests
import time
import datetime
import pytz
import os
import autologin
import pickle
import time
from bs4 import BeautifulSoup
# User's modules
from FDU_headers import HEADER_CAPTCHA, HEADER_LOGIN, HEADER_LT
from utils import parseCookie, saveHtml


class FDU_User():

    def __init__(self, fdu_id, fdu_pw):
        self.__session = requests.Session()
        self.__cookies = None
        self.__fdu_id = fdu_id
        self.__fdu_pw = fdu_pw
        self.__form_login = {}
        self.__gen_header = {}

        self._needCaptcha()
        self._get_lt()
        time.sleep(2)
        resp_login = self.login()
        saveHtml('Login', resp_login.text, resp_login.status_code)

    def _get_lt(self):
        '''
        Get lt verification code
        '''
        header = HEADER_LT
        response = self.__session.get(
            "http://uis.fudan.edu.cn/authserver/login?service=http%3A%2F%2Fjwfw.fudan.edu.cn%2Feams%2Flogin.action", headers=header)
        print(("Success " if response.status_code == 200 else "Fail"),
              "\tin fetching lt and cookies.")

        if response.status_code == 200:
            parsed_text = BeautifulSoup(response.text, 'lxml')
            self.__form_login['lt'] = (parsed_text.body.find(
                'input', attrs={'name': 'lt', 'type': 'hidden'}))['value']
            self.__form_login['_eventId'] = (parsed_text.body.find(
                'input', attrs={'name': '_eventId', 'type': 'hidden'}))['value']
            self.__form_login['execution'] = (parsed_text.body.find(
                'input', attrs={'name': 'execution', 'type': 'hidden'}))['value']
            self.__form_login['dllt'] = (parsed_text.body.find(
                'input', attrs={'name': 'dllt', 'type': 'hidden'}))['value']
            self.__form_login['_eventId'] = (parsed_text.body.find(
                'input', attrs={'name': '_eventId', 'type': 'hidden'}))['value']
            self.__cookies = response.cookies.get_dict()
            self.__cookies.update(
                {"route": "261c7137ce5a442a6edfb7812f5be6ad"})

        else:
            raise Exception(
                "Cannot connect to FDU Teaching Affair login page.")

    def login(self):
        '''
        Login to jwfw.fdu
        '''
        time.sleep(5)
        url = "http://uis.fudan.edu.cn/authserver/login?service=http%3A%2F%2Fjwfw.fudan.edu.cn%2Feams%2Flogin.action"
        form_data = {
            "username": self.__fdu_id,
            "password": self.__fdu_pw,
        }
        self.__form_login.update(form_data)
        print(self.__form_login)
        login_header = HEADER_LOGIN
        self._needCaptcha()
        response = self.__session.post(
            url, data=self.__form_login, headers=login_header, cookies=self.__cookies, timeout=40, allow_redirects=False)
        if response.status_code == 200:
            print(self.__cookies)
            print("Login Fails")
        if response.status_code == 302:  # First redirect
            print("Login Success")
            auth_cookies = response.cookies.get_dict()
            set_cookies = parseCookie(response.headers['Set-Cookie'])
            self.__cookies.update(auth_cookies)
            self.__cookies.update(set_cookies)
            resp_1 = self.login_redirect(response, 1)
            resp_2 = self.login_redirect(resp_1, 2)
            return resp_2

    def _needCaptcha(self):
        '''
        Generate time stamp for needcaptcha
        Auth will be expired 1 day 
        '''

        header = HEADER_LOGIN
        self.__gen_header = header
        pst_now_0 = datetime.datetime.now(pytz.timezone("Etc/GMT+0"))
        time_stamp = int(float(pst_now_0.strftime("%s.%f"))*1000)
        url = "http://uis.fudan.edu.cn/authserver/needCaptcha.html?username=%s&_=%s" % (
            self.__fdu_id, time_stamp)
        response = self.__session.get(url, headers=header)
        print(("Success " if response.status_code == 200 else "Fail"),
              "\tin needCaptcha check.")
        if response.status_code == 200:
            print("PASS")
        else:
            print("Fail")
        return response

    def login_redirect(self, response, index):
        '''
        Handle redirect
        '''
        print("Redirect to %s" % response.url)
        url = response.url
        header = HEADER_LOGIN
        resp = self.__session.get(
            url, headers=header, cookies=self.__cookies)
        print("Redirect_%d: %d" % (index, resp.status_code))
        set_cookies = parseCookie(resp.headers['Set-Cookie'])
        self.__cookies.update(set_cookies)
        saveHtml('Redirct_%d' % index, resp.text, resp.status_code)
        return resp

    def finish_login(self):
        return self.__session, self.__cookies

    def logout(self):
        url = "http://jwfw.fudan.edu.cn/eams/logout.action"
        header = {
            "Host": "uis.fudan.edu.cn",
            "Connection": "keep-alive",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
            "Referer": "http://uis.fudan.edu.cn/authserver/login?service=http%3A%2F%2Fjwfw.fudan.edu.cn%2Feams%2Flogin.action",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6"
        }
        response = self.__session.get(url, headers=header)
        print("Logout: %d" % response.status_code)
        return response


if __name__ == "__main__":
    user = FDU_User(autologin.id(), autologin.pw())
    resp_login = user.login()
    time.sleep(3.5)
    saveHtml('Login', resp_login.text, resp_login.status_code)
