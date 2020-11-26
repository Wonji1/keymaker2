
# -*- coding: utf-8 -*-

import logging
import os
import time

from config.config import log_data
from etc.createFolder import createFolder

# 로그를 저장할 파일을 선택
# 로그 파일 형식 : log_파일넘버.log
def select_file():

    number_start = log_data['number_start']
    max_size = log_data['max_size']

    # 날짜별로 폴더 생성
    # file_path = "./flask_log/" + time.strftime('%Y%m%d', time.localtime(time.time()))
    file_path = '/home/keona/keymaker/flask_log/' + time.strftime('%Y%m%d', time.localtime(time.time()))
    createFolder(file_path)

    file_list = os.listdir(file_path)

    # 폴더에 파일이 존재하지 않을 경우
    if not file_list:

        file_name = "log_1.log"
        file_name = file_path + "/" + file_name

        return file_name

    # 오늘 날짜 폴더에 저장되어 있는 로그 파일 목록
    log_file_list = []

    for file in file_list:
        if file.endswith(".log"):
            file = file.split(".")[0]
            log_file_list.append(file)

    # 폴더에 로그 파일이 존재하지 않을 경우
    if not log_file_list:

        file_name = "log_1.log"
        file_name = file_path + "/" + file_name

        return file_name

    last_log_file = log_file_list[0]

    # 가장 최신 로그 파일 가져오기
    for file in log_file_list:

        if file[number_start] > last_log_file[number_start]:
            last_log_file = file

    # 가장 최신 파일의 크기가 5MB 이상일 경우
    if os.path.getsize(file_path + "/" + last_log_file + ".log") > max_size:
        log_count = int(last_log_file[number_start:]) + 1
        file_name = "log_" + str(log_count) + ".log"

    else:
        file_name = last_log_file + ".log"

    file_name = file_path + "/" + file_name

    return file_name

# cmd 창과 파일에 남기는 로그 함수
# 파이썬의 logging 모듈 사용
def set_log():

    logger = logging.getLogger(__name__)

    # 로그를 저장할 파일 설정
    file_name = select_file()

    # 파일 및 cmd 창에 남는 로그의 형태
    # [현재 시간][사용자 ip][사용자 id][레벨|파이썬 파일 이름:함수 이름:라인넘버]메시지
    # 레벨 : debug, info, warning, error, critical
    formatter = logging.Formatter('[%(asctime)s][%(clientip)s][%(user_id)s][%(levelname)s|%(filename)s:%(funcName)s:%(lineno)s]%(message)s')

    #stream_handler = logging.StreamHandler()
    #file_handler = logging.FileHandler(file_name)

    #stream_handler.setFormatter(formatter)
    #file_handler.setFormatter(formatter)

    #logger.addHandler(stream_handler)
    #logger.addHandler(file_handler)

    logger.setLevel(level=logging.DEBUG)

    return logger
