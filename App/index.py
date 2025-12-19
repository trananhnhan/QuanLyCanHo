import math

import cloudinary
import cloudinary.uploader
from flask import Flask, render_template, request, redirect
from flask_login import login_user, logout_user

from App import app, login, dao, db
from App.dao import taikhoan_co_thue
from App.decorators import anonymous_required

@login.user_loader
def get_user(user_id):
    return dao.get_taikhoan_by_id(user_id)

@app.route('/')
def index():
    return render_template('index.html',taikhoan_co_thue = taikhoan_co_thue())

@app.route('/phong')
def phong():
    ten = request.args.get('ten')
    phongngu = request.args.get('phongngu')
    songuoi = request.args.get('songuoi')
    page = request.args.get('page')
    rooms = dao.load_free_room_with_page(ten = ten,phongngu= phongngu,songuoi=songuoi,page=page)
    pages = math.ceil(dao.count_free_room(ten = ten,phongngu= phongngu,songuoi=songuoi)/app.config["PAGE_SIZE"])
    print(pages)
    for r in rooms:
        print(r.ten)
    return render_template('phong.html',rooms = rooms,pages=pages)

@app.route('/lienhe')
def lienhe():
    return render_template("lienhe.html")

@app.route("/dangnhap", methods=["get", "post"])
@anonymous_required
def dangnhap():
    err_msg = None
    if request.method.__eq__("POST"):
        username = request.form.get("username")
        password = request.form.get("password")
        user = dao.auth_user(username, password)

        if user:
            login_user(user)
            next = request.args.get('next')
            return redirect(next if next else "/")
        else:
            err_msg = "Tài khoản hoặc mật khẩu không đúng!"

    return render_template("dangnhap.html", err_msg=err_msg)

@app.route("/dangxuat")
def dangxuat():
    logout_user()
    return redirect("/")


@app.route("/dangky", methods=['get', 'post'])
def register():
    err_msg = None
    if request.method.__eq__("POST"):
        password = request.form.get("password")
        confirm = request.form.get("confirm-password")

        if password.__eq__(confirm):
            username = request.form.get("username")
            avatar = request.files.get('avatar')
            print(avatar)
            file_path = None

            if avatar:
                res = cloudinary.uploader.upload(avatar)
                print(res)
                file_path = res['secure_url']
                print(file_path)

            try:
                dao.tao_taikhoan(username= username,password=password,avatar=file_path)
                return redirect('/dangnhap')
            except:
                db.session.rollback()
                err_msg = "Hệ thống đang bị lỗi! Vui lòng quay lại sau!"
        else:
            err_msg = "Mật khẩu không khớp!"

    return render_template("dangky.html", err_msg=err_msg)

@app.route("/chitietphong/<int:id>")
def chitietphong(id):
    phong = dao.get_phong_by_id(id)
    so_nguoi_thue = dao.count_nguoi_dang_thue_phong(id)
    dichvu = dao.get_dich_vu_tu_phong(id)
    print(so_nguoi_thue,phong)
    return render_template("chitietphong.html",phong = phong,so_nguoi_thue = so_nguoi_thue,dichvu = dichvu)

if __name__ == "__main__":
    app.run(debug=True)