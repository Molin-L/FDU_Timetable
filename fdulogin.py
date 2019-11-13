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

    def _get_lt(self):
        '''
        Get lt verification code
        '''
        header = {
            "Host": "uis.fudan.edu.cn",
            "Connection": "keep-alive",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
            "Referer": "http://jwfw.fudan.edu.cn/eams/home.action",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6",
            "Upgrade-Insecure-Requests": "1"
        }
        response = self.__session.get(
            "http://uis.fudan.edu.cn/authserver/login?service=http%3A%2F%2Fjwfw.fudan.edu.cn%2Feams%2Flogin.action", headers=header)
        print("Get lt:\t%d" % response.status_code)
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
        login_header = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
        }
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
            self.login_redirect(resp_1, 2)
        return response

    def _needCaptcha(self):
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
        self.__gen_header = header
        pst_now_0 = datetime.datetime.now(pytz.timezone("Etc/GMT+0"))
        time_stamp = int(float(pst_now_0.strftime("%s.%f"))*1000)
        url = "http://uis.fudan.edu.cn/authserver/needCaptcha.html?username=%s&_=%s" % (
            self.__fdu_id, time_stamp)
        response = self.__session.get(url, headers=header)
        print("Need captcha check status:\t%d" % response.status_code)
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
        header = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
        }
        resp = self.__session.get(
            url, headers=header, cookies=self.__cookies)
        print("Redirect_%d: %d" % (index, resp.status_code))
        set_cookies = parseCookie(resp.headers['Set-Cookie'])
        self.__cookies.update(set_cookies)
        saveHtml('Redirct_%d' % index, resp.text, resp.status_code)
        return resp

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


def parseCookie(value):
    result = {}
    for item in value.split(';'):
        item = item.strip()
        if not item:
            continue
        if '=' not in item:
            result[item] = None
            continue
        name, value = item.split('=', 1)
        result[name] = value
    return result


def saveHtml(title, text, code):
    i = 0
    filename = 'Test_%s_0_%d.html' % (title, code)
    while(os.path.exists(filename)):
        i += 1
        filename = 'Test_%s_%d_%d.html' % (title, i, code)
    with open(filename, 'w') as file:
        file.write(text)
        file.close()


if __name__ == "__main__":
    user = FDU_User(autologin.id(), autologin.pw())
    resp_login = user.login()
    saveHtml('Login', resp_login.text, resp_login.status_code)

    time.sleep(5)
    #resp_logout = user.logout()
    #saveHtml('Logout', resp_logout.text, resp_logout.status_code)
