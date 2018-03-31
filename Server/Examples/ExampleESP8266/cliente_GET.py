#!/usr/bin/env python
"""Para probar example 5 server de esp8266 arduino"""

import urllib2
import urllib

# response = urllib2.urlopen('http://127.1.1.1:80/params?params1=Jorge')
# print response.info()
# html = response.read()
# print html
# response.close()

params = {'nm': '111'}
print("start")
for i in range(1, 10):
    req = urllib2.Request("http://192.168.1.104:80/Server"+'?'+'nm=Jose&nm2=ANA')
    res = urllib2.urlopen(req)
    data = res.read()
    print(data)
print("end")
res.close()