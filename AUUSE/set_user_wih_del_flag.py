
# -*- coding: utf-8 -*-
import os
import sys

from flask import request

from AUSYS.log import log

from AUUSE.set_user_API_req import set_user_API_req
from etc.set_log import set_log

from etc.set_send import set_send
from etc.check_auth import check_auth
from etc.check_text import check_text
from config.config_set import db_data

from sqlalchemy import create_engine

# 사용자의 탈퇴(사용자 본인), 삭제(관리자) 정보 수정
# user_key : API 를 호출하는 사용자의 키
# log_request : 요청코드
# 요청코드가 탈퇴일 경우 LGUSE0011 입력
# 요청코드가 삭제일 경우 LGUSE0006 입력
def set_user_wih_del_flag(user_key, log_request):

    # 로그를 남기기 위한 값
    # user_ip : API 를 호출한 사용자의 ip
    # user_id : API 를 호출한 사용자의 id
    user_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    user_id = None
    # 파이썬의 logging 함수를 불러오는 함수
    logger = set_log()
    # 받아온 user_ip, user_id 를 로그에 추가
    logger_data = {'clientip': user_ip, 'user_id': user_id}

    logger.info("Request set_user_wih_del_flag", extra=logger_data)

    api = os.path.split(__file__)[1]
    function = sys._getframe().f_code.co_name

    # DB 에 로그를 남기기 위해 입력값, 요청값, api, function 명 등을 정의
    input = {}
    input['user_key'] = user_key
    input['log_request'] = log_request

    api = os.path.split(__file__)[1]
    function = sys._getframe().f_code.co_name

    # 사용자의 마지막 API 변경 함수
    set_user_API_req(user_key, "set_user_wih_del_flag")

    input_list = [user_key, log_request]

    # 입력값에서 디비 또는 API 파라미터에 입력할 수 없는 특수문자가 포함되어 있는 경우
    for input_data in input_list:
        status = check_text("input_db", input_data)
        if status == "400":
            # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
            user_id = None
            log_status = "ERROR"
            output = ""
            message = "Input data include special character"
            success_flag = "N"

            # log : DB 에 로그를 저장하는 함수
            # log_db : DB 에 저장한 로그값
            log_db = log(user_id, log_status, log_request, api, function, input, output, message, success_flag)
            logger.error(message, extra=logger_data)
            logger.error(log_db, extra=logger_data)

            data = []
            result = "fail"
            status = "403"

            # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
            send = set_send(data, result, status)
            logger.error(send, extra=logger_data)

            return send

    # 요청코드 종류 : 탈퇴, 사용자 삭제

    # 탈퇴 'LGUSE0011'
    if log_request == "LGUSE0011":
        request_type = "withdraw"
    # 사용자 정보 삭제 'LGUSE0006'
    elif log_request == "LGUSE0006":
        request_type = "del_user_info"
    # 위 패턴으로 요청한 기능 판단

    send = check_auth(user_key, request_type)

    data = []
    status = send['status']

    # 접속해 있는 사용자가 아닌 경우
    if status == "400":
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

        result = "fail"

        # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
        send = set_send(data, result, status)
        logger.error(send, extra=logger_data)

        return send

    # 필요한 권한이 존재하지 않는 경우
    elif status == "401":
        # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
        user_id = None
        log_status = "ERROR"
        output = ""
        message = "You don't have permission"
        success_flag = "N"

        # log : DB 에 로그를 저장하는 함수
        # log_db : DB 에 저장한 로그값
        log_db = log(user_id, log_status, log_request, api, function, input, output, message, success_flag)
        logger.error(message, extra=logger_data)
        logger.error(log_db, extra=logger_data)

        result = "fail"

        # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
        send = set_send(data, result, status)
        logger.error(send, extra=logger_data)

        return send

    # 필요한 권한이 존재하는 경우
    elif status == "200":
        # API 를 호출한 사용자의 ID
        user_id = send['data'][0]['result_data_1']

        withdraw_flag = 'N'
        delete_flag = 'N'

        if request_type == "withdraw":
            withdraw_flag = 'Y'

        elif request_type == "del_user_info":
            delete_flag = 'Y'

        engine = create_engine(db_data)
        connection = engine.raw_connection()
        cursor = connection.cursor()

        try:
            cursor.callproc('SP_KEYM_SET_USR_WIH_DEL_FLAG', [user_id, withdraw_flag, delete_flag])

            # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
            user_id = None
            log_status = "REQUEST"
            output = data
            message = "set_user_wih_del_flag success"
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
            status = "402"

            # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
            send = set_send(data, result, status)
            logger.error(send, extra=logger_data)

            return send

        finally:
            connection.close()