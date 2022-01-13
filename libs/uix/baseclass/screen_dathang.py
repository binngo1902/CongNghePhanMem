from kivy.clock import Clock
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog

from libs.applibs import utils

utils.load_kv("screen_dathang.kv")
class ScreenDatHang(MDBoxLayout):
    def __init__(self, **kwargs):
        super(ScreenDatHang, self).__init__(**kwargs)
        Clock.schedule_once(self.load_widget)
      
    def load_widget(self,obj):
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
        self.tong_soluong = 0
        self.tong_tien = 0
        for i in range(1,9):
            if (self.ids[f"sl_hanghoa{i}"].text != "" or self.ids[f"gia_tien{i}"].text != ""):
                if (self.ids[f"ma_hanghoa{i}"].text == "" or self.ids[f"ten_hanghoa{i}"].text == ""):
                    self.text1 = "Chưa nhập đầy đủ thông tin giá tiền hàng hóa"
                    return
            if (self.ids[f"sl_hanghoa{i}"].text != ""):
                self.tong_soluong += int(self.ids[f"sl_hanghoa{i}"].text)
            if (self.ids[f"gia_tien{i}"].text != ""):
                self.tong_tien += int(self.ids[f"gia_tien{i}"].text)    
        print(self.tong_soluong) 
        print(self.tong_tien)
        self.text1 = f"Tổng số lượng: {self.tong_soluong} \n\nTổng tiền: {self.tong_tien} VNĐ \n"
    def open_dialog(self):
        self.calculate()
        self.dialog =MDDialog(
            title="Đặt hàng",
            type="simple",
            text= self.text1,
            buttons=[
                MDRaisedButton(text="Đóng",on_release=self.close_dialog),
                MDRaisedButton(text="Đặt hàng",on_release=self.dathang)
            ],
        )
        self.dialog.open()

    def dathang(self,obj):
        self.dialog.dismiss()
        print("123")
    def close_dialog(self,obj):
        self.dialog.dismiss()
    def delete_all(self):
        for i in range(1,9):
            self.ids[f'ma_hanghoa{i}'].text = ""
            self.ids[f'ten_hanghoa{i}'].text = ""
            self.ids[f'sl_hanghoa{i}'].text = ""

