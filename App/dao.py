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

def count_free_room(ten = None, phongngu = None, songuoi = None):
    query = CanHo.query.filter(CanHo.tinhtrang == TinhTrang.COTHETHUE)

    if ten:
        query = query.filter(CanHo.ten.contains(ten))

    if phongngu:

        query = query.filter( CanHo.phongngu.__eq__(int(phongngu)))

    if songuoi:
        query = query.filter( CanHo.songuoitoida.__eq__(int(songuoi)))


    return query.count()

def get_taikhoan_by_id(taikhoan_id):
    return TaiKhoan.query.get(taikhoan_id)

def auth_user(username, password):
    password = hashlib.md5(password.encode("utf-8")).hexdigest()
    return TaiKhoan.query.filter(TaiKhoan.username.__eq__(username),TaiKhoan.password.__eq__(password)).first()

def taikhoan_co_thue():
    if current_user.is_authenticated:
        return NguoiThue.query.filter(NguoiThue.id_taikhoan == current_user.id).first()
    return None

if __name__ == '__main__':
    with app.app_context():
        print(taikhoan_co_thue())