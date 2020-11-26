
# -*- coding: utf-8 -*-
import os
import sys

from flask import request
from sqlalchemy import create_engine

from AUSYS.log import log

from AUUSE.logout import logout
from AUUSE.access import access

from config.config_set import db_data
from etc.check_text import check_text
from etc.set_log import set_log
from etc.set_send import set_send

# 로그인
# user_id : 로그인 요청한 사용자 id
# user_pw : 로그인 요청한 사용자 pw
def login(user_id, user_pw):

    # 로그를 남기기 위한 값
    # user_ip : API 를 호출한 사용자의 ip
    # user_id : API 를 호출한 사용자의 id
    user_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    # user_id = None
    # 파이썬의 logging 함수를 불러오는 함수
    logger = set_log()
    # 받아온 user_ip, user_id 를 로그에 추가
    logger_data = {'clientip': user_ip, 'user_id': user_id}

    logger.info("Request login", extra=logger_data)

    # DB 에 로그를 남기기 위해 입력값, 요청값, api, function 명 등을 정의
    input = {}
    input['user_id'] = user_id
    input['user_pw'] = user_pw

    log_request = "login"
    api = os.path.split(__file__)[1]
    function = sys._getframe().f_code.co_name

    input_list = [user_id, user_pw]

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
            status = "412"

            # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
            send = set_send(data, result, status)
            logger.error(send, extra=logger_data)

            return send

    # ID, PW 조건 확인
    # 상태코드 리턴
    status_id = check_text('id', user_id)
    status_pw = check_text('pw', user_pw)

    # ID에 영어, 숫자 이외의 문자가 존재할 경우
    if status_id == "400":
        userinfo = {}
        data = []
        data.append(userinfo)

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

        result = "fail"
        status = status_id

        # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
        send = set_send(data, result, status)
        logger.error(send, extra=logger_data)

        return send

    # PW에 영어, 숫자 이외의 문자가 존재할 경우
    elif status_pw == "400":

        userinfo = {}
        data = []
        data.append(userinfo)

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

        result = "fail"
        status = "401"

        # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
        send = set_send(data, result, status)
        logger.error(send, extra=logger_data)

        return send

    engine = create_engine(db_data)
    connection = engine.raw_connection()
    cursor = connection.cursor()

    # 접속 테이블에서 동일 아이피 존재 확인
    user_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    status = ""

    try:
        cursor.callproc('SP_KEYM_GET_USR_INFO_IP', [user_ip])
        column_names_list = [x[0] for x in cursor.description]

        result_user_access_info = []

        for row in cursor.fetchall():
            result_user_access_info.append(dict(zip(column_names_list, row)))

        # 접속 테이블에 동일한 ip가 존재할 경우 로그아웃
        if result_user_access_info:
            # 로그아웃 API 호출
            send = logout(user_ip)

            # IP가 입력이 제대로 되지 않은 경우
            if send['status'] == "400":
                send['status'] = "402"
            # 동일한 IP로 접속한 사용자가 없을 경우
            elif send['status'] == "401":
                send['status'] = "403"
            # DB 조회 시 에러가 난 경우
            elif send['status'] == "402":
                send['status'] = "404"
            elif send['status'] == "403":
                send['status'] = "412"
            # 동일한 IP로 접속한 사용자가 존재하여 접속해 있던 사용자는 로그아웃 되는 경우
            elif send['status'] == "200":
                send['result'] = "success"
                send['status'] = "201"

            if send['status'] != "201":
                data = []

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

                result = "fail"

                # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
                send = set_send(data, result, status)
                logger.error(send, extra=logger_data)

                return send
            else:
                status = "201"

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
        status = "406"

        # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
        send = set_send(data, result, status)
        logger.error(send, extra=logger_data)

        return send

    finally:
        connection.close()

    # 사용자 테이블에서 사용자 정보 조회
    userinfo = {}

    try:
        cursor.callproc('SP_KEYM_GET_USR_INFO_ID_PW', [user_id, user_pw])
        column_names_list = [x[0] for x in cursor.description]

        result_user_info = []

        for row in cursor.fetchall():
            result_user_info.append(dict(zip(column_names_list, row)))

        # 해당 ID와 PW를 가지는 사용자가 존재할 경우 로그인 성공
        if result_user_info:
            userinfo = result_user_info[0]

            # 탈퇴한 사용자인 경우
            if userinfo['WITHDRAW_FLAG'] == 'Y':
                data = result_user_info

                # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
                user_id = None
                log_status = "REQUEST"
                output = data
                message = "You have withdrawn"
                success_flag = "Y"

                # log : DB 에 로그를 저장하는 함수
                # log_db : DB 에 저장한 로그값
                log_db = log(user_id, log_status, log_request, api, function, input, output, message, success_flag)
                logger.error(message, extra=logger_data)
                logger.error(log_db, extra=logger_data)

                result = "fail"
                status = "410"

                # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
                send = set_send(data, result, status)
                logger.error(send, extra=logger_data)

                return send

            # 관리자에의해 삭제된 사용자인 경우
            if userinfo['DELETE_FLAG'] == 'Y':
                data = result_user_info

                # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
                user_id = None
                log_status = "REQUEST"
                output = data
                message = "Deleted user"
                success_flag = "Y"

                # log : DB 에 로그를 저장하는 함수
                # log_db : DB 에 저장한 로그값
                log_db = log(user_id, log_status, log_request, api, function, input, output, message, success_flag)
                logger.error(message, extra=logger_data)
                logger.error(log_db, extra=logger_data)

                result = "fail"
                status = "410"

                # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
                send = set_send(data, result, status)
                logger.error(send, extra=logger_data)

                return send

            auth_list = userinfo['AUTH'].split(',')
            userinfo['AUTH'] = auth_list

            # 접속 API 호출
            # 사용자 key 반환
            access_info = access(user_id, user_ip)

            # 접속 테이블에 저장하는 도중 DB 에러가 난 경우
            if access_info['status'] == "400":
                access_info['status'] = "407"

                # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
                user_id = None
                log_status = "REQUEST"
                output = None
                message = "User information does not exist"
                success_flag = "Y"

                # log : DB 에 로그를 저장하는 함수
                # log_db : DB 에 저장한 로그값
                log_db = log(user_id, log_status, log_request, api, function, input, output, message, success_flag)
                logger.error(message, extra=logger_data)
                logger.error(log_db, extra=logger_data)

                send = access_info
                logger.error(send, extra=logger_data)

                return send

            # 접속 테이블에 저장이 된 경우
            userinfo["USER_KEY"] = access_info['data'][0]['result_data_3']

            # URL 추가
            if userinfo['MAIN_AUTH'] == 'MVIEW0001':
                userinfo['URL'] = '/notice'
            else:
                userinfo['URL'] = '/notadd'

            data = []
            data.append(userinfo)

            result = 'success'

            # 동일한 IP로 접속한 사용자가 없어 로그아웃이 되지 않은 경우
            if status != "201":
                status = "200"
                message = "login success"
            else:
                status = "201"
                message = "Logged out because there is a user with the same IP connection"

            # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
            user_id = None
            log_status = "REQUEST"
            output = data
            success_flag = "Y"

            # log : DB 에 로그를 저장하는 함수
            # log_db : DB 에 저장한 로그값
            log_db = log(user_id, log_status, log_request, api, function, input, output, message, success_flag)
            logger.info(message, extra=logger_data)
            logger.debug(log_db, extra=logger_data)

            # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
            send = set_send(data, result, status)
            logger.debug(send, extra=logger_data)

            return send

        # 해당 ID와 PW를 가지는 사용자가 존재하지 않을 경우
        else:
            data = []
            data.append(userinfo)

            # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
            user_id = None
            log_status = "ERROR"
            output = ""
            message = "User information corresponding to the input value does not exist"
            success_flag = "N"

            # log : DB 에 로그를 저장하는 함수
            # log_db : DB 에 저장한 로그값
            log_db = log(user_id, log_status, log_request, api, function, input, output, message, success_flag)
            logger.error(message, extra=logger_data)
            logger.error(log_db, extra=logger_data)

            result = "fail"
            status = "408"

            # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
            send = set_send(data, result, status)
            logger.error(send, extra=logger_data)

            return send

    except Exception as e:
        print("error type : ", type(e))
        print("error : ", e)

        data = []

        # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
        user_id = None
        log_status = "ERROR"
        output = ""
        message = "exception error"
        success_flag = "N"

        # log : DB 에 로그를 저장하는 함수
        # log_db : DB 에 저장한 로그값
        log_db = log(user_id, log_status, log_request, api, function, input, output, message, success_flag)
        logger.error(message, extra=logger_data)
        logger.error(log_db, extra=logger_data)

        result = "fail"
        status = "409"

        # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
        send = set_send(data, result, status)
        logger.error(send, extra=logger_data)

        return send

    finally:
        connection.close()
