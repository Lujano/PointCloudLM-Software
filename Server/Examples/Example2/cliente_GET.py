#!/usr/bin/env python

import urllib2
import urllib

# response = urllib2.urlopen('http://127.1.1.1:80/params?params1=Jorge')
# print response.info()
# html = response.read()
# print html
# response.close()

params = {'nm': '111'}
print("start")
for i in range(1, 100):
    req = urllib2.Request("http://127.1.1.1:80/login"+'?'+)
    res = urllib2.urlopen(req)
    data = res.read()
print("end")
res.close()