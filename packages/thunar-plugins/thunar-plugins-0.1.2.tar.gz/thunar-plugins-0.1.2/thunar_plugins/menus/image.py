# system modules
from urllib.parse import urlparse, unquote

# internal modules
from thunar_plugins import l10n

# external modules
import gi

gi.require_version("Gtk", "3.0")

from gi.repository import GObject, Gtk, Thunarx


class ImageSubmenu(GObject.GObject, Thunarx.MenuProvider):
    def __init__(self):
        pass

    @staticmethod
    def all_are_images(menuitems):
        return all(
            (
                m.get_mime_type().startswith("image")
                if not m.is_directory()
                else False
            )
            for m in menuitems
        )

    def get_file_menu_items(self, window, files):
        for f in files:
            print(f)
            print(f"get_location().get_uri():   {f.get_location().get_uri()}")
            print(
                f"get_location().get_path():   {f.get_location().get_path()}"
            )
            print(f"get_uri:        {f.get_uri()}")
            print(f"get_mime_type:  {f.get_mime_type()}")
            print(f"get_parent_uri: {f.get_parent_uri()}")
            print(f"is_directory:   {f.is_directory()}")
        if not self.all_are_images(files):
            return tuple()

        image_menuitem = Thunarx.MenuItem(
            name="Image",
            label=_("Images") if len(files) > 1 else _("Image"),
            tooltip=_("Manipulate the selected images")
            if len(files) > 1
            else _("Manipulate the selected image"),
            icon="image-x-generic",
        )

        image_submenu = Thunarx.Menu()

        shrink_item = Thunarx.MenuItem(
            name="Image::Shrink",
            label=_("Shrink"),
            tooltip=_("Shrink selected images")
            if len(files) > 1
            else _("Shrink selected image"),
            icon="image-crop",
        )
        shrink_item.connect("activate", self.__shrink_callback, files)
        image_submenu.append_item(shrink_item)

        image_menuitem.set_menu(image_submenu)

        return (image_menuitem,)

    def __shrink_callback(self, item, files):
        for f in files:
            print("Shrink file {}".format(f.get_location().get_path()))
