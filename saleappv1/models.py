from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Boolean
from saleappv1 import db, app
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as UserEnum
from flask_login import UserMixin
import hashlib


class UserRole(UserEnum):
    USER = 1
    ADMIN = 2


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    name = Column(String(50), nullable=True)
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    user_chuyenbay = relationship('ChuyenBay', backref='user', lazy=True)

    def __str__(self):
        return self.username


class SanBay(db.Model):
    __tablename__ = 'sanbay'
    masb = Column(Integer, primary_key=True, autoincrement=True)
    tensb = Column(String(50), nullable=False)
    sanbay_tramdungs = relationship('TramDung', backref='sanbay', lazy=True)
    def __str__(self):
        return self.tensb



class TuyenBay(db.Model):
    __tablename__ = 'tuyenbay'
    matb = Column(Integer, primary_key=True, autoincrement=True)
    sanbaydi_id = Column(Integer, ForeignKey(SanBay.masb), nullable=False)
    sanbayden_id = Column(Integer, ForeignKey(SanBay.masb), nullable=False)
    gia = Column(Float, default=0)
    sanbaydi = relationship('SanBay', foreign_keys=[sanbaydi_id])
    sanbayden = relationship('SanBay', foreign_keys=[sanbayden_id])
    tuyenbay_chuyenbay = relationship('ChuyenBay', backref='tuyenbay', lazy=True)


class ChuyenBay(db.Model):
    __tablename__ = 'chuyenbay'
    macb = Column(Integer, primary_key=True, autoincrement=True)
    ngaygio = Column(DateTime, nullable=False)
    thoigianbay = Column(Integer, nullable=False)
    soluonghangghe1 = Column(Integer, nullable=False)
    soluonghangghe2 = Column(Integer, nullable=False)
    slhangghe1daban = Column(Integer, nullable=False)
    slhangghe2daban = Column(Integer, nullable=False)
    tuyenbay_id = Column(Integer, ForeignKey(TuyenBay.matb), nullable=False)
    chuyenbay_tramdung = relationship('TramDung', backref='chuyenbay', lazy=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    chuyenbay_ve = relationship('Ve', backref='chuyenbay', lazy=True)

    def __str__(self):
        return str(self.ngaygio)


class TramDung(db.Model):
    __tablename__ = 'tramdung'
    ma_cb = Column(Integer, ForeignKey(ChuyenBay.macb), primary_key=True)
    ma_sb = Column(Integer, ForeignKey(SanBay.masb), primary_key=True)
    thoigiandung = Column(Integer, nullable=False)


class HangVe(db.Model):
    __tablename__ = 'hangve'
    mahv = Column(Integer, primary_key=True, autoincrement=True)
    loaihangve = Column(Integer, nullable=False)
    hangve_ve = relationship('Ve', backref='hangve', lazy=True)


class Ve(db.Model):
    __tablename__ = 've'
    mave = Column(Integer, primary_key=True, autoincrement=True)
    ngaygioxuatve = Column(DateTime, default=datetime.now())
    hangve_id = Column(Integer, ForeignKey(HangVe.mahv), nullable=False)
    giave = Column(Float)
    tenkh = Column(String(50), nullable=False)
    dienthoai = Column(Float, nullable=False)
    cccd = Column(Float, nullable=False)
    chuyenbay_id = Column(Integer, ForeignKey(ChuyenBay.macb), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        # Tao CSDL
        # db.create_all()
        #
        # Them data SanBay
        sb1 = SanBay(tensb='Nội Bài')
        sb2 = SanBay(tensb='Tân Sơn Nhất')
        sb3 = SanBay(tensb='Cam Ranh')
        sb4 = SanBay(tensb='Đà Nẵng')
        sb5 = SanBay(tensb='Phú Bài')
        sb6 = SanBay(tensb='Phú Quốc')
        sb7 = SanBay(tensb='Vinh')
        sb8 = SanBay(tensb='Cần Thơ')
        sb9 = SanBay(tensb='Chu Lai')
        sb10 = SanBay(tensb='Huế')

        db.session.add_all([sb1, sb2, sb3, sb4, sb5, sb6, sb7, sb8, sb9, sb10])
        db.session.commit()
        # Them tuyen bay
        tb1 = TuyenBay(sanbaydi_id=1, sanbayden_id=2, gia=1000000)
        tb2 = TuyenBay(sanbaydi_id=1, sanbayden_id=3, gia=9000000)
        tb3 = TuyenBay(sanbaydi_id=2, sanbayden_id=4, gia=1000000)
        tb4 = TuyenBay(sanbaydi_id=2, sanbayden_id=5, gia=8000000)
        tb5 = TuyenBay(sanbaydi_id=2, sanbayden_id=3, gia=8000000)

        db.session.add_all([tb1, tb2, tb3, tb4, tb5])
        db.session.commit()

        # Them user
        import hashlib

        password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        u = User(username='admin', name='Admin', password=password, user_role=UserRole.ADMIN)
        db.session.add(u)
        db.session.commit()

        # Them chuyen bay
        cb1 = ChuyenBay(ngaygio='2022/12/01:10:00:00', thoigianbay=30, soluonghangghe1=40, soluonghangghe2=20,
                        slhangghe1daban=1, slhangghe2daban=2, tuyenbay_id=1, user_id=1)
        cb2 = ChuyenBay(ngaygio='2022/12/01:11:00:00', thoigianbay=30, soluonghangghe1=40, soluonghangghe2=20,
                        slhangghe1daban=2, slhangghe2daban=2, tuyenbay_id=2, user_id=1)
        cb3 = ChuyenBay(ngaygio='2022/12/23:10:00:00', thoigianbay=30, soluonghangghe1=40, soluonghangghe2=20,
                        slhangghe1daban=1, slhangghe2daban=2, tuyenbay_id=1, user_id=1)
        cb4 = ChuyenBay(ngaygio='2022/12/24:11:00:00', thoigianbay=30, soluonghangghe1=40, soluonghangghe2=20,
                        slhangghe1daban=2, slhangghe2daban=2, tuyenbay_id=2, user_id=1)
        db.session.add_all([cb1, cb2, cb3, cb4])
        db.session.commit()

        # Them tram dung
        td1 = TramDung(ma_cb=1, ma_sb=4, thoigiandung=20)
        db.session.add_all([td1])
        db.session.commit()

        # Them data HangVe
        hv1 = HangVe(loaihangve=1)
        hv2 = HangVe(loaihangve=2)
        db.session.add_all([hv1, hv2])
        db.session.commit()

        # Ve
        ve1 = Ve(hangve_id=1, giave=2000000, tenkh='Pham Thuy', dienthoai=8496575200, cccd=12356789, chuyenbay_id=1)
        ve2 = Ve(hangve_id=1, giave=2000000, tenkh='Pham Hao', dienthoai=8496575100, cccd=12356799, chuyenbay_id=1)
        ve3 = Ve(hangve_id=1, giave=2000000, tenkh='Nguyen Tan', dienthoai=8496575101, cccd=12356779, chuyenbay_id=1)
        db.session.add_all([ve1, ve2, ve3])
        db.session.commit()
