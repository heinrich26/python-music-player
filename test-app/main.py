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
            text: "Open manager"
            icon: "folder"
            pos_hint: {'center_x': .5, 'center_y': .33}
            on_release: app.file_manager_open()

        MDRoundFlatIconButton:
            text: "Open plyer manager"
            icon: "folder"
            pos_hint: {'center_x': .5, 'center_y': .66}
            on_release: app.plyer_file_manager_open()
'''



class Example(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = BetterFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            show_filetype=True,
        )

    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)

    def file_manager_open(self):
        self.file_manager.show(path=str(primary_external_storage_path()) if platform == "android" else str(Path.home()) + "/Music/")  # output manager to the screen
        self.manager_open = True

    def plyer_file_manager_open(self):
        files = filechooser.open_file(title="Select FILES!!!", multiple=True)  # output manager to the screen
        print("Type of selection:", type(files), files)

    def select_path(self, path):
        self.exit_manager()
        try:
            toast(path)
        except:
            pass

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True


if __name__ == "__main__":
    Example().run()
