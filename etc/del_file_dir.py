
# -*- coding: utf-8 -*-

import os

# 서버에 업로드 된 파일 삭제
# file_path : 삭제하려는 파일의 경로
# file_name : 삭제하려는 파일의 이름
def del_file_dir(file_path, file_name):

    if file_path[len(file_path)-1] != "/":
        file_path += "/"

    file = file_path + file_name

    if file_path == None or file_name == None:
        return

    if os.path.isfile(file):
        print("삭제됨")
        os.remove(file)

    # 해당 폴더 안에 파일이 존재하지 않을 경우 폴더 삭제
    '''
    if os.listdir(file_path):
        os.rmdir(file_path)
    '''