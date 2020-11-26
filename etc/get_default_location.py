
# -*- coding: utf-8 -*-

import os
import sys

from flask import request

from AUSYS.log import log
from config.config import location_data
from etc.get_loc_info import get_loc_info

# ip 로 위치정보를 호출하는 API 가 제대로 된 값을 가져오지 못할 경우 실패한 메시지 설정 및 미리 저장되어 있는 주소 정보로 저장
# user_id : 위치정보가 추출되는 사용자의 id
def get_default_location(user_id):

    # DB 에 로그를 남기기 위해 입력값, 요청값, api, function 명 등을 정의
    input = {}
    input['user_id'] = user_id

    log_request = "issue_key"
    api = os.path.split(__file__)[1]
    function = sys._getframe().f_code.co_name

    user_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

    loc_api_data = get_loc_info(user_ip)

    message = ""
    success_flag = "Y"
    log_status = "REQUEST"

    # 주소가 정상적으로 추출되지 않았을 경우 디폴트값으로 정해둔 위경도값 입력
    if loc_api_data['returnCode'] != 0:

        success_flag = "N"
        log_status = "ERROR"

        # 지역정보를 찾을 수 없는 경우
        if loc_api_data['returnCode'] == "131000":
            message = "Local information not found. Use other IP address."

        # 공인 IP 가 아닌 경우거나 IP 주소 형식이 잘못된 경우
        elif loc_api_data['returnCode'] == "131001":
            message = "Either it is not an authorized IP or the IP address format is incorrect."

        # GeoLocation 서버의 오류 발생, 고객 센터 문의 필요
        elif loc_api_data['returnCode'] == "131002":
            message = "An error has occurred in the GeoLocation server. Please contact customer service."

        # 설정한 Quota 한도만큼 API 를 사용했을 경우
        elif loc_api_data['returnCode'] == "131003":
            message = "API was used as much as the Quota limit."

        # 네이버 클라우드 API 를 신청하지 않고 사용한 경우
        elif loc_api_data['returnCode'] == "131004":
            message = "You didn't apply for Naver Cloud API."

        # 네이버 클라우드 API 이용하여 받는 결과값과 같은 형태로 만들기
        country = location_data['country']
        code = location_data['code']
        r1 = location_data['r1']
        r2 = location_data['r2']
        r3 = location_data['r3']
        lat = location_data['lat']
        long = location_data['long']
        net = location_data['net']

        geoLocation = {}
        geoLocation['country'] = country
        geoLocation['code'] = code
        geoLocation['r1'] = r1
        geoLocation['r2'] = r2
        geoLocation['r3'] = r3
        geoLocation['lat'] = lat
        geoLocation['long'] = long
        geoLocation['net'] = net

        loc_api_data['geoLocation'] = geoLocation

    # user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag

    output = loc_api_data

    log(user_id, log_status, log_request, api, function, input, output, message, success_flag)

    return loc_api_data
