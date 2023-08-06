#!/usr/bin/python
# coding:utf-8
import hashlib
import sys
PY2 = sys.version_info[0] == 2
if PY2:
    from urlparse import urlsplit, parse_qsl
    from urllib import urlencode, unquote
else:
    from urllib.parse import urlparse as urlsplit
    from urllib.parse import urlparse, parse_qsl, urlencode, unquote


# urldata = 'http://api.xvideo.weibo.com/v1/status/timeline/user?mw-appkey=100028&mw-ttid=nmmain@mgj_pc_1.0&mw-t
# =1572403666864&mw-uuid=fa0dbe28-126c-4bfd-b6d4-f1f01f7a8e65&mw-h5-os=unknown&mw-sign
# =90aa90fbefffab1f4604bc294a29406f'

# SplitResult(scheme='http', netloc='api.xvideo.weibo.com', path='/v1/status/timeline/user',
# query='mw-appkey=100028&mw-ttid=nmmain%40mgj_pc_1.0&mw-t=1572403666864&mw-uuid=fa0dbe28-126c-4bfd-b6d4-f1f01f7a8e65
# &mw-h5-os=unknown&mw-sign=90aa90fbefffab1f4604bc294a29406f', fragment='')
def getUrlQuery(urldata):
    return urlsplit(urldata).query


# mw-appkey=100028&mw-h5-os=unknown&mw-sign=90aa90fbefffab1f4604bc294a29406f&mw-t=1572403666864&mw-ttid=nmmain@mgj_pc_1.0&mw-uuid=fa0dbe28-126c-4bfd-b6d4-f1f01f7a8e65
def sortUrlParam(urldata):
    result = dict(parse_qsl(getUrlQuery(urldata)))
    rtns = sorted(result.items(), key=lambda d: d[0])
    urldata = urlencode(rtns)
    return unquote(urldata)


if __name__ == '__main__':
    urldata = 'http://api.xvideo.weibo.com/v1/status/timeline/user?mw-appkey=100028&mw-ttid=nmmain@mgj_pc_1.0&mw-t' \
              '=1572403666864&mw-uuid=fa0dbe28-126c-4bfd-b6d4-f1f01f7a8e65&mw-h5-os=unknown&mw-sign' \
              '=90aa90fbefffab1f4604bc294a29406f '
    print(sortUrlParam(urldata))
