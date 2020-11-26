
# -*- coding: utf-8 -*-
import os
import sys

from flask import request

from AUPAT.get_company_list import get_company_list

from AUSYS.log import log

from AUUSE.get_user_info_from_key import get_user_info_from_key
from AUUSE.set_user_API_req import set_user_API_req

from config.config_set import db_data
from etc.check_text import check_text
from etc.set_send import set_send
from etc.set_log import set_log

import datetime
from sqlalchemy import create_engine

# 업체 정보를 등록하는 함수
# user_key : API 를 호출하는 사용자의 키
# com_name : 업체명
# com_address : 주소
# phone_number : 전화번호
# email : 이메일
# memo : 메모
# day_max_count : 하루 당 최대 발급 개수
# max_count : 최대 발급 개수
# date_max : 발급할 수 있는 최대 날짜
def add_company(user_key, com_name, com_address, phone_number, email, memo, day_max_count, max_count, date_max):

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

    log_request = "add_company"

    # 사용자의 마지막 API 변경 함수
    set_user_API_req(user_key, log_request)
    logger.info("Request set_user_API_req", extra=logger_data)

    # DB 에 로그를 남기기 위해 입력값, 요청값, api, function 명 등을 정의
    input = {}
    input['user_key'] = user_key
    input['com_name'] = com_name
    input['com_address'] = com_address
    input['phone_number'] = phone_number
    input['email'] = email
    input['memo'] = memo
    input['day_max_count'] = day_max_count
    input['max_count'] = max_count
    input['date_max'] = date_max

    api = os.path.split(__file__)[1]
    function = sys._getframe().f_code.co_name

    input_list = [user_key, com_name, com_address, phone_number, email, memo, day_max_count, max_count, date_max]

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
            status = "416"

            # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
            send = set_send(data, result, status)
            logger.error(send, extra=logger_data)

            return send

    # 업체를 등록한 사용자 ID
    add_user_id = "admin01"
    # DB 에서 조회한 사용자 정보
    user_info = {}

    status = check_text('user_key', user_key)

    # 사용자의 키가 8자리 str, 0~9사이의 문자가 아니면 등록한 사용자 ID null 값으로 지정(회원가입 전 업체 자가 등록 요청)
    if len(user_key) != 8 or type(user_key) != str or status == "400":
        status = "200"
        user_info['AUTH'] = "AUPAT0006"
        requset_type = "add_company_user"

    # 사용자의 키로 사용자 아이디 조회
    else:
        user_info = get_user_info_from_key(user_key)
        logger.info("Get user information", extra=logger_data)

        # 업체 정보를 등록하려는 사용자의 아이디
        add_user_id = user_info['data'][0]['result_data_1']

        requset_type = ""

        # AUPAT0006(업체정보 자가 등록)만 있을 경우 키 발급 설정란은 null 값으로 지정(다른 값 타입, 크기 확인)
        # AUPAT0005(업체정보 등록)만 있을 경우 키 발급 설정란은 null 값으로 지정(다른 값 타입, 크기 확인)
        # AUPAT0006, AUPAT0005, AUPAT0004(업체정보 키 발급 설정)이 있을 경우 변경 X(다른 값 타입, 크기 확인)
        for auth in user_info['data'][0]['AUTH']:
            # 모든 사용자가 AUPAT0006 권한을 가진다는 전제
            if auth == 'AUPAT0006':
                if 'AUPAT0005' in user_info['data'][0]['AUTH']:
                    if 'AUPAT0004' in user_info['data'][0]['AUTH']:
                        requset_type = "add_company_admin_key"
                    else:
                        requset_type = "add_company_admin"
                else:
                    requset_type = "add_company_user"

    # 회원가입 시 업체정보 자가 등록을 요청했을 경우
    if requset_type == "add_company_user":
        day_max_count = None
        max_count = None
        date_max = None
        add_user_id = None

    # 관리자가 업체정보 등록을 요청했을 경우
    elif requset_type == "add_company_admin":
        day_max_count = None
        max_count = None
        date_max = None

    # 관리자가 업체정보 등록 + 키 발급 설정을 요청했을 경우 설정하는 값 X

    # 업체명 중복 확인
    com_list = get_company_list(user_key, com_name, '0', '0')
    logger.info("Check duplication of company name", extra=logger_data)
    if com_list:
        com_list = com_list['data']
    else:
        com_list['data'] = []

    for com_info in com_list:
        com_name_exist = com_info['COMPANY_NAME']

        # 업체명이 중복될 경우
        if com_name_exist == com_name:
            # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
            user_id = None
            log_status = "ERROR"
            output = ""
            message = "Company name duplicates"
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

    # 입력된 정보 타입, 크기 확인
    # 업체명
    if len(com_name) == 0 or len(com_name) > 100:
        status = "401"
    if type(com_name) != str:
        status = "402"

    # 주소
    if len(com_address) > 100:
        status = "403"
    if type(com_address) != str:
        status = "404"

    # 전화번호
    if len(phone_number) < 12 or len(phone_number) > 13:
        status = "405"
    if type(com_name) != str:
        status = "406"

    # 이메일
    if len(email) > 100:
        status = "407"
    if type(email) != str:
        status = "408"

    # 메모
    if len(memo) > 255:
        status = "409"
    if type(memo) != str:
        status = "410"

    # 하루 최대 발급 개수
    if type(day_max_count) != int:
        status = "411"

    # 최대 발급 개수
    if type(max_count) != int:
        status = "412"

    # 최대 발급 날짜
    if type(date_max) != str:
        status = "413"

    # null 가능 값 중 입력하지 않은 값 null 설정
    if not com_address or com_address == "":
        com_address = None
    if not phone_number or phone_number == "":
        phone_number = None
    if not email or email == "":
        email = None
    if not memo or memo == "":
        memo = None
    if not day_max_count or day_max_count == "":
        day_max_count = None
    if not max_count or max_count == "":
        max_count = None

    if date_max is not None:
        convert_date = datetime.datetime.strptime(date_max, "%Y-%m-%d").date()
    else:
        convert_date = None

    # 업체 저장
    engine = create_engine(db_data)
    connection = engine.raw_connection()
    cursor = connection.cursor()

    try:
        cursor.callproc('SP_KEYM_ADD_COM_INFO', [com_name, com_address, phone_number, email, memo, day_max_count,
                                                 max_count, convert_date, add_user_id])
        logger.info("Save company information", extra=logger_data)

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
        status = '414'
        result = "fail"

        # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
        send = set_send(data, result, status)
        logger.error(send, extra=logger_data)

        return send

    finally:
        connection.close()

    # 업체를 등록한 후 등록된 모든 업체 리스트를 불러옴
    com_list = get_company_list(user_key, '', '0', '0')
    logger.info("Get company information", extra=logger_data)

    send = {}

    # 업체 리스트 조회 시 에러가 났을 경우
    if com_list['status'] == "400":
        # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
        user_id = None
        log_status = "ERROR"
        output = ""
        message = "An error occurred while inquiring about the company"
        success_flag = "N"

        # log : DB 에 로그를 저장하는 함수
        # log_db : DB 에 저장한 로그값
        log_db = log(user_id, log_status, log_request, api, function, input, output, message, success_flag)
        logger.error(message, extra=logger_data)
        logger.error(log_db, extra=logger_data)

        error = {}
        error['error'] = message

        data = []
        data.append(error)
        result = "fail"
        status = "415"

        # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
        send = set_send(data, result, status)
        logger.error(send, extra=logger_data)

        return send

    else:
        status = "200"

    com_list = com_list['data']

    # 등록이 성공했을 경우 로그 저장
    # 상태코드 : 요청
    if status == "200":
        log_status = 'LGSTA0001'
        if requset_type == "add_company_user":
            # 요청코드 : 업체정보 자가 등록
            log_request = 'LGPAT0006'
        elif requset_type == "add_company_admin":
            # 요청코드 : 업체정보 등록
            log_request = 'LGPAT0005'
        else:
            # 요청코드 : 업체정보 키 발급 설정
            log_request = 'LGPAT0004'
        # log(add_user_id, log_status, log_request)

    data = com_list

    # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
    user_id = None
    log_status = "REQUEST"
    output = data
    message = "add_company success"
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
