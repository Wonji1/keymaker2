
# -*- coding: utf-8 -*-

from flask import request

from config.config_set import db_data

from sqlalchemy import create_engine

def log(user_id, log_status, log_request, api, function, input, output, message, success_flag):

    try:
        if user_id == '' or user_id is None:
            user_id = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        if input == '':
            input = None
        if output == '':
            output = None
        if message == '':
            message = None
        if log_status == "EXCEPTION":
            display_flag = "N"
        else:
            display_flag = "Y"

        if output:
            if type(output) == list:
                output = output[0]
            if type(output) == dict:
                output = str(output)
        else:
            output = str(output)

        if input:
            if type(input) == list:
                input = input[0]

            if type(input) == dict:
                input = str(input)
        else:
            input = str(input)

        engine = create_engine(db_data)

        connection = engine.raw_connection()
        cursor = connection.cursor()

        # 로그 저장
        cursor.callproc('SP_KEYM_ADD_LOG', [user_id, log_status, log_request, api, function, input, output, message, success_flag, display_flag])

        # 로그 출력
        cursor.callproc('SP_KEYM_GET_LOG', [None, None, None, None, None])

        column_names_list = [x[0] for x in cursor.description]

        result_log_info = []

        for row in cursor.fetchall():
            result_log_info.append(dict(zip(column_names_list, row)))

        return result_log_info[0]

    except Exception as e:
        print("error type : ", type(e))
        print("error : ", e)

    finally:
        connection.close()
