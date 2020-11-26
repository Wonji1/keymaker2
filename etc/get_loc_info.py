# -*- coding: utf-8 -*-

import base64
import hashlib
import hmac
import time

import requests
import json

# ip 로 위치 정보 찾기
def get_loc_info(ip):
    # Signature 생성에 필요한 항목
    method = "GET"
    basestring = "/geolocation/v2/geoLocation?ip="+ip+"&ext=t&responseFormatType=json"
    timestamp = str(int(time.time() * 1000))
    access_key = "Rq6GcpUu78vcmh6Zk3s0"  # access key id (from portal or sub account)
    secret_key = "FYzYAtDvRE2tDfvgnuD8FyPgiUrcw1AK64tego55"  # secret key (from portal or sub account)
    signature = make_signature(method, basestring, timestamp, access_key, secret_key)

    # GET Request
    hostname = "https://geolocation.apigw.ntruss.com"
    requestUri = hostname + basestring

    return json.loads(requestApi(timestamp, access_key, signature, requestUri))

# 암호키 생성
def make_signature(method, basestring, timestamp, access_key, secret_key):
    message = method + " " + basestring + "\n" + timestamp + "\n" + access_key
    signature = base64.b64encode(hmac.new(secret_key.encode('utf-8'), message.encode('utf-8'), digestmod=hashlib.sha256).digest())

    return signature

# API 헤더 설정, 호출
def requestApi(timestamp, access_key, signature, uri):
    # Header for Request
    headers = {'x-ncp-apigw-timestamp': timestamp,
               'x-ncp-iam-access-key': access_key,
               'x-ncp-apigw-signature-v2': signature}

    # Geolocation API Request
    res = requests.get(uri, headers=headers)

    # Check Response
    #print('status : %d' % res.status_code)
    #print('content : %s' % res.content)

    return res.content