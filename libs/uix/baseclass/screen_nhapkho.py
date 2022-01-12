from kivymd.uix.boxlayout import MDBoxLayout
from libs.applibs import utils

utils.load_kv("screen_nhapkho.kv")
class ScreenNhapKho(MDBoxLayout):
    def delete_all(self):
        self.ids.ma_hanghoa.text = ""
        self.ids.ma_hanghoa2.text = ""
        self.ids.ma_hanghoa3.text = ""
        self.ids.ten_hanghoa.text = ""
        self.ids.ten_hanghoa2.text = ""
        self.ids.ten_hanghoa3.text = ""
        self.ids.sl_hanghoa.text = ""
        self.ids.sl_hanghoa2.text = ""
        self.ids.sl_hanghoa3.text = ""

