
# -*- coding: utf-8 -*-

# 입력한 문자열의 타입과 길이를 판단
# type_text : 입력한 문자열의 타입
# text : 문자열
def check_type_len(type_text, text):

    # 200 : 적합
    # 400 : 타입 부적합
    # 401 : 크기 부적합

    # 사용자 ID, PW
    if type_text == 'user_id' or type_text == 'user_pw':
        if type(text) != str:
            return "400"
        if len(text) <= 0 or len(text) > 21:
            return "401"

    # 사용자명
    if type_text == 'user_name':
        if type(text) != str:
            return "400"
        if len(text) <= 0 or len(text) > 26:
            return "401"

    # 회사명
    if type_text == 'company':
        if type(text) != str:
            return "400"
        if len(text) <= 0 or len(text) > 101:
            return "401"

    # 부서명, 직급, 이메일
    if type_text == 'department' or type_text == 'position' or type_text == 'email':
        if type(text) != str:
            return "400"
        if len(text) > 101:
            return "401"

    # 전화번호
    if type_text == 'phone_number':
        if type(text) != str:
            return "400"
        if len(text) > 21:
            return "401"

    return "200"