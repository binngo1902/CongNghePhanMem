from kivymd.uix.boxlayout import MDBoxLayout
from libs.applibs import utils
from kivy.clock import Clock
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
utils.load_kv("screen_hanghoa.kv")
class ScreenHangHoa(MDBoxLayout):
    def __init__(self, **kwargs):
        super(ScreenHangHoa, self).__init__(**kwargs)
        Clock.schedule_once(self.load_data)
    def load_data(self,obj):
        data_tables = MDDataTable(
            size_hint=(1, 1),
            column_data=[
                ("Mã hàng hóa", dp(50)),
                ("Tên hàng hóa", dp(50)),
                ("Số lượng ", dp(50)),
               
            ],
            row_data=[
                # The number of elements must match the length
                # of the `column_data` list.
                (
                    "1",
                    ("alert", [255 / 256, 165 / 256, 0, 1], "No Signal"),
                    "Astrid: NE shared managed",
                    
                ),
                (
                    "2",
                    ("alert-circle", [1, 0, 0, 1], "Offline"),
                    "Cosmo: prod shared ares",
                   
                ),
                (
                    "3",
                    (
                        "checkbox-marked-circle",
                        [39 / 256, 174 / 256, 96 / 256, 1],
                        "Online",
                    ),
                    "Phoenix: prod shared lyra-lists",
                ),
            ],
        )
        self.ids.hanghoa.add_widget(data_tables)