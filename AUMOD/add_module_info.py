
# -*- coding: utf-8 -*-
import os
import sys

from flask import request
from sqlalchemy import create_engine

from AUMOD.get_module_list import get_module_list

from AUSYS.log import log

from AUUSE.get_user_info_from_key import get_user_info_from_key
from AUUSE.set_user_API_req import set_user_API_req
from etc.set_log import set_log

from etc.set_send import set_send
from etc.check_text import check_text
from config.config_set import module_tmp_path
from config.config_set import db_data

# 인식모듈을 등록하는 함수
# user_key : API 를 호출하는 사용자의 키
# module_name : 인식모듈 게시글 제목
# version : 인식모듈 게시글에 입력한 버전
# memo : 인식모듈 게시글 내용
def add_module_info(user_key, module_name, version, memo):

    # 로그를 남기기 위한 값
    # user_ip : API 를 호출한 사용자의 ip
    # user_id : API 를 호출한 사용자의 id
    user_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    user_id = None
    # 파이썬의 logging 함수를 불러오는 함수
    logger = set_log()
    # 받아온 user_ip, user_id 를 로그에 추가
    logger_data = {'clientip': user_ip, 'user_id': user_id}
    logger.info("Request create_qr", extra=logger_data)

    log_request = "add_module_info"

    # 사용자의 마지막 API 변경 함수
    set_user_API_req(user_key, log_request)
    logger.info("Request set_user_API_req", extra=logger_data)

    # DB 에 로그를 남기기 위해 입력값, 요청값, api, function 명 등을 정의
    input = {}
    input['user_key'] = user_key
    input['module_name'] = module_name
    input['version'] = version
    input['memo'] = memo

    api = os.path.split(__file__)[1]
    function = sys._getframe().f_code.co_name

    input_list = [user_key, module_name, version, memo]

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

        # 인식모듈 등록 권한이 있는지 확인
        user_auth_list = send['data'][0]['AUTH']

        # 인식모듈 등록 권한 'AUMOD0005'
        request_auth = 'AUMOD0005'

        logger.info("Check authority", extra=logger_data)
        for auth in user_auth_list:
            # 권한이 존재하는 경우
            if auth == request_auth:
                logger.info("Authority exists", extra=logger_data)

                # 인식모듈 게시글을 등록한 사용자 id
                user_id = send['data'][0]['result_data_1']

                # 첨부파일이 존재하지 않을 경우 첨부파일 관련 정보 None 으로 설정
                file_name_ori = None
                file_name = None
                file_path = module_tmp_path
                file_size = None
                logger.info("You have not added an attachment to the post", extra=logger_data)

                engine = create_engine(db_data)
                connection = engine.raw_connection()
                cursor = connection.cursor()

                # 인식모듈 게시글을 저장하는 포르시저 호출
                try:
                    cursor.callproc('SP_KEYM_ADD_MODULE_INFO', [user_id, module_name, file_name_ori, file_name,
                                                                file_path, file_size, version, memo])

                    logger.info("save module post information", extra=logger_data)

                    # 등록한 모듈의 인덱스값을 반환하기 위해 등록되어있는 모듈 게시글의 모든 정보를 가져옴
                    send = get_module_list(user_key, "0", "0", "0", "0", "0", "0", "0", "0")

                    # 등록된 모듈 게시글의 인덱스값이 가장 큰 값(가장 최신값)을 저장
                    module_list = send['data']
                    module_index = module_list[0]['IX_KMMITN_MODULEINFO']

                    data = []
                    module_info = {}
                    module_info['index'] = module_index
                    data.append(module_info)

                    # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
                    user_id = None
                    log_status = "REQUEST"
                    output = data
                    message = "add_module_info success"
                    success_flag = "Y"

                    # log : DB 에 로그를 저장하는 함수
                    # log_db : DB 에 저장한 로그값
                    log_db = log(user_id, log_status, log_request, api, function, input, output, message, success_flag)
                    logger.info(message, extra=logger_data)
                    logger.debug(log_db, extra=logger_data)

                    status = "200"
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
                    status = '403'
                    result = "fail"

                    # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
                    send = set_send(data, result, status)
                    logger.error(send, extra=logger_data)

                    return send

                finally:
                    connection.close()

        # 인식모듈 등록 권한이 존재하지 않는 경우

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
        status = "402"

        # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
        send = set_send(data, result, status)
        logger.error(send, extra=logger_data)

        return send