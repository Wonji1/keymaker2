
# -*- coding: utf-8 -*-

import random

# 회사 API 연결에 실패한 경우 랜덤값 출력
from sqlalchemy import create_engine

from config.config_set import db_data


def issue_key_random_result(version, check_version_api_value, create_key_api_value):

    # version 이 new 인 경우 8자리 랜덤 수 반환
    if version == "new":
        Key = random.randint(0, 99999999)
        Key = str(Key)

        if len(Key) != 8:
            Key = Key.zfill(8)
    # version 이 old 인 경우 6자리 랜덤 수 반환
    else:
        Key = random.randint(0, 999999)
        Key = str(Key)

        if len(Key) != 6:
            Key = Key.zfill(6)

    engine = create_engine(db_data)
    connection = engine.raw_connection()
    cursor = connection.cursor()

    # check_version API 결과 DB 저장
    index = check_version_api_value['index']
    company_id = check_version_api_value['company_id']
    user_code = check_version_api_value['user_code']
    user_id = check_version_api_value['user_id']
    phone_number = check_version_api_value['phone_number']
    app_version = check_version_api_value['app_version']
    session_key = check_version_api_value['session_key']

    cursor.callproc('SP_KEYM_ADD_KEY_VERSION_INFO',
                    [index, company_id, user_code, user_id, phone_number, app_version, session_key])

    # create_key API 결과 DB 저장
    index = create_key_api_value['index']
    company_id = create_key_api_value['company_id']
    user_code = create_key_api_value['user_code']
    user_id = create_key_api_value['user_id']
    user_name = create_key_api_value['user_name']
    session_key = create_key_api_value['session_key']
    version = create_key_api_value['version']
    latitude = create_key_api_value['latitude']
    longitude = create_key_api_value['longitude']
    phone_number = create_key_api_value['phone_number']
    req_serial = create_key_api_value['req_serial']
    issue_key = Key
    memo = create_key_api_value['memo']
    address = create_key_api_value['address']
    country = create_key_api_value['country']
    city = create_key_api_value['city']
    state = create_key_api_value['state']
    street = create_key_api_value['street']

    cursor.callproc('SP_KEYM_ADD_KEY_INFO',
                    [index, company_id, user_code, user_id, user_name, session_key, version, latitude, longitude,
                     phone_number, req_serial, issue_key, memo, address, country, city, state, street])

    return Key
