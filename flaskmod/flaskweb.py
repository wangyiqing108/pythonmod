#encoding: utf-8

from flask import Flask
from flask import render_template                   #从flask包导入render_template函数
from flask import request                           #从flask包导入request对象
from flask import redirect                          #从flask包导入redirect函数
from flask import url_for
from flask import session

app = Flask(__name__)

@app.route('/')                        
def index():
    #return render_template('login.html')
    #return 'hello,{0}'.format(name)
    return '<h1>Hello, 你好!</h1>'
@app.route('/login/', methods=["POST"])         
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    return 'usename=%s,password=%s' % (usename,password)

@app.route('/getargs/', methods=["GET"])
def getargs():
    return  "获取get参数{0}".format(request.args.get('a'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9002, debug=True)

