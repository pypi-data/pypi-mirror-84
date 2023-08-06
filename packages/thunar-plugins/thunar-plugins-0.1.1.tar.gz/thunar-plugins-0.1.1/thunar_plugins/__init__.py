# system modules

# GObject Introspection
import gi

gi.require_version("Thunarx", "3.0")

# internal modules
import thunar_plugins.version
from thunar_plugins.version import __version__
import thunar_plugins.l10n
import thunar_plugins.menus

# external modules
