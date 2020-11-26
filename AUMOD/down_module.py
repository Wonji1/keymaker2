
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

# 인식모듈 게시글에 등록된 첨부파일 다운로드하는 함수
# user_key : API 를 호출하는 사용자의 키
# module_index : 첨부파일을 다운로드 하려는 인식모듈 게시글의 인덱스
def down_module(user_key, module_index):

    # 로그를 남기기 위한 값
    # user_ip : API 를 호출한 사용자의 ip
    # user_id : API 를 호출한 사용자의 id
    user_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    user_id = None
    # 파이썬의 logging 함수를 불러오는 함수
    logger = set_log()
    # 받아온 user_ip, user_id 를 로그에 추가
    logger_data = {'clientip': user_ip, 'user_id': user_id}
    logger.info("Request down_module", extra=logger_data)

    log_request = "down_module"

    # 사용자의 마지막 API 변경 함수
    set_user_API_req(user_key, log_request)
    logger.info("Request set_user_API_req", extra=logger_data)

    # DB 에 로그를 남기기 위해 입력값, 요청값, api, function 명 등을 정의
    input = {}
    input['user_key'] = user_key
    input['module_index'] = module_index

    api = os.path.split(__file__)[1]
    function = sys._getframe().f_code.co_name

    input_list = [user_key, module_index]

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

        # 인식모듈 다운로드 권한 'AUMOD0002'
        request_auth = 'AUMOD0002'

        logger.info("Check authority", extra=logger_data)
        for auth in user_auth_list:

            user_id = send['data'][0]['result_data_1']

            # 권한이 존재하는 경우
            if auth == request_auth:
                logger.info("Authority exists", extra=logger_data)

                engine = create_engine(db_data)
                connection = engine.raw_connection()
                cursor = connection.cursor()

                try:
                    # 해당 모듈 게시글의 정보 조회
                    # 다운로드하기위해 인식모듈 게시글 정보를 조회하는 것 이므로 조회수 증가하지 않음
                    count_click = "N"
                    cursor.callproc('SP_KEYM_GET_MODULE_DETAILS_INFO', [module_index, count_click])

                    logger.info("get module post information", extra=logger_data)

                    column_names_list = [x[0] for x in cursor.description]

                    result_module_info = []

                    for row in cursor.fetchall():
                        result_module_info.append(dict(zip(column_names_list, row)))

                    # 조회한 첨부파일 정보 설정
                    file_path = result_module_info[0]['FILE_PATH']
                    file_name = result_module_info[0]['FILE_NAME']
                    file_name_ori = result_module_info[0]['FILE_NAME_ORI']
                    file_exist_flag = result_module_info[0]['FILE_EXIST_FLAG']

                    # 다운로드 요청한 게시글에 첨부파일이 존재하지 않을 경우
                    if file_exist_flag == "N":
                        # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
                        user_id = None
                        log_status = "ERROR"
                        output = ""
                        message = "Attachment does not exist"
                        success_flag = "N"

                        # log : DB 에 로그를 저장하는 함수
                        # log_db : DB 에 저장한 로그값
                        log_db = log(user_id, log_status, log_request, api, function, input, output, message,
                                     success_flag)
                        logger.error(message, extra=logger_data)
                        logger.error(log_db, extra=logger_data)

                        data = []
                        result = "fail"
                        status = "402"

                        # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
                        send = set_send(data, result, status)
                        logger.error(send, extra=logger_data)

                        return send

                    # 해당 경로에 저장된 파일 찾아 변수에 저장
                    file = file_path + file_name

                    module_info = {}
                    module_info['FILE_PATH'] = file_path
                    module_info['FILE_NAME'] = file_name
                    module_info['FILE_NAME_ORI'] = file_name_ori
                    module_info['FILE'] = file

                    # 다운로드 수 1 증가
                    cursor.callproc('SP_KEYM_SET_MODULE_DOWM_INFO', [module_index])
                    logger.info("The number of downloads has increased", extra=logger_data)

                    # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
                    user_id = None
                    log_status = "REQUEST"
                    output = module_info
                    message = "down_module success"
                    success_flag = "Y"

                    # log : DB 에 로그를 저장하는 함수
                    # log_db : DB 에 저장한 로그값
                    log_db = log(user_id, log_status, log_request, api, function, input, output, message, success_flag)
                    logger.info(message, extra=logger_data)
                    logger.debug(log_db, extra=logger_data)

                    data = []
                    data.append(module_info)
                    status = '200'
                    result = "success"

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
                    status = '402'
                    result = "fail"

                    # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
                    send = set_send(data, result, status)
                    logger.error(send, extra=logger_data)

                    return send

                finally:
                    connection.close()