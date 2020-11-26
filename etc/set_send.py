
# -*- coding: utf-8 -*-

from etc.set_data import set_data
from etc.set_datetime_to_str import set_datetime_to_str

# API 결과값 설정
# data : 최종적으로 출력하려는 API 결과값에서 실제 값
# result : API 성공 여부
# status : API 상태코드
def set_send(data, result, status):

    data = set_data(data)
    data = set_datetime_to_str(data)

    send = {}

    send['data'] = data
    send['result'] = result
    send['status'] = status

    return send