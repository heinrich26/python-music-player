import kivy

from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.utils import platform
from kivy.uix.widget import Widget

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import IRightBodyTouch, TwoLineAvatarIconListItem
from kivymd.uix.button import MDIconButton
from kivymd.toast import toast

from pathlib import Path

from better_filemanager import BetterFileManager


if platform == "android":
    from android.storage import primary_external_storage_path
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])


KV = '''
<ButtonListItem>:
    ImageLeftWidget:
        source: root.source

    DropdownButton:
        icon: "dots-vertical"

Screen:
    ScreenManager:
        id: screen_manager
        Screen:
            name: "main_page"
            BoxLayout:
                orientation: "vertical"

                MDRectangleFlatButton:
                    text: "Music Libary"
                    pos_hint: {'center_x': .5, 'center_y': 1}
                    on_press:
                        app.nav_to("song_view")

                MDLabel:
                    text: "Hendriks Stupid Music Player"
                    halign: "center"
        Screen:
            name: "song_view"
            BoxLayout:
                orientation: "vertical"

                MDToolbar:
                    title: "Libary"
                    left_action_items: [["keyboard-backspace", lambda event: app.nav_to("main_page")]]

                MDRectangleFlatButton:
                    text: 'Add Song(s)'
                    pos_hint: {'center_x': 0.5, 'center_y': 1}
                    on_press:
                        app.add_song()

                ScrollView:
                    MDList:
                        id: container

    MDToolbar:
        title: 'Track Bar'
        md_bg_color: .2, .2, .2, 1
        specific_text_color: 1, 1, 1, 1
'''


class ButtonListItem(TwoLineAvatarIconListItem):
    source = StringProperty("src/img/music_logo.png")

class DropdownButton(IRightBodyTouch, MDIconButton):
    pass


class MainApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        self.file_manager = BetterFileManager(
        exit_manager=self.exit_manager,
        select_path=self.select_path, ext=[".mp3",".m4a",".ogg",".wav"], selector="multi", show_filetype=True)

    def add_song(self):
        self.file_manager_open()
        # self.root.ids.container.add_widget(ButtonListItem(on_release=self.hello, text="Hello", secondary_text="You"))

    def nav_to(self, page):
        self.root.ids.screen_manager.current = page

    def hello(self, *args):
        print("hi")


# file manager
    def file_manager_open(self):
        self.file_manager.show(path=primary_external_storage_path() if platform == "android" else str(Path.home()) + "/Music/")  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        self.file_manager.exit_manager()
        print(path)

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()


MainApp().run()
