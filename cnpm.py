import os
import platform

from kivy.core.window import Window
from kivymd.app import MDApp

from libs.uix.baseclass.root import Root
from libs.uix.baseclass.screen_hanghoa import ScreenHangHoa
# This is needed for supporting Windows 10 with OpenGL < v2.0
if platform.system() == "Windows":
    os.environ["KIVY_GL_BACKEND"] = "angle_sdl2"


class CNPM(MDApp):  # NOQA: N801
    screen_hanghoa = ScreenHangHoa()
    def __init__(self, **kwargs):
        super(CNPM, self).__init__(**kwargs)
        Window.soft_input_mode = "below_target"
        self.title = "demo_app"

        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "500"

        self.theme_cls.accent_palette = "Amber"
        self.theme_cls.accent_hue = "500"

        self.theme_cls.theme_style = "Light"

    def build(self):
        MDApp.chitiet = ""
        return Root()
