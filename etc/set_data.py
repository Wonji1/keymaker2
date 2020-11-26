
# -*- coding: utf-8 -*-

# user_id, user_pw, user_ip 의 변수명(딕셔너리의 키 값) 변경
# data : 최종적으로 출력하려는 API 결과값
def set_data(data):

    # 입력된 data 에 저장된 값이 있는지 확인
    if not data:
        return data

    # data 에 값이 있을 경우 딕셔너리의 키 값 중 USER_ID, USER_PW, USER_KEY 와 일치하는 것이 있는지 확인
    for info in data:
        key_list = info.keys()

        for key in key_list:
            if key == "USER_ID" or key == "PK_KMUITN_USERINFO" or key == "user_id" or key == "FK_KMMITN_MODULEINFO" or key == "FK_KMKITN_KEYINFO":

                value = info[key]

                del info[key]

                key_name = "result_data_1"

                info[key_name] = value

            elif key == "USER_PW" or key == "user_pw":
                value = info[key]

                del info[key]

                key_name = "result_data_2"

                info[key_name] = value

            elif key == "USER_KEY" or key == "user_key" or key == "PK_KMAUTN_ACCESSUSER":
                value = info[key]

                del info[key]

                key_name = "result_data_3"

                info[key_name] = value

    return data
