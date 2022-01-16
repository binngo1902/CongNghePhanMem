import json
from kivy.clock import Clock
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from apiWeb import ApiWeb

from libs.applibs import utils

utils.load_kv("screen_dathang.kv")
class ScreenDatHang(MDScreen):
    def __init__(self, **kwargs):
        super(ScreenDatHang, self).__init__(**kwargs)
        self.api_web = ApiWeb()
    def on_enter(self):
        self.method = ""
        self.text_error = ""
        self.text_dathang = ""
        Clock.schedule_once(self.load_widget)
      
    def load_widget(self,obj):
        self.ids.bigbox_dathang.clear_widgets()
        for i in range(1,9):
            box = MDBoxLayout(
                
                size_hint=(1,0.1),
                orientation='horizontal',
                spacing=10,
            )
            self.ids[f'box{i}'] = box
            field1 = MDTextField(
                hint_text=f"Mã hàng hóa {i}",
                font_size=15,
            )
            self.ids[f"ma_hanghoa{i}"]= field1
            field2 = MDTextField(
                hint_text=f"Tên hàng hóa ",
                font_size=15
            )
            self.ids[f"ten_hanghoa{i}"]= field2

            field3 = MDTextField(
                hint_text=f"Số lượng ",
                input_filter= 'int',

                font_size=15
            )
            self.ids[f"sl_hanghoa{i}"]= field3
            field4 = MDTextField(
                hint_text=f"Giá tiền (VNĐ) ",
                input_filter= 'int',
                font_size=15
            )
            self.ids[f"gia_tien{i}"]= field4

            box.add_widget(field1)
            box.add_widget(field2)
            box.add_widget(field3)
            box.add_widget(field4)
            self.ids.bigbox_dathang.add_widget(box)
    def calculate(self):
        self.rows = []
        self.tong_soluong = 0
        self.tong_tien = 0
        for i in range(1,9):
            if (self.ids[f'sl_hanghoa{i}'].text == "" and self.ids[f'ma_hanghoa{i}'].text == "" 
                    and self.ids[f'ten_hanghoa{i}'].text == "" and self.ids[f'gia_tien{i}'].text == ""):
                continue
            if (self.ids[f"sl_hanghoa{i}"].text == "" or self.ids[f"gia_tien{i}"].text == "" or self.ids[f"ma_hanghoa{i}"].text == "" or self.ids[f"ten_hanghoa{i}"].text == ""):
                    self.text_error = "Chưa nhập đầy đủ thông tin giá tiền hàng hóa"
                    return
            if (self.ids[f"sl_hanghoa{i}"].text != ""):
                self.tong_soluong += int(self.ids[f"sl_hanghoa{i}"].text)
            if (self.ids[f"gia_tien{i}"].text != ""):
                self.tong_tien += int(self.ids[f"gia_tien{i}"].text) 
            self.rows.append(i)
        if self.ids["khach_hang"].text == "": 
            self.text_error= "Chưa nhập tên khách hàng"
            return
        if self.method == "": 
            self.text_error= "Chưa chọn phương thức thanh toán"
            return
        # print(self.tong_soluong) 
        # print(self.tong_tien)
        self.text_dathang = f"Tổng số lượng: {self.tong_soluong} \n\nTổng tiền: {self.tong_tien} VNĐ \n"
    def open_dialog(self):
        self.calculate()
        if self.text_error != "":
            self.dialog =MDDialog(
                title="Thông báo lỗi",
                type="simple",
                text= self.text_error,
                buttons=[
                    MDRaisedButton(text="Đóng",on_release=self.close_dialog),
                ],
            )
            self.text_error = ""
            self.dialog.open()
        if self.text_dathang != "":
            self.dialog =MDDialog(
                title="Đặt hàng",
                type="simple",
                text= self.text_dathang,
                buttons=[
                    MDRaisedButton(text="Hủy",on_release=self.close_dialog),
                    MDRaisedButton(text="Đặt hàng",on_release=self.dathang),

                ],
            )
            self.text_dathang = ""
            self.dialog.open()

    def close_dialog(self,obj):
        self.dialog.dismiss()

    def dathang(self,obj):
        self.dialog.dismiss()
        if self.tong_soluong == 0 or self.tong_tien == 0:
            self.dialog =MDDialog(
                title="Thông báo lỗi",
                type="simple",
                text= "Bạn chưa chọn sản phẩm nào",
                buttons=[
                    MDRaisedButton(text="Đóng",on_release=self.close_dialog),
                ],
            )
            self.dialog.open()
            return
        dathang = {}
        dathang['danhsach'] = []
        self.error = []
        for i in self.rows:
            data = {}
            data["id"] = self.ids[f"ma_hanghoa{i}"].text
            data["ten_hang_hoa"] = self.ids[f"ten_hanghoa{i}"].text
            data["so_luong"] = self.ids[f"sl_hanghoa{i}"].text
            data["gia_tien"] = self.ids[f"gia_tien{i}"].text
            dathang['danhsach'].append(data) 
        # print(json.dumps(list_hanghoa)) 
        dathang['khach_hang'] = self.ids['khach_hang'].text
        dathang['thanh_toan'] = self.method
        dathang['tong_tien'] = self.tong_tien
        dathang['tong_sanpham'] = self.tong_soluong
        check = self.api_web.check_hanghoa(json.dumps(dathang))
        # print(data)
        # return
        # data = self.api_web.order_hanghoa(json.dumps(dathang))
        # print(data)
        if check != 1:
            self.dialog =MDDialog(
                title="Thông báo",
                type="simple",
                text= check,
                buttons=[
                    MDRaisedButton(text="Đóng",on_release=self.close_dialog),
                ],
            )
            self.dialog.open()
        else:
            order = self.api_web.order_hanghoa(json.dumps(dathang))
            if order !=1:
                self.dialog =MDDialog(
                title="Thông báo",
                type="simple",
                text= "Đơn hàng bị lỗi hoặc bị trùng, xin kiểm tra lại",
                buttons=[
                    MDRaisedButton(text="Đóng",on_release=self.close_dialog),
                ],
                )
                self.dialog.open()
            else:
                self.dialog =MDDialog(
                title="Thông báo",
                type="simple",
                text= "Đặt hàng thành công",
                buttons=[
                    MDRaisedButton(text="Đóng",on_release=self.close_dialog),
                ],
                )
                self.dialog.open()

    def method_pay(self,method):
        if method == 1:
            self.method = "Tiền mặt"
        if method == 2:
            self.method = "Chuyển khoản"
        print(self.method)
    def delete_all(self):
        for i in range(1,9):
            self.ids[f'ma_hanghoa{i}'].text = ""
            self.ids[f'ten_hanghoa{i}'].text = ""
            self.ids[f'sl_hanghoa{i}'].text = ""

