
# -*- coding: utf-8 -*-

import qrcode
import time
import os
import sys

from flask import request

from AUSYS.log import log

from config.config_set import key_path
from etc.set_log import set_log

from etc.set_send import set_send
from etc.createFolder import createFolder

# 특정 값(url)을 가지는 QR 코드 이미지를 만드는 함수
# 배포하지 않음(테스트용)
# url : QR 코드 이미지에 담기는 값
# image_name : QR 코드 이미지의 이름, 확장자는 입력하지 않음(ex. test.png -> test 입력)
def create_qr(url, image_name):

    # 로그를 남기기 위한 값
    # user_ip : API 를 호출한 사용자의 ip
    # user_id : API 를 호출한 사용자의 id
    user_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    user_id = None
    # 파이썬의 logging 함수를 불러오는 함수
    logger = set_log()
    # 받아온 user_ip, user_id 를 로그에 추가
    logger_data = {'clientip' : user_ip, 'user_id' : user_id}

    logger.info("Request create_qr", extra=logger_data)

    # DB 에 로그를 남기기 위해 입력값, 요청값, api, function 명 등을 정의
    input = {}
    input['url'] = url
    input['image_name'] = image_name
    log_request = "create_qr"
    api = os.path.split(__file__)[1]
    function = sys._getframe().f_code.co_name

    try:

        # 입력값이 하나라도 없을 경우
        if url == "" or url is None or image_name == "" or image_name is None:
            # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
            user_id = None
            log_status = "ERROR"
            output = ""
            message = "URL or QR name is None"
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
            status = "400"

            # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
            send = set_send(data, result, status)
            logger.error(send, extra=logger_data)

            return send

        # 입력한 이미지 이름에 확장자 설정
        qr_name = image_name + ".png"

        # DB 또는 서버에 저장할 QR 코드 이미지의 이름으로 변경(현재 날짜 + 현재 시간)
        qr_name_ori = qr_name
        qr_name = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + ".png"

        # 이미지 저장 경로 설정
        image_path = key_path
        # createFolder : 해당 폴더가 없을 경우 폴더를 만드는 함수
        createFolder(image_path)

        # 입력한 url 을 포함하는 QR 코드 이미지 생성
        image = qrcode.make(url)
        # QR 코드 이미지 서버에 업로드
        image.save(key_path + qr_name)
        logger.info("Image upload", extra=logger_data)

        # DB 에 저장할 QR 코드 정보 설정
        qr_data = {}
        qr_data['OR_NAME_ORI'] = qr_name_ori
        qr_data['QR_NAME'] = qr_name
        qr_data['QR_PATH'] = key_path + qr_name
        qr_data['QR_URL'] = url

        # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
        user_id = None
        log_status = "REQUEST"
        output = qr_data
        message = "create_qr success"
        success_flag = "Y"

        # log : DB 에 로그를 저장하는 함수
        # log_db : DB 에 저장한 로그값
        log_db = log(user_id, log_status, log_request, api, function, input, output, message, success_flag)
        logger.info(message, extra=logger_data)
        logger.debug(log_db, extra=logger_data)

        data = []
        data.append(qr_data)
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
