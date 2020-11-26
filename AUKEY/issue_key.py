
# -*- coding: utf-8 -*-

import os
import sys
import requests
from flask import request
from sqlalchemy import create_engine
import json

from AUKEY.issue_key_random_result import issue_key_random_result
from AUSYS.log import log

from AUUSE.get_user_info_from_key import get_user_info_from_key
from AUUSE.set_user_API_req import set_user_API_req

from config.config_set import db_data
from config.config import key_data
from config.config_set import key_url
from etc.get_default_location import get_default_location
from etc.get_loc_info import get_loc_info
from etc.set_log import set_log
from etc.set_send import set_send

# QR 코드 값을 입력하여 발급키를 받는 함수
# user_key : API 를 호출하는 사용자의 키
# index : read_qr 을 호출했을 경우 DB 에 저장한 인식키 인덱스(read_qr 을 호출하지 않았을 경우 0 입력됨)
# req_serial : QR 코드 값
# version : 발급키를 받는 API 버전
# memo : 인식키 메모
def issue_key(user_key, index, user_ip, req_serial, version, memo):

    # 로그를 남기기 위한 값
    # user_ip : API 를 호출한 사용자의 ip
    # user_id : API 를 호출한 사용자의 id
    # user_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    user_id = None
    # 파이썬의 logging 함수를 불러오는 함수
    logger = set_log()
    # 받아온 user_ip, user_id 를 로그에 추가
    logger_data = {'clientip': user_ip, 'user_id': user_id}
    logger.info("Request issue_key", extra=logger_data)

    log_request = "issue_key"

    # 사용자의 마지막 API 변경 함수
    set_user_API_req(user_key, log_request)
    logger.info("Request set_user_API_req", extra=logger_data)

    # DB 에 로그를 남기기 위해 입력값, 요청값, api, function 명 등을 정의
    input = {}
    input['user_key'] = user_key
    input['index'] = index
    input['req_serial'] = req_serial
    input['version'] = version
    if memo == "0":
        memo = None
    input['memo'] = memo

    log_request = "issue_key"
    api = os.path.split(__file__)[1]
    function = sys._getframe().f_code.co_name

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

        # 이미지가 실제로 존재하는 지 확인
        '''
        if not image:
            data = []
            result = "fail"
            status = "402"

            send = set_send(data, result, status)

            return send
        '''

        # 인식키 발급 권한이 있는지 확인
        user_auth_list = send['data'][0]['AUTH']

        engine = create_engine(db_data)
        connection = engine.raw_connection()
        cursor = connection.cursor()

        logger.info("Check authority", extra=logger_data)

        try:
            user_id = send['data'][0]['result_data_1']
            # 사용자 정보 조회
            cursor.callproc('SP_KEYM_GET_USR_DETAILS_INFO', [user_id])
            column_names_list = [x[0] for x in cursor.description]
            result_user_info = []

            for row in cursor.fetchall():
                result_user_info.append(dict(zip(column_names_list, row)))

            company_id = result_user_info[0]['FK_KMUITN_USERINFO']
            # phone_number = result_user_info[0]['PHONE_NUMBER']

            # 전화번호가 하이픈(-)이 포함된 채로 저장되어 있었을 경우
            '''
            if '-' in phone_number:
                print(phone_number)
                number_list = phone_number.split('-')
                phone_number = ""
                for number_list in (0, len(number_list)-1):
                    print(number_list)
                    phone_number += number_list

                print(phone_number)
            '''

            # 사용자가 속해있는 회사 정보 조회
            cursor.callproc('SP_KEYM_GET_COM_DETAILS_INFO', [company_id])
            column_names_list = [x[0] for x in cursor.description]
            result_company_info = []

            for row in cursor.fetchall():
                result_company_info.append(dict(zip(column_names_list, row)))

            user_code = result_company_info[0]['USER_CODE']

            # user_code = "fa"
            phone_number = "01027231797"

            # 인식키 발급 권한 : 직원 발급 요청 'AUKEY0001', 파트너 발급 요청 'AUKEY0002'
            if user_code == "fa":
                request_auth = "AUKEY0001"
            else:
                request_auth = "AUKEY0002"

            for auth in user_auth_list:

                # 권한이 있을 경우 이미지 이름 변경 후 서버에 이미지 업로드
                if auth == request_auth:
                    logger.info("Authority exists", extra=logger_data)

                    code_check_version = "version"
                    app_version = key_data['app_version']

                    # check_version API 호출 (GET)
                    url_check_version = key_url + user_code + "/" + phone_number + "/" + code_check_version + "/" + app_version + "/Keona"
                    response_check_version = requests.get(url_check_version)
                    logger.info("call check_version API", extra=logger_data)

                    data_check_version = json.loads(response_check_version.text)

                    if data_check_version['Result'] == "ok":
                        logger.info("check_version API call succeeded", extra=logger_data)
                        session_key = data_check_version['SessionKey']
                    # check_version API 호출 실패
                    else:
                        logger.info("check_version API call failed", extra=logger_data)

                        # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
                        log_status = "REQUEST"
                        output = data_check_version
                        message = "check_version API error"
                        success_flag = "N"

                        # log : DB 에 로그를 저장하는 함수
                        # log_db : DB 에 저장한 로그값
                        log_db = log(user_id, log_status, log_request, api, function, input, output, message,
                                     success_flag)
                        logger.error(message, extra=logger_data)
                        logger.error(log_db, extra=logger_data)

                        data = []
                        result = "fail"
                        status = "403"

                        # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
                        send = set_send(data, result, status)
                        logger.error(send, extra=logger_data)

                        return send

                    # DB 저장
                    cursor.callproc('SP_KEYM_ADD_KEY_VERSION_INFO',
                                    [index, company_id, user_code, user_id, phone_number, app_version, session_key])

                    logger.info("save check_version API information", extra=logger_data)

                    column_names_list = [x[0] for x in cursor.description]
                    result_key_info = []

                    for row in cursor.fetchall():
                        result_key_info.append(dict(zip(column_names_list, row)))

                    # key version 테이블에 저장한 index 로 변경하여 key_info 테이블에 해당 index 로 저장
                    index = result_key_info[0]['IN_INT_PK_KMKVTN_KEYVERSION']

                    code_create_key = "makekey"

                    # ip 이용하여 주소 정보 찾기
                    location_data = get_default_location(user_id)
                    logger.info("Find address information using ip", extra=logger_data)

                    country = location_data['geoLocation']['country']
                    r1 = location_data['geoLocation']['r1']
                    r2 = location_data['geoLocation']['r2']
                    r3 = location_data['geoLocation']['r3']
                    address = r1 + " " + r2 + " " + r3

                    latitude = str(location_data['geoLocation']['lat'])
                    longitude = str(location_data['geoLocation']['long'])

                    logger.info("call create_key API", extra=logger_data)

                    # create_key API 호출 (POST)
                    url_create_key = key_url + user_code + "/" + session_key + "/" + code_create_key + "/" + version + "/Keona"
                    location = latitude + "," + longitude
                    post_data = {"location": location, "phonenumber": phone_number, "req_serial": req_serial}
                    response_create_key = requests.post(url_create_key, data=post_data)

                    data_create_key = json.loads(response_create_key.text)

                    if data_create_key['Result'] != "ok":
                        logger.info("create_key API call failed", extra=logger_data)

                        # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
                        log_status = "ERROR"
                        output = data_create_key
                        message = "create_key API error"
                        success_flag = "N"

                        # log : DB 에 로그를 저장하는 함수
                        # log_db : DB 에 저장한 로그값
                        log_db = log(user_id, log_status, log_request, api, function, input, output, message,
                                     success_flag)
                        logger.error(message, extra=logger_data)
                        logger.error(log_db, extra=logger_data)

                        data = []
                        result = "fail"
                        status = "404"

                        # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
                        send = set_send(data, result, status)
                        logger.error(send, extra=logger_data)

                        return send

                    logger.info("create_key API call succeeded", extra=logger_data)

                    data_create_key['qr_key'] = req_serial
                    issue_key = data_create_key['Key']

                    city = r1
                    state = r2
                    street = r3
                    user_name = result_user_info[0]['USER_NAME']

                    # DB 저장
                    cursor.callproc('SP_KEYM_ADD_KEY_INFO',
                                    [index, company_id, user_code, user_id, user_name, session_key, version, latitude, longitude,
                                     phone_number, req_serial, issue_key, memo, address, country, city, state, street])

                    logger.info("save create_key API information", extra=logger_data)

                    column_names_list = [x[0] for x in cursor.description]
                    result_key_info = []

                    for row in cursor.fetchall():
                        result_key_info.append(dict(zip(column_names_list, row)))

                    data = []
                    data.append(data_create_key)

                    # 로그 저장
                    # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
                    log_status = "REQUEST"
                    output = data
                    message = "issue_key success"
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

            # 인식키 발급 권한이 존재하지 않을 경우

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
            status = "405"

            # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
            send = set_send(data, result, status)
            logger.error(send, extra=logger_data)

            return send

        except Exception as e:
            print("error type : ", type(e))
            print("error : ", e)

            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # 회사 API 연결에 실패한 경우 랜덤값 출력하는 파일로 연결
            print("10061" in str(e))

            if "10061" in str(e):

                # DB 에 저장할 check_version api 값 임의 설정
                check_version_api_value = {}
                check_version_api_value['index'] = index
                check_version_api_value['company_id'] = company_id
                check_version_api_value['user_code'] = user_code
                check_version_api_value['user_id'] = user_id
                check_version_api_value['phone_number'] = phone_number
                check_version_api_value['app_version'] = app_version
                check_version_api_value['session_key'] = "session_key_tmp"

                # DB 에 저장할 create_key api 값 임의 설정
                create_key_api_value = {}
                create_key_api_value['index'] = index
                create_key_api_value['company_id'] = company_id
                create_key_api_value['user_code'] = user_code
                create_key_api_value['user_id'] = user_id
                create_key_api_value['user_name'] = result_user_info[0]['USER_NAME']
                create_key_api_value['session_key'] = "session_key_tmp"
                create_key_api_value['version'] = version

                # ip 이용하여 주소 정보 찾기
                location_data = get_default_location(user_id)

                country = location_data['geoLocation']['country']
                r1 = location_data['geoLocation']['r1']
                r2 = location_data['geoLocation']['r2']
                r3 = location_data['geoLocation']['r3']
                address = r1 + " " + r2 + " " + r3

                latitude = str(location_data['geoLocation']['lat'])
                longitude = str(location_data['geoLocation']['long'])

                create_key_api_value['latitude'] = latitude
                create_key_api_value['longitude'] = longitude
                create_key_api_value['phone_number'] = phone_number
                create_key_api_value['req_serial'] = req_serial
                create_key_api_value['issue_key'] = None
                create_key_api_value['memo'] = memo
                create_key_api_value['address'] = address
                create_key_api_value['country'] = country

                city = r1
                state = r2
                street = r3

                create_key_api_value['city'] = city
                create_key_api_value['state'] = state
                create_key_api_value['street'] = street

                Key = issue_key_random_result(version, check_version_api_value, create_key_api_value)
                print("대체 함수 실행")

                key_result = {}
                key_result['Key'] = Key
                key_result['Result'] = "success"
                key_result['qr_key'] = req_serial

                data = []
                data.append(key_result)

                status = "201"
                result = "success"
                send = set_send(data, result, status)

                return send

            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
            user_id = ""
            log_status = "EXCEPTION"
            output = ""
            message = e
            success_flag = "N"

            # log : DB 에 로그를 저장하는 함수
            # log_db : DB 에 저장한 로그값
            log_db = log(user_id, log_status, log_request, api, function, input, output, message, success_flag)
            logger.error(message, extra=logger_data)
            logger.error(log_db, extra=logger_data)

            data = []
            status = '480'
            result = "fail"

            # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
            send = set_send(data, result, status)
            logger.error(send, extra=logger_data)

            return send

        finally:
            connection.close()

