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

from plyer import filechooser


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
                    right_action_items: [["music-note-plus", lambda event: app.add_song()]]

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
        ext=[]

    def add_song(self):
        files = filechooser.open_file(multiple=True, filters=[["Music Files", "*mp3", "*m4a", "*ogg", "*wav"]])
        # self.root.ids.container.add_widget(ButtonListItem(on_release=self.hello, text="Hello", secondary_text="You"))
        for file in files:
            print(file)


    def nav_to(self, page):
        self.root.ids.screen_manager.current = page

MainApp().run()
