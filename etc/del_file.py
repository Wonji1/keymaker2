
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine

from AUMOD.get_module_info import get_module_info

from AUSYS.log import log

from AUUSE.get_user_info_from_key import get_user_info_from_key
from AUUSE.set_user_API_req import set_user_API_req

from config.config_set import module_tmp_path
from config.config_set import db_data

from .set_send import set_send
from .del_file_dir import del_file_dir
from .check_text import check_text

# 디비에 저장된 첨부파일 정보 삭제
# user_key : 첨부파일 삭제를 요청한 사용자의 key
# log_request : 요청코드
# index : 첨부파일을 삭제하려는 게시글의 인덱스
# 요청코드가 인식모듈 게시글의 첨부파일 삭제일 경우 LGMOD0004 입력
# 요청코드가 공지사항 게시글의 첨부파일 삭제일 경우 LGNOT0003 입력
def del_file(user_key, log_request, index):

    # log_request = "set_user_info"

    print("********** " + log_request + " **********")
    # 사용자의 마지막 API 변경 함수
    set_user_API_req(user_key, log_request)

    input_list = [user_key, log_request, index]

    # 입력값에서 디비 또는 API 파라미터에 입력할 수 없는 특수문자가 포함되어 있는 경우
    for input_data in input_list:
        status = check_text("input_db", input_data)
        if status == "400":
            data = []
            result = "fail"
            status = "402"

            # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
            send = set_send(data, result, status)

            return send

    # 각 요청에 따라 경로 설정 및 수정 프로시저 호출
    engine = create_engine(db_data)
    connection = engine.raw_connection()
    cursor = connection.cursor()

    # 입력받은 사용자 키를 이용하여 사용자의 아이디 조회
    send = get_user_info_from_key(user_key)
    user_id = send['data'][0]['result_data_1']

    file_path_exist = None
    file_name_exist = None

    try:

        # 인식모듈 삭제 'LGMOD0004'
        if log_request == 'LGMOD0004':
            request_auth = 'AUMOD0004'

            # 요청한 게시글에 실제 저장되어 있던 파일이 있는지 확인
            # 입력한 인덱스에 해당하는 게시글에 저장되어있던 첨부파일이 존재하는지 확인하기 위한 절차이므로 인식모듈 상세조회 코드 입력(기본권한, 작성자 중요X)
            send = get_module_info(user_key, "LGMOD0001", index)

            # 파일이 존재하지 않았을 경우
            if send['data'][0]['FILE_EXIST_FLAG'] == "N" or send['data'][0]['FILE_EXIST_FLAG'] == None:
                data = []
                result = "fail"
                status = "200"

                # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
                send = set_send(data, result, status)

                return send

            file_path_exist = send['data'][0]['FILE_PATH']
            file_name_exist = send['data'][0]['FILE_NAME']

            file_name_ori = None
            file_name = None
            file_path = module_tmp_path
            file_size = None
            file_exist_flag = "N"

            # 인식모듈 테이블에 파일 정보 저장
            cursor.callproc('SP_KEYM_SET_MODULE_FILE_INFO',
                            [index, file_name_ori, file_name, file_path, file_size, file_exist_flag])

        # 공지사항 삭제 'LGNOT0003'
        elif log_request == 'LGNOT0003':
            request_auth = 'AUNOT0003'

        # 서버에 저장된 파일 삭제
        del_file_dir(file_path_exist, file_name_exist)

        # 로그 API 호출
        # 상태코드 : 예외
        # 요청코드 : 인식모듈 삭제 또는 공지사항 삭제
        # log_status = 'LGSTA0005'
        # log(user_id, log_status, log_request)

        data = []
        status = '200'
        result = "success"

        # set_send : API 출력값 정렬 함수(아이디, 비밀번호 변수명 변경, 날짜 정보 형태 타입 변경 등)
        send = set_send(data, result, status)

        return send

    except Exception as e:
        print("error type : ", type(e))
        print("error : ", e)

        # 로그 API 호출
        # 상태코드 : 예외
        # 요청코드 : 인식모듈 삭제 또는 공지사항 삭제
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