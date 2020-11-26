
# -*- coding: utf-8 -*-

from AUUSE.get_user_info_from_key import get_user_info_from_key

from etc.set_send import set_send

# API 를 호출한 사용자가 해당 기능을 수행할 권한이 있는지 판단
# user_key : 권한을 확인할 사용자의 key
# request_type : 요청타입
# 요청타입이 자기 정보 수정일 경우 AUUSE0007 입력
# 요청타입이 사용자 정보 수정일 경우 AUUSE0002 입력
# 요청타입이 탈퇴일 경우 AUUSE0008 입력
# 요청타입이 사용자 정보 삭제일 경우 AUUSE0003 입력
def check_auth(user_key, request_type):

    data = []
    result = "fail"

    # 사용자 정보 조회
    user_info = get_user_info_from_key(user_key)

    # 접속 정보가 없는 경우
    if not user_info['data']:
        status = "400"

        # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
        send = set_send(data, result, status)

        return send

    # 동일한 key 에 대한 정보는 하나밖에 존재하지 않음
    data = user_info['data']
    user_auth_list = data[0]['AUTH']

    # 자기 정보 수정 'AUUSE0007'
    if request_type == "set_my_info":
        request_auth = "AUUSE0007"
    # 사용자 정보 수정 'AUUSE0002'
    elif request_type == "set_user_info":
        request_auth = "AUUSE0002"
    # 탈퇴 'AUUSE0008'
    elif request_type == "withdraw":
        request_auth = "AUUSE0008"
    # 사용자 정보 삭제 'AUUSE0003'
    elif request_type == "del_user_info":
        request_auth = "AUUSE0003"
    # 위 패턴으로 각 요청마다 필요한 권한 지정

    # 권한 확인
    for user_auth in user_auth_list:

        # API 를 호출한 사용자가 필요한 권한을 가지고 있는 경우
        if user_auth == request_auth:
            result = "success"
            status = "200"

            # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
            send = set_send(data, result, status)

            return send

    # API 를 호출한 사용자가 필요한 권한을 가지고 있지 않은 경우
    result = "fail"
    status = "401"

    # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
    send = set_send(data, result, status)

    return send