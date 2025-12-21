from datetime import datetime, timedelta
from enum import Enum as RoleEnum
from symtable import Class
import hashlib
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Enum, Text, false
from sqlalchemy.orm import relationship
from App import db, app
from flask_login import UserMixin




class UserRole(RoleEnum):
    USER = 0
    ADMIN = 1
class TinhTrang(RoleEnum):
    COTHETHUE = 0
    DADAY = 1
    BAOTRI = 2

class Base(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True,autoincrement=True)
    create_date = Column(DateTime, default=datetime.now)
    active = Column(Boolean, default=True)

    def __str__(self):
        return str(self.id)

class TaiKhoan(Base, UserMixin):
    username = Column(String(150), nullable=False, unique=True)
    password = Column(String(150), nullable=False)
    avatar = Column(String(150),default="https://res.cloudinary.com/dy1unykph/image/upload/v1740037805/apple-iphone-16-pro-natural-titanium_lcnlu2.webp")
    role = Column(Enum(UserRole), default= UserRole.USER, nullable= false)

    def __str__(self):
        return str(self.username)

class NguoiThue(Base):
    ho = Column(String(50), nullable=False)
    ten = Column(String(100), nullable=False)
    ngaysinh = Column(DateTime)
    congviec = Column(String(100))
    sodienthoai = Column(String(20), nullable=False)

    id_taikhoan = Column(Integer,ForeignKey(TaiKhoan.id))
    taikhoan = relationship('TaiKhoan', backref="NguoiThue", lazy=True)

    def __str__(self):
        return str(self.ho +" " +self.ten)

class LoaiPhi(Base):
    ten = Column(String(50), nullable=False)
    mota = Column(String(150))
    def __str__(self):
        return str(self.ten)

class ChiTietPhi(Base):
    sotienthu = Column(Integer, nullable=False)
    donvi = Column(String(30), nullable=False)
    ghichu = Column(String(150))

    loaiphi = relationship('LoaiPhi', backref="ChiTietPhi", lazy=True)
    id_loaiphi = Column(Integer,ForeignKey(LoaiPhi.id), nullable=False)

    @property
    def canho(self):
        if not self.DichVu:
            return "Chưa sử dụng"
        ds_phong = []
        for dv in self.DichVu:
            if dv.canho:
                ds_phong.append(dv.canho.ten)
        return ", ".join(ds_phong)


class CanHo(Base):
    ten = Column(String(100), nullable=False)
    dientich = Column(Integer, nullable=False)
    phongngu = Column(Integer, nullable=False)
    tinhtrang = Column(Enum(TinhTrang), default=TinhTrang.COTHETHUE)
    songuoitoida = Column(Integer, default=1)
    mota = Column(String(150),default="Căn hộ này rất đẹp")
    img = Column(String(150),default="https://res.cloudinary.com/dy1unykph/image/upload/v1740037805/apple-iphone-16-pro-natural-titanium_lcnlu2.webp")

    def __str__(self):
        return str(self.ten)

class DichVu(Base):
    chitietphi = relationship('ChiTietPhi', backref="DichVu", lazy=True)
    id_chitietphi = Column(Integer, ForeignKey(ChiTietPhi.id), nullable=False)
    canho = relationship('CanHo', backref="DichVu", lazy=True)
    id_canho = Column(Integer, ForeignKey(CanHo.id), nullable=False)

    @property
    def loai_phi(self):
        return self.chitietphi.loaiphi

class HopDong(Base):
    ngaybatdau = Column(DateTime, default=datetime.now)
    thoihan = Column(Integer,default=1,nullable=False)
    tiencoc = Column(Integer, default=0)

    canho = relationship('CanHo',backref="HopDong",lazy=True)
    id_canho = Column(Integer, ForeignKey(CanHo.id), nullable=False)
    nguoithue = relationship('NguoiThue',backref="HopDong",lazy=True)
    id_nguoithue = Column(Integer, ForeignKey(NguoiThue.id), nullable=False)

    @property
    def ngayketthuc(self):
        return self.ngaybatdau + timedelta(days=self.thoihan * 30)

class HoaDon(Base):
    ngaythanhtoan = Column(DateTime)
    tongtien = Column(Integer)

    hopdong = relationship('HopDong',backref="HoaDon",lazy=True)
    id_hopdong = Column(Integer, ForeignKey(HopDong.id), nullable=False)

class ChiTietHoaDon(Base):
    soluong = Column(Integer,default= 1, nullable=False)
    dongia = Column(Integer, nullable=True)

    hoadon = relationship('HoaDon',backref="ChiTietHoaDon",lazy=True)
    id_hoadon = Column(Integer, ForeignKey(HoaDon.id), nullable=False)
    chitietphi = relationship('ChiTietPhi',backref="ChiTietHoaDon",lazy=True)
    id_chitietphi = Column(Integer, ForeignKey(ChiTietPhi.id), nullable=False)

class YeuCau(Base):
    tieude = Column(String(50), nullable=False)
    noidung = Column(String(500))
    ngayxuly = Column(DateTime)

    taikhoan = relationship('TaiKhoan',backref="YeuCau",lazy=True)
    id_taikhoan = Column(Integer, ForeignKey(TaiKhoan.id), nullable=False)


import hashlib
from datetime import datetime


# Import db và models của bạn ở đây nếu file tách biệt

def create_fake_data():
    print(">>> Bắt đầu tạo dữ liệu giả...")

    # 1. BẢNG TÀI KHOẢN (TaiKhoan)

    pwhash = hashlib.md5("123".encode('utf-8')).hexdigest()

    admin_acc = TaiKhoan(username="admin", password=pwhash, role=UserRole.ADMIN)
    user_acc1 = TaiKhoan(username="nguyenvana", password=pwhash, role=UserRole.USER)
    user_acc2 = TaiKhoan(username="tranthib", password=pwhash, role=UserRole.USER)
    user_acc3 = TaiKhoan(username="user1", password=pwhash, role=UserRole.USER)  # User test chính: Nhân

    db.session.add_all([admin_acc, user_acc1, user_acc2, user_acc3])
    db.session.commit()


    # 2. BẢNG NGƯỜI THUÊ (NguoiThue)

    nt1 = NguoiThue(ho="Nguyễn Văn", ten="A", ngaysinh=datetime(1995, 5, 20), congviec="Lập trình viên",
                    sodienthoai="0909123456", id_taikhoan=user_acc1.id)
    nt2 = NguoiThue(ho="Trần Thị", ten="B", ngaysinh=datetime(1998, 8, 15), congviec="Kế toán",
                    sodienthoai="0909888999", id_taikhoan=user_acc2.id)
    nt3 = NguoiThue(ho="Trần Anh", ten="Nhân", ngaysinh=datetime(1998, 8, 15), congviec="IT", sodienthoai="0909888999",
                    id_taikhoan=user_acc3.id)

    db.session.add_all([nt1, nt2, nt3])
    db.session.commit()


    # 3. BẢNG LOẠI PHÍ (LoaiPhi)

    lp_phong = LoaiPhi(ten="Tiền Phòng", mota="Phí thuê căn hộ hàng tháng")
    lp_dien = LoaiPhi(ten="Tiền Điện", mota="Tính theo số kWh")
    lp_nuoc = LoaiPhi(ten="Tiền Nước", mota="Tính theo khối hoặc đầu người")
    lp_dv = LoaiPhi(ten="Dịch Vụ", mota="Rác, vệ sinh, thang máy")
    lp_gui_xe = LoaiPhi(ten="Gửi xe", mota="Phí bãi giữ xe")  # Đưa lên đây luôn cho gọn

    db.session.add_all([lp_phong, lp_dien, lp_nuoc, lp_dv, lp_gui_xe])
    db.session.commit()

    # 4. BẢNG CHI TIẾT PHÍ (ChiTietPhi - Bảng giá niêm yết)

    # Giá phòng
    ctp_phong_vip = ChiTietPhi(sotienthu=5000000, donvi="Tháng", id_loaiphi=lp_phong.id, ghichu="Phòng VIP 1")
    ctp_phong_thuong = ChiTietPhi(sotienthu=3000000, donvi="Tháng", id_loaiphi=lp_phong.id, ghichu="Phòng thường")
    # Giá điện nước
    ctp_dien = ChiTietPhi(sotienthu=3500, donvi="kWh", id_loaiphi=lp_dien.id, ghichu="Giá điện nhà nước")
    ctp_nuoc = ChiTietPhi(sotienthu=100000, donvi="Người/Tháng", id_loaiphi=lp_nuoc.id, ghichu="Khoán theo đầu người")
    # Giá dịch vụ
    ctp_internet = ChiTietPhi(sotienthu=200000, donvi="Tháng", id_loaiphi=lp_dv.id, ghichu="Internet tốc độ cao")
    ctp_xe_may = ChiTietPhi(sotienthu=150000, donvi="Xe/Tháng", id_loaiphi=lp_gui_xe.id, ghichu="Xe máy tay ga")

    db.session.add_all([ctp_phong_vip, ctp_phong_thuong, ctp_dien, ctp_nuoc, ctp_internet, ctp_xe_may])
    db.session.commit()

    # 5. BẢNG CĂN HỘ (CanHo)

    ch1 = CanHo(ten="P101", dientich=40, phongngu=1, tinhtrang=TinhTrang.DADAY, songuoitoida=2)
    ch2 = CanHo(ten="P102", dientich=25, phongngu=1, tinhtrang=TinhTrang.COTHETHUE, songuoitoida=1)
    ch3 = CanHo(ten="P201", dientich=50, phongngu=2, tinhtrang=TinhTrang.BAOTRI, songuoitoida=4)
    ch4 = CanHo(ten="P202", dientich=50, phongngu=3, tinhtrang=TinhTrang.COTHETHUE, songuoitoida=5)
    ch5 = CanHo(ten="P203", dientich=50, phongngu=3, tinhtrang=TinhTrang.COTHETHUE, songuoitoida=5)
    ch6 = CanHo(ten="P301", dientich=50, phongngu=2, tinhtrang=TinhTrang.COTHETHUE, songuoitoida=5)
    ch7 = CanHo(ten="P302", dientich=50, phongngu=4, tinhtrang=TinhTrang.COTHETHUE, songuoitoida=7)
    ch8 = CanHo(ten="P303", dientich=50, phongngu=5, tinhtrang=TinhTrang.COTHETHUE, songuoitoida=15)
    ch9 = CanHo(ten="SVIP", dientich=500, phongngu=8, tinhtrang=TinhTrang.COTHETHUE, songuoitoida=8)

    db.session.add_all([ch1, ch2, ch3, ch4, ch5, ch6, ch7, ch8, ch9])
    db.session.commit()


    # 6. BẢNG DỊCH VỤ (DichVu - Cấu hình phí cho từng phòng)

    # P101: VIP + Điện + Nước
    db.session.add_all([
        DichVu(id_canho=ch1.id, id_chitietphi=ctp_phong_vip.id),
        DichVu(id_canho=ch1.id, id_chitietphi=ctp_dien.id),
        DichVu(id_canho=ch1.id, id_chitietphi=ctp_nuoc.id)
    ])
    # P102: Thường
    db.session.add(DichVu(id_canho=ch2.id, id_chitietphi=ctp_phong_thuong.id))

    db.session.commit()

    # 7. BẢNG HỢP ĐỒNG (HopDong)

    # HD1: Nguyễn Văn A - P101 (Hết hạn/Hủy)
    hd1 = HopDong(ngaybatdau=datetime(2024, 11, 1), thoihan = 7, tiencoc=5000000, id_canho=ch1.id,
                  id_nguoithue=nt1.id, active=False)
    # HD2: Trần Thị B - P101 (Hết hạn/Hủy)
    hd2 = HopDong(ngaybatdau=datetime(2024, 10, 1), thoihan = 9, tiencoc=5000000, id_canho=ch1.id,
                  id_nguoithue=nt2.id, active=False)

    # --- CÁC HỢP ĐỒNG ĐANG HOẠT ĐỘNG (Dùng để test) ---
    # HD3: Nhân (User1) - P101
    hd3 = HopDong(ngaybatdau=datetime(2025, 11, 1), thoihan = 5, tiencoc=5000000, id_canho=ch1.id,
                  id_nguoithue=nt3.id)
    # HD4: Nhân (User1) - P202 (Thuê thêm phòng nữa)
    hd4 = HopDong(ngaybatdau=datetime(2025, 10, 1), thoihan = 3, tiencoc=5000000, id_canho=ch4.id,
                  id_nguoithue=nt3.id)
    # HD5: Nguyễn Văn A - P302
    hd5 = HopDong(ngaybatdau=datetime(2025, 11, 1), thoihan = 2, tiencoc=5000000, id_canho=ch7.id,
                  id_nguoithue=nt1.id)

    db.session.add_all([hd1, hd2, hd3, hd4, hd5])
    db.session.commit()


    # 8. BẢNG HÓA ĐƠN & CHI TIẾT HÓA ĐƠN



    # --- KỊCH BẢN 1: HÓA ĐƠN CHO HD5 (NGUYỄN VĂN A) ---
    # Giả sử có 3 tháng hóa đơn mẫu
    base_total = 5000000 + (100 * 3500) + (1 * 100000)

    hdon_mau_1 = HoaDon(id_hopdong=hd5.id, ngaythanhtoan=datetime(2025, 12, 5), tongtien=base_total,
                        create_date=datetime(2025, 12, 1))
    hdon_mau_2 = HoaDon(id_hopdong=hd5.id, ngaythanhtoan=datetime(2025, 11, 5), tongtien=base_total,
                        create_date=datetime(2025, 11, 1))
    hdon_mau_3 = HoaDon(id_hopdong=hd5.id, ngaythanhtoan=datetime(2025, 10, 5), tongtien=base_total,
                        create_date=datetime(2025, 10, 1))

    db.session.add_all([hdon_mau_1, hdon_mau_2, hdon_mau_3])
    db.session.commit()

    # Thêm chi tiết cho hdon_mau_1 (Demo 1 cái đại diện)
    db.session.add_all([
        ChiTietHoaDon(id_hoadon=hdon_mau_1.id, id_chitietphi=ctp_phong_vip.id, soluong=1, dongia=5000000),
        ChiTietHoaDon(id_hoadon=hdon_mau_1.id, id_chitietphi=ctp_dien.id, soluong=100, dongia=3500),
        ChiTietHoaDon(id_hoadon=hdon_mau_1.id, id_chitietphi=ctp_nuoc.id, soluong=1, dongia=100000)
    ])

    # --- KỊCH BẢN 2: USER "NHÂN" (HD3 - P101) - TEST TRANG CHI TIÊU & THANH TOÁN ---

    # 2.1 Tháng 10/2025 (Đã thanh toán)
    hd3_t10 = HoaDon(id_hopdong=hd3.id, ngaythanhtoan=datetime(2025, 10, 5), tongtien=5620000,
                     create_date=datetime(2025, 10, 1))
    db.session.add(hd3_t10)
    db.session.commit()
    db.session.add_all([
        ChiTietHoaDon(id_hoadon=hd3_t10.id, id_chitietphi=ctp_phong_vip.id, soluong=1, dongia=5000000),
        ChiTietHoaDon(id_hoadon=hd3_t10.id, id_chitietphi=ctp_dien.id, soluong=120, dongia=3500),
        ChiTietHoaDon(id_hoadon=hd3_t10.id, id_chitietphi=ctp_nuoc.id, soluong=1, dongia=100000),
        ChiTietHoaDon(id_hoadon=hd3_t10.id, id_chitietphi=ctp_internet.id, soluong=1, dongia=200000)
    ])

    # 2.2 Tháng 11/2025 (Đã thanh toán - Dùng ít điện hơn)
    hd3_t11 = HoaDon(id_hopdong=hd3.id, ngaythanhtoan=datetime(2025, 11, 5), tongtien=5480000,
                     create_date=datetime(2025, 11, 1))
    db.session.add(hd3_t11)
    db.session.commit()
    db.session.add_all([
        ChiTietHoaDon(id_hoadon=hd3_t11.id, id_chitietphi=ctp_phong_vip.id, soluong=1, dongia=5000000),
        ChiTietHoaDon(id_hoadon=hd3_t11.id, id_chitietphi=ctp_dien.id, soluong=80, dongia=3500),
        ChiTietHoaDon(id_hoadon=hd3_t11.id, id_chitietphi=ctp_nuoc.id, soluong=1, dongia=100000),
        ChiTietHoaDon(id_hoadon=hd3_t11.id, id_chitietphi=ctp_internet.id, soluong=1, dongia=200000)
    ])

    # 2.3 Tháng 12/2025 (CHƯA THANH TOÁN - Test chức năng thanh toán)
    # Có thêm phí gửi xe
    hd3_t12 = HoaDon(id_hopdong=hd3.id, ngaythanhtoan=None, tongtien=5875000, create_date=datetime(2025, 12, 1))
    db.session.add(hd3_t12)
    db.session.commit()
    db.session.add_all([
        ChiTietHoaDon(id_hoadon=hd3_t12.id, id_chitietphi=ctp_phong_vip.id, soluong=1, dongia=5000000),
        ChiTietHoaDon(id_hoadon=hd3_t12.id, id_chitietphi=ctp_dien.id, soluong=150, dongia=3500),
        ChiTietHoaDon(id_hoadon=hd3_t12.id, id_chitietphi=ctp_nuoc.id, soluong=1, dongia=100000),
        ChiTietHoaDon(id_hoadon=hd3_t12.id, id_chitietphi=ctp_internet.id, soluong=1, dongia=200000),
        ChiTietHoaDon(id_hoadon=hd3_t12.id, id_chitietphi=ctp_xe_may.id, soluong=1, dongia=150000)
    ])

    # --- KỊCH BẢN 3: USER "NHÂN" (HD4 - P202) - TEST ĐA HỢP ĐỒNG ---

    # 3.1 Tháng 11/2025 (Đã thanh toán)
    hd4_t11 = HoaDon(id_hopdong=hd4.id, ngaythanhtoan=datetime(2025, 11, 10), tongtien=3375000,
                     create_date=datetime(2025, 11, 1))
    db.session.add(hd4_t11)
    db.session.commit()
    db.session.add_all([
        ChiTietHoaDon(id_hoadon=hd4_t11.id, id_chitietphi=ctp_phong_thuong.id, soluong=1, dongia=3000000),
        ChiTietHoaDon(id_hoadon=hd4_t11.id, id_chitietphi=ctp_dien.id, soluong=50, dongia=3500),
        ChiTietHoaDon(id_hoadon=hd4_t11.id, id_chitietphi=ctp_nuoc.id, soluong=2, dongia=100000)  # 2 người
    ])

    # 3.2 Tháng 12/2025 (CHƯA THANH TOÁN)
    hd4_t12 = HoaDon(id_hopdong=hd4.id, ngaythanhtoan=None, tongtien=3340000, create_date=datetime(2025, 12, 1))
    db.session.add(hd4_t12)
    db.session.commit()
    db.session.add_all([
        ChiTietHoaDon(id_hoadon=hd4_t12.id, id_chitietphi=ctp_phong_thuong.id, soluong=1, dongia=3000000),
        ChiTietHoaDon(id_hoadon=hd4_t12.id, id_chitietphi=ctp_dien.id, soluong=40, dongia=3500),
        ChiTietHoaDon(id_hoadon=hd4_t12.id, id_chitietphi=ctp_nuoc.id, soluong=2, dongia=100000)
    ])

    # 9. BẢNG YÊU CẦU (YeuCau)
    yc1 = YeuCau(
        tieude="Hỏng bóng đèn",
        noidung="Bóng đèn nhà vệ sinh P101 bị cháy, nhờ admin thay giúp.",
        ngayxuly=None,
        id_taikhoan=user_acc1.id
    )
    db.session.add(yc1)

    # Commit cuối cùng cho chắc chắn
    db.session.commit()
    print(">>> ĐÃ TẠO DỮ LIỆU GIẢ THÀNH CÔNG! <<<")

if __name__ == '__main__':
    with app.app_context():
        # Xóa hết bảng cũ (cẩn thận khi dùng lệnh này nếu có dữ liệu thật)
        db.drop_all()

        # Tạo lại bảng
        db.create_all()

        # Kiểm tra xem đã có dữ liệu chưa, nếu chưa thì tạo
        if not TaiKhoan.query.first():
            try:
                create_fake_data()
            except Exception as e:
                print(f"Có lỗi khi tạo dữ liệu giả: {e}")
                db.session.rollback()
        else:
            print(">>> Dữ liệu đã tồn tại, không tạo thêm.")