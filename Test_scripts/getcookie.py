# coding:utf-8
import cookielib
import urllib
import urllib2


def gecookie(api_ver):
    c = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(c))
    url = 'http://192.168.31.99:7385/API/Account/Login'
    data = {
        "APIVersion": api_ver,
        "phonenumber": "18121225109",
        "password": "123456",
        "rememberme": "True"
    }
    post_info = urllib.urlencode(data)
    request = urllib2.Request(url, post_info)
    html = opener.open(request).read()
    return c
