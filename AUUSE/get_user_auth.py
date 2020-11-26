
# -*- coding: utf-8 -*-
import os
import sys

from flask import request

from AUSYS.log import log
from etc.set_log import set_log
from etc.set_send import set_send
from etc.check_text import check_text
from config.config_set import db_data

from sqlalchemy import create_engine

# 사용자가 가지는 모든 권한 반환
# 페이지 이동 시 사용자의 권한에 따라 메뉴 노출을 조정하기 위함
# user_key : API 를 호출하는 사용자의 키
def get_user_auth(user_key):

    # 로그를 남기기 위한 값
    # user_ip : API 를 호출한 사용자의 ip
    # user_id : API 를 호출한 사용자의 id
    user_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    user_id = None
    # 파이썬의 logging 함수를 불러오는 함수
    logger = set_log()
    # 받아온 user_ip, user_id 를 로그에 추가
    logger_data = {'clientip': user_ip, 'user_id': user_id}

    logger.info("Request add_user_info", extra=logger_data)

    # DB 에 로그를 남기기 위해 입력값, 요청값, api, function 명 등을 정의
    input = {}
    input['user_key'] = user_key
    log_request = "get_user_auth"
    api = os.path.split(__file__)[1]
    function = sys._getframe().f_code.co_name

    input_list = [user_key]

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
            status = "402"

            # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
            send = set_send(data, result, status)
            logger.error(send, extra=logger_data)

            return send

    engine = create_engine(db_data)
    connection = engine.raw_connection()
    cursor = connection.cursor()

    try:
        # 접속한 사용자의 모든 정보 반환
        cursor.callproc('SP_KEYM_GET_USR_ACCESS_INFO', [user_key])
        column_names_list = [x[0] for x in cursor.description]

        result_dicts = []

        for row in cursor.fetchall():
            result_dicts.append(dict(zip(column_names_list, row)))

        # 입력받은 user_key 에 해당하는 정보가 없는 경우
        if not result_dicts:
            # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
            user_id = None
            log_status = "ERROR"
            output = ""
            message = "User information does not exist"
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

        # 입력한 key 와 현재 사용자가 접속해 있는 IP 에 해당하는 key 와 일치하는지 확인
        for userinfo in result_dicts:
            # 추출한 사용자의 key 와 입력한 key 가 정확히 일치하지 않은 경우 = 존재하지 않는 경우
            if userinfo['PK_KMAUTN_ACCESSUSER'] != user_key:
                # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
                user_id = None
                log_status = "ERROR"
                output = ""
                message = "User information does not exist"
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

        userinfo = result_dicts[0]

        auth_list = userinfo['AUTH'].split(',')
        userinfo['AUTH'] = auth_list

        user_auth = {}
        user_auth['AUTH'] = userinfo['AUTH']

        result_dicts = []

        result_dicts.append(user_auth)

        data = []
        data.append(user_auth)

        # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
        user_id = None
        log_status = "REQUEST"
        output = data
        message = "get_user_auth success"
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

        data = []
        result = "fail"
        status = "401"

        # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
        send = set_send(data, result, status)
        logger.error(send, extra=logger_data)

        return send

    finally:
        connection.close()