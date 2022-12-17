from flask import render_template, request, redirect, session, jsonify
from saleappv1 import dao
from saleappv1 import app, login
from flask_login import login_user, logout_user, current_user, login_required
from saleappv1 import admin
from flask_login import current_user
import cloudinary.uploader
from saleappv1.decorator import annonymous_user
import datetime

@app.route('/')
# @login_required
def index():
    ma_sb = request.args.get('masb')
    kw = request.args.get('keyword')
    sanbay = dao.load_sanbay(ma_sb=ma_sb, kw=kw)
    tuyenbay = dao.load_tuyenbay()
    chuyenbay = dao.load_chuyenbay()

    return render_template('index.html', sanbay=sanbay, tuyenbay=tuyenbay, chuyenbay=chuyenbay)


@app.route('/chuyenbay/<int:macb>')
def detail(macb):
    p = dao.get_product_by_id(macb)
    t = dao.get_price_by_id(matb=macb)
    s = dao.get_terminal_by_id(masb=macb)
    return render_template('detail.html', chuyenbay=p, tuyenbay=t, sanbay=s)


@app.route('/login-admin', methods=['post'])
def admin_login():
    username = request.form['username']
    password = request.form['password']

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)
    return redirect('/admin')  # chuyen trang


@app.route('/datve', methods=['post', 'get'])
def datve():
    # load
    sanbay = dao.load_sanbay()
    tuyenbay = dao.load_tuyenbay()
    chuyenbay = dao.load_chuyenbay()
    err_msg = ''
    flag = 0

    if request.method.__eq__('POST'):
        chuyenbay = request.form['chuyenbay']
        hangve = request.form['hangve']
        hoten = request.form['name']  # name html
        sdt = request.form['phone']
        cccd = request.form['cccd']
        ngayxuatve = datetime.datetime.now()
        try:
            giave = dao.get_giave(chuyenbay)
            dao.upload_ve(ngaygioxuatve=ngayxuatve, giave=giave, chuyenbay=chuyenbay, hangve_id=hangve,
                          hoten=hoten, sdt=sdt, cccd=cccd)
            flag = 0
            return redirect('/thanhtoan')
        except:
            err_msg = "Nhập hạng vé lỗi!!!!"

    return render_template('datve.html', flag=flag, err_msg=err_msg,
                           sanbay=sanbay, tuyenbay=tuyenbay, chuyenbay=chuyenbay)

@app.route('/thanhtoan')
def thanhtoan():
    return render_template('thanhtoan.html')


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = ''
    if request.method.__eq__('POST'):
        password = request.form['password']
        confirm = request.form['confirm']
        if password.__eq__(confirm):
            try:
                dao.register(name=request.form['name'],
                             username=request.form['username'],
                             password=password)
                return redirect('/login')
            except:
                err_msg = "Hệ thống đang báo lỗi! Vui lòng quay lại sau"
        else:
            err_msg = "Mật khẩu không khớp"

    return render_template('register.html', err_msg=err_msg)


@app.route('/login', methods=['get', 'post'])
@annonymous_user
def login_my_user():
    if request.method.__eq__('POST'):
        username = request.form['username']
        password = request.form['password']
        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)
            n = request.args.get('next')
            return redirect(n if n else '/')

    return render_template('login.html')


@app.route('/logout')
def logout_my_user():
    logout_user()
    return redirect('/login')

