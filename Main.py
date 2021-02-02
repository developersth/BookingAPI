# This is a sample Python script.
import  datetime
from flask import Flask, jsonify, request
from ServiceDb import ServiceDb
from MainFunction import MainFunction
from MongoDb import MongoDb
from flask_cors import CORS
import requests
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
service = ServiceDb()
fn = MainFunction()
db = MongoDb()
@app.route('/')
def home():
    config =db.getConfig()
    arr = {
        "fname"     :   "Prisan",
        "lname"     :   "Pimprasan",
        "nickname"  :   "Big",
        "str"       :   config.env.connection_string
    }
    return jsonify(arr)

@app.route('/api/users')
def users():
    res =service.getusers()
    return jsonify(res)

@app.route('/api/getconnection',methods=["GET"])
def getConnection():
    lang = fn.getLanuage(request)
    fn.getMessage("%s" % lang, "status")
    print(fn.getMessage(f'{lang}', "status"))
    res =service.getConnectionDb()
    return res

@app.route('/api/users',methods=["POST"])
def insertUser():
    print(str(datetime.datetime.now()))
    lang = fn.getLanuage(request)
    res =service.insertUser(lang,request)
    return res

@app.route('/api/auth/login',methods=["POST"])
def vadidateUserLogin():
    print(str(datetime.datetime.now()))
    lang = fn.getLanuage(request)
    res =service.validateUserLogin(lang,request)
    return res

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
