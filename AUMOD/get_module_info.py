
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

# 인식모듈 게시글을 조회하는 함수
# user_key : API 를 호출하는 사용자의 키
# log_request : 요청코드(인식모듈 상세정보 조회, 인식모듈 수정 시 정보 호출)
# module_index : 정보를 조회하려는 인식모듈 게시글의 인덱스
def get_module_info(user_key, log_request, module_index):

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

    request_log = "get_module_info"

    # 사용자의 마지막 API 변경 함수
    set_user_API_req(user_key, request_log)
    logger.info("Request set_user_API_req", extra=logger_data)

    # DB 에 로그를 남기기 위해 입력값, 요청값, api, function 명 등을 정의
    input = {}
    input['user_key'] = user_key
    input['log_request'] = log_request
    input['module_index'] = module_index

    api = os.path.split(__file__)[1]
    function = sys._getframe().f_code.co_name

    input_list = [user_key, log_request, module_index]

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
        # 수정을 요청한 사용자와 작성자가 동일한지 확인

        # API 를 호출한 사용자 아이디
        user_id = send['data'][0]['result_data_1']

        engine = create_engine(db_data)
        connection = engine.raw_connection()
        cursor = connection.cursor()

        # 인식모듈 상세정보 조회하는 프로시저 호출
        try:
            # 작성자인지 판단하기 위해 조회하는 것 이므로 조회수 증가하지 않음
            count_click = "N"
            cursor.callproc('SP_KEYM_GET_MODULE_DETAILS_INFO', [module_index, count_click])

            column_names_list = [x[0] for x in cursor.description]

            result_module_info = []

            for row in cursor.fetchall():
                result_module_info.append(dict(zip(column_names_list, row)))

            # 입력한 인덱스에 해당하는 인식모듈 정보가 존재하지 않을 경우(삭제된 인식모듈을 호출한 경우)
            if not result_module_info:
                # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
                user_id = None
                log_status = "ERROR"
                output = ""
                message = "Module post does not exist"
                success_flag = "N"

                # log : DB 에 로그를 저장하는 함수
                # log_db : DB 에 저장한 로그값
                log_db = log(user_id, log_status, log_request, api, function, input, output, message,
                             success_flag)
                logger.error(message, extra=logger_data)
                logger.error(log_db, extra=logger_data)

                data = []
                result = "fail"
                status = "405"

                # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
                send = set_send(data, result, status)
                logger.error(send, extra=logger_data)

                return send

            # 초반에 None 으로 설정해뒀던 파일은 N 으로 바꾸어 출력
            for module_info in result_module_info:
                if module_info['FILE_EXIST_FLAG'] is None:
                    module_info['FILE_EXIST_FLAG'] = "N"

            # 인식모듈을 등록한 사용자 ID
            user_id_module = result_module_info[0]['FK_KMMITN_MODULEINFO']
            logger.info("Verify that the user and author match", extra=logger_data)

            # 작성자가 동일한지 확인
            if user_id != user_id_module:
                logger.info("User and author do not match", extra=logger_data)
                id_equal_flag = "N"
            else:
                logger.info("User and author match", extra=logger_data)
                id_equal_flag = "Y"

            # 인식모듈을 조회하려는 사용자의 권한 리스트
            user_auth_list = send['data'][0]['AUTH']

            request_auth = ""
            # 인식모듈 조회 'LGMOD0001'
            if log_request == "LGMOD0001":
                request_auth = 'AUMOD0001'
                count_click = "Y"
            # 인식모듈 수정 'LGMOD0003'
            elif log_request == "LGMOD0003":
                request_auth = 'AUMOD0003'
                count_click = "N"

            auth_exist_flag = ""
            logger.info("Check authority", extra=logger_data)
            # 인식모듈 조회 또는 수정 권한 조회
            for auth in user_auth_list:
                if auth == request_auth:
                    logger.info("Authority exists", extra=logger_data)
                    auth_exist_flag = "Y"
                    break
                else:
                    auth_exist_flag = "N"

            # 인식모듈 조회를 요청했을 경우 권한이 없으면 조회 불가
            if log_request == "LGMOD0001":
                if auth_exist_flag == "N":

                    # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
                    user_id = None
                    log_status = "ERROR"
                    output = ""
                    message = "You do not have permission"
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

                # 자격이 있을 경우 조회수 증가
                else:
                    # 조회수 증가 후 증가된 값을 호출
                    cursor.callproc('SP_KEYM_GET_MODULE_DETAILS_INFO', [module_index, count_click])

                    column_names_list = [x[0] for x in cursor.description]

                    result_module_info = []

                    for row in cursor.fetchall():
                        result_module_info.append(dict(zip(column_names_list, row)))

            # 인식모듈 수정을 요청헀을 경우 작성자도 아니고 권한도 없을 경우 조회 불가(택1)
            elif log_request == "LGMOD0003":
                if id_equal_flag == "N" and auth_exist_flag == "N":
                    # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
                    user_id = None
                    log_status = "ERROR"
                    output = ""
                    message = "You do not have permission"
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

            result_module_info[0]['id_equal_flag'] = id_equal_flag

            data = result_module_info

            # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
            user_id = None
            log_status = "REQUEST"
            output = data
            message = "get_module_info success"
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
            status = '403'
            result = "fail"

            # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
            send = set_send(data, result, status)
            logger.error(send, extra=logger_data)

            return send

        finally:
            connection.close()