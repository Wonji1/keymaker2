
# -*- coding: utf-8 -*-
import os
import sys

from AUSYS.log import log
from config.config_set import db_data
from etc.set_send import set_send
from etc.set_log import set_log

import random
from sqlalchemy import create_engine

# 로그인한 사용자 접속 테이블에 저장
# user_id : 로그인한 사용자의 id
# user_ip : 로그인한 사용자의 ip
def access(user_id, user_ip):

    # 로그를 남기기 위한 값
    # user_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    # user_id = None
    # 파이썬의 logging 함수를 불러오는 함수
    logger = set_log()
    # 받아온 user_ip, user_id 를 로그에 추가
    logger_data = {'clientip': user_ip, 'user_id': user_id}

    logger.info("Request access", extra=logger_data)

    # DB 에 로그를 남기기 위해 입력값, 요청값, api, function 명 등을 정의
    input = {}
    input['user_id'] = user_id
    input['user_ip'] = user_ip
    log_request = "access"
    api = os.path.split(__file__)[1]
    function = sys._getframe().f_code.co_name

    # IP를 이용하여 사용자 key 설정
    # user_key : 접속해있는 사용자에 대한 일회용 아이디, 접속한 사용자의 ip 4자리 합 + 랜덤 4자리 수
    user_ip_list = user_ip.split('.')

    user_ip_start = 0
    for i in user_ip_list:
        user_ip_start += int(i)
    user_ip_start = str(user_ip_start).zfill(4)

    user_ip_end = random.randint(0, 9999)
    user_ip_end = str(user_ip_end).zfill(4)

    user_key = user_ip_start + user_ip_end
    logger.info("Set the user key", extra=logger_data)

    # 접속 테이블에 저장
    engine = create_engine(db_data)
    connection = engine.raw_connection()
    cursor = connection.cursor()

    data = []

    try:
        cursor.callproc('SP_KEYM_ADD_USR_ACCESS_INFO', [user_key, user_id, user_ip])
        logger.info("Store the information of the user who is connected", extra=logger_data)

        user_info = {}
        user_info['user_key'] = user_key
        data.append(user_info)

        # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
        user_id = None
        log_status = "REQUEST"
        output = data
        message = "access success"
        success_flag = "Y"

        # log : DB 에 로그를 저장하는 함수
        # log_db : DB 에 저장한 로그값
        log_db = log(user_id, log_status, log_request, api, function, input, output, message, success_flag)
        logger.info(message, extra=logger_data)
        logger.debug(log_db, extra=logger_data)

        result = "success"
        status = "200"

        # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
        send = set_send(data, result, status)
        logger.debug(send, extra=logger_data)

        return send

    except Exception as e:
        print("error type : ", type(e))
        print("error : ", e)

        # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
        user_id = None
        log_status = "EXCEPTION"
        output = ""
        message = "exception error"
        success_flag = "Y"

        # log : DB 에 로그를 저장하는 함수
        # log_db : DB 에 저장한 로그값
        log_db = log(user_id, log_status, log_request, api, function, input, output, message, success_flag)
        logger.error(message, extra=logger_data)
        logger.error(log_db, extra=logger_data)

        result = "fail"
        status = "400"

        # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
        send = set_send(data, result, status)
        logger.error(send, extra=logger_data)

        return send

    finally:
        connection.close()