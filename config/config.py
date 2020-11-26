
# -*- coding: utf-8 -*-

import time

# 디비 연결 시 필요 정보
database = {
    "host" : "15.164.70.209",
    "port" : "3306",
    "user" : "wonji",
    "passsword" : "aq124578",
    "db" : "keymaker",
    "charset" : "utf8",
    "autocommit" : "True"
}

# 첨부파일, 이미지 저장 경로
filedata_path = {
    "basic_path" : "/home/keona/keymaker/filedata",
    "module" : "/MODULE",
    "key" : "/KEY",
    "notice" : "/NOTICE",
    "current_date" : "/" + time.strftime('%Y%m%d', time.localtime(time.time())) + "/",
    "tmp" : "/tmp",
    "key_ori" : "ORI",
    "key_success" : "success",
    "key_fail" : "fail",
    "key_crop" : "/CROP",
    "key_draw" : "/DRAW"
}

# 인식키 발급 관련 정보
key_data = {
    "app_version" : "ver.ktool.0.7",
    "host" : "35.186.148.42",
    "port" : "12041"
}

# 입력할 수 없는 특수문자
special_char = ['#', '\\', '?', '/', '%']

import os
import sys

# 로그 정보
log_data = {
    "API" : os.path.split(__file__)[1],
    "function" : sys._getframe().f_code.co_name,
    "number_start" : 4,
    "max_size" : 5 * 1024 * 1024
}

# 위경도값 추출 실패시 사용할 임시 위경도값(회사 위경도)
location_data = {
    "country" : "KR",
    "code" : "1171052000",
    "r1" : "서울특별시",
    "r2" : "송파구",
    "r3" : "올림픽로",
    "lat" : "37.527937",
    "long" : "127.118431",
    "net" : "NexG Co., LTD"
}
