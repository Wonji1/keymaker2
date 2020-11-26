
# -*- coding: utf-8 -*-

from .config import database

host_db = database['host']
port_db = database['port']
user_db = database['user']
password_db = database['passsword']
db = database['db']
charset = database['charset']
autocommit = database['autocommit']

db_data = "mysql+pymysql://" + user_db + ":" + password_db + "@" + host_db + ":" + port_db + "/" + db\
        + "?charset=" + charset + "&autocommit=" + autocommit

from .config import filedata_path

basic_path = filedata_path['basic_path']
module = filedata_path['module']
key = filedata_path['key']
notice = filedata_path['notice']
current_date = filedata_path['current_date']
tmp = filedata_path['tmp']
key_success = filedata_path['key_success']
key_ori = filedata_path['key_ori']
key_fail = filedata_path['key_fail']
key_crop = filedata_path['key_crop']
key_draw = filedata_path['key_draw']

module_path = basic_path + module + current_date
key_path = basic_path + key + current_date + key_ori
notice_path = basic_path + notice + current_date

module_tmp_path = basic_path + module + tmp
key_tmp_path = basic_path + key + tmp
notice_tmp_path = basic_path + notice + tmp

key_fail_path = basic_path + key + current_date + key_fail
key_success_path = basic_path + key + current_date + key_success

from .config import key_data

host_key = key_data['host']
port_key = key_data['port']

key_url = "http://" + host_key + ":" + port_key + "/"

from .config import log_data

API = log_data['API']
function = log_data['function']
number_start = log_data['number_start']
max_size = log_data['max_size']
