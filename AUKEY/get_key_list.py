
# -*- coding: utf-8 -*-

import os
import sys

from flask import request
from sqlalchemy import create_engine

from AUUSE.get_user_info_from_key import get_user_info_from_key
from AUUSE.set_user_API_req import set_user_API_req

from AUSYS.log import log

from etc.check_text import check_text
from etc.set_log import set_log
from etc.set_send import set_send
from config.config_set import db_data

# 인식키 리스트를 조회하는 함수
# user_key : API 를 호출하는 사용자의 키
# user_name : 검색 내용(사용자명)
# address : 검색 내용(주소)
# user_id_search : 검색 내용(사용자 id)
# date_start : 검색 내용(시작 일시)
# date_end : 검색 내용(종료 일시)
# currentpage : 현재 페이지
# countperpage : 페이지 당 개수
def get_key_list(user_key, user_name, address, user_id_search, date_start, date_end, currentpage, countperpage):

    # 로그를 남기기 위한 값
    # user_ip : API 를 호출한 사용자의 ip
    # user_id : API 를 호출한 사용자의 id
    user_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    user_id = None
    # 파이썬의 logging 함수를 불러오는 함수
    logger = set_log()
    # 받아온 user_ip, user_id 를 로그에 추가
    logger_data = {'clientip': user_ip, 'user_id': user_id}
    logger.info("Request get_key_list", extra=logger_data)

    log_request = "get_key_list"

    # 사용자의 마지막 API 변경 함수
    set_user_API_req(user_key, log_request)
    logger.info("Request set_user_API_req", extra=logger_data)

    # DB 에 로그를 남기기 위해 입력값, 요청값, api, function 명 등을 정의
    input = {}
    input['user_key'] = user_key
    input['user_name'] = user_name
    input['address'] = address
    input['user_id_search'] = user_id_search
    input['date_start'] = date_start
    input['date_end'] = date_end
    input['currentpage'] = currentpage
    input['countperpage'] = countperpage

    log_request = "get_key_list"
    api = os.path.split(__file__)[1]
    function = sys._getframe().f_code.co_name

    # 입력값 리스트
    input_list = [user_key, user_name, address, user_id_search, date_start, date_end, currentpage, countperpage]

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

        # 검색 내용이 없을 경우(0으로 입력이 들어왔을 경우) None 으로 설정
        if user_name == "0":
            user_name = None
        if address == "0":
            address = None
        if user_id_search == "0":
            user_id_search = None
        if date_start == "0":
            date_start = None
        if date_end == "0":
            date_end = None
        # 현재 페이지가 None 일 경우 1페이지로 설정되어 있음
        if currentpage == "0":
            currentpage = None
        # 페이지 당 개수가 None 일 경우 저장되어 있는 모든 정보를 가져오도록 설정되어 있음
        if countperpage == "0":
            countperpage = None

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
            message = "get_user_info_from_key DB error"
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

            # 인식키 조회 권한이 있는지 확인
            user_auth_list = send['data'][0]['AUTH']
            user_id = send['data'][0]['result_data_1']

            # 인식키 조회 권한 'AUKEY0003'
            request_auth = 'AUKEY0003'

            logger.info("Check authority", extra=logger_data)
            for auth in user_auth_list:

                # 권한이 있을 경우 인식키 정보 조회
                if auth == request_auth:
                    logger.info("Authority exists", extra=logger_data)

                    # 인식키 리스트를 가져오는 프로시저
                    cursor.callproc('SP_KEYM_GET_KEY_LIST', [user_name, address, user_id_search, date_start, date_end,
                                                             currentpage, countperpage])

                    column_names_list = [x[0] for x in cursor.description]
                    result_key_info = []

                    for row in cursor.fetchall():
                        result_key_info.append(dict(zip(column_names_list, row)))

                    # 인식키 리스트 조회에 성공하였으나 결과값이 존재하지 않는 경우
                    if not result_key_info:

                        # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
                        log_status = "REQUEST"
                        output = ""
                        message = "Result is None"
                        success_flag = "Y"

                        # log : DB 에 로그를 저장하는 함수
                        # log_db : DB 에 저장한 로그값
                        log_db = log(user_id, log_status, log_request, api, function, input, output, message, success_flag)
                        logger.error(message, extra=logger_data)
                        logger.error(log_db, extra=logger_data)

                        data = []
                        result = "success"
                        status = "201"

                        # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
                        send = set_send(data, result, status)
                        logger.error(send, extra=logger_data)

                        return send

                    # 사용자 상태 한글로 변경
                    for key_info in result_key_info:

                        key_info['LOGIN'] = "사용"

                        if key_info['DELETE_FLAG'] == "Y":
                            key_info['LOGIN'] = "삭제"
                        elif key_info['WITHDRAW_FLAG'] == "Y":
                            key_info['LOGIN'] = "탈퇴"

                    logger.info("change the state of a user", extra=logger_data)

                    # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
                    log_status = "REQUEST"
                    output = result_key_info
                    message = "get_key_list success"
                    success_flag = "Y"

                    # log : DB 에 로그를 저장하는 함수
                    # log_db : DB 에 저장한 로그값
                    log_db = log(user_id, log_status, log_request, api, function, input, output, message, success_flag)
                    logger.info(message, extra=logger_data)
                    logger.debug(log_db, extra=logger_data)

                    data = result_key_info
                    result = "success"
                    status = "200"

                    # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
                    send = set_send(data, result, status)
                    logger.debug(send, extra=logger_data)

                    return send

            # 인식키 조회 권한이 존재하지 않을 경우

            # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
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

        data = []
        status = '402'
        result = "fail"

        # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
        send = set_send(data, result, status)
        logger.error(send, extra=logger_data)

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

        return send

    finally:
        connection.close()
