#!/usr/bin/env python

import urllib2
import urllib

# response = urllib2.urlopen('http://127.1.1.1:80/params?params1=Jorge')
# print response.info()
# html = response.read()
# print html
# response.close()

params = {'nm': '111'}

for i in range(1, 10):
    req = urllib2.Request("http://127.1.1.1:80/login", urllib.urlencode(params))
    res = urllib2.urlopen(req)
    data = res.read()
    print(data)
