
# -*- coding: utf-8 -*-
import os
import sys

from flask import request
from sqlalchemy import create_engine

from AUSYS.log import log

from AUUSE.get_user_info_from_key import get_user_info_from_key
from AUUSE.set_user_API_req import set_user_API_req

from etc.set_log import set_log
from etc.set_send import set_send
from etc.check_text import check_text
from config.config_set import db_data

# 인식모듈 게시글의 리스트를 조회하는 함수
# user_key : API 를 호출하는 사용자의 키
# module_name : 인식모듈 게시글의 제목(검색 내용)
# user_name : 인식모듈 게시글을 작성한 사용자명(검색 내용)
# version : 인식모듈 게시글의 버전(검색 내용)
# memo : 인식모듈 게시글의 내용(검색 내용)
# date_reg_start : 인식모듈 게시글 작성 일자 시작(검색 내용)
# date_reg_end : 인식모듈 게시글 작성 일자 마지막(검색 내용)
# currentpage : 현재 페이지
# countperpage : 페이지당 개수
def get_module_list(user_key, module_name, user_name, version, memo, date_reg_start, date_reg_end, currentpage,
                    countperpage):

    # 로그를 남기기 위한 값
    # user_ip : API 를 호출한 사용자의 ip
    # user_id : API 를 호출한 사용자의 id
    user_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    user_id = None
    # 파이썬의 logging 함수를 불러오는 함수
    logger = set_log()
    # 받아온 user_ip, user_id 를 로그에 추가
    logger_data = {'clientip': user_ip, 'user_id': user_id}
    logger.info("Request get_module_info", extra=logger_data)
    log_request = "get_module_list"

    # 사용자의 마지막 API 변경 함수
    set_user_API_req(user_key, log_request)
    logger.info("Request set_user_API_req", extra=logger_data)

    # DB 에 로그를 남기기 위해 입력값, 요청값, api, function 명 등을 정의
    input = {}
    input['user_key'] = user_key
    input['module_name'] = module_name
    input['user_name'] = user_name
    input['version'] = version
    input['memo'] = memo
    input['date_reg_start'] = date_reg_start
    input['date_reg_end'] = date_reg_end
    input['currentpage'] = currentpage
    input['countperpage'] = countperpage

    api = os.path.split(__file__)[1]
    function = sys._getframe().f_code.co_name

    input_list = [user_key, module_name, user_name, version, memo, date_reg_start, date_reg_end, currentpage, countperpage]

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
            status = "404"

            # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
            send = set_send(data, result, status)
            logger.error(send, extra=logger_data)

            return send

    # 검색 내용이 없을 경우 0을 입력 받음
    # 0으로 받았을 경우 None 으로 설정
    if module_name == "0":
        module_name = None
    if user_name == "0":
        user_name = None
    if version == "0":
        version = None
    if memo == "0":
        memo = None
    if date_reg_start == "0":
        date_reg_start = None
    if date_reg_end == "0":
        date_reg_end = None
    if currentpage == "0":
        currentpage = None
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

        # 인식모듈 조회 권한이 있는지 확인
        user_auth_list = send['data'][0]['AUTH']

        # 인식모듈 조회 권한 'AUMOD0001'
        request_auth = 'AUMOD0001'

        logger.info("Check authority", extra=logger_data)
        for auth in user_auth_list:
            user_id = send['data'][0]['result_data_1']

            # 권한이 존재하는 경우
            if auth == request_auth:
                logger.info("Authority exists", extra=logger_data)

                engine = create_engine(db_data)
                connection = engine.raw_connection()
                cursor = connection.cursor()

                # 인식모듈 조회하는 포르시저 호출
                try:
                    cursor.callproc('SP_KEYM_GET_MODULE_LIST', [module_name, user_name, version, memo,
                                                                date_reg_start, date_reg_end, currentpage,
                                                                countperpage])

                    column_names_list = [x[0] for x in cursor.description]

                    result_module_info = []

                    for row in cursor.fetchall():
                        result_module_info.append(dict(zip(column_names_list, row)))

                    for module_info in result_module_info:
                        if module_info['FILE_EXIST_FLAG'] == None:
                            module_info['FILE_EXIST_FLAG'] = "N"

                    if not result_module_info:
                        data = []
                        result = "success"
                        status = "201"
                    else:
                        data = result_module_info
                        result = "success"
                        status = "200"

                    # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
                    user_id = None
                    log_status = "REQUEST"
                    output = data
                    message = "get_module_list success"
                    success_flag = "Y"

                    # log : DB 에 로그를 저장하는 함수
                    # log_db : DB 에 저장한 로그값
                    log_db = log(user_id, log_status, log_request, api, function, input, output, message,
                                         success_flag)
                    logger.info(message, extra=logger_data)
                    logger.debug(log_db, extra=logger_data)

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
                    status = '403'
                    result = "fail"

                    # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
                    send = set_send(data, result, status)
                    logger.error(send, extra=logger_data)

                    return send

                finally:
                    connection.close()
