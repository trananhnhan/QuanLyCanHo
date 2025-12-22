def tinh_tong_tien_da_tra_thang_tu_ds_hoa_don(ds_hoa_don,nam,thang):
    tong = 0
    for hd in ds_hoa_don:
        if hd.ngaythanhtoan and hd.ngaythanhtoan.month == thang and hd.ngaythanhtoan.year == nam:
            tong += hd.tongtien
    return tong

