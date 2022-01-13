from kivy.clock import Clock
from kivymd.uix.boxlayout import MDBoxLayout
from libs.applibs import utils
from kivymd.uix.textfield import MDTextField
from kivy.uix.widget import Widget
from kivymd.uix.button import MDRaisedButton
utils.load_kv("screen_nhapkho.kv")
class ScreenNhapKho(MDBoxLayout):
    def __init__(self, **kwargs):
        super(ScreenNhapKho, self).__init__(**kwargs)
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
       
            
    def delete_all(self):
        for i in range(1,9):
            self.ids[f'ma_hanghoa{i}'].text = ""
            self.ids[f'ten_hanghoa{i}'].text = ""
            self.ids[f'sl_hanghoa{i}'].text = ""

