
# -*- coding: utf-8 -*-

import os

# 원하는 경로의 폴더 생성
# directory : 생성하려는 폴더 경로
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Creating directory. " + directory)

