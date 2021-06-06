__all__ = ("BetterFileManager",)

import locale
import os

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import (
    BooleanProperty,
    ColorProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    OptionProperty,
    StringProperty,
)
from kivy.utils import get_hex_from_color
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.modalview import ModalView

from kivymd import images_path
from kivymd.theming import ThemableBehavior
from kivymd.icon_definitions import md_icons
from kivymd.uix.behaviors import CircularRippleBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import BaseListItem, ContainerSupport, IRightBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.button import MDFlatButton
from kivymd.utils.fitimage import FitImage


ACTIVITY_MANAGER = """
#:import os os


<BodyManagerFile@BoxLayout>
    icon: "folder"
    path: ""
    background_normal: ""
    background_down: ""
    dir_or_file_name: ""
    _selected: False
    events_callback: lambda x: None
    orientation: "vertical"

    ModifiedOneLineIconListItem:
        text: root.dir_or_file_name
        bg_color: self.theme_cls.primary_light if root._selected else self.theme_cls.bg_normal
        on_release: root.events_callback(root.path, root)

        IconLeftWidget:
            icon: root.icon
            theme_text_color: "Custom"
            text_color: self.theme_cls.primary_color

        RightCheckbox:
            active: True if root._selected else False
            on_release: root.events_callback(root.path, root)

    MDSeparator:
        height: dp(1.25)


<BodyManagerFolder@BoxLayout>
    icon: "folder"
    path: ""
    background_normal: ""
    background_down: ""
    dir_or_file_name: ""
    _selected: False
    events_callback: lambda x: None
    orientation: "vertical"

    ModifiedOneLineIconListItem:
        text: root.dir_or_file_name
        bg_color: self.theme_cls.bg_darkest if root._selected else self.theme_cls.bg_normal
        on_release: root.events_callback(root.path, root)

        IconLeftWidget:
            icon: root.icon
            theme_text_color: "Custom"
            text_color: self.theme_cls.icon_color

    MDSeparator:
        height: dp(1.25)

<LabelContent@MDLabel>
    size_hint_y: None
    height: self.texture_size[1]
    shorten: True
    shorten_from: "center"
    halign: "center"
    text_size: self.width, None


<BodyManagerWithPreview>
    name: ""
    path: ""
    realpath: ""
    type: "folder"
    events_callback: lambda x: None
    _selected: False
    orientation: "vertical"
    size_hint_y: None
    height: root.height
    padding: dp(20)

    IconButton:
        mipmap: True
        source: root.path
        bg_color: app.theme_cls.bg_darkest if root._selected else app.theme_cls.bg_normal
        on_release:
            root.events_callback(\
            os.path.join(root.path if root.type != "folder" else root.realpath, \
            root.name), root)

    LabelContent:
        text: root.name


<FloatButton>
    anchor_x: "right"
    anchor_y: "bottom"
    size_hint_y: None
    height: dp(56)
    padding: dp(10)

    MDFloatingActionButton:
        size_hint: None, None
        size:dp(56), dp(56)
        icon: root.icon
        opposite_colors: True
        elevation: 8
        on_release: root.callback()
        md_bg_color: root.md_bg_color


<BetterFileManager>
    md_bg_color: root.theme_cls.bg_normal
    selected_all: False

    MDBoxLayout:
        orientation: "vertical"
        spacing: dp(5)

        MDToolbar:
            id: toolbar
            markup: True
            title: "Select Music Files or Folders"
            right_action_items: [["close-box", lambda x: root.exit_manager(1)], ["checkbox-multiple-marked" if root.selected_all else "checkbox-multiple-blank-outline", lambda x: root.select_all_files_on_button_press()]] if root.selector == "multi" else [["close-box", lambda x: root.exit_manager(1)]]
            left_action_items: [["chevron-left", lambda x: root.back()]]
            md_bg_color: root.theme_cls.bg_normal
            elevation: 10

        ScrollView:
            orientation: "horizontal"
            height: dp(32)
            size_hint_y: None
            MDLabel:
                padding: dp(10), 0
                id: pathlabel
                markup: True
                text: root.format_path(root.current_path)



        RecycleView:
            id: rv
            key_viewclass: "viewclass"
            key_size: "height"
            bar_width: dp(4)
            bar_color: root.theme_cls.primary_color

            RecycleGridLayout:
                id: rgl
                padding: dp(10)
                spacing: dp(2)
                cols: 3 if root.preview else 1
                default_size: None, dp(48)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height

<ModifiedOneLineIconListItem>
    BoxLayout:
        id: _left_container
        size_hint: None, None
        x: root.x + dp(16)
        y: root.y + root.height / 2 - self.height / 2
        size: dp(48), dp(48)

    BoxLayout:
        id: _right_container
        size_hint: None, None
        x: root.x + root.width - dp(64)
        y: root.y + root.height / 2 - self.height / 2
        size: dp(48), dp(48)

"""


# adds a Checkbox to the ListItems
class RightCheckbox(IRightBodyTouch, MDCheckbox):
    '''Custom right container.'''


class BodyManagerWithPreview(MDBoxLayout):
    """Base class for folder icons and thumbnails images in ``preview`` mode."""


class IconButton(CircularRippleBehavior, ButtonBehavior, FitImage):
    """Folder icons/thumbnails images in ``preview`` mode."""


class FloatButton(AnchorLayout):
    callback = ObjectProperty()
    md_bg_color = ColorProperty([1, 1, 1, 1])
    icon = StringProperty()


class ModifiedOneLineIconListItem(ContainerSupport, BaseListItem):
    _txt_left_pad = NumericProperty("72dp")
    _txt_top_pad = NumericProperty("16dp")
    _txt_bot_pad = NumericProperty("15dp")
    _num_lines = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.height = dp(48)


class BetterFileManager(ThemableBehavior, MDRelativeLayout):

    icon = StringProperty("check")

    icon_folder = StringProperty(f"{images_path}folder.png")

    icon_type = OptionProperty("outline", options=["outline", "solid"])

    exit_manager = ObjectProperty(lambda x: None)

    select_path = ObjectProperty(lambda x: None)

    ext = ListProperty()

    search = OptionProperty("all", options=["all", "dirs", "files"])

    current_path = StringProperty(os.getcwd())

    use_access = BooleanProperty(True)

    preview = BooleanProperty(False)

    show_hidden_files = BooleanProperty(False)

    sort_by = OptionProperty(
        "name", options=["nothing", "name", "date", "size", "type"]
    )

    sort_by_desc = BooleanProperty(False)

    selector = OptionProperty("any", options=["any", "file", "folder", "multi"])

    selection = ListProperty()

    show_filetype = BooleanProperty(False)


    _window_manager = None
    _window_manager_open = False

    def __init__(self, **kwargs):
        self.fs_name = self.current_path[0:self.current_path.replace("\\", "/").find("/")]
        super().__init__(**kwargs)


        toolbar_label = self.ids.toolbar.children[1].children[0]
        toolbar_label.font_style = "Subtitle1"
        self.ids.pathlabel.on_ref_press = self.nav_from_ref
        toolbar_label.shorten_from = "left"

        if (self.selector == "any" or self.selector == "multi" or self.selector == "folder"):
            self.add_widget(
                FloatButton(
                    callback=self.select_directory_on_press_button,
                    md_bg_color=self.theme_cls.primary_color,
                    icon=self.icon,
                )
            )

        if self.preview:
            self.ext = [".png", ".jpg", ".jpeg"]

        if self.icon_type == "solid":
            self.folder_icon = "folder"
            self.folder_locked_icon = "folder-lock"
        else:
            self.folder_icon = "folder-outline"
            self.folder_locked_icon = "folder-lock-outline"

    def __sort_files(self, files):
        def sort_by_name(files):
            files.sort(key=locale.strxfrm)
            files.sort(key=str.casefold)
            return files

        if self.sort_by == "name":
            sorted_files = sort_by_name(files)
        elif self.sort_by == "date":
            _files = sort_by_name(files)
            _sorted_files = [os.path.join(self.current_path, f) for f in _files]
            _sorted_files.sort(key=os.path.getmtime, reverse=True)
            sorted_files = [os.path.basename(f) for f in _sorted_files]
        elif self.sort_by == "size":
            _files = sort_by_name(files)
            _sorted_files = [os.path.join(self.current_path, f) for f in _files]
            _sorted_files.sort(key=os.path.getsize, reverse=True)
            sorted_files = [os.path.basename(f) for f in _sorted_files]
        elif self.sort_by == "type":
            _files = sort_by_name(files)
            sorted_files = sorted(
                _files,
                key=lambda f: (os.path.splitext(f)[1], os.path.splitext(f)[0]),
            )
        else:
            sorted_files = files

        if self.sort_by_desc:
            sorted_files.reverse()

        return sorted_files

    def show(self, path):
        print(path)
        """Forms the body of a directory tree.
        :param path:
            The path to the directory that will be opened in the file manager.
        """

        self.current_path = path
        self.selection = []
        dirs, files = self.get_content()
        manager_list = []

        if dirs == [] and files == []:  # selected directory
            pass
        elif not dirs and not files:  # directory is unavailable
            return

        if self.preview:
            for name_dir in self.__sort_files(dirs):
                manager_list.append(
                    {
                        "viewclass": "BodyManagerWithPreview",
                        "path": self.icon_folder,
                        "realpath": os.path.join(path),
                        "type": "folder",
                        "name": name_dir,
                        "events_callback": self.select_dir_or_file,
                        "height": dp(150),
                        "_selected": False,
                    }
                )
            for name_file in self.__sort_files(files):
                if (
                    os.path.splitext(os.path.join(path, name_file))[1]
                    in self.ext
                ):
                    manager_list.append(
                        {
                            "viewclass": "BodyManagerWithPreview",
                            "path": os.path.join(path, name_file),
                            "name": name_file,
                            "type": "files",
                            "events_callback": self.select_dir_or_file,
                            "height": dp(150),
                            "_selected": False,
                        }
                    )
        else:
            for name in self.__sort_files(dirs):
                _path = os.path.join(path, name)
                access_string = self.get_access_string(_path)
                if "r" not in access_string:
                    icon = self.folder_locked_icon
                else:
                    icon = self.folder_icon

                manager_list.append(
                    {
                        "viewclass": "BodyManagerFolder",
                        "path": _path,
                        "icon": icon,
                        "dir_or_file_name": name,
                        "events_callback": self.select_dir_or_file,
                        "_selected": False,
                    }
                )
            for name in self.__sort_files(files):
                if self.ext and os.path.splitext(name)[1] not in self.ext:
                    continue

                manager_list.append(
                    {
                        "viewclass": "BodyManagerFile" if self.selector == "multi" else "BodyManagerFolder",
                        "path": name,
                        "icon": self.filetype_icon(name) if self.show_filetype else "file" if self.icon_type == "solid" else "file-outline",
                        "dir_or_file_name": os.path.split(name)[1],
                        "events_callback": self.select_dir_or_file,
                        "_selected": False,
                    }
                )
        self.ids.rv.data = manager_list

        if not self._window_manager:
            self._window_manager = ModalView(
                size_hint=self.size_hint, auto_dismiss=False
            )
            self._window_manager.add_widget(self)
        if not self._window_manager_open:
            self._window_manager.open()
            self._window_manager_open = True

    def get_access_string(self, path):
        access_string = ""
        if self.use_access:
            access_data = {"r": os.R_OK, "w": os.W_OK, "x": os.X_OK}
            for access in access_data.keys():
                access_string += (
                    access if os.access(path, access_data[access]) else "-"
                )
        return access_string

    def get_content(self):
        """Returns a list of the type [[Folder List], [file list]]."""

        try:
            files = []
            dirs = []

            for content in os.listdir(self.current_path):
                if os.path.isdir(os.path.join(self.current_path, content)):
                    if self.search == "all" or self.search == "dirs":
                        if (not self.show_hidden_files) and (
                            content.startswith(".")
                        ):
                            continue
                        else:
                            dirs.append(content)

                else:
                    if self.search == "all" or self.search == "files":
                        if len(self.ext) != 0:
                            try:
                                files.append(
                                    os.path.join(self.current_path, content)
                                )
                            except IndexError:
                                pass
                        else:
                            if (
                                not self.show_hidden_files
                                and content.startswith(".")
                            ):
                                continue
                            else:
                                files.append(content)

            return dirs, files

        except OSError:
            return None, None

    def close(self):
        """Closes the file manager window."""

        self._window_manager.dismiss()
        self._window_manager_open = False

    def select_dir_or_file(self, path, widget):
        """Called by tap on the name of the directory or file."""

        if os.path.isfile(os.path.join(self.current_path, path)):
            if self.selector == "multi":
                file_path = os.path.join(self.current_path, path)
                if file_path in self.selection:
                    widget._selected = False
                    self.selection.remove(file_path)
                    if self.selected_all:
                        self.selected_all = False
                else:
                    widget._selected = True
                    self.selection.append(file_path)
                    if len(self.selection) == len(self.ids.rv.data):
                        self.selected_all = True
            elif self.selector == "folder":
                return
            else:
                self.select_path(os.path.join(self.current_path, path))

        else:
            self.current_path = path
            self.show(path)

    def back(self):
        """Returning to the branch down in the directory tree."""

        path, end = os.path.split(self.current_path)

        if not end:
            self.close()
            self.exit_manager(1)

        else:
            self.show(path)

    def select_directory_on_press_button(self, *args):
        """Called when a click on a floating button."""

        if self.selector == "multi":
            if len(self.selection) > 0:
                self.select_path(self.selection)
            else:
                self.select_path(self.current_path)
        elif self.selector == "folder" or self.selector == "any":
            self.select_path(self.current_path)

    def select_all_files_on_button_press(self):
        if len(self.selection) >= len(self.ids.rv.data):
            for widget in self.ids.rv.data:
                widget["_selected"] = False
            self.selection = []
            self.selected_all = False
        else:
            selection = []
            for widget in self.ids.rv.data:
                if not widget["_selected"]:
                    widget["_selected"] = True
                selection.append(os.path.join(self.current_path, widget["path"]))
            self.selection = selection
            self.selected_all = True

        # update widgets
        self.ids.rv.refresh_from_data()

    def filetype_icon(self, path):
        ext = os.path.splitext(path)[1].lower()

        # syntax for adding a new Filetype
        # if ext in ():
        #     return "file" if self.icon_type == "solid" else "file-outline"

        if ext in (".mp3", ".mpa", ".wav", ".ogg", ".m4a", ".aif", ".cda", ".mid", ".midi", ".wma", ".wpl", ".m3u", ".pls", ".asx", ".cue"):
            return "file-music" if self.icon_type == "solid" else "file-music-outline"
        if ext in (".mp4", ".mov", ".avi", ".3g2", ".3gp", ".flv", ".h264", ".m4v", ".mkv", ".mpg", ".mpeg", ".rm", ".swf", ".vob", ".wmv"):
            return "file-video" if self.icon_type == "solid" else "file-video-outline"
        if ext in (".bmp", ".png", "jpg", ".jpeg", ".jpe", ".gif", ".tif", ".tiff", ".svg", ".ai", ".ico", ".ps", ".psd", ".icns", ".xcf"):
            return "file-image" if self.icon_type == "solid" else "file-image-outline"
        if ext in (".xls", ".xlt", ".xlm", ".xlsx", ".xltx", ".xltm", ".xlsb", ".xla", ".xlam", ".xll", ".xlw"):
            return "file-excel" if self.icon_type == "solid" else "file-excel-outline"
        if ext in (".ppt", ".pot", ".pps", ".pptx", ".pptm", ".potx", ".ppam", ".ppsx", ".ppsm", ".sldx", ".sldm"):
            return "file-powerpoint" if self.icon_type == "solid" else "file-powerpoint-outline"
        if ext in (".doc", ".dot", ".wbk", ".docx", ".docm", ".dotx", ".dotm", ".docb"):
            return "file-word" if self.icon_type == "solid" else "file-word-outline"
        if ext in (".pdf", ".fdf", ".xfdf"):
            return "file-pdf" if self.icon_type == "solid" else "file-pdf-outline"
        if ext in (".txt", ".md", ".readme", ".odt", ".ods", ".odp", ".log", ".tex"):
            return "file-document" if self.icon_type == "solid" else "file-document-outline"
        if ext in (".h", ".c", ".cpp", ".cxx", ".cs", ".xml", ".py", ".html", ".htm", ".xhtml", ".js", ".jsp", ".java", ".pas", ".css", ".vala", ".erl", ".d", ".lua", ".asp", ".aspx", ".cfm", ".cgi", ".pl", ".rss", ".php", ".sh", ".swift", ".bat", ".vb"):
            return "file-code" if self.icon_type == "solid" else "file-code-outline"
        if ext in (".csv", ".dat", ".db", ".dbf", ".mdb", ".sav", ".sql"):
            return "file-chart" if self.icon_type == "solid" else "file-chart-outline"
        if ext in (".bak", ".cab", ".cfg", ".cpl", ".cur", ".dll", ".dmp", ".drv", ".ini", ".msi", ".sys", ".tmp"):
            return "file-cog" if self.icon_type == "solid" else "file-cog-outline"
        if ext in (".lnk"):
            return "file-link" if self.icon_type == "solid" else "file-link-outline"
        if ext in (".part", ".crdownload"):
            return "file-download" if self.icon_type == "solid" else "file-download-outline"
        else:
            return "file" if self.icon_type == "solid" else "file-outline"

    def nav_from_ref(self, reference):
        depth = int(reference)
        path = self.current_path.replace("\\", "/").rsplit("/", depth)[0]
        self.current_path = path if path.count("/") != 0 else "/"
        print(path)
        self.show(path if path != "C:" else "C:\\")


    def format_path(self, path):
        fixed_path = path.replace("\\", "/").strip("/").split("/")
        return f"[color={get_hex_from_color(self.theme_cls.secondary_text_color)}]" + f" [font=Icons]{md_icons['chevron-right']}[/font][/ref] ".join([f"[ref={i}][color={get_hex_from_color(self.theme_cls.secondary_text_color)}]{folder}[/color]" if i != 0 else f"[color={get_hex_from_color(self.theme_cls.primary_light)}]{folder}[/color][/color]" for folder, i in zip(fixed_path, range(len(fixed_path) -1, -1, -1))])
        # " > ".join([f"{f'[ref={i}]'if i != 0 else ''}[color={get_hex_from_color(self.theme_cls.primary_color) if i == 0 else get_hex_from_color(self.ids.toolbar.specific_text_color)}]{folder}[/color]{'[/ref]'if i != 0 else ''}" for folder, i in zip(fixed_path.split("/"), range(fixed_path.count("/"), -1, -1))])


Builder.load_string(ACTIVITY_MANAGER)


if __name__ == "__main__":
    from main import Example
