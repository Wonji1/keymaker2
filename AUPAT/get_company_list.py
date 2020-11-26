
# -*- coding: utf-8 -*-
import os
import sys

from flask import request

from AUSYS.log import log

from AUUSE.get_user_info_from_key import get_user_info_from_key
from AUUSE.set_user_API_req import set_user_API_req

from config.config_set import db_data
from etc.set_log import set_log
from etc.set_send import set_send
from etc.check_text import check_text

from sqlalchemy import create_engine

# 업체 정보 리스트 조회
# user_key : API 를 호출하는 사용자의 키
# company_name : 업체명(검색 내용)
# current_page : 현재 페이지
# count_per_page : 페이지당 개수
def get_company_list(user_key, company_name, current_page, count_per_page):

    # 로그를 남기기 위한 값
    # user_ip : API 를 호출한 사용자의 ip
    # user_id : API 를 호출한 사용자의 id
    user_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    user_id = None
    # 파이썬의 logging 함수를 불러오는 함수
    logger = set_log()
    # 받아온 user_ip, user_id 를 로그에 추가
    logger_data = {'clientip': user_ip, 'user_id': user_id}
    logger.info("Request add_company", extra=logger_data)

    log_request = "get_company_list"

    # 사용자의 마지막 API 변경 함수
    set_user_API_req(user_key, log_request)
    logger.info("Request set_user_API_req", extra=logger_data)

    # DB 에 로그를 남기기 위해 입력값, 요청값, api, function 명 등을 정의
    input = {}
    input['user_key'] = user_key
    input['company_name'] = company_name
    input['current_page'] = current_page
    input['count_per_page'] = count_per_page

    api = os.path.split(__file__)[1]
    function = sys._getframe().f_code.co_name

    input_list = [user_key, company_name, current_page, count_per_page]

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
            status = "401"

            # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
            send = set_send(data, result, status)
            logger.error(send, extra=logger_data)

            return send

    engine = create_engine(db_data)
    connection = engine.raw_connection()
    cursor = connection.cursor()

    try:
        # 업체 정보 리스트 조회
        cursor.callproc('SP_KEYM_GET_COM_LIST', [company_name, current_page, count_per_page])
        column_names_list = [x[0] for x in cursor.description]

        result_company_info = []

        for row in cursor.fetchall():
            result_company_info.append(dict(zip(column_names_list, row)))

        # 회원가입 화면에서 회사명 리스트를 불러올 경우
        if current_page == '0' or count_per_page == '0':
            URL = '/reg'
        # 업체정보 조회 화면에서 회사명 리스트를 불러올 경우
        else:
            URL = '/업체명리스트조회페이지'

        if result_company_info:
            for company_info in result_company_info:
                company_info['URL'] = URL
            status = "200"
        else:
            result_company_info = []
            status = "201"

        data = result_company_info

        # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
        user_id = None
        log_status = "REQUEST"
        output = data
        message = "get_company_list success"
        success_flag = "Y"

        # log : DB 에 로그를 저장하는 함수
        # log_db : DB 에 저장한 로그값
        log_db = log(user_id, log_status, log_request, api, function, input, output, message, success_flag)
        logger.info(message, extra=logger_data)
        logger.debug(log_db, extra=logger_data)

        result = "success"

        # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
        send = set_send(data, result, status)
        logger.debug(send, extra=logger_data)

        # 사용자 key 를 이용해서 사용자 정보 조회
        status_key = check_text('user_key', user_key)

        user_info = {}

        # 회원가입 시 업체 리스트를 표출하는 경우
        if len(user_key) != 8 or type(user_key) != str or status_key == "400":
            request_type = "regitser"

        # 업체정보 조회 페이지에서 호출한 경우
        else:
            request_type = "search_company"
            user_info = get_user_info_from_key(user_key)

        # 사용자 정보 조회하는 중에 DB 에러가 난 경우
        if user_info:
            if user_info['status'] == "400":
                # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
                user_id = None
                log_status = "ERROR"
                output = ""
                message = "Error occurred while inquiring user information"
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

            user_id = user_info['data'][0]['result_data_1']

        # 업체정보 조회 화면에서 조회한 경우에만 로그 저장
        # 회원가입 전 업체명 리스트를 확인하는 과정에서는 로그인 전 단계이므로 로그를 저장할 수 없음
        if request_type == "search_company":
            # 로그 API 호출
            # 상태코드 : 요청
            # 요청코드 : 업체정보 조회
            # log_status = 'LGSTA0001'
            # log_request = 'LGPAT0001'

            # log(user_id, log_status, log_request)
            print("")

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
        status = "400"

        # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
        send = set_send(data, result, status)
        logger.error(send, extra=logger_data)

        return send

    finally:
        connection.close()