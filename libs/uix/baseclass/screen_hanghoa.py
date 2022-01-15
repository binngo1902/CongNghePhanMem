from kivymd.uix.boxlayout import MDBoxLayout
from libs.applibs import utils
from kivy.clock import Clock
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen

from ApiWeb import ApiWeb
utils.load_kv("screen_hanghoa.kv")
class ScreenHangHoa(MDScreen):
    def __init__(self, **kwargs):
        super(ScreenHangHoa, self).__init__(**kwargs)
        self.api_web = ApiWeb()
    def on_enter(self):
        Clock.schedule_once(self.load_data)
    def load_data(self,obj=""):
        self.ids.hanghoa.clear_widgets()
        data=(self.api_web.get_hanghoa())
        self.data_tables = MDDataTable(
            use_pagination=True,
            rows_num=6,
            pos_hint={'center_x': 0.5 , 'center_y': 0.5 },
            size_hint=(0.8, 0.9),
            column_data=[
                ("Mã hàng hóa", dp(50)),
                ("Tên hàng hóa", dp(50)),
                ("Số lượng ", dp(50)),
               
            ],
            row_data=data
        )
        self.ids.hanghoa.add_widget(self.data_tables)