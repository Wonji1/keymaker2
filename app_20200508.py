# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from AUUSE.login import login
from AUUSE.logout import logout

app = Flask(__name__)


@app.route("/")
def login_page():s
    return render_template("api.html");

# 접속한 사용자의 ip 호출
@app.route('/api/ip', methods = ['GET'])
def client_ip_fn():
    return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)


@app.route("/login")
def login_fn():
    return render_template("login/login.html");


# login API
@app.route('/api/login', methods = ['POST'])
def login_api_fn():
    user_id = request.form['user_id']
    user_pw = request.form['user_pw']

    print(user_id)

    userinfo = login(user_id, user_pw)

    print("success")

    return userinfo

@app.route('/api/logout', methods = ['GET'])
def logout_fn():
    user_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    print(user_ip)
    print(type(user_ip))
    msg = logout(user_ip)
    return msg

@app.route('/api/test')
def loginTest():
    return render_templates('/test/loginTest.html')

@app.route("/mod")
def mod_fn():
    return render_template("login/mod.html");

@app.route("/reg")
def reg_fn():
    return render_template("login/reg.html");

@app.route("/notadd")
def notadd_fn():
    return render_template("notice/notadd.html");

@app.route("/notdetail")
def notdetail_fn():
    return render_template("notice/notdetail.html");

@app.route("/notice")
def notice_fn():
    return render_template("notice/notice.html");

@app.route("/notmod")
def notmod_fn():
    return render_template("notice/notmod.html");

@app.route("/keyissue")
def keyissue_fn():
    return render_template("key/keyissue.html");

@app.route("/keysearch")
def keysearch_fn():
    return render_template("key/keysearch.html");

# @app.route("/user/login/<string:passWord>")
# def userLogin2(passWord):
#     if(passWord == '1234'):
#         return render_template("abc2.html");
#     else:
#         return render_template("abc.html");

if __name__ == '__main__':
    app.run(host='0.0.0.0')
