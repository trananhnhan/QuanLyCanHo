from datetime import datetime, timedelta

from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_admin.theme import Bootstrap4Theme
from flask_login import current_user, logout_user
from sqlalchemy import func
from werkzeug.utils import redirect

from App import app, db
from App.models import UserRole, HopDong, HoaDon, CanHo, ChiTietPhi, LoaiPhi, DichVu, ChiTietHoaDon


class MyAuthenticatedView(ModelView):
    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.role==UserRole.ADMIN


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect('/')
        elif current_user.role != UserRole.ADMIN:
            return redirect('/')
        return super(MyAdminIndexView, self).index()

admin = Admin(app=app, name= 'Quản lý Căn Hộ', theme=Bootstrap4Theme(), index_view=MyAdminIndexView())
class MyLogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect("/admin")

    def is_accessible(self) -> bool:
        return current_user.is_authenticated

class HopDongView(MyAuthenticatedView):
    column_list = ('id', 'ngaybatdau','thoihan', 'ngayketthuc', 'tiencoc','canho','nguoithue', 'active')

    column_searchable_list = ['id']
    column_filters = ['active', 'tiencoc']
    can_delete = False


class HoaDonView(MyAuthenticatedView):
    column_list = ('id', 'hopdong', 'ngaythanhtoan', 'tongtien')
    column_filters = ['ngaythanhtoan', 'tongtien']
    can_export = True

    inline_models = (ChiTietHoaDon,)

    def on_model_change(self, form, model, is_created):
        tong_tien_moi = 0
        if model.ChiTietHoaDon:
            for cthd in model.ChiTietHoaDon:
                if not cthd.dongia and cthd.chitietphi:
                    cthd.dongia = cthd.chitietphi.sotienthu
                thanh_tien = cthd.dongia * cthd.soluong
                tong_tien_moi += thanh_tien
        model.tongtien = tong_tien_moi

class CanHoView(MyAuthenticatedView):
    column_list = ('ten','dientich','phongngu','tinhtrang','songuoitoida','DichVu')
    column_filters = ['dientich','phongngu','tinhtrang','songuoitoida','ten']
    can_delete = False

class ChiTietPhiView(MyAuthenticatedView):
    column_list = ('id','sotienthu','donvi','ghichu','DichVu','loaiphi','canho')
    column_filters = ['id','sotienthu','donvi','ghichu']
    can_delete = False
    can_edit = False

    column_labels = dict(
        canho='Các Phòng Đang Dùng'
    )

class DichVuView(MyAuthenticatedView):
    column_list = ('id','canho','id_canho','loai_phi',"id_chitietphi")
    column_searchable_list = ['id','id_canho','id_chitietphi']
    can_delete = False

class LoaiPhiView(MyAuthenticatedView):
    column_list = ('ten','mota')
    column_filters = ['ten','mota']
    can_delete = False

class HopDongSapHetHanView(MyAuthenticatedView):
    column_list = ('id','ngaybatdau','ngayketthuc','tiencoc','canho')
    can_edit = False
    can_delete = False
    can_create = False

    def get_query(self):
        hien_tai = datetime.now()
        ngay_gan_het_han = hien_tai + timedelta(days = 30)

        return self.session.query(HopDong).filter(HopDong.ngayketthuc <= ngay_gan_het_han, HopDong.active == True)

    def get_count_query(self):
        hien_tai = datetime.now()
        ngay_gan_het_han = hien_tai + timedelta(days = 30)

        return self.session.query(func.count("*")).filter(HopDong.ngayketthuc <= ngay_gan_het_han, HopDong.active == True)

admin.add_view(HoaDonView(HoaDon, db.session, name="Hóa Đơn"))
admin.add_view(HopDongView(HopDong, db.session, name="Hợp Đồng"))
admin.add_view(CanHoView(CanHo,db.session,name = "Căn Hộ"))
admin.add_view(DichVuView(DichVu,db.session,name= "Dịch Vụ"))
admin.add_view(ChiTietPhiView(ChiTietPhi,db.session,name="Chi tiết Phí"))
admin.add_view(LoaiPhiView(LoaiPhi,db.session,name="Loại Phí"))
admin.add_view(HopDongSapHetHanView(HopDong,db.session,name = "Hợp Đồng Sắp hết Hạn",endpoint="hop_dong_sap_het_han"))
admin.add_view(MyLogoutView("đăng xuất"))
