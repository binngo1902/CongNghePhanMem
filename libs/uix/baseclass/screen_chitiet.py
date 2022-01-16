from kivy.clock import Clock
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from apiWeb import ApiWeb
from libs.applibs import utils
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
utils.load_kv("screen_chitiet.kv")

class ScreenChiTiet(MDScreen):
    def __init__(self, **kwargs):
        super(ScreenChiTiet, self).__init__(**kwargs)
        self.api_web = ApiWeb()
    def on_enter(self):
        self.data = self.api_web.get_chitiet(MDApp.chitiet)
        self.status1 = self.data['table1'][5]
        self.status2 = self.data['table1'][6]
        Clock.schedule_once(self.load_widget)

    def status_delivery(self,status):
        if status == 1:
            self.status1 = 0
        if status == 2:
            self.status1 = 1
        if status == 3:
            self.status1 = 2
        print(self.status1)
    
    def status_pay(self,status):
        if status == 0:
            self.status2 = 0
        if status == 1:
            self.status2 = 1
        print(self.status2)
        
    def update(self):
        print(self.data['table1'][7])
        data = self.api_web.update_hoadon(self.data['table1'][0],self.status1,self.status2,self.data['table1'][7],self.data['table1'][8])
        self.dialog =MDDialog(
            title="Thông báo",
            type="simple",
            text= data,
            buttons=[
                MDRaisedButton(text="Đóng",on_release=self.close_dialog),
            ],
        )
        self.dialog.open()

    def close_dialog(self,obj):
        self.dialog.dismiss()
        self.manager.current = "hoadon"

    def load_widget(self,obj):
        self.ids.layout_content.clear_widgets()
        self.ids.title.text= "Chi tiết đơn hàng số "+str(self.data['table1'][0])+" - (Đại lý) "+self.data['table1'][1]+" - Tổng tiền: "+str(self.data['table1'][2])+" VNĐ - Tổng sản phẩm: "+str(self.data['table1'][3])
        for i in self.data['table2']:
           

            field1 = MDTextField(
                hint_text=f"Mã hàng hóa",
                font_size=15,
                readonly=True
            )
            field1.text = str(i[0])
            field2 = MDTextField(
                hint_text=f"Tên hàng hóa ",
                font_size=15,
                readonly=True

            )
            field2.text = str(i[1])

            field3 = MDTextField(
                hint_text=f"Số lượng ",

                input_filter= 'int',

                font_size=15,
                readonly=True

            )
            field3.text = str(i[2])

            field4 = MDTextField(
                hint_text=f"Giá tiền (VNĐ) ",
                input_filter= 'int',
                font_size=15,
                readonly=True

            )
            field4.text = str(i[3])

           
            self.ids.layout_content.add_widget(field1)
            self.ids.layout_content.add_widget(field2)
            self.ids.layout_content.add_widget(field3)
            self.ids.layout_content.add_widget(field4)
        if (self.data['table1'][5] == 0):
            self.ids.t1.state = "down"
        if (self.data['table1'][5] == 1):
            self.ids.t2.state = "down"
        if (self.data['table1'][5] == 2):
            self.ids.t3.state = "down"    

        if (self.data['table1'][6] == 0):
            self.ids.m1.state = "down"
        if (self.data['table1'][6] == 1):
            self.ids.m2.state = "down"