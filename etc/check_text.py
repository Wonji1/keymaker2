
# -*- coding: utf-8 -*-

from config.config import special_char

# 입력한 문자열이 적합한지 판단하는 함수
# type : 입력한 문자열의 타입
# text : 문자열
def check_text(type, text):

    # type 이 input_db 일 경우 db 에 입력할 수 있는지 판단
    # 쿼리문에 입력하는 모든 값에서 특수문자 제외
    # ['#', '\\', '?', '/', '%', '_']
    if type == "input_db":
        for char in text:
            # 입력한 문자에서 입력할 수 없는 특수문자를 포함하고 있는 경우
            if char in special_char:
                return "400"

    # type 이 id 또는 pw 일 경우
    # 아스키코드 이용해서 영문자, 숫자 이외의 문자 찾아내기
    if type == 'id' or type == 'pw':
        # 숫자(0~9) : 48~57
        # 영어 대문자(A~Z) : 65~90
        # 영어 소문자(a~z) : 97~122
        for char in text:
            char_ascii = ord(char)

            # 현재 문자가 숫자일 경우 넘어감
            if 48 <= char_ascii <= 57:
                continue
            # 현재 문자가 대문자일 경우 넘어감
            if 65 <= char_ascii <= 90:
                continue
            # 현재 문자가 소문자일 경우 넘어감
            if 97 <= char_ascii <= 122:
                continue

            return "400"

    # type 이 user_key 일 경우
    # 아스키코드 이용해서 영문자, 숫자 이외의 문자 찾아내기
    if type == 'user_key':
        # 숫자(0~9) : 48~57
        for char in text:
            char_ascii = ord(char)

            # 현재 문자가 숫자일 경우 넘어감
            if 48 <= char_ascii <= 57:
                continue

            return "400"

    # type 이 name 일 경우
    # 아스키코드 이용해서 특수문자 제외하기
    if type == 'name':
        for char in text:
            char_ascii = ord(char)

            # 현재 문자가 특수문자 일 경우 400리턴
            if 33 <= char_ascii <= 47:
                return "401"
            if 58 <= char_ascii <= 64:
                return "401"
            if 91 <= char_ascii <= 96:
                return "401"
            if 123 <= char_ascii <= 126:
                return "401"

    # 특수문자 허용

    # type 이 company 또는 department 일 경우
    # 아스키코드 이용해서 영문자, 숫자, 한글 이외의 문자 찾아내기
    if type == 'company' or type == 'department':
        for char in text:
            char_ascii = ord(char)

            # 현재 문자가 숫자일 경우 넘어감
            if 48 <= char_ascii <= 57:
                continue
            # 현재 문자가 대문자일 경우 넘어감
            if 65 <= char_ascii <= 90:
                continue
            # 현재 문자가 소문자일 경우 넘어감
            if 97 <= char_ascii <= 122:
                continue
            # 현재 문자가 '가'~'힣'사이의 문자일 경우 넘어감
            if 44032 <= char_ascii <= 55203:
                continue
            # 현재 문자가 'ㄱ'~'ㅎ'사이의 문자일 경우 넘어감
            if 12593 <= char_ascii <= 12622:
                continue
            # 현재 문자가 'ㅏ'~'ㅣ'사이의 문자일 경우 넘어감
            if 12623 <= char_ascii <= 12643:
                continue

            return "400"

    return "200"
