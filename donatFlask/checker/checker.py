#!/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import utils

from random import randrange, shuffle, choice
from time import time
from sys import argv, stderr
from socket import error as network_error

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from time import time
import sys

__author__ = 'm_messiah, crassirostris, LSD'

OK, CORRUPT, MUMBLE, DOWN, INTERNAL_ERROR = 101, 102, 103, 104, 110

# CHANGE THIS BEFORE DEPLOY
SERVICE_PORT = ":31415"

PAGE_CREDIT = "/donation/credits/"
PAGE_HISTORY = "/donation/credits/history"
PAGE_KARMA = "/donation/karma/"

def close(code, public="", private=""):
    if public:
        print(public)
    if private:
        print(private, file=stderr)
    sys.exit(code)

def check(*args):
    addr = args[0]
    try:
        r = requests.get('http://'+addr+SERVICE_PORT+PAGE_CREDIT)
        if r.status_code != 200:
            close(DOWN, "Can't open donat page", "1/3 fail")

        r = requests.get('http://'+addr+SERVICE_PORT+PAGE_HISTORY)
        if r.status_code != 200:
            close(DOWN, "Can't open history page", "2/3 fail")

        r = requests.get('http://'+addr+SERVICE_PORT+PAGE_KARMA)
        if r.status_code != 200:
            close(DOWN, "Can't open karma page", "3/3 fail")
        close(OK)
    except requests.exceptions.RequestException as e:
        close(DOWN, "Donat service is unavailable", "Requests error: %s" %e)
    except Exception as e:
        close(INTERNAL_ERROR, "Unknown error", "check command COMMON exception: %s" % e)

def put(*args):
    addr = args[0]
    flag = args[2]

    try:
        with requests.Session() as s:
            URL = "http://"+addr+SERVICE_PORT+PAGE_CREDIT

            a = s.get(URL)
            csrf = ""

            soup = BeautifulSoup(a.text, "lxml")
            csrf = soup.find('input', {'id': 'csrf_token'}).get('value')

            data = {'csrf_token':csrf,
            'name':utils.getFullName(),
            'number':utils.getNum(),
            'expired':utils.getMY(),
            'ccv':str(choice(range(999))),
            'value':str(choice(range(1000))),
            'email':"",
            'comment':flag}

            #print(data)

            a = s.post(URL, data=data, allow_redirects=True)
            if a.status_code == 200 :
                checker_id = ""
                soup = BeautifulSoup(a.text, "lxml")
                for link in soup.find_all('a', href=True):
                    if "info?id=" in link.get('href'):
                        checker_id = link.get('href')
                close(OK, public=checker_id)
            else:
                close(MUMBLE, "Can't donat money", "There was error in donating process")
    except requests.exceptions.RequestException as e:
        close(MUMBLE, "Donat service unavailable", "Requests error: %s" %e)
    except Exception as e:
        close(INTERNAL_ERROR, "Unknown error", "put command COMMON exception: %s" % e)

def get(*args):
    addr = args[0]
    checker_flag_id = args[1]
    best_flag = args[2]

    try:
        with requests.Session() as s:
            URL = "http://"+addr+SERVICE_PORT+checker_flag_id

            a = s.get(URL)
            if a.status_code == 200:
                soup = BeautifulSoup(a.text, "lxml")
                for el in soup.find_all('td'):
                    if best_flag == el.text:
                        close(OK)
            close(CORRUPT, "Can't get one of the flags", "can't get flag %s with id %s" % (best_flag, checker_flag_id))
    except requests.exceptions.RequestException as e:
        close(MUMBLE, "Donat service unavailable", "Requests error: %s" %e)
    except Exception as e:
        close(INTERNAL_ERROR, "Unknown error", "get command COMMON exception: %s" % e)

def info(*args):
    close(OK, "vulns: 1")

COMMANDS = {'check': check, 'put': put, 'get': get, 'info': info}

def not_found(*args):
    print("Unsupported command %s" % argv[1], file=stderr)
    return INTERNAL_ERROR

if __name__ == '__main__':
    try:
        COMMANDS.get(argv[1], not_found)(*argv[2:])
    except Exception as e:
        close(INTERNAL_ERROR, "Checker problem, plz contact LSD", "INTERNAL ERROR: %s" % e)
