#!/usr/bin/python
# coding=utf-8
"""
获取代理ip 来源以下两个网址
http://cn-proxy.com/
https://www.xicidaili.com/
"""

from bs4 import BeautifulSoup
import requests, sys, random, time, string

sys.path.append('/Users/momo/PycharmProjects/bbs-fetch/lib')
import mredis.weedredis as msredis

PY2 = sys.version_info[0] == 2
if PY2:
    from Cookie import SimpleCookie
else:
    from http.cookies import SimpleCookie


class IpProxy:
    def __init__(self):
        self.siteRedis = msredis.weedRedis()
        self.siteRedis.Redis(conn_str_tpl='127.0.0.1:6379')
        self.url = 'https://www.xicidaili.com/nt/2'
        self.ipKey = 'ip_{0}_list'

    def fetchIpList(self):
        raw_cookie = '_free_proxy_session={0}3Npb25faWQGOgZFVEkiJWY5ODkyMjcwNmFhOWE4ZWNiMGZj' \
                     'ZGZiNGRkZDM1MWNmBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMWt2NWpZUlFrdGtWeEN5Y1p' \
                     'VUWJjdjlEamVuME1kandDd1lNcjJUS{1}%3D%3D--c8817e140fd32cdffb40db21568781a5ad9d1d0e;' \
                     ' Hm_lvt_0cf76c77469e965d2957f0553e6ecf59={2}; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59={3}'
        salt = ''.join(random.sample(string.ascii_letters + string.digits, 13))
        salt1 = ''.join(random.sample(string.ascii_letters + string.digits, 13))
        t = time.time()
        raw_cookie = raw_cookie.format(salt, salt1, t, t)
        cookie = SimpleCookie(raw_cookie)
        cookies = dict([(c, cookie[c].value) for c in cookie])
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/61.0.3163.100 Safari/537.36'}
        ipproxy = self.__getLocalIpProxy('https')
        if ipproxy == '':
            response = requests.get(self.url, cookies=cookies, headers=headers, timeout=(5, 10))
        else:
            response = requests.get(self.url, cookies=cookies, headers=headers, proxies=ipproxy, timeout=(5, 10))
        soup = BeautifulSoup(response.text, "html.parser")
        tables = soup.find_all('table', id='ip_list')
        index = 0
        for table in tables:
            trs = table.find_all('tr')
            for tr in trs[2:]:
                tds = tr.find_all('td')
                if len(tds) == 0:
                    continue
                ip = tds[1].text.strip()
                port = tds[2].text.strip()
                httpType = tds[5].text.strip().lower()
                if PY2:
                    speed = tds[6].find('div', class_='bar')['title'].encode('UTF-8')
                else:
                    speed = tds[6].find('div', class_='bar')['title']
                if speed.find('秒') != -1:
                    speed = float(speed.strip().replace('秒', ''))
                    if speed < 0.5:
                        ipInfo = '{0}:{1}'.format(ip, port)
                        self.__saveToredis(httpType, ipInfo)
        self.siteRedis.expire(self.ipKey.format('http'), 600)
        self.siteRedis.expire(self.ipKey.format('https'), 600)

    def getIPList(self):
        url = 'http://cn-proxy.com'
        raw_cookie = 'UM_distinctid=15f57fdae0e50b-0c61cf0213e044-31657c00-13c680-15f57fdae0f5dc; CNZZDATA5540483=cnzz_eid%3D313329075-1509008980-%26ntime%3D1509436445'
        cookie = SimpleCookie(raw_cookie)
        cookies = dict([(c, cookie[c].value) for c in cookie])
        headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        proxy = self.__getLocalIpProxy('https')
        try:
            if proxy:
                response = requests.get(url, cookies=cookies, headers=headers, proxies=proxy)
            else:
                response = requests.get(url, cookies=cookies, headers=headers)
        except requests.exceptions.InvalidProxyURL:
            print('getIPList 代理获取失败')
            return ''
        except requests.exceptions.TooManyRedirects:
            print('getIPList ip被封')
            return ''
        except requests.RequestException as e:
            print('getIPList 请求失败')
            return ''
        soup = BeautifulSoup(response.text, "html.parser")
        tables = soup.find_all('table', class_='sortable')
        for table in tables:
            trs = table.find_all('tbody')[0].find_all('tr')
            for tr in trs[1:]:
                tds = tr.find_all('td')
                speeds = tds[3].strong['style']
                speed = speeds.split(' ')[1]
                speed = int(speed.replace('%;', ''))
                if speed > 50:
                    ip = tds[0].text.strip()
                    port = tds[1].text.strip()
                    ipInfo = '{0}:{1}'.format(ip, port)
                    self.__saveToredis('http', ipInfo)
                    self.__saveToredis('https', ipInfo)
        self.siteRedis.expire(self.ipKey.format('http'), 600)
        self.siteRedis.expire(self.ipKey.format('https'), 600)

    def __saveToredis(self, httpType, ip):
        key = self.ipKey.format(httpType)
        self.siteRedis.sadd(key, ip)

    def __getLocalIpProxy(self, httpType):
        key = self.ipKey.format(httpType)
        ipRand = self.siteRedis.srandmember(key)
        if len(ipRand) == 0:
            return ''
        if PY2:
            ipPort = ipRand[0]
        else:
            ipPort = ipRand[0].decode('utf-8')
        return ipPort

    def getIpProxy(self, httpType, ipOnly=False):
        ipPort = self.__getLocalIpProxy(httpType)
        if ipPort == '':
            # self.fetchIpList()
            self.getIPList()
            ipPort = self.__getLocalIpProxy(httpType)
        if ipOnly:
            return ipPort
        else:
            proxyIp = {httpType: httpType + "://" + ipPort}
            return proxyIp

    def delBadIp(self, httpType, ip):
        key = self.ipKey.format(httpType)
        self.siteRedis.srem(key, ip)

# if __name__ == '__main__':
#     proxy = IpProxy()
#     proxyIp1 = proxy.getIpProxy('https', True)
#     print(proxyIp1)
