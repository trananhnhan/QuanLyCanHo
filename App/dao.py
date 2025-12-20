import hashlib
from idlelib.query import Query
from operator import is_none

from flask_login import current_user
from sqlalchemy import func
from sqlalchemy.testing.pickleable import User

from App.models import (
    TaiKhoan, NguoiThue, LoaiPhi, ChiTietPhi, CanHo,
    DichVu, HopDong, HoaDon, ChiTietHoaDon, YeuCau,
    UserRole, TinhTrang
)
from App import db, login, app


def load_free_room_with_page(ten = None, phongngu = None, songuoi = None,page = 1):
    query = CanHo.query.filter(CanHo.tinhtrang == TinhTrang.COTHETHUE)

    if ten:
        query = query.filter(CanHo.ten.contains(ten))

    if phongngu:

        query = query.filter( CanHo.phongngu.__eq__(int(phongngu)))

    if songuoi:
        query = query.filter( CanHo.songuoitoida.__eq__(int(songuoi)))
    if is_none(page):
        page = 1
    size = app.config["PAGE_SIZE"]
    start = (int(page) - 1) * size
    query = query.slice(start, (start + size))

    return query.all()

def count_free_room(ten = None, phongngu = None, songuoi = None, id_nguoi_thue= None):
    query = CanHo.query.filter(CanHo.tinhtrang == TinhTrang.COTHETHUE)

    if ten:
        query = query.filter(CanHo.ten.contains(ten))

    if phongngu:

        query = query.filter( CanHo.phongngu.__eq__(int(phongngu)))

    if songuoi:
        query = query.filter( CanHo.songuoitoida.__eq__(int(songuoi)))
    if id_nguoi_thue:
        query = query.filter()

    return query.count()

def get_tai_khoan_by_id(tai_khoan_id):
    return TaiKhoan.query.get(tai_khoan_id)

def auth_user(username, password):
    password = hashlib.md5(password.encode("utf-8")).hexdigest()
    return TaiKhoan.query.filter(TaiKhoan.username.__eq__(username),TaiKhoan.password.__eq__(password)).first()

def tai_khoan_co_thue():
    if current_user.is_authenticated:
        return NguoiThue.query.filter(NguoiThue.id_taikhoan == current_user.id).first()
    return None

def tao_tai_khoan(username = None, password = None, avatar = None):
    password = hashlib.md5(password.encode("utf-8")).hexdigest()
    if avatar:
        print("yes avatar")
        taikhoan = TaiKhoan()
        taikhoan.username = username.strip()
        taikhoan.password = password
        taikhoan.avatar = avatar
    else:
        print("no avatar")
        taikhoan = TaiKhoan()
        taikhoan.username = username.strip()
        taikhoan.password = password

    db.session.add(taikhoan)
    db.session.commit()
    return taikhoan

def get_phong_by_id(id):
    return CanHo.query.filter(CanHo.id == id).first()

def count_nguoi_dang_thue_phong(id):
    return HopDong.query.filter(HopDong.id_canho == id,HopDong.active == True).count()

def get_ds_dich_vu_tu_phong(id):
    return DichVu.query.filter(DichVu.id_canho == id).all()

def get_ds_hop_dong_active_tu_nguoi_thue(id):
    return HopDong.query.filter(HopDong.id_nguoithue == id,HopDong.active == True).all()

def chuyen_ds_hop_dong_qua_ds_can_ho(ds_hopdong):
    can_ho = []
    for hd in ds_hopdong:
        can_ho.append(hd.canho)
    return can_ho

def phan_trang_tu_ds_can_ho(ds_can_ho,page = 0):
    if is_none(page):
        page = 1
    size = app.config["PAGE_SIZE"]
    start = (int(page) - 1) * size

    ds_can_ho_moi = ds_can_ho[start:start+size]
    return ds_can_ho_moi


if __name__ == '__main__':
    with app.app_context():
        for hd in get_ds_hop_dong_active_tu_nguoi_thue(3):
            print(hd.ngaybatdau.strftime('%d/%m/%Y'))

