import hashlib

from saleappv1 import app
from saleappv1.models import ChuyenBay, SanBay, User, TuyenBay, Ve
from saleappv1 import db
from sqlalchemy import func

def load_sanbay(ma_sb=None, kw=None):
    query = SanBay.query

    if ma_sb:
        query = query.filter(SanBay.masb.__eq__(ma_sb))

    if kw:
        query = query.filter(SanBay.tensb.contains(kw))

    return query.all()

def load_tuyenbay():
    return TuyenBay.query.all()


def load_chuyenbay():
    return ChuyenBay.query.all()


def get_giave(chuyenbay_id):
    query = db.session.query(TuyenBay.matb, TuyenBay.gia, ChuyenBay.macb)\
        .join(ChuyenBay, ChuyenBay.tuyenbay_id.__eq__(TuyenBay.matb)).filter(ChuyenBay.macb.__eq__(chuyenbay_id)).first()
    giave = query.gia
    return giave
def upload_ve(ngaygioxuatve, giave, chuyenbay, hangve_id, hoten, sdt, cccd):
    v = Ve(ngaygioxuatve=ngaygioxuatve, hangve_id=hangve_id, giave=giave, tenkh=hoten,dienthoai=sdt, cccd=cccd, chuyenbay_id=chuyenbay)
    db.session.add(v)
    db.session.commit()

def thongke():
    query = db.session.query(TuyenBay.matb, TuyenBay.sanbaydi_id, TuyenBay.sanbayden_id,
                             func.sum(TuyenBay.gia), func.count(Ve.mave))\
        .join(ChuyenBay, ChuyenBay.tuyenbay_id.__eq__(TuyenBay.matb))\
        .join(Ve, Ve.chuyenbay_id.__eq__(ChuyenBay.macb))
    return query.group_by(TuyenBay.matb).order_by(TuyenBay.matb).all()


def auth_user(username, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()

def register(name, username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name, username=username.strip(), password=password)
    db.session.add(u)
    db.session.commit()

def get_user_by_id(user_id):
    return User.query.get(user_id)


def get_product_by_id(macb):
    return ChuyenBay.query.get(macb)

def get_price_by_id(matb):
    return TuyenBay.query.get(matb)

def get_terminal_by_id(masb):
    return SanBay.query.get(masb)