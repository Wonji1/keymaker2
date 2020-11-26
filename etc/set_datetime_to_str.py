
# -*- coding: utf-8 -*-

import datetime

# 디비에서 불러온 날짜, 시간 정보 str 으로 변경
# data : 최종적으로 출력하려는 API 결과값
def set_datetime_to_str(data):
    # datetime.timedelta 타입은 json 에서 지원하지 않기 때문에 str 으로 변환
    # datetime.date 타입은 변환하지 않고 출력할 경우 datetime.date 타입만의 방식으로 출력되므로 str 으로 변한

    # 입력된 data 에 저장된 값이 있는지 확인
    if not data:
        return data

    for info in data:
        key_list = info.keys()

        for key in key_list:
            value = info[key]

            if type(value) == datetime.timedelta or type(value) == datetime.date:
                info[key] = str(value)

    return data