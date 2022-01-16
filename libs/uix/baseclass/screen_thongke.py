from kivymd.uix.boxlayout import MDBoxLayout
from apiWeb import ApiWeb
from libs.applibs import utils
from kivymd.uix.screen import MDScreen
from datetime import datetime


utils.load_kv("screen_thongke.kv")
class ScreenThongKe(MDScreen):
    def __init__(self, **kwargs):
        super(ScreenThongKe, self).__init__(**kwargs)
        self.api_web = ApiWeb()
    def view_thongke(self):
        self.ids.error.text = ""
        month = self.ids.month.text
        year = self.ids.year.text
        if (month == "" or year == ""):
            self.ids.error.text = "Chưa chọn tháng hoặc năm"
            return
        s = f"1 {month}, {year}"
        d = datetime.strptime(s, '%d %m, %Y')
        print(d.strftime('%m-%d-%Y'))