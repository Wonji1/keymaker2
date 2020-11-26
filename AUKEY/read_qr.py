
# -*- coding: utf-8 -*-
from flask import request
from pyzbar.pyzbar import decode
from PIL import Image
import time
import os
import sys
from sqlalchemy import create_engine

from etc.set_log import set_log
from .crop_qr import crop_qr

from AUSYS.log import log

from AUUSE.get_user_info_from_key import get_user_info_from_key
from AUUSE.set_user_API_req import set_user_API_req

from etc.set_send import set_send
from etc.createFolder import createFolder
from config.config_set import key_path
from config.config_set import db_data

# QR 코드를 인식하는 함수
# user_key : API 를 호출하는 사용자의 키
# image : QR 코드 이미지
# image_name : QR 코드 이미지 이름(확장자 포함)
# image_size : QR 코드 이미지 크기
def read_qr(user_key, image, image_name, image_size):

    # 로그를 남기기 위한 값
    # user_ip : API 를 호출한 사용자의 ip
    # user_id : API 를 호출한 사용자의 id
    user_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    user_id = None
    # 파이썬의 logging 함수를 불러오는 함수
    logger = set_log()
    # 받아온 user_ip, user_id 를 로그에 추가
    logger_data = {'clientip' : user_ip, 'user_id' : user_id}
    logger.info("Request read_qr", extra=logger_data)
    time_start = time.time()

    log_request = "read_qr"

    # 사용자의 마지막 API 변경 함수
    set_user_API_req(user_key, log_request)
    logger.info("Request set_user_API_req", extra=logger_data)

    # DB 에 로그를 남기기 위해 입력값, 요청값, api, function 명 등을 정의
    input = {}
    input['user_key'] = user_key
    input['image'] = image
    input['image_name'] = image_name
    input['image_size'] = image_size
    log_request = "read_qr"
    api = os.path.split(__file__)[1]
    function = sys._getframe().f_code.co_name

    engine = create_engine(db_data)
    connection = engine.raw_connection()
    cursor = connection.cursor()

    try:

        # 입력받은 사용자 키를 이용하여 사용자의 아이디, 권한 조회
        send = get_user_info_from_key(user_key)
        logger.info("Get user information", extra=logger_data)

        # 접속해있는 사용자가 아닐 경우
        if send['status'] == "201":

            # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
            user_id = None
            log_status = "ERROR"
            output = None
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
            message = "get_user_info_from_key DB error"
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

            user_id = send['data'][0]['result_data_1']

            # 이미지가 제대로 입력되지 않았을 경우
            if not image:

                # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
                log_status = "ERROR"
                output = None
                message = "Image is None"
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

            # 서버에 저장할 이미지명 변경(현재날짜 + 현재시간 + 등록한 사용자 ID)
            if image_name:
                file_name_split = image_name.split('.')
                extension = file_name_split[1]
            else:
                extension = "png"

            image_name_ori = image_name
            image_name = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + user_id + "." + extension

            image_path = key_path
            # createFolder : 해당 폴더가 없을 경우 폴더를 만드는 함수
            createFolder(image_path)

            # 서버 업로드
            image.save(image_path + "/" + image_name)
            logger.info("Image upload", extra=logger_data)

            # QR 코드 값 추출
            # 이미지 업로드 후 QR 코드값을 추출할 것 -> 추출 후 업로드하면 이미지가 깨짐
            decode_data = decode(Image.open(image))
            logger.info("Recognize the image", extra=logger_data)

            # 원본 이미지로 인식이 안될 경우 이미지 처리
            if not decode_data:
                logger.info("Image recognition failed", extra=logger_data)
                send = crop_qr(user_id, image, image_name, image_path)

                # 이미지가 제대로 인식되지 않았을 경우
                if send['status'] != "200":

                    # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
                    log_status = "ERROR"
                    output = None
                    message = "Image is not QR code"
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
                else:
                    # crop_qr 함수를 거쳐 인식에 성공한 경우
                    logger.info("Image recognition succeed", extra=logger_data)
                    url = send['data'][0]['qr_key']

            # crop_qr 을 실행하기 전에 인식에 성공한 경우
            else:
                logger.info("Image recognition succeed", extra=logger_data)
                # 이미지 인식
                url = decode_data[0].data.decode('utf-8')
                # 회사에서 사용하는 QR 코드의 경우 앞의 16자리까지가 QR 코드의 값이므로 16자리까지 문자열 자르기
                url = url[:16]

            # 이미지 정보 DB 에 저장
            cursor.callproc('SP_KEYM_ADD_KEY_IMAGE_INFO', [image_name_ori, image_name, image_path, image_size, url])

            logger.info("save image information", extra=logger_data)

            column_names_list = [x[0] for x in cursor.description]
            result_key_info = []

            for row in cursor.fetchall():
                result_key_info.append(dict(zip(column_names_list, row)))

            qr_data = {}
            qr_data['qr_key'] = url
            qr_data['index'] = result_key_info[0]['IN_INT_PK_KMKITN_KEYIMAGEINFO']
            qr_data['time'] = time.time() - time_start

            data = []
            data.append(qr_data)

            # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
            log_status = "REQUEST"
            output = data
            message = None
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

        error = {}
        error['error'] = e

        # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
        user_id = None
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
        result = "fail"
        status = "404"

        # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
        send = set_send(data, result, status)
        logger.error(send, extra=logger_data)

        return send

    finally:
        connection.close()
