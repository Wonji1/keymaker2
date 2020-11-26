
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
from etc.del_file_dir import del_file_dir
from config.config_set import db_data

# 인식모듈 게시글을 삭제하는 함수
# user_key : API 를 호출하는 사용자의 키
# module_index : 삭제하려는 인식모듈 게시글의 인덱스
# file_exist_flag : 삭제하려는 인식모듈 게시글의 첨부파일 존재 여부
def del_module_info(user_key, module_index, file_exist_flag):

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

    log_request = "del_module_info"

    # 사용자의 마지막 API 변경 함수
    set_user_API_req(user_key, log_request)
    logger.info("Request set_user_API_req", extra=logger_data)

    # DB 에 로그를 남기기 위해 입력값, 요청값, api, function 명 등을 정의
    input = {}
    input['user_key'] = user_key
    input['module_index'] = module_index
    input['file_exist_flag'] = file_exist_flag

    api = os.path.split(__file__)[1]
    function = sys._getframe().f_code.co_name

    input_list = [user_key, module_index, file_exist_flag]

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
            status = "405"

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

        # 인식모듈 상세정보 조회하는 포르시저 호출
        try:
            count_click = "N"
            cursor.callproc('SP_KEYM_GET_MODULE_DETAILS_INFO', [module_index, count_click])

            column_names_list = [x[0] for x in cursor.description]

            result_module_info = []

            for row in cursor.fetchall():
                result_module_info.append(dict(zip(column_names_list, row)))

            # 인식모듈을 등록한 사용자 ID
            user_id_module = result_module_info[0]['FK_KMMITN_MODULEINFO']

            logger.info("Verify that the user and author match", extra=logger_data)

            # 작성자가 동일하지 않을 경우 권한 확인
            if user_id != user_id_module:
                logger.info("User and author do not match", extra=logger_data)
                id_equal_flag = "N"
            else:
                logger.info("User and author match", extra=logger_data)
                id_equal_flag = "Y"

            user_auth_list = send['data'][0]['AUTH']

            # 인식모듈 삭제 권한 'AUMOD0004'
            request_auth = 'AUMOD0004'

            auth_exist_flag = ""
            logger.info("Check authority", extra=logger_data)
            # 인식모듈 수정 권한 조회
            for auth in user_auth_list:
                if auth == request_auth:
                    logger.info("Authority exists", extra=logger_data)
                    auth_exist_flag = "Y"
                    break
                else:
                    auth_exist_flag = "N"

            # 작성자 동일 또는 권한 존재 중 하나라도 값이 Y 라면 인식모듈 삭제 가능
            if id_equal_flag == "Y" or auth_exist_flag == "Y":
                # 이전에 등록한 첨부파일명
                file_name_del = result_module_info[0]['FILE_NAME']
                # 이전에 등록한 첨부파일 경로
                file_path_del = result_module_info[0]['FILE_PATH']

                # 첨부파일이 존재하는 경우 서버에 저장된 파일 삭제
                if file_exist_flag == "Y":
                    del_file_dir(file_path_del, file_name_del)

                cursor.callproc('SP_KEYM_DEL_MODULE_INFO', [module_index])

                data = []

                # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
                user_id = None
                log_status = "REQUEST"
                output = data
                message = "del_module_info success"
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

            else:
                # 작성자가 아니거나 인식모듈 삭제 권한이 존재하지 않는 경우
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
            status = '404'
            result = "fail"

            # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
            send = set_send(data, result, status)
            logger.error(send, extra=logger_data)

            return send

        finally:
            connection.close()