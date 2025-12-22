from datetime import datetime, timedelta

from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_admin.theme import Bootstrap4Theme
from flask_login import current_user, logout_user
from sqlalchemy import func
from werkzeug.utils import redirect

from App import app, db, dao
from App.models import UserRole, HopDong, HoaDon, CanHo, ChiTietPhi, LoaiPhi, DichVu, ChiTietHoaDon, NguoiThue


class MyAuthenticatedView(ModelView):
    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.role==UserRole.ADMIN

class MyAuthenticatedBaseView(BaseView):
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
        return redirect("/")

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

class NguoiThueView(MyAuthenticatedView):
    column_list = ('ho','ten','congviec','sodienthoai','taikhoan')
    column_filters = ('ho','ten','congviec','sodienthoai','taikhoan')

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
        ngay_gan_het_han = hien_tai + timedelta(days=30)

        ds_hd_active = self.session.query(HopDong).filter(HopDong.active == True).all()
        ids_can_lay = []
        for hd in ds_hd_active:
            if hd.ngayketthuc and hien_tai <= hd.ngayketthuc <= ngay_gan_het_han:
                ids_can_lay.append(hd.id)
        if not ids_can_lay:
            return self.session.query(HopDong).filter(False)
        return self.session.query(HopDong).filter(HopDong.id.in_(ids_can_lay))

    def get_count_query(self):
        hien_tai = datetime.now()
        ngay_gan_het_han = hien_tai + timedelta(days = 30)

        ds_hop_dong_active = self.session.query(HopDong).filter(HopDong.active == True).all()
        ids_can_lay = []
        for hd in ds_hop_dong_active:
            if hd.ngayketthuc <= ngay_gan_het_han:
                ids_can_lay.append(hd.id)
        return self.session.query(func.count('*')).filter(HopDong.id.in_(ids_can_lay))

class DoanhThuView(MyAuthenticatedBaseView):
    @expose('/')
    def hien_doanh_thu(self):
        ds_du_lieu_truy_van = dao.tinh_doanh_thu()
        ds_du_lieu_giao_dien = []
        for dl in ds_du_lieu_truy_van:
            nam = int(dl[0])
            thang = int(dl[1])
            tien = int(dl[2])

            ten_thoi_gian = f"{thang:02d}/{nam}"
            ds_du_lieu_giao_dien.append((ten_thoi_gian,tien))
        return self.render("admin/doanhthu.html", ds_du_lieu_giao_dien = ds_du_lieu_giao_dien)

class TinhTrangThueView(MyAuthenticatedBaseView):
    @expose('/')
    def hien_tinh_trang_thue(self):
        ds_du_lieu_truy_van = dao.tinh_trang_thue_phong()
        ds_du_lieu_giao_dien = []
        for dl in ds_du_lieu_truy_van:
            ten_phong = dao.get_phong_by_id(int(dl[0])).ten
            tong_thoi_han = int(dl[1])

            ds_du_lieu_giao_dien.append((ten_phong,tong_thoi_han))
        return self.render("admin/tinhtrangthue.html",ds_du_lieu_giao_dien = ds_du_lieu_giao_dien )

admin.add_view(HoaDonView(HoaDon, db.session, name="Hóa Đơn"))
admin.add_view(HopDongView(HopDong, db.session, name="Hợp Đồng"))
admin.add_view(CanHoView(CanHo,db.session,name = "Căn Hộ"))
admin.add_view(NguoiThueView(NguoiThue, db.session, name="Người Thuê"))
admin.add_view(DichVuView(DichVu,db.session,name= "Dịch Vụ"))
admin.add_view(ChiTietPhiView(ChiTietPhi,db.session,name="Chi tiết Phí"))
admin.add_view(LoaiPhiView(LoaiPhi,db.session,name="Loại Phí"))
admin.add_view(HopDongSapHetHanView(HopDong,db.session,name = "Hợp Đồng Sắp hết Hạn",endpoint="hop_dong_sap_het_han"))
admin.add_view(DoanhThuView(name="Doanh thu",endpoint="doanh_thu"))
admin.add_view(TinhTrangThueView(name="Tình Trạng Thuê",endpoint="tinh_trang_thue"))
admin.add_view(MyLogoutView("đăng xuất"))
