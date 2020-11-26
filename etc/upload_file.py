
# -*- coding: utf-8 -*-

import time
from sqlalchemy import create_engine

from AUMOD.get_module_info import get_module_info

from AUUSE.get_user_info_from_key import get_user_info_from_key
from AUUSE.set_user_API_req import set_user_API_req

from config.config_set import module_path
from config.config_set import notice_path
from config.config_set import db_data
from etc.set_send import set_send
from etc.createFolder import createFolder
from etc.del_file_dir import del_file_dir

# 입력받은 파일을 서버에 올리고 디비에 저장된 내용을 수정함
# user_key : API 를 호출한 사용자 key
# log_request : 요청코드
# index : 파일을 업로드 하려는 게시글의 인덱스
# file : 업로드 하려는 파일
# file_name : 업로드 하려는 파일의 이름
# file_size : 업로드 하려는 파일의 크기

def upload_file(user_key, log_request, index, file, file_name, file_size):

    # log_request = "set_user_info"

    print("********** " + log_request + " **********")
    # 사용자의 마지막 API 변경 함수
    set_user_API_req(user_key, log_request)

    # 파일이 실제로 존재하는 지 확인
    if not file:
        data = []
        result = "fail"
        status = "400"

        # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
        send = set_send(data, result, status)

        return send

    # 입력받은 사용자 키를 이용하여 사용자의 아이디 조회
    send = get_user_info_from_key(user_key)
    user_id = send['data'][0]['result_data_1']

    # 서버에 저장할 첨부파일명 변경(현재날짜 + 현재시간 + 등록한 사용자 ID)
    if file_name:
        file_name_split = file_name.split('.')
        extension = file_name_split[1]
    else:
        extension = "zip"

    file_name_ori = file_name
    file_name = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + user_id + "." + extension

    # 각 요청에 따라 경로 설정 및 수정 프로시저 호출
    engine = create_engine(db_data)
    connection = engine.raw_connection()
    cursor = connection.cursor()

    try:
        # 인식모듈 등록 또는 수정을 요청헀을 경우
        if log_request == 'LGMOD0005' or log_request == 'LGMOD0003':
            file_path = module_path

            # 인식모듈 수정을 요청하여 원래 게시글에 첨부파일이 존재했었을 경우(첨부파일 변경)
            # 입력한 인덱스에 해당하는 게시글에 저장되어있던 첨부파일이 존재하는지 확인하기 위한 절차이므로 인식모듈 상세조회 코드 입력(기본권한, 작성자 중요X)
            send = get_module_info(user_key, "LGMOD0001", index)

            if send['data'][0]['FILE_EXIST_FLAG'] == "Y":

                file_path_exist = send['data'][0]['FILE_PATH']
                file_name_exist = send['data'][0]['FILE_NAME']

                # 서버에 등록된 파일 삭제
                del_file_dir(file_path_exist, file_name_exist)

            file_exist_flag = "Y"
            # 인식모듈 테이블에 파일 정보 저장
            cursor.callproc('SP_KEYM_SET_MODULE_FILE_INFO', [index, file_name_ori, file_name, file_path, file_size, file_exist_flag])

        # 공지사항 등록 또는 수정을 요청했을 경우
        else:
            file_path = notice_path

            # 공지사항 파일 테이블에 파일 정보 저장

        # 해당 경로에 변경한 이름으로 파일 서버에 업로드
        createFolder(file_path)

        file.save(file_path + file_name)

        # 로그 API 호출
        # 상태코드 : 요청
        # 요청코드 : 인식모듈 등록 또는 수정 또는 공지사항 등록 또는 수정
        # log_status = 'LGSTA0001'
        # log(user_id, log_status, log_request)

        data = []
        result = "success"
        status = "200"

        # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
        send = set_send(data, result, status)

        return send

    except Exception as e:
        print("error type : ", type(e))
        print("error : ", e)

        # 로그 API 호출
        # 상태코드 : 예외
        # 요청코드 : 인식모듈 등록 또는 수정 또는 공지사항 등록 또는 수정
        # log_status = 'LGSTA0005'
        # log(user_id, log_status, log_request)

        data = []
        status = '401'
        result = "fail"

        # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
        send = set_send(data, result, status)

        return send

    finally:
        connection.close()