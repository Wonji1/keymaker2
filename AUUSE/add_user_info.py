
# -*- coding: utf-8 -*-
import os
import sys

from flask import request

from AUPAT.get_company_list import get_company_list

from AUSYS.log import log

from AUUSE.get_user_info import get_user_info

from etc.check_type_len import check_type_len
from etc.set_log import set_log
from etc.set_send import set_send
from etc.check_text import check_text
from config.config_set import db_data

from sqlalchemy import create_engine

# 사용자 정보 저장
# user_id : 사용자 id
# user_pw : 사용자 pw
# user_name : 사용자명
# company_name : 사용자가 속해있는 회사명
# department : 사용자가 속해있는 부서명
# position : 사용자의 직급
# phone_number : 사용자의 핸드폰 번호
# email : 사용자의 이메일 주소
def add_user_info(user_id, user_pw, user_name, company_name, department, position, phone_number, email):

    # 로그를 남기기 위한 값
    # user_ip : API 를 호출한 사용자의 ip
    # user_id : API 를 호출한 사용자의 id
    user_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    # user_id = None
    # 파이썬의 logging 함수를 불러오는 함수
    logger = set_log()
    # 받아온 user_ip, user_id 를 로그에 추가
    logger_data = {'clientip': user_ip, 'user_id': user_id}

    logger.info("Request add_user_info", extra=logger_data)

    # DB 에 로그를 남기기 위해 입력값, 요청값, api, function 명 등을 정의
    input = {}
    input['user_id'] = user_id
    input['user_pw'] = user_pw
    input['user_name'] = user_name
    input['company_name'] = company_name
    input['department'] = department
    input['position'] = position
    input['phone_number'] = phone_number
    input['email'] = email

    log_request = "add_user_info"
    api = os.path.split(__file__)[1]
    function = sys._getframe().f_code.co_name

    status = "200"

    # 입력된 정보 타입, 크기 확인
    status_id = check_type_len('user_id', user_id)
    status_pw = check_type_len('user_pw', user_pw)
    status_name = check_type_len('user_name', user_name)
    status_company = check_type_len('company', company_name)
    status_department = check_type_len('department', department)
    status_position = check_type_len('position', position)
    status_phone_number = check_type_len('phone_number', phone_number)
    status_email = check_type_len('email', email)

    logger.info("Check the type and size of the input value", extra=logger_data)

    if status_id == "400":
        status = "400"
    elif status_id == "401":
        status = "401"

    if status_pw == "400":
        status = "402"
    elif status_pw == "401":
        status = "403"

    if status_name == "400":
        status = "404"
    elif status_name == "401":
        status = "405"

    if status_company == "400":
        status = "406"
    elif status_company == "401":
        status = "407"

    if status_department == "400":
        status = "408"
    elif status_department == "401":
        status = "409"

    if status_position == "400":
        status = "410"
    elif status_position == "401":
        status = "411"

    if status_phone_number == "400":
        status = "412"
    elif status_phone_number == "401":
        if phone_number != '0':
            status = "413"
        else:
            status = "200"

    if status_email == "400":
        status = "414"
    elif status_email == "401":
        status = "415"

    # 입력값 중 하나라도 조건에 맞지 않으면 리턴
    if status != "200":

        # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
        user_id = None
        log_status = "ERROR"
        output = ""
        message = "The type and size of the input value are not appropriate"
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

    # 조건이 있는 값 적합성 확인
    status_id = check_text('id', user_id)
    status_pw = check_text('pw', user_pw)
    status_name = check_text('name', user_name)
    status_company = check_text('company', company_name)
    status_department = check_text('department', department)

    logger.info("Check the conditions of the input values", extra=logger_data)

    # 조건에 맞지 않은 값이 존재하는 경우
    if status_id != "200":
        status = "416"
    if status_pw != "200":
        status = "417"
    if status_name != "200":
        status = "418"
    if status_company != "200":
        status = "419"
    if status_department != "200":
        status = "420"

    if status != "200":

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

    # 입력된 값이 없는 것 중 null 가능 값은 None 으로 변환
    if not department or department == "" or department == '0':
        department = None
    if not position or position == "" or position == '0':
        position = None
    if not phone_number or phone_number == "" or phone_number == '0':
        phone_number = None
    if not email or email == "" or email == '0':
        email = None

    # 아이디 중복 확인
    user_list = get_user_info("0", user_id, "login_before")
    status = user_list['status']

    # ID 에 영어, 숫자 이외의 문자가 있는 경우
    if status == "400":
        status = "416"
        message = "The ID does not meet the conditions"
    # 동일한 ID 조회 과정에서 DB 에러가 난 경우
    elif status == "401":
        status = "421"
        message = "DB error occurred while inquiring the same ID"
    # 동일한 ID 가 존재하는 경우
    elif status == "200":
        status = "422"
        message = "The same ID exists"
    # 동일한 ID 가 존재하지 않는 경우
    else:
        status = "200"

    if status != "200":
        # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
        user_id = None
        log_status = "ERROR"
        output = ""
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

    # 회사명 존재 확인
    company_list = get_company_list('0', company_name, '0', '0')
    status = company_list['status']
    data = company_list['data']

    logger.info("Check that the selected company name exists", extra=logger_data)

    # 동일한 회사명 조회 과정에서 DB 에러가 난 경우
    if status == "400":
        status = "423"
        message = "DB error occurred while inquiring the same company name"
    # 동일한 회사명이 존재하지 않는 경우
    elif status == "201":
        status = "424"
        message = "The same company name does not exist"
    # 동일한 회사명이 존재하는 경우
    else:
        for company in data:
            company_name_exist = company['COMPANY_NAME']

            if company_name == company_name_exist:
                status = "200"
                # 사용자가 선택한 회사명의 회사 ID
                company_id_exist = company['PK_KMPTTN_PARTNER']
                break
            # 입력한 회사명이 포함되는 회사명이 존재하나 완벽하게 일치하지는 않는 경우 동일한 회사명이 존재하지 않는 경우로 설정
            else:
                status = "424"
                message = "The same company name does not exist"

    if status != "200":
        # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
        user_id = None
        log_status = "ERROR"
        output = ""
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

    # 사용자 정보 저장
    engine = create_engine(db_data)
    connection = engine.raw_connection()
    cursor = connection.cursor()

    try:
        cursor.callproc('SP_KEYM_ADD_USR_INFO', [user_id, user_pw, user_name, company_id_exist,
                                                 department, position, phone_number, email])
        logger.info("Store the user's information", extra=logger_data)

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
        status = "425"

        # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
        send = set_send(data, result, status)
        logger.error(send, extra=logger_data)

        return send

    finally:
        connection.close()

    data = []

    # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
    user_id = None
    log_status = "REQUEST"
    output = data
    message = "add_user_info success"
    success_flag = "Y"

    # log : DB 에 로그를 저장하는 함수
    # log_db : DB 에 저장한 로그값
    log_db = log(user_id, log_status, log_request, api, function, input, output, message, success_flag)
    logger.info(message, extra=logger_data)
    logger.debug(log_db, extra=logger_data)

    # 성공 여부 반환
    result = "success"
    status = "200"

    # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
    send = set_send(data, result, status)
    logger.debug(send, extra=logger_data)

    return send