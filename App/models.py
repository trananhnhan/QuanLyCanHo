from datetime import datetime
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

class NguoiThue(Base):
    ho = Column(String(50), nullable=False)
    ten = Column(String(100), nullable=False)
    ngaysinh = Column(DateTime)
    congviec = Column(String(100))
    sodienthoai = Column(String(20), nullable=False)

    id_taikhoan = Column(Integer,ForeignKey(TaiKhoan.id))
    taikhoan = relationship('TaiKhoan', backref="NguoiThue", lazy=True)

class LoaiPhi(Base):
    ten = Column(String(50), nullable=False)
    mota = Column(String(150))

class ChiTietPhi(Base):
    sotienthu = Column(Integer, nullable=False)
    donvi = Column(String(30), nullable=False)
    ghichu = Column(String(150))

    loaiphi = relationship('LoaiPhi', backref="ChiTietPhi", lazy=True)
    id_loaiphi = Column(Integer,ForeignKey(LoaiPhi.id), nullable=False)

class CanHo(Base):
    ten = Column(String(100), nullable=False)
    dientich = Column(Integer, nullable=False)
    phongngu = Column(Integer, nullable=False)
    tinhtrang = Column(Enum(TinhTrang), default=TinhTrang.COTHETHUE)
    songuoitoida = Column(Integer, default=1)

class DichVu(Base):
    chitietphi = relationship('ChiTietPhi', backref="DichVu", lazy=True)
    id_chitietphi = Column(Integer, ForeignKey(ChiTietPhi.id), nullable=False)
    canho = relationship('CanHo', backref="DichVu", lazy=True)
    id_canho = Column(Integer, ForeignKey(CanHo.id), nullable=False)

class HopDong(Base):
    ngaybatdau = Column(DateTime, default=datetime.now)
    ngayketthuc = Column(DateTime, default=datetime.now)
    tiencoc = Column(Integer, default=0)

    canho = relationship('CanHo',backref="HopDong",lazy=True)
    id_canho = Column(Integer, ForeignKey(CanHo.id), nullable=False)
    nguoithue = relationship('NguoiThue',backref="HopDong",lazy=True)
    id_nguoithue = Column(Integer, ForeignKey(NguoiThue.id), nullable=False)

class HoaDon(Base):
    ngaythanhtoan = Column(DateTime)
    tongtien = Column(Integer)

    hopdong = relationship('HopDong',backref="HoaDon",lazy=True)
    id_hopdong = Column(Integer, ForeignKey(HopDong.id), nullable=False)

class ChiTietHoaDon(Base):
    soluong = Column(Integer,default= 1, nullable=False)
    dongia = Column(Integer, nullable=False)

    hoadon = relationship('HoaDon',backref="ChiTietHoaDon",lazy=True)
    id_hoadon = Column(Integer, ForeignKey(HoaDon.id), nullable=False)
    chitietphi = relationship('ChiTietPhi',backref="ChiTietHoaDon",lazy=True)
    id_chitietphi = Column(Integer, ForeignKey(ChiTietPhi.id), nullable=False)

class YeuCau(Base):
    tieude = Column(String(50), nullable=False)
    noidung = Column(String(500))
    ngaysua = Column(DateTime)

    taikhoan = relationship('TaiKhoan',backref="YeuCau",lazy=True)
    id_taikhoan = Column(Integer, ForeignKey(TaiKhoan.id), nullable=False)


def create_fake_data():

    pwhash = hashlib.md5("123456".encode('utf-8')).hexdigest()

    admin_acc = TaiKhoan(username="admin", password=pwhash, role=UserRole.ADMIN)
    user_acc1 = TaiKhoan(username="nguyenvana", password=pwhash, role=UserRole.USER)
    user_acc2 = TaiKhoan(username="tranthib", password=pwhash, role=UserRole.USER)

    db.session.add_all([admin_acc, user_acc1, user_acc2])
    db.session.commit()  # Commit để lấy ID cho các bước sau

    # 2. Tạo Người Thuê (Gắn với tài khoản)
    nt1 = NguoiThue(
        ho="Nguyễn Văn", ten="A",
        ngaysinh=datetime(1995, 5, 20),
        congviec="Lập trình viên",
        sodienthoai="0909123456",
        id_taikhoan=user_acc1.id
    )
    nt2 = NguoiThue(
        ho="Trần Thị", ten="B",
        ngaysinh=datetime(1998, 8, 15),
        congviec="Kế toán",
        sodienthoai="0909888999",
        id_taikhoan=user_acc2.id
    )
    db.session.add_all([nt1, nt2])

    # 3. Tạo Loại Phí & Chi Tiết Phí
    lp_phong = LoaiPhi(ten="Tiền Phòng", mota="Phí thuê căn hộ hàng tháng")
    lp_dien = LoaiPhi(ten="Tiền Điện", mota="Tính theo số kWh")
    lp_nuoc = LoaiPhi(ten="Tiền Nước", mota="Tính theo khối hoặc đầu người")
    lp_dv = LoaiPhi(ten="Dịch Vụ", mota="Rác, vệ sinh, thang máy")

    db.session.add_all([lp_phong, lp_dien, lp_nuoc, lp_dv])
    db.session.commit()

    # Tạo giá cụ thể (Snapshot giá)
    ctp_phong_vip = ChiTietPhi(sotienthu=5000000, donvi="Tháng", id_loaiphi=lp_phong.id, ghichu="Phòng VIP 1")
    ctp_phong_thuong = ChiTietPhi(sotienthu=3000000, donvi="Tháng", id_loaiphi=lp_phong.id, ghichu="Phòng thường")
    ctp_dien = ChiTietPhi(sotienthu=3500, donvi="kWh", id_loaiphi=lp_dien.id, ghichu="Giá điện nhà nước")
    ctp_nuoc = ChiTietPhi(sotienthu=100000, donvi="Người/Tháng", id_loaiphi=lp_nuoc.id, ghichu="Khoán theo đầu người")
    ctp_internet = ChiTietPhi(sotienthu=200000, donvi="Tháng", id_loaiphi=lp_dv.id, ghichu="Internet tốc độ cao")

    db.session.add_all([ctp_phong_vip, ctp_phong_thuong, ctp_dien, ctp_nuoc, ctp_internet])
    db.session.commit()

    # 4. Tạo Căn Hộ
    ch1 = CanHo(ten="P101", dientich=40, phongngu=1, tinhtrang=TinhTrang.DADAY, songuoitoida=2)
    ch2 = CanHo(ten="P102", dientich=25, phongngu=1, tinhtrang=TinhTrang.COTHETHUE, songuoitoida=1)
    ch3 = CanHo(ten="P201", dientich=50, phongngu=2, tinhtrang=TinhTrang.BAOTRI, songuoitoida=4)
    ch4 = CanHo(ten="P202", dientich=50, phongngu=2, tinhtrang=TinhTrang.BAOTRI, songuoitoida=4)
    ch5 = CanHo(ten="P203", dientich=50, phongngu=2, tinhtrang=TinhTrang.BAOTRI, songuoitoida=4)

    db.session.add_all([ch1, ch2, ch3, ch4, ch5])
    db.session.commit()

    # 5. Gán Dịch Vụ cho Căn Hộ (Cấu hình phí cho từng phòng)
    # P101 dùng phòng VIP, điện, nước, internet
    dv1 = DichVu(id_canho=ch1.id, id_chitietphi=ctp_phong_vip.id)
    dv2 = DichVu(id_canho=ch1.id, id_chitietphi=ctp_dien.id)
    dv3 = DichVu(id_canho=ch1.id, id_chitietphi=ctp_nuoc.id)

    # P102 dùng phòng thường
    dv4 = DichVu(id_canho=ch2.id, id_chitietphi=ctp_phong_thuong.id)

    db.session.add_all([dv1, dv2, dv3, dv4])
    db.session.commit()

    # 6. Tạo Hợp Đồng (Nguyễn Văn A thuê P101)
    hd1 = HopDong(
        ngaybatdau=datetime(2024, 1, 1),
        ngayketthuc=datetime(2025, 1, 1),
        tiencoc=5000000,
        id_canho=ch1.id,
        id_nguoithue=nt1.id
    )
    db.session.add(hd1)
    db.session.commit()

    # 7. Tạo Hóa Đơn (Tháng 2/2024 cho Hợp đồng 1)
    # Giả sử: 1 tháng tiền nhà + 100 số điện + 1 người nước
    tong_tien_tinh_toan = 5000000 + (100 * 3500) + (1 * 100000)  # = 5.450.000

    hdon1 = HoaDon(
        id_hopdong=hd1.id,
        ngaythanhtoan=datetime(2024, 2, 5),  # Đã thanh toán ngày 5
        tongtien=tong_tien_tinh_toan
    )
    db.session.add(hdon1)
    db.session.commit()

    # 8. Chi Tiết Hóa Đơn (Lưu snapshot giá tại thời điểm đó)
    cthd1 = ChiTietHoaDon(id_hoadon=hdon1.id, id_chitietphi=ctp_phong_vip.id, soluong=1, dongia=5000000)
    cthd2 = ChiTietHoaDon(id_hoadon=hdon1.id, id_chitietphi=ctp_dien.id, soluong=100, dongia=3500)
    cthd3 = ChiTietHoaDon(id_hoadon=hdon1.id, id_chitietphi=ctp_nuoc.id, soluong=1, dongia=100000)

    db.session.add_all([cthd1, cthd2, cthd3])

    # 9. Tạo Yêu Cầu (Support Ticket)
    yc1 = YeuCau(
        tieude="Hỏng bóng đèn",
        noidung="Bóng đèn nhà vệ sinh P101 bị cháy, nhờ admin thay giúp.",
        ngaysua=None,  # Chưa sửa
        id_taikhoan=user_acc1.id
    )
    db.session.add(yc1)

    # Lưu tất cả vào DB
    db.session.commit()
    print(">>> Đã tạo dữ liệu giả thành công!")

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