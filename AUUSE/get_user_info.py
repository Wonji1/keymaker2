
# -*- coding: utf-8 -*-
import os
import sys

from flask import request
from sqlalchemy import create_engine

from AUSYS.log import log
from AUUSE.get_user_info_from_key import get_user_info_from_key
from AUUSE.set_user_API_req import set_user_API_req

from etc.check_text import check_text
from etc.set_log import set_log
from etc.set_send import set_send
from config.config_set import db_data

# 사용자 정보 조회
# user_key : API 를 호출하는 사용자의 키
# user_id : API 를 호출하는 사용자의 id
# log_request : 요청코드(사용자 (상세)정보 조회, 사용자 정보 수정, 자기 정보 수정, ID 중복 확인)
# 요청코드가 사용자 (상세)정보 조회일 경우 user_key 만 입력 id 는 0 입력 (LGUSE0004)
# 요청코드가 사용자 정보 수정일 경우 user_key 만 입력 id 는 0 입력 (LGUSE0005)
# 요청코드가 자기 정보 수정일 경우 user_key 만 입력 id 는 0 입력 (LGUSE0010)
# 요청코드가 ID 중복 확인일 경우 user_id 만 입력 key 는 0 입력 (0)
def get_user_info(user_key, user_id, log_request):

    # 로그를 남기기 위한 값
    # user_ip : API 를 호출한 사용자의 ip
    # user_id : API 를 호출한 사용자의 id
    user_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    # user_id = None
    # 파이썬의 logging 함수를 불러오는 함수
    logger = set_log()
    # 받아온 user_ip, user_id 를 로그에 추가
    logger_data = {'clientip': user_ip, 'user_id': user_id}

    logger.info("Request get_user_info", extra=logger_data)

    # DB 에 로그를 남기기 위해 입력값, 요청값, api, function 명 등을 정의
    input = {}
    input['user_id'] = user_id
    input['user_ip'] = user_ip
    input['log_request'] = log_request

    api = os.path.split(__file__)[1]
    function = sys._getframe().f_code.co_name

    # 사용자의 마지막 API 변경 함수
    set_user_API_req(user_key, "get_user_info")

    input_list = [user_key, user_id, "get_user_info"]

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

    # 사용자 (상세)정보 조회(user_key)
    if log_request == 'LGUSE0004':
        request_type = "get_user_info"

    # 사용자 정보 수정(user_key)
    elif log_request == 'LGUSE0005':
        request_type = "set_user_info"

    # 자기 정보 수정(user_key)
    elif log_request == 'LGUSE0010':
        request_type = "set_my_info"

    # ID 중복 확인(user_id)
    else:
        request_type = "login_before"

    # 요청이 ID 중복 확인일 경우 user_id 로 사용자 정보 조회
    if request_type == "login_before":

        status = check_text('id', user_id)

        # 입력받은 ID가 영어, 숫자 이외의 문자가 있는 경우
        if status == '400':
            # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
            user_id = None
            log_status = "ERROR"
            output = ""
            message = "The conditions of the input value are not correct"
            success_flag = "N"

            # log : DB 에 로그를 저장하는 함수
            # log_db : DB 에 저장한 로그값
            log_db = log(user_id, log_status, log_request, api, function, input, output, message, success_flag)
            logger.error(message, extra=logger_data)
            logger.error(log_db, extra=logger_data)

            data = []
            result = "fail"

            # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
            send = set_send(data, result, status)
            logger.error(send, extra=logger_data)

            return send

        engine = create_engine(db_data)
        connection = engine.raw_connection()
        cursor = connection.cursor()

        try:
            cursor.callproc('SP_KEYM_GET_USR_DETAILS_INFO', [user_id])
            column_names_list = [x[0] for x in cursor.description]

            result_user_info = []

            for row in cursor.fetchall():
                result_user_info.append(dict(zip(column_names_list, row)))

            print(result_user_info)

            # 입력한 ID에 해당하는 사용자 정보가 존재하지 않는 경우
            if not result_user_info:

                data = []

                # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
                user_id = None
                log_status = "REQUEST"
                output = data
                message = "User information does not exist"
                success_flag = "Y"

                # log : DB 에 로그를 저장하는 함수
                # log_db : DB 에 저장한 로그값
                log_db = log(user_id, log_status, log_request, api, function, input, output, message, success_flag)
                logger.info(message, extra=logger_data)
                logger.debug(log_db, extra=logger_data)

                result = "success"
                status = "201"

                # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
                send = set_send(data, result, status)
                logger.debug(send, extra=logger_data)

                return send

            # 입력한 ID에 해당하는 사용자 정보가 존재하는 경우
            userinfo = result_user_info[0]

            auth_list = userinfo['AUTH'].split(',')
            userinfo['AUTH'] = auth_list

            data = result_user_info

            # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
            user_id = None
            log_status = "REQUEST"
            output = data
            message = "get_user_info success"
            success_flag = "Y"

            # log : DB 에 로그를 저장하는 함수
            # log_db : DB 에 저장한 로그값
            log_db = log(user_id, log_status, log_request, api, function, input, output, message, success_flag)
            logger.info(message, extra=logger_data)
            logger.debug(log_db, extra=logger_data)

            result = "success"
            status = '200'

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
            status = '401'
            result = "fail"

            # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
            send = set_send(data, result, status)
            logger.error(send, extra=logger_data)

            return send

        finally:
            connection.close()

    # 요청이 ID 중복 확인이 아닌 경우 user_key 로 권한 조회 후 사용자 정보 조회
    else:
        user_info = get_user_info_from_key(user_key)
        user_auth_list = user_info['data'][0]['AUTH']
        user_id = user_info['data'][0]['result_data_1']

        request_auth = ""

        # 요청이 사용자 (상세) 정보 조회인 경우
        if request_type == "get_user_info":
            request_auth = 'AUUSE0001'

        # 요청이 사용자 정보 수정에서 조회한 경우
        elif request_type == "set_user_info":
            request_auth = 'AUUSE0002'

        # 요청이 자기 정보 수정에서 조회한 경우
        elif request_type == "set_my_info":
            request_auth = 'AUUSE0007'

        for auth in user_auth_list:

            # 요청한 권한이 존재하는 경우
            if auth == request_auth:
                engine = create_engine(db_data)
                connection = engine.raw_connection()
                cursor = connection.cursor()

                try:
                    cursor.callproc('SP_KEYM_GET_USR_DETAILS_INFO', [user_id])
                    column_names_list = [x[0] for x in cursor.description]

                    result_user_info = []

                    for row in cursor.fetchall():
                        result_user_info.append(dict(zip(column_names_list, row)))

                    # 입력한 ID에 해당하는 사용자 정보가 존재하지 않는 경우
                    if not result_user_info:

                        data = []

                        # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
                        user_id = None
                        log_status = "REQUEST"
                        output = data
                        message = "User information does not exist"
                        success_flag = "Y"

                        # log : DB 에 로그를 저장하는 함수
                        # log_db : DB 에 저장한 로그값
                        log_db = log(user_id, log_status, log_request, api, function, input, output, message,
                                     success_flag)
                        logger.info(message, extra=logger_data)
                        logger.debug(log_db, extra=logger_data)

                        result = "success"
                        status = "201"

                        # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
                        send = set_send(data, result, status)
                        logger.debug(send, extra=logger_data)

                        return send

                    # 입력한 ID에 해당하는 사용자 정보가 존재하는 경우
                    userinfo = result_user_info[0]

                    auth_list = userinfo['AUTH'].split(',')
                    userinfo['AUTH'] = auth_list

                    data = result_user_info

                    # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
                    user_id = None
                    log_status = "REQUEST"
                    output = data
                    message = "get_user_info success"
                    success_flag = "Y"

                    # log : DB 에 로그를 저장하는 함수
                    # log_db : DB 에 저장한 로그값
                    log_db = log(user_id, log_status, log_request, api, function, input, output, message,
                                 success_flag)
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
                    message = e
                    success_flag = "Y"

                    # log : DB 에 로그를 저장하는 함수
                    # log_db : DB 에 저장한 로그값
                    log_db = log(user_id, log_status, log_request, api, function, input, output, message, success_flag)
                    logger.error(message, extra=logger_data)
                    logger.error(log_db, extra=logger_data)

                    data = []
                    status = '401'
                    result = "fail"

                    # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
                    send = set_send(data, result, status)
                    logger.error(send, extra=logger_data)

                    return send

                finally:
                    connection.close()

        # 요청하는 권한이 존재하지 않는 경우
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
        status = "402"

        # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
        send = set_send(data, result, status)
        logger.error(send, extra=logger_data)

        return send