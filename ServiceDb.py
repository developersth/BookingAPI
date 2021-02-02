from os import abort
import pymongo
from flask import Flask , jsonify
from  MainFunction import  MainFunction
from MongoDb import MongoDb
import datetime
db = MongoDb()
fn = MainFunction()

class ServiceDb:
    def __init__(self):
        print("Calling parent constructor")
    def __del__(self):
        print('Object was destroyed')

    # database
    def getusers(self):
        res = []
        conn = self.connectdb()
        for users in conn[self.getconfigmongodb()["db"]]["user_members"].find({}):
            res.append({
                "id": "%s" % users["_id"],
                "uuid": "%s" % users["uuid"],
                "user": "%s" % users["username"],
                "name": "%s %s" % (users["details"]["firstname"], users["details"]["lastname"]),
                "email": "%s" % users["email"]
            })
        return res

    def insertUser(self,lang,request):
        try:
            #GET Message form JSON
            config = db.getConfig()

            username = request.form["username"]
            password = request.form["password"]
            email = request.form["email"]
            mobile = request.form["mobile"]
            status = bool(request.form["status"])
            imgUrl = request.form["imgUrl"]
            role = request.form["role"]
            roleName = request.form["roleName"]
            vCheck, vMsg = db.insertUserDB(
                username,
                password,
                email,
                mobile,
                status,
                imgUrl,
                role,
                roleName
            )
            if (vCheck) :
                return jsonify({
                    "code": 200,
                    "icon": "success",
                    "title": "สมัครสมาชิก",
                    "description": "",
                    "message": "สำเร็จ",
                    "status": "success"
                }), 200
            else:
                if vMsg == "USERNAME_TAKEN":
                    return jsonify({
                        "code": 401,
                        "icon": "info",
                        "title": fn.getMessage(lang, "somting_wrong"),
                        "description": fn.getMessage(lang, "please_again"),
                        "message": fn.getMessage(lang, "username_used"),
                        "status": fn.getMessage(lang, "error")
                    }), 200
                elif vMsg == "EMAIL_TAKEN":
                    return jsonify({
                        "code": 401,
                        "icon": "info",
                        "title": "เกิดข้อมูลผิดพลาด",
                        "description": "กรุณาลองใหม่อีกครั้ง",
                        "message": "อีเมล์นี้มีในระบบแล้ว",
                        "status": "error"
                    }), 200
                else:
                    return jsonify({
                        "code": 401,
                        "icon": "info",
                        "title": "เกิดข้อมูลผิดพลาด",
                        "description": "กรุณาลองใหม่อีกครั้ง",
                        "message": "เบอร์มือถือนี้มีในระบบแล้ว",
                        "status": "error"
                    }), 200



        except Exception as e:
            return jsonify({
                "code": 401,
                "icon": "error",
                "title": "เกิดข้อมูลผิดพลาด",
                "description": "กรุณาลองใหม่อีกครั้ง",
                "message": str(e),
                "status": "error"
            }), 200

    def getConnectionDb(self):
        return  db.getConfigMongoDb()

    def validateUserLogin(self, lang, request):
        try:
            c_data = db.checkuser(
                user=request.form["username"],
                passwd=request.form["password"]
            )
            if not c_data is None:
                return jsonify({
                    "code": 200,
                    "icon": "success",
                    "title": "เข้าสู่ระบบสำเร็จ",
                    "description": "",
                    "message": "เข้าสู่ระบบสำเร็จ",
                    "status": "success"
                }), 200

            return jsonify({
                "code": 401,
                "icon": "error",
                "title": "เข้าสู่ระบบไม่สำเร็จ",
                "description": "ชื่อผู้ใช้งานหรือรหัสผ่านไม่ถูกต้อง โปรดกรุณาลองใหม่อีกครั้ง",
                "message": "ชื่อผู้ใช้งานหรือรหัสผ่านไม่ถูกต้อง โปรดกรุณาลองใหม่อีกครั้ง",
                "status": "error"

            }), 200
        except Exception as e:
            return jsonify({
                "code": e.code,
                "icon": "info",
                "title": "เกิดข้อมูลผิดพลาด",
                "description": str(e.description),
                "message": str(e),
                "status": "error"
            }), 200

