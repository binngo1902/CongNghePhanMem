from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from apiWeb import ApiWeb
from libs.applibs import utils
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.app import MDApp

utils.load_kv("screen_hoadon.kv")


class ScreenHoaDon(MDScreen):
    def __init__(self, **kwargs):
        super(ScreenHoaDon, self).__init__(**kwargs)
        self.api_web = ApiWeb()
    def on_enter(self):
        self.ids.hoadon.clear_widgets()
        self.data=(self.api_web.get_hoadon())
        Clock.schedule_once(self.load_data,3)
    def load_data(self,obj=""):
    
        
        self.data_tables = MDDataTable(
            use_pagination=True,
            rows_num=6,
            pos_hint={'center_x': 0.5 , 'center_y': 0.5 },
            size_hint=(0.8, 0.9),
            elevation= 2,
            column_data=[
                ("Mã đơn", dp(30)),
                ("Mã đại lý", dp(30)),
                ("Tổng tiền ", dp(30)),
                ("Tổng sản phẩm ", dp(30)),
                ("Hình thức ", dp(30)),
                ("Vận chuyển ", dp(30)),
                ("Thanh toán ", dp(30)),
                ("Giờ tạo",dp(30)),

            
            ],
            row_data=self.data
        )
        self.data_tables.bind(on_row_press=self.on_row_press)
        self.ids.hoadon.add_widget(self.data_tables)


    def on_row_press(self, instance_table, row):
        '''Called when a table row is clicked.'''
        try:
            if row.table:
                if row.table.recycle_data:
                    if (row.table.recycle_data[row.index]):
                        start_index, end_index = row.table.recycle_data[row.index]["range"]
                        MDApp.chitiet = row.table.recycle_data[start_index]["text"]
        except IndexError:
            pass
        self.manager.current = 'chitiet'
        print(self.manager)
            # loop over selected row items
       
       