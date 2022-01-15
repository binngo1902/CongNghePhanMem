import json
from kivy.clock import Clock
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from ApiWeb import ApiWeb
from libs.applibs import utils
from kivymd.uix.textfield import MDTextField
from kivy.uix.widget import Widget
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp


utils.load_kv("screen_nhapkho.kv")
class ScreenNhapKho(MDScreen):
    def __init__(self, **kwargs):
        super(ScreenNhapKho, self).__init__(**kwargs)
        self.api_web = ApiWeb()
    def on_enter(self):
        Clock.schedule_once(self.load_widget)

    def load_widget(self,obj):
        self.ids.bigbox.clear_widgets()
        for i in range(1,9):
            box = MDBoxLayout(
                
                size_hint=(1,0.1),
                orientation='horizontal',
                spacing=10,
            )
            self.ids[f'box{i}'] = box
            field1 = MDTextField(
                hint_text=f"Mã hàng hóa {i}",
                font_size=15
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

            box.add_widget(field1)
            box.add_widget(field2)
            box.add_widget(field3)
            self.ids.bigbox.add_widget(box)
       
    def insert(self):
        list_hanghoa = {}
        list_hanghoa['danhsach'] = []
        self.error = []
        for i in range(1,9):
            if (self.ids[f"sl_hanghoa{i}"].text == ""  and self.ids[f"ma_hanghoa{i}"].text == "" and self.ids[f"ten_hanghoa{i}"].text == "" ):
                continue
            if (self.ids[f"sl_hanghoa{i}"].text == ""  or self.ids[f"ma_hanghoa{i}"].text == "" or self.ids[f"ten_hanghoa{i}"].text == ""):
                    self.error.append(i)
                    continue
            data = {}
            data["id"] = self.ids[f"ma_hanghoa{i}"].text
            data["ten_hang_hoa"] = self.ids[f"ten_hanghoa{i}"].text
            data["so_luong"] = self.ids[f"sl_hanghoa{i}"].text
            list_hanghoa['danhsach'].append(data) 
        # print(json.dumps(list_hanghoa)) 
        data = self.api_web.insert_hanghoa(json.dumps(list_hanghoa))
        if data == 1:
            
            self.dialog =MDDialog(
                title="Nhập hàng",
                type="simple",
                text= f"Nhập hàng thành công\nNgoại trừ các hàng: {self.error} ",
                buttons=[
                    MDRaisedButton(text="Đóng",on_release=self.close_dialog),
                ],
            )
            self.dialog.open()
        else:
            print(data)         
   
    def close_dialog(self,obj):
        self.delete(self.error)
        self.dialog.dismiss()
    def delete(self,array):
        for i in range(1,9):
            if i not in array:
                self.ids[f'ma_hanghoa{i}'].text = ""
                self.ids[f'ten_hanghoa{i}'].text = ""
                self.ids[f'sl_hanghoa{i}'].text = ""


    def delete_all(self):
        for i in range(1,9):
            self.ids[f'ma_hanghoa{i}'].text = ""
            self.ids[f'ten_hanghoa{i}'].text = ""
            self.ids[f'sl_hanghoa{i}'].text = ""

