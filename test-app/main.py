from kivy.core.window import Window
from kivy.lang import Builder
from kivy.utils import platform

from kivymd.app import MDApp
from kivymd.toast import toast

from plyer import filechooser

from pathlib import Path

from better_filemanager import BetterFileManager


if platform == "android":
    from android.storage import primary_external_storage_path
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])


KV = '''
BoxLayout:
    orientation: 'vertical'

    MDToolbar:
        title: "BetterFileManager"
        left_action_items: [['menu', lambda x: None]]
        elevation: 10

    FloatLayout:

        MDRoundFlatIconButton:
            text: "Open plyer manager"
            icon: "folder"
            pos_hint: {'center_x': .5, 'center_y': .66}
            on_release: app.plyer_file_manager_open()
'''



class Example(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)


    def plyer_file_manager_open(self):
        files = filechooser.open_file(title="Select FILES!!!", multiple=True)  # output manager to the screen
        print("Type of selection:", type(files), files)


if __name__ == "__main__":
    Example().run()
