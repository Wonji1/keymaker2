
# -*- coding: utf-8 -*-

import os
import sys

from flask import request
from sqlalchemy import create_engine

from etc.set_log import set_log
from etc.set_send import set_send

from AUSYS.log import log

from AUUSE.set_user_API_req import set_user_API_req
from AUUSE.get_user_info_from_key import get_user_info_from_key
from AUUSE.get_user_info import get_user_info

from config.config_set import db_data
from etc.check_text import check_text

# 인식키의 상세 정보를 출력하는 함수
# user_key : API 를 호출하는 사용자의 키
# index : 상세정보를 조회할 인식키 인덱스
def get_key_info(user_key, index):

    # 로그를 남기기 위한 값
    # user_ip : API 를 호출한 사용자의 ip
    # user_id : API 를 호출한 사용자의 id
    user_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    user_id = None
    # 파이썬의 logging 함수를 불러오는 함수
    logger = set_log()
    # 받아온 user_ip, user_id 를 로그에 추가
    logger_data = {'clientip': user_ip, 'user_id': user_id}
    logger.info("Request get_key_info", extra=logger_data)

    log_request = "get_key_info"

    # 사용자의 마지막 API 변경 함수
    set_user_API_req(user_key, log_request)
    logger.info("Request set_user_API_req", extra=logger_data)

    # DB 에 로그를 남기기 위해 입력값, 요청값, api, function 명 등을 정의
    input = {}
    input['user_key'] = user_key
    input['index'] = index

    input_list = [user_key, index]

    api = os.path.split(__file__)[1]
    function = sys._getframe().f_code.co_name

    engine = create_engine(db_data)
    connection = engine.raw_connection()
    cursor = connection.cursor()

    try:

        # 입력값에서 디비 또는 API 파라미터에 입력할 수 없는 특수문자가 포함되어 있는 경우
        for input_data in input_list:
            # check_text : 입력받은 문자열이 적합한지 판단
            # check_text(문자열 타입, 문자열)
            # 문자열 타입이 input_db 일 경우 db 에 입력할 수 있는지 판단(특수문자 여부)
            status = check_text("input_db", input_data)
            # 문자열에 특수문자가 있는 경우
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

        # 입력받은 사용자 키를 이용하여 사용자의 아이디, 권한 조회
        send = get_user_info_from_key(user_key)
        logger.info("Get user information", extra=logger_data)

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

            # 인식키 조회 권한이 있는 확인
            user_auth_list = send['data'][0]['AUTH']

            # 인식키 조회 권한 'AUKEY0003'
            request_auth = 'AUKEY0003'

            logger.info("Check authority", extra=logger_data)
            for auth in user_auth_list:
                # 권한이 존재하는 경우
                if auth == request_auth:
                    logger.info("Authority exists", extra=logger_data)

                    # 인식키 정보 조회
                    cursor.callproc('SP_KEYM_GET_KEY_DETAILS_INFO', [index])

                    column_names_list = [x[0] for x in cursor.description]
                    result_key_info = []

                    for row in cursor.fetchall():
                        result_key_info.append(dict(zip(column_names_list, row)))

                    key_info = result_key_info[0]

                    # 인식키를 발급받은 사용자의 아이디
                    user_id = key_info['FK_KMKITN_KEYINFO']

                    # 사용자 정보 조회
                    user_info = get_user_info(user_key, user_id, '0')
                    user_info = user_info['data']

                    # 사용자 상태 한글로 변경
                    for info in user_info:

                        info['LOGIN'] = "사용"

                        if info['DELETE_FLAG'] == "Y":
                            info['LOGIN'] = "삭제"
                        elif info['WITHDRAW_FLAG'] == "Y":
                            info['LOGIN'] = "탈퇴"

                    logger.info("change the state of a user", extra=logger_data)

                    # 사용자 비밀번호가 속해있을 경우 삭제
                    key_list = user_info[0].keys()

                    # get_user_info 이용하여 가져온 정보 중 get_key_info 에서 필요없는 정보 제외
                    if "AUTH" in key_list:
                        del user_info[0]["AUTH"]
                    if "AUTH_GROUP_NAME" in key_list:
                        del user_info[0]["AUTH_GROUP_NAME"]
                    if "AUTH_GRUOP_ID" in key_list:
                        del user_info[0]["AUTH_GRUOP_ID"]
                    if "DATE_LAST" in key_list:
                        del user_info[0]["DATE_LAST"]
                    if "DATE_REG" in key_list:
                        del user_info[0]["DATE_REG"]
                    if "DELETE_FLAG" in key_list:
                        del user_info[0]["DELETE_FLAG"]
                    if "FK_KMUITN_USERINFO" in key_list:
                        del user_info[0]["FK_KMUITN_USERINFO"]
                    if "LOGIN_APPROVAL_FLAG" in key_list:
                        del user_info[0]["LOGIN_APPROVAL_FLAG"]
                    if "SESSION_ID" in key_list:
                        del user_info[0]["SESSION_ID"]
                    if "TIME_LAST" in key_list:
                        del user_info[0]["TIME_LAST"]
                    if "TIME_REG" in key_list:
                        del user_info[0]["TIME_REG"]
                    if "WITHDRAW_FLAG" in key_list:
                        del user_info[0]["WITHDRAW_FLAG"]

                    logger.info("Delete information that is not needed for the output", extra=logger_data)

                    # 아이디가 총 두번 포함되므로 제외
                    if "result_data_1" in key_list:
                        del user_info[0]["result_data_1"]
                    # 비밀번호 제외
                    if "result_data_2" in key_list:
                        del user_info[0]["result_data_2"]

                    # 출력값에 인식키 정보와 사용자의 정보가 모두 필요하므로 인식키 정보와 사용자 정보를 가지는 딕셔너리를 합침
                    key_info.update(user_info[0])

                    data = []
                    data.append(key_info)

                    # 로그 저장
                    # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
                    log_status = "REQUEST"
                    output = data
                    message = "get_key_info success"
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

            # 인식키 조회 권한이 존재하지 않을 경우

            # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
            user_id = None
            log_status = "ERROR"
            output = ""
            message = "permission error"
            success_flag = "N"

            # log : DB 에 로그를 저장하는 함수
            # log_db : DB 에 저장한 로그값
            log_db = log(user_id, log_status, log_request, api, function, input, output, message, success_flag)
            logger.error(message, extra=logger_data)
            logger.error(log_db, extra=logger_data)

            data = []
            result = "fail"
            status = "404"

            # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
            send = set_send(data, result, status)
            logger.error(send, extra=logger_data)

            return send

    except Exception as e:
        print("error type : ", type(e))
        print("error : ", e)

        # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
        user_id = None
        log_status = "EXCEPTION"
        output = ""
        message = e
        success_flag = "N"

        # log : DB 에 로그를 저장하는 함수
        # log_db : DB 에 저장한 로그값
        log_db = log(user_id, log_status, log_request, api, function, input, output, message, success_flag)
        logger.error(message, extra=logger_data)
        logger.error(log_db, extra=logger_data)

        data = []
        status = '402'
        result = "fail"

        # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
        send = set_send(data, result, status)
        logger.error(send, extra=logger_data)

        return send

    finally:
        connection.close()