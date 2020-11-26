
# -*- coding: utf-8 -*-

import cv2
import numpy as np
from flask import request
from pyzbar.pyzbar import decode
from PIL import Image
import os
import sys

from AUSYS.log import log

from etc.createFolder import createFolder
from etc.set_log import set_log
from etc.set_send import set_send
from config.config_set import key_fail_path
from config.config_set import key_success_path

# 경계값을 구하기 위하여 adaptive threshold 시, block_size 를 구함
# block_size : adaptive threshold 는 구역을 나누어 경계값을 구함 나누는 구역의 크기를 block_size 라 함
# block_size 의 값이 클수록(width 와 가까워질수록) 일반 threshold 와 결과가 비슷해짐
# block_size 의 값이 작을수록 이미지의 경계값을 더욱 세밀하게 구할 수 있음
def get_block_size(width):
    if width > 500:

        block_size = width / 20

        # block_size 가 소수일 경우 정수로 변경
        if type(block_size) == float:
            block_size = int(block_size)

        # block_size 가 짝수일 경우 홀수로 변경
        # block 은 해당 구역의 평균값 또는 가우시안 값을 구하여 현재 구역의 중심점에 값을 적용하므로 홀수값이어야 함
        if block_size % 2 == 0:
            block_size += 1

    elif width > 100:
        block_size = width / 10

        # block_size 가 소수일 경우 정수로 변경
        if type(block_size) == float:
            block_size = int(block_size)

        # block_size 가 짝수일 경우 홀수로 변경
        if block_size % 2 == 0:
            block_size += 1

    else:
        block_size = width / 5

    # 설정된 block_size 의 크기가 10픽셀 미만일 경우 19로 설정
    if block_size < 10:
        block_size = 19

    return block_size

# 블러 처리 함수
# 물결 현상이 있는 이미지일 경우 물결 현상을 완화시키기 위하여 블러 처리 함수 사용
def blur(image_input):
    # ksize : 입력한 이미지를 블러처리 하기 위해 설정하는 필터 크기
    # 필터 : 입력한 이미지를 (0,0) 지점부터 (x,y) 지점까지 이동하여 필터의 크기의 범위만큼 블러처리하여 중심점에 블러처리값 적용
    image_blur = cv2.blur(image_input, ksize=(3, 3))

    return image_blur

# read_qr 에서 입력한 이미지의 인식이 제대로 이루어지지 않았을 경우 이미지를 가공하여 인식률을 높임
# user_id : 사용자의 id, 로그 및 서버에 업로드할 이미지의 이름을 재설정할때 사용
# image : read_qr 에서 입력한 원본 이미지
# image_name : 입력한 이미지의 실제 이름
# image_path : 입력한 이미지가 업로드 되어 있는 경로
def crop_qr(user_id, image, image_name, image_path):

    log_request = "crop_qr"

    # 로그를 남기기 위한 값
    # user_ip : API 를 호출한 사용자의 ip
    # user_id : API 를 호출한 사용자의 id
    user_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    # user_id = None
    # 파이썬의 logging 함수를 불러오는 함수
    logger = set_log()
    # 받아온 user_ip, user_id 를 로그에 추가
    logger_data = {'clientip': user_ip, 'user_id': user_id}
    logger.info("Request crop_qr", extra=logger_data)

    # DB 에 로그를 남기기 위해 입력값, 요청값, api, function 명 등을 정의
    input = {}
    input['user_id'] = user_id
    input['image'] = image
    input['image_name'] = image_name
    api = os.path.split(__file__)[1]
    function = sys._getframe().f_code.co_name

    try:
        # QR 코드의 가장자리에 있는 3개(또는 그 이상)의 겹쳐진 네모 이미지를 찾음(인식 코드라 표기)
        # 이미지의 컨투어 박스를 구하고 QR 코드의 인식 코드의 특징을 이용하여 조건에 맞는 컨투어 박스를 인식 코드라 판단
        # 인식 코드를 기준으로 QR 코드를 크롭하고, QR 코드의 색상 히스토그램을 이용하여 적절한 임계값을 찾아 흑백 변환을 뚜렷하게 함
        # 뚜렷하게 보정한 QR 코드를 다시 인식

        # 아래 코드에서 사용할 대부분의 함수가 cv2 에서 이미지 호출한 결과의 타입(numpy array)에 적합
        # 폼으로 받아온 원본 이미지를 서버에 업로드 하고 해당 경로와 이름을 이용하여 다시 호출
        # imread : 해당 경로에 저장되어 있는 이미지를 numpy array 형식으로 불러오기 (cv2.imread(경로 + 이름))
        image = cv2.imread(image_path + "/" + image_name)
        logger.info("Image read", extra=logger_data)

        # 입력한 이미지의 높이, 너비, 채널
        # shape : 이미지의 높이, 너비, 채널의 값을 추출하는 함수
        height, width, channel = image.shape

        # cvtColor : 경계값을 추출하기 위해 흑백 변환
        # COLOR_RGB2GRAY : RGB 에서 GRAY 로 변환
        # cv2.cvtColor(변환할 이미지, 변환할 방식)
        image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        logger.info("Image convert to gray", extra=logger_data)

        # 이미지 너비에 따라 적합한 block 의 크기를 구하는 함수
        block_size = get_block_size(width)

        # 경계값 추출
        # adaptiveThreshold : 필터의 크기를 설정해 이미지의 (0,0) 에서 (x,y) 까지 이동하면서 해당 구역만큼의 값을 구하여 적용
        # 일반 threshold 는 전체 이미지의 임계값을 설정해 해당 임계값을 넘기면 설정해둔 값(보통 흰색 또는 검정)으로 적용되기때문에
        # 어두운 이미지거나 밝은 이미지의 경우 정확한 경계값을 찾기 어려움
        # adaptiveThreshold 를 이용하면 일부 영역의 값들을 비교하여 적절한 값을 찾기 때문에 더욱 세밀한 경계값을 추출할 수 있음
        # cv2.adaptiveThreshold(입력 이미지, 임계값을 넘길 경우 적용될 값, 경계값을 추출할 방법, 경계값을 추출한 후 이미지 표현 방법, 필터 크기, 필터를 씌운 후 결과값에서 뺄 값)
        # ADAPTIVE_THRESH_GAUSSIAN_C : 가우시안 방법을 이용하여 필터 중심점에 결과값 적용
        # THRESH_BINARY : 선명한 흑백 대비로 이미지 표현
        image_adapthresh = cv2.adaptiveThreshold(
            image_gray,
            maxValue=255.0,
            adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            thresholdType=cv2.THRESH_BINARY,
            blockSize=block_size,
            C=9
        )
        logger.info("The boundary value of the image was obtained", extra=logger_data)

        # 추출한 경계값에서 덩어리를 이루고 있는 묶음들의 경계선 표시(같은 색상을 가지는 묶음을 하나의 객체로 인식하기 위해 하는 과정)
        # 컨투어(contour) : 같은 레벨(색상 등)을 가지는 하나의 덩어리
        # hierarchy : 컨투어의 상하구조
        # cv2.findContours(입력 이미지, 컨투어를 찾는 방법, 컨투어를 찾을 때 사용하는 근사화 방법)
        # RETR_LIST : 모든 컨투어 라인을 찾지만, 상하구조(hierachy)관계를 구성하지 않음
        # CHAIN_APPROX_SIMPLE : 컨투어 라인을 그릴 수 있는 포인트만 반환
        contours, hierarchy = cv2.findContours(
            image_adapthresh,
            mode=cv2.RETR_LIST,
            method=cv2.CHAIN_APPROX_SIMPLE
        )

        # 원본 이미지와 같은 크기, 채널을 가지는 검은색(0 : zero) 배경의 이미지 생성
        image_contour = np.zeros((height, width, channel), dtype=np.uint8)

        # 검은색 배경의 이미지에 컨투어 표시
        # cv2.drawContours(입력 이미지, 컨투어 라인 정보, 컨투어 라인 번호, 색상, 두께)
        cv2.drawContours(image_contour, contours=contours, contourIdx=-1, color=(255, 255, 255), thickness=2)
        logger.info("It draw a contour", extra=logger_data)

        # 원본 이미지와 같은 크기, 채널을 가지는 검은색 배경의 이미지 생성
        image_contours_box = np.zeros((height, width, channel), dtype=np.uint8)

        # 모든 컨투어 박스의 정보를 저장
        # 컨투어 박스 : 하나의 컨투어를 감싸는 박스 -> QR 코드를 찾기 위해 박스의 크기 및 비율 등을 비교하기 위해 사용
        list_contours = []
        # 각 컨투어의 인덱스, 동일한 컨투어인지 비교하는데에 사용
        index = 0

        # 입력한 이미지에서 추출해낸 컨투어가 존재하지 않을 경우
        if not contours:

            # 인식 실패한 이미지 저장
            # Image.fromarray : numpy 배열을 이미지 객체로 변경(서버에 업로드 하기 위해서는 실제 이미지로 변경해야 함)
            image_fail = Image.fromarray(image)
            # createFolder : 해당 폴더가 없을 경우 폴더를 만드는 함수
            createFolder(key_fail_path)
            # 서버 업로드
            image_fail.save(key_fail_path + "/" + image_name)
            logger.error("Fail image upload", extra=logger_data)

            # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
            log_status = "ERROR"
            output = None
            message = "Image is one color"
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

        # findContours 함수로 찾아낸 컨투어들을 이용하여 컨투어 박스를 구하고, 각 컨투어의 정보 저장
        for contour in contours:
            # boundingRect : 컨투어를 둘러싸는 박스의 정보 추출
            x, y, w, h = cv2.boundingRect(contour)
            # 검은색 배경의 이미지에 컨투어 박스 표시
            # rectangle : 입력 이미지에 직사각형을 그림
            # cv2.rectangle(입력 이미지, 직사각형의 왼쪽 위의 점, 직사각형의 오른쪽 아래 점, 색상, 두께)
            cv2.rectangle(image_contours_box, pt1=(x, y), pt2=(x + w, y + h), color=(255, 255, 255), thickness=2)

            # 컨투어 정보 저장
            # x, y : 직사각형의 왼쪽 위의 지점
            # x_end, y_end : 직사각형의 오른쪽 아래 지점, w 와 h 는 x 또는 y 의 점까지 포함한 길이이기 때문에 -1 추가
            list_contours.append({
                'contour': contour,
                'index': index,
                'x': x,
                'y': y,
                'x_end': x + w - 1,
                'y_end': y + h - 1,
                'w': w,
                'h': h,
                'cx': int(x + (w / 2)),
                'cy': int(y + (h / 2))
            })

            index += 1

        logger.info("It find contour", extra=logger_data)

        # 너무 작은 컨투어 박스(길이가 10픽셀 이하)는 제거
        # QR 코드의 인식 코드의 너비, 높이의 비율이 약 1
        # 컨투어 박스의 비율이 1/2이하 또는 2 이상인 것 제거

        # 크기 또는 비율 조건에 맞지 않은 컨투어 박스를 제외한 컨투어 박스를 저장할 리스트
        list_contours_except_mini = []
        # 크기 또는 비율 조건에 맞지 않은 컨투어 박스를 제외한 컨투어 박스를 그릴 이미지
        image_contours_box_except_mini = np.zeros((height, width, channel), dtype=np.uint8)

        for contour in list_contours:

            # 현재 컨투어의 x, y, w, h
            x = contour['x']
            y = contour['y']
            w = contour['w']
            h = contour['h']

            # 너비가 10픽셀 이하인 컨투어 박스 제외
            if w < 10:
                continue

            # 비율 조건에 맞지 않은 컨투어 박스 제외
            if w / h < 1 / 2 or w / h > 2:
                continue

            # 입력 이미지의 너비와 높이의 90프로 이상인 컨투어박스(입력 이미지의 크기와 같은 컨투어 박스) 제외
            if w > width * 0.9:
                continue
            if h > height * 0.9:
                continue

            # cv2.rectangle(입력 이미지, 직사각형의 왼쪽 위의 점, 직사각형의 오른쪽 아래 점, 색상, 두께)
            cv2.rectangle(image_contours_box_except_mini, pt1=(x, y), pt2=(x + w, y + h), color=(255, 255, 255),
                          thickness=2)

            # 기준에 맞는 컨투어들 따로 저장
            list_contours_except_mini.append(contour)

        logger.info("It exclude contours that are too small or too large", extra=logger_data)

        # 작은 컨투어를 제외하였더니 남은 컨투어가 없는 경우
        if not list_contours_except_mini:

            # 인식 실패한 이미지 저장
            # Image.fromarray : numpy 배열을 이미지 객체로 변경(서버에 업로드 하기 위해서는 실제 이미지로 변경해야 함)
            image_fail = Image.fromarray(image)
            # createFolder : 해당 폴더가 없을 경우 폴더를 만드는 함수
            createFolder(key_fail_path)
            # 서버 업로드
            image_fail.save(key_fail_path + "/" + image_name)
            logger.error("Fail image upload", extra=logger_data)

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
            status = "401"

            # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
            send = set_send(data, result, status)
            logger.error(send, extra=logger_data)

            return send

        # QR 코드의 인식 코드 후보군의 개수
        count = 0
        # QR 코드의 인식 코드 후보군들의 리스트를 저장한 리스트
        list_contours_QR_possible_list = []

        # 컨투어 박스 리스트(list_contours_except_mini)에서 하나의 컨투어(contour_1)를 기준으로 또 다른 컨투어(contour_2)와 비교하여 인식 코드일 가능성이 있는지 판단
        # 두번째 컨투어(contour_2)가 첫번째 컨투어(contour_1)에 포함되어 있다고 전제하고 그 조건을 벗어나는 경우는 제외
        for contour_1 in list_contours_except_mini:

            # QR 코드의 인식 코드일 가능성이 있는 컨투어 박스들을 저장한 리스트
            list_contours_QR_possible = []

            for contour_2 in list_contours_except_mini:

                # 첫번째 컨투어의 정보
                x_1 = contour_1['x']
                y_1 = contour_1['y']
                x_end_1 = contour_1['x_end']
                y_end_1 = contour_1['y_end']
                w_1 = contour_1['w']
                h_1 = contour_1['h']
                cx_1 = contour_1['cx']
                cy_1 = contour_1['cy']

                # 두번째 컨투어의 정보
                x_2 = contour_2['x']
                y_2 = contour_2['y']
                x_end_2 = contour_2['x_end']
                y_end_2 = contour_2['y_end']
                w_2 = contour_2['w']
                h_2 = contour_2['h']
                cx_2 = contour_2['cx']
                cy_2 = contour_2['cy']

                # 비교하는 두 컨투어가 일치할 경우 제외
                if contour_1['index'] == contour_2['index']:
                    continue

                # 두번째 컨투어가 첫번째 컨투어 안에 속해있지 않은 경우 제외
                if x_1 > x_2 or y_1 > y_2 or x_end_1 < x_end_2 or y_end_1 < y_end_2:
                    continue

                # 첫번째 컨투어보다 두번째 컨투어의 면적이 더 클 경우 제외
                if w_1 * h_1 < w_2 * h_2:
                    continue

                # 첫번째 컨투어의 너비와 높이보다 두번째 컨투어의 너비와 높이가 넓은 경우 제외
                if w_1 < w_2 or h_1 < h_2:
                    continue

                # 첫번째 컨투어의 중심점이 두번째 컴투어의 내부에 있지 않을 경우 제외
                if cx_1 < x_2 or cx_1 > x_end_2 or cy_1 < y_2 or cy_1 > y_end_2:
                    continue

                # 두번째 컨투어가 첫번째 컨투어 면적의 1/10보다 작은 경우
                if w_2 * h_2 < (w_1 * h_1) / 10:
                    continue

                # 해당 조건을 만족하는 두번째 컨투어들을 저장
                list_contours_QR_possible.append(contour_2)

            # 두번째 컨투어가 하나라도 저장이 되었을 경우에만 첫번째 컨투어 저장
            if list_contours_QR_possible:

                # QR 코드의 인식 코드일 가능성이 있는 컨투어 박스들을 그릴 이미지
                image_contours_QR = np.zeros((height, width, channel), dtype=np.uint8)

                # QR 코드의 인식 코드일 가능성이 있는 컨투어 박스들 그리기
                # cv2.rectangle(입력 이미지, 직사각형의 왼쪽 위의 점, 직사각형의 오른쪽 아래 점, 색상, 두께)
                for contour in list_contours_QR_possible:
                    cv2.rectangle(
                        image_contours_QR,
                        pt1=(contour['x'], contour['y']),
                        pt2=(contour['x'] + contour['w'], contour['y'] + contour['h']),
                        color=(255, 255, 255),
                        thickness=2
                    )

                # 첫번째 컨투어 저장
                list_contours_QR_possible.append(contour_1)
                # 기준이 되었던 첫번째 컨투어는 다른 색상으로 그리기
                # cv2.rectangle(입력 이미지, 직사각형의 왼쪽 위의 점, 직사각형의 오른쪽 아래 점, 색상, 두께)
                cv2.rectangle(image_contours_QR, pt1=(x_1, y_1), pt2=(x_1 + w_1, y_1 + h_1), color=(0, 0, 255), thickness=2)

                # 컨투어 박스가 총 2개 이하인 것 제외
                if len(list_contours_QR_possible) < 3:
                    continue

                # QR 인식 코드 최종 후보군 저장
                list_contours_QR_possible_list.append(list_contours_QR_possible)

                count += 1

        logger.info("Only store the contour box that matches the QR code", extra=logger_data)

        # QR 코드의 인식 코드 후보군이 존재하지 않는 경우
        if not list_contours_QR_possible_list:

            # 인식 실패한 이미지 저장
            # Image.fromarray : numpy 배열을 이미지 객체로 변경(서버에 업로드 하기 위해서는 실제 이미지로 변경해야 함)
            image_fail = Image.fromarray(image)
            # createFolder : 해당 폴더가 없을 경우 폴더를 만드는 함수
            createFolder(key_fail_path)
            # 서버 업로드
            image_fail.save(key_fail_path + "/" + image_name)
            logger.error("Fail image upload", extra=logger_data)

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
            status = "402"

            # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
            send = set_send(data, result, status)
            logger.error(send, extra=logger_data)

            return send

        # QR 코드의 인식 코드 후보군들을 하나의 리스트에 저장

        # 최종 후보군 컨투어 박스들을 그리는 이미지
        image_contours_QR_except_equal = np.zeros((height, width, channel), dtype=np.uint8)
        # 최종 후보군 컨투어박스들을 저장하는 리스트
        list_contours_except_equal = []

        # 후보군에 들었던 모든 컨투어 저장
        for list_contours in list_contours_QR_possible_list:
            for contour in list_contours:

                # 최종 후보군(컨투어)들의 인덱스를 담은 리스트(저장 시 중복 확인)
                list_index_contours_except_equal = []
                for contour_except_equal in list_contours_except_equal:
                    list_index_contours_except_equal.append(contour_except_equal['index'])

                # 저장한 컨투어가 하나이상 존재할 경우
                if list_contours_except_equal:
                    # 저장하려는 컨투어가 이미 저장되어 있을 경우
                    if contour['index'] in list_index_contours_except_equal:
                        continue
                    # 저장하려는 컨투어가 저장되어 있지 않을 경우
                    else:
                        list_contours_except_equal.append(contour)

                # 저장한 컨투어가 없을 경우
                else:
                    list_contours_except_equal.append(contour)

        logger.info("Combine all Contour Boxes", extra=logger_data)

        # 최종 후보군에 저장된 컨투어 박스가 존재할 경우 해당 컨투어 박스 그리기
        if list_contours_except_equal:

            for contour in list_contours_except_equal:
                # cv2.rectangle(입력 이미지, 직사각형의 왼쪽 위의 점, 직사각형의 오른쪽 아래 점, 색상, 두께)
                cv2.rectangle(image_contours_QR_except_equal,
                              pt1=(contour['x'], contour['y']),
                              pt2=(contour['x'] + contour['w'], contour['y'] + contour['h']),
                              color=(0, 0, 255), thickness=2)

        # 최종 후보군이 존재하지 않는 경우
        else:

            # 인식 실패한 이미지 저장
            # Image.fromarray : numpy 배열을 이미지 객체로 변경(서버에 업로드 하기 위해서는 실제 이미지로 변경해야 함)
            image_fail = Image.fromarray(image)
            # createFolder : 해당 폴더가 없을 경우 폴더를 만드는 함수
            createFolder(key_fail_path)
            # 서버 업로드
            image_fail.save(key_fail_path + "/" + image_name)
            logger.error("Fail image upload", extra=logger_data)

            # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
            log_status = "ERROR"
            output = None
            message = "Final candidate for Contour Box does not exist"
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

        # 최종 후보군에 든 컨투어 박스의 가장자리 크롭

        x_start = width
        y_start = height
        x_end = 0
        y_end = 0

        # 최종 후보군들의 가장자리 값 구하기
        for contour in list_contours_except_equal:
            if contour['x'] < x_start:
                x_start = contour['x']
            if contour['y'] < y_start:
                y_start = contour['y']

            if contour['x_end'] > x_end:
                x_end = contour['x_end']
            if contour['y_end'] > y_end:
                y_end = contour['y_end']

        # QR 코드라고 인식한 부분의 너비와 높이
        QR_width = x_end - x_start
        QR_height = y_end - y_start

        # 실제 QR 코드보다 여유를 두고 크롭
        x_start = int(x_start - QR_width * 0.1)
        y_start = int(y_start - QR_height * 0.1)
        x_end = int(x_end + QR_width * 0.1)
        y_end = int(y_end + QR_height * 0.1)

        logger.info("Obtain the size of the image you want to crop", extra=logger_data)

        # 크롭할 이미지의 크기가 음수거나 원본 이미지의 크기를 벗어날 경우 0 또는 원본 이미지의 크기로 설정
        if x_start < 0:
            x_start = 0
        if y_start < 0:
            y_start = 0
        if x_end > width:
            x_end = width
        if y_end > height:
            y_end = height

        # 크롭할 너비, 높이, 중심점
        QR_width = x_end - x_start
        QR_height = y_end - y_start
        QR_cx = int(x_start + QR_width / 2)
        QR_cy = int(y_start + QR_height / 2)

        # QR 코드로 인식한 부분을 검은 이미지에 표시
        # cv2.rectangle(입력 이미지, 직사각형의 왼쪽 위의 점, 직사각형의 오른쪽 아래 점, 색상, 두께)
        cv2.rectangle(image_contours_QR_except_equal, pt1=(x_start, y_start), pt2=(x_end, y_end), color=(0, 0, 255),
                      thickness=2)
        cv2.rectangle(image_contours_QR_except_equal, pt1=(QR_cx, QR_cy), pt2=(QR_cx, QR_cy), color=(255, 0, 0),
                      thickness=5)

        # 원본 이미지에 QR 코드로 인식한 부분 크롭
        # getRectSubPix : 직사각형의 모양으로 이미지 크롭
        # cv2.getRectSubPix(입력 이미지, 크롭 이미지의 크기, 크롭 이미지의 중심점)
        image_crop = cv2.getRectSubPix(
            image,
            patchSize=(QR_width, QR_height),
            center=(QR_cx, QR_cy)
        )
        logger.info("Crop the image", extra=logger_data)

        # cv2.imread 를 이용하여 불러와 있는 이미지를 인식할 경우
        decode_data = decode(image_crop)
        logger.info("Recognize the image", extra=logger_data)

        # 이미지를 크롭한 것만으로 인식에 성공한 경우
        if decode_data:

            logger.info("Image recognition succeed", extra=logger_data)

            # 이미지 인식
            url = decode_data[0].data.decode('utf-8')
            # 회사에서 사용하는 QR 코드의 경우 앞의 16자리까지가 QR 코드의 값이므로 16자리까지 문자열 자르기
            url = url[:16]

            # 출력값에 인식한 결과값 추가
            qr_data = {}
            qr_data['qr_key'] = url

            # 크롭한 이미지 저장
            # Image.fromarray : numpy 배열을 이미지 객체로 변경(서버에 업로드 하기 위해서는 실제 이미지로 변경해야 함)
            image_crop_scalar = Image.fromarray(image_crop)
            # createFolder : 해당 폴더가 없을 경우 폴더를 만드는 함수
            createFolder(key_success_path)
            # 서버 업로드
            image_crop_scalar.save(key_success_path + "/" + image_name)
            logger.error("Success image upload", extra=logger_data)

            # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
            log_status = "REQUEST"
            output = None
            message = ""
            success_flag = "Y"

            # log : DB 에 로그를 저장하는 함수
            # log_db : DB 에 저장한 로그값
            log_db = log(user_id, log_status, log_request, api, function, input, output, message, success_flag)
            logger.error(message, extra=logger_data)
            logger.error(log_db, extra=logger_data)

            data = []
            data.append(qr_data)
            result = "success"
            status = "200"

            # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
            send = set_send(data, result, status)
            logger.error(send, extra=logger_data)

            return send

        logger.info("Image recognition failed", extra=logger_data)
        logger.info("Blur the image", extra=logger_data)

        # 이미지를 크롭하였으나 인식에 실패한 경우 -> 화면 울림 현상이 있는 경우
        # 화면에 있는 QR 코드를 찍었을 경우 화면 울림 현상 완화
        # 원본 이미지에서 크롭하였으니 다시 흑백 변환

        # cvtColor : 경계값을 추출하기 위해 흑백 변환
        # COLOR_RGB2GRAY : RGB 에서 GRAY 로 변환
        # cv2.cvtColor(변환할 이미지, 변환할 방식)
        image_crop_gray = cv2.cvtColor(image_crop, cv2.COLOR_RGB2GRAY)
        image_crop_blur = image_crop_gray

        # 블러 처리 횟수
        count_blur = 0

        # 인식이 될 때까지 블러 처리
        while True:
            image_crop_blur = blur(image_crop_blur)
            decode_data_blur = decode(image_crop_blur)

            count_blur += 1

            # 블러처리한 이미지가 인식이 될 경우 종료
            if decode_data_blur:
                break

            # 1000번을 블러 처리 해도 인식이 되지 않을 경우 인식 실패로 판단
            if count_blur == 100:

                logger.info("Image recognition failed", extra=logger_data)

                # 인식 실패한 이미지 저장
                # Image.fromarray : numpy 배열을 이미지 객체로 변경(서버에 업로드 하기 위해서는 실제 이미지로 변경해야 함)
                image_fail = Image.fromarray(image_crop_blur)
                # createFolder : 해당 폴더가 없을 경우 폴더를 만드는 함수
                createFolder(key_fail_path)
                # 서버 업로드
                image_fail.save(key_fail_path + "/" + image_name)
                logger.error("Fail image upload", extra=logger_data)

                # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
                log_status = "ERROR"
                output = None
                message = "Failed to recognize"
                success_flag = "N"

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

        # 이미지 인식
        url = decode_data_blur[0].data.decode('utf-8')
        # 회사에서 사용하는 QR 코드의 경우 앞의 16자리까지가 QR 코드의 값이므로 16자리까지 문자열 자르기
        url = url[:16]

        # 출력값에 인식값 추가
        qr_data = {}
        qr_data['qr_key'] = url

        # 인식 성공
        # 블러처리한 이미지 저장
        # Image.fromarray : numpy 배열을 이미지 객체로 변경(서버에 업로드 하기 위해서는 실제 이미지로 변경해야 함)
        image_crop_blur = Image.fromarray(image_crop_blur)
        # createFolder : 해당 폴더가 없을 경우 폴더를 만드는 함수
        createFolder(key_success_path)
        # 서버 업로드
        image_crop_blur.save(key_success_path + "/" + image_name)
        logger.error("Success image upload", extra=logger_data)

        # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
        log_status = "REQUEST"
        output = None
        message = "crop_qr success"
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
        print("##################### crop_qr 에서 EXCEPTION error 발생")
        print("error type : ", type(e))
        print("error : ", e)

        error = {}
        error['error'] = e

        # 인식 실패한 이미지 저장
        # Image.fromarray : numpy 배열을 이미지 객체로 변경(서버에 업로드 하기 위해서는 실제 이미지로 변경해야 함)
        image_fail = Image.fromarray(image)
        # createFolder : 해당 폴더가 없을 경우 폴더를 만드는 함수
        createFolder(key_fail_path)
        # 서버 업로드
        image_fail.save(key_fail_path + "/" + image_name)
        logger.error("Fail image upload", extra=logger_data)

        # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag
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
        status = "405"

        # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
        send = set_send(data, result, status)
        logger.error(send, extra=logger_data)

        return send
