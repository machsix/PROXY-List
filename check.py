#!/usr/bin/env python3
import requests
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
import urllib.parse

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
DEFAULT_HEADER = {
    'authority': 'www.jpxgmn.net',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/538.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/538.36 Edg/92.0.902.67',
    'accept': 'image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
}


def test_proxy(p, testLink, testKeyword, timeout=20):
    try:
        s = requests.Session()
        s.headers.update(DEFAULT_HEADER)
        s.proxies.update({
            'http': p,
            'https': p
        })
        r = s.get(testLink, timeout=timeout, verify=False)
        r.encoding = 'utf-8'
        time_cost = r.elapsed.total_seconds()
        if r.status_code != 200 or testKeyword not in r.text:
            return -1
        return time_cost
    except:
        return -1


if (__name__ == '__main__'):
    proxy = set()
    with open('http.txt', 'r') as f:
        data = f.read().split()

    for i in data:
        proxy.add(f'http://{i}')

    testLink = os.environ['LINK']
    testKeyword = urllib.parse.unquote_plus(os.environ['KEYWORD'])
    proxyPass = []
    proxyPassTime = []
    proxyFail = []
    ntest = 20
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(test_proxy, p, testLink, testKeyword, timeout=15): p for p in proxy}
        for f in as_completed(futures):
            p = futures[f]
            if f.result() > 0:
                print(f'Test: {p}   Success, Time cost {f.result()}s')
                proxyPass.append(p)
                proxyPassTime.append(f.result())
            else:
                #  print(f'Test: {p}   Fail')
                proxyFail.append(p)

    index = sorted(range(len(proxyPassTime)), key=lambda k: proxyPassTime[k])
    proxyPass = [proxyPass[i] for i in index]
    with open('proxy.yaml', 'w') as f:
        json.dump(proxyPass, f, indent=2)
