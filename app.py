
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, send_file, jsonify

from AUKEY.issue_key import issue_key
from AUKEY.create_qr import create_qr
from AUKEY.read_qr import read_qr
from AUKEY.get_key_list import get_key_list
from AUKEY.get_key_info import get_key_info

from AUMOD.add_module_info import add_module_info
from AUMOD.get_module_list import get_module_list
from AUMOD.get_module_info import get_module_info
from AUMOD.set_module_info import set_module_info
from AUMOD.del_module_info import del_module_info
from AUMOD.down_module import down_module

from AUPAT.add_company import add_company
from AUPAT.get_company_list import get_company_list

from AUUSE.login import login
from AUUSE.logout import logout
from AUUSE.get_user_info import get_user_info
from AUUSE.add_user_info import add_user_info
from AUUSE.get_access_info import get_access_info
from AUUSE.set_user_info import set_user_info
from AUUSE.set_user_wih_del_flag import set_user_wih_del_flag
from AUUSE.get_user_auth import get_user_auth

from AUSYS.log import log

from etc.upload_file import upload_file
from etc.del_file import del_file
from etc.get_loc_info import get_loc_info

#2020-06-01 cors pro swyoo
from flask_cors import CORS #

app = Flask(__name__)

cors = CORS(app, resources={r"*": {"origins": "*"}})

#20200602 wonjihoon 암호화키 생성
import sys
import os
import requests
import hashlib
import hmac
import base64
import time

@app.route('/api/get_loc_info/<ip>', methods = ['GET', 'POST'])
def get_loc_info_api_fn(ip):
    send = get_loc_info(ip)
    return send

@app.route("/")
def login_page():
    return render_template("api.html");

# 접속한 사용자의 ip 호출
@app.route('/api/ip', methods = ['GET', 'POST'])
def client_ip_fn():
    return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)


@app.route("/login")
def login_fn():
    return render_template("login/login.html");

@app.route('/api/login/<user_id>/<user_pw>', methods = ['GET', 'POST'])
def login_get_api_fn(user_id, user_pw):
    userinfo = login(user_id, user_pw)
    return userinfo

# 동일한 IP로 접속한 사용자가 있을 경우 실행
# 사용자가 로그아웃 버튼을 눌렀을 때 실행
@app.route('/api/logout/<user_ip>', methods = ['GET', 'POST'])
def logout_api_fn(user_ip):
    send = logout(user_ip)
    return send

@app.route('/api/get_user_info/<user_key>/<user_id>/<log_request>', methods = ['GET', 'POST'])
def get_user_info_api_fn(user_key, user_id, log_request):
    send = get_user_info(user_key, user_id, log_request)
    return send

@app.route('/api/add_user_info/<user_id>/<user_pw>/<user_name>/<company_name>/<department>/<position>/<phone_number>/<email>', methods = ['GET', 'POST'])
def add_user_info_api_fn(user_id, user_pw, user_name, company_name, department, position, phone_number, email):
    send = add_user_info(user_id, user_pw, user_name, company_name, department, position, phone_number, email)
    return send

@app.route('/api/set_user_info/<user_key>/<request>/<user_pw>/<user_name>/<company_name>/<department>/<position>/<phone_number>/<email>', methods = ['GET', 'POST'])
def set_user_info_api_fn(user_key, request, user_pw, user_name, company_name, department, position, phone_number, email):
    send = set_user_info(user_key, request, user_pw, user_name, company_name, department, position, phone_number, email)
    return send

@app.route('/api/get_access_info/<user_key>', methods = ['GET', 'POST'])
def get_access_info_api_fn(user_key):
    send = get_access_info(user_key)
    return send

@app.route('/api/set_user_wih_del_flag/<user_key>/<request>', methods = ['GET', 'POST'])
def set_user_wih_del_flag_api_fn(user_key, request):
    send = set_user_wih_del_flag(user_key, request)
    return send

@app.route('/api/get_user_auth/<user_key>', methods = ['GET', 'POST'])
def get_user_auth_api_fn(user_key):
    send = get_user_auth(user_key)
    return send

@app.route('/loginTest')
def loginTest():
    return render_template('/test/loginTest.html')

@app.route('/api/get_company_list/<user_key>/<user_name>/<currentpage>/<countperpage>', methods = ['GET', 'POST'])
def get_company_list_api_fn(user_key, user_name, currentpage, countperpage):
    send = get_company_list(user_key, user_name, currentpage, countperpage)
    return send

@app.route('/api/add_company_list/<user_key>/<com_name>/<com_address>/<phone_number>/<email>/<memo>/<day_max_count>/<max_count>/<date_max>', methods = ['GET', 'POST'])
def add_company_api_fn(user_key, com_name, com_address, phone_number, email, memo, day_max_count, max_count, date_max):
    send = add_company(user_key, com_name, com_address, phone_number, email, memo, day_max_count, max_count, date_max)
    return send

@app.route('/companyTest')
def companyTest_api_fn():
    return render_template('/test/companyTest.html')

@app.route('/api/add_module_info/<user_key>/<module_name>/<version>/<memo>', methods = ['GET', 'POST'])
def add_module_info_api_fn(user_key, module_name, version, memo):
    send = add_module_info(user_key, module_name, version, memo)
    return send

@app.route('/api/get_module_list/<user_key>/<module_name>/<user_name>/<version>/<memo>/<date_reg_start>/<date_reg_end>/<currentpage>/<countperpage>', methods = ['GET', 'POST'])
def get_module_list_api_fn(user_key, module_name, user_name, version, memo, date_reg_start, date_reg_end, currentpage, countperpage):
    send = get_module_list(user_key, module_name, user_name, version, memo, date_reg_start, date_reg_end, currentpage, countperpage)
    return send

@app.route('/api/get_module_info/<user_key>/<log_request>/<module_index>', methods = ['GET', 'POST'])
def get_module_info_api_fn(user_key, log_request, module_index):
    send = get_module_info(user_key, log_request, module_index)
    return send

@app.route('/api/set_module_info/<user_key>/<module_index>/<module_name>/<version>/<memo>', methods = ['GET', 'POST'])
def set_module_info_api_fn(user_key, module_index, module_name, version, memo):
    send = set_module_info(user_key, module_index, module_name, version, memo)
    return send

@app.route('/api/del_module_info/<user_key>/<module_index>/<file_exist_flag>', methods = ['GET', 'POST'])
def del_module_info_api_fn(user_key, module_index, file_exist_flag):
    send = del_module_info(user_key, module_index, file_exist_flag)
    return send

@app.route('/api/down_module/<user_key>/<module_index>', methods = ['GET', 'POST'])
def down_module_api_fn(user_key, module_index):
    send = down_module(user_key, module_index)

    if send['status'] == "402":
        return send

    file = send['data'][0]['FILE']
    file_name_ori = send['data'][0]['FILE_NAME_ORI']

    return send_file(file, attachment_filename=file_name_ori, as_attachment=True)

@app.route('/api/upload_file', methods = ['GET', 'POST'])
def upload_file_api_fn():
    if request.method == "POST":
        user_key = request.form['upload_file_user_key']
        log_request = request.form['upload_file_request']
        index = request.form['upload_file_index']
        file_name = request.form['upload_file_file_name']
        file_size = request.form['upload_file_file_size']

        file = request.files['upload_file_file']

        send = upload_file(user_key, log_request, index, file, file_name, file_size)
        return send

@app.route('/api/del_file/<user_key>/<log_request>/<index>', methods = ['GET', 'POST'])
def del_file_api_fn(user_key, log_request, index):
    send = del_file(user_key, log_request, index)
    return send

@app.route('/moduleTest')
def moduleTest_api_fn():
    return render_template('/test/moduleTest.html')

@app.route("/mod")
def mod_fn():
    return render_template("login/mod.html");

@app.route("/reg")
def reg_fn():
    return render_template("login/reg.html");

@app.route("/keyissue")
def keyissue_fn():
    return render_template("key/keyissue.html");

@app.route("/keysearch")
def keysearch_fn():
    return render_template("key/keysearch.html");

@app.route('/api/create_qr/<url>/<image_name>')
def create_qr_api_fn(url, image_name):
    send = create_qr(url, image_name)
    return send

@app.route('/api/read_qr', methods = ['GET', 'POST'])
def read_qr_api_fn():
    if request.method == "POST":
        user_key = request.form['read_qr_user_key']
        image = request.files['read_qr_image']
        image_name = request.form['read_qr_image_name']
        image_size = request.form['read_qr_image_size']

        send = read_qr(user_key, image, image_name, image_size)
        return send

@app.route('/api/issue_key/<user_key>/<index>/<user_ip>/<req_serial>/<version>/<memo>', methods = ['GET', 'POST'])
def issue_key_api_fn(user_key, index, user_ip, req_serial, version, memo):
    '''
    if request.method == "POST":
        user_key = request.form['issue_key_user_key']
        image_name = request.form['issue_key_image_name']
        image_size = request.form['issue_key_image_size']

        image = request.files['issue_key_image']

        send = issue_key(user_key, image, image_name, image_size)
        return send
    '''
    send = issue_key(user_key, index, user_ip, req_serial, version, memo)
    return send

@app.route('/api/get_key_list/<user_key>/<user_name>/<address>/<user_id_search>/<date_start>/<date_end>/<currentpage>/<countperpage>', methods = ['GET', 'POST'])
def get_key_list_api_fn(user_key, user_name, address, user_id_search, date_start, date_end, currentpage, countperpage):
    send = get_key_list(user_key, user_name, address, user_id_search, date_start, date_end, currentpage, countperpage)
    return send

@app.route('/api/get_key_info/<user_key>/<index>', methods = ['GET', 'POST'])
def get_key_info_api_fn(user_key, index):
    send = get_key_info(user_key, index)
    return send

@app.route('/keyTest')
def keyTest_api_fn():
    return render_template('/test/keyTest.html')

@app.route("/addcomppop")
def addcomppop_fn():
    return render_template("partneradmin/addcomppop.html");

@app.route("/moduleadd")
def moduleadd_fn():
    return render_template("module/moduleadd.html");

@app.route("/moduledetail/<moduleindex>")
def moduledetail_fn(moduleindex):
    return render_template("module/moduledetail.html",
                           moduleindex = moduleindex);

@app.route("/modulesearch")
def modulesearch_fn():
    return render_template("module/modulesearch.html");

@app.route("/modulemod/<moduleindex>")
def modulemod_fn(moduleindex):
    return render_template("module/modulemod.html",
                           moduleindex = moduleindex);

@app.route("/keydetail/<keyindex>")
def keydetail_fn(keyindex):
    return render_template("key/keydetail.html",
                           keyindex = keyindex);


@app.route("/geo")
def geo_fn():
    return render_template("main/test.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0')
