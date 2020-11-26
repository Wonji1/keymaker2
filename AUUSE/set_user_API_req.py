
# -*- coding: utf-8 -*-

import os
import sys

from flask import request
from sqlalchemy import create_engine

from AUSYS.log import log

from AUUSE.get_user_info_from_key import get_user_info_from_key

from config.config_set import db_data
from etc.set_log import set_log
from etc.set_send import set_send

# 접속한 사용자가 새로운 API 를 호출했을 때 접속 테이블에 마지막 API 호출 시간을 표시하기 위한 함수
# user_key : 다른 API 를 요청한 사용자의 key
# log_request : 사용자가 실제로 요청한 API 이름
def set_user_API_req(user_key, log_request):

    # 로그를 남기기 위한 값
    # user_ip : API 를 호출한 사용자의 ip
    # user_id : API 를 호출한 사용자의 id
    user_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    user_id = None
    # 파이썬의 logging 함수를 불러오는 함수
    logger = set_log()
    # 받아온 user_ip, user_id 를 로그에 추가
    logger_data = {'clientip': user_ip, 'user_id': user_id}

    logger.info("Request set_user_API_req", extra=logger_data)

    # DB 에 로그를 남기기 위해 입력값, 요청값, api, function 명 등을 정의
    input = {}
    input['user_key'] = user_key
    input['log_request'] = log_request

    # log_request = "set_user_API_req"
    api = os.path.split(__file__)[1]
    function = sys._getframe().f_code.co_name

    # 입력받은 사용자 키를 이용하여 사용자의 정보 조회
    send = get_user_info_from_key(user_key)

    # 접속해있는 사용자가 아닐 경우
    if send['status'] == "201":
        # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
        user_id = None
        log_status = "ERROR"
        output = ""
        message = "User need login"
        success_flag = "N"

        # log : DB 에 로그를 저장하는 함수
        # log_db : DB 에 저장한 로그값
        log_db = log(user_id, log_status, log_request, api, function, input, output, message, success_flag)
        logger.error(message, extra=logger_data)
        logger.error(log_db, extra=logger_data)

        data = []
        result = "fail"
        status = "400"

        # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
        send = set_send(data, result, status)
        logger.error(send, extra=logger_data)

        return send

    # 접속 여부 확인 도중 DB 에러가 난 경우
    elif send['status'] == "400":
        # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
        user_id = None
        log_status = "EXCEPTION"
        output = ""
        message = send['data'][0]['error']
        success_flag = "N"

        # log : DB 에 로그를 저장하는 함수
        # log_db : DB 에 저장한 로그값
        log_db = log(user_id, log_status, log_request, api, function, input, output, message, success_flag)
        logger.error(message, extra=logger_data)
        logger.error(log_db, extra=logger_data)

        data = []
        result = "fail"
        status = "401"

        # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
        send = set_send(data, result, status)
        logger.error(send, extra=logger_data)

        return send

    # 현재 접속 중인 사용자일 경우
    elif send['status'] == "200":
        engine = create_engine(db_data)
        connection = engine.raw_connection()
        cursor = connection.cursor()

        try:
            # 접속한 사용자의 마지막 API 호출시간 수정
            cursor.callproc('SP_KEYM_SET_USR_ACCESS_INFO', [user_key])

            # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
            user_id = send['data'][0]['result_data_1']
            log_status = "REQUEST"
            output = None
            message = None
            success_flag = "Y"

            # log : DB 에 로그를 저장하는 함수
            # log_db : DB 에 저장한 로그값
            log_db = log(user_id, log_status, log_request, api, function, input, output, message, success_flag)
            logger.info(message, extra=logger_data)
            logger.debug(log_db, extra=logger_data)

            data = []
            result = "success"
            status = "200"

            # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
            send = set_send(data, result, status)
            logger.debug(send, extra=logger_data)

            return send

        except Exception as e:
            print("error type : ", type(e))
            print("error : ", e)

            data = []

            # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
            user_id = ""
            log_status = "EXCEPTION"
            output = ""
            message = e
            success_flag = "N"

            # log : DB 에 로그를 저장하는 함수
            # log_db : DB 에 저장한 로그값
            log_db = log(user_id, log_status, log_request, api, function, input, output, message, success_flag)
            logger.error(message, extra=logger_data)
            logger.error(log_db, extra=logger_data)

            status = '402'
            result = "fail"

            # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
            send = set_send(data, result, status)
            logger.error(send, extra=logger_data)

            return send

        finally:
            connection.close()
