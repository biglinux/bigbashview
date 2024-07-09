import os
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.1")
from gi.repository import Gtk, WebKit2, Gdk
from bbv.globaldata import ICON, TITLE

class Window(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.webview = WebKit2.WebView()
        settings = self.webview.get_settings()
        settings.set_user_agent("BigBashView-Agent")
        self.webview.show()
        self.add(self.webview)
        self.set_icon_from_file(ICON)
        if TITLE:
            self.set_title(TITLE)
        else:
            self.webview.connect("notify::title", self.title_changed)
        self.webview.connect("load-changed", self.add_script)
        self.webview.connect("close", self.close_window)
        self.webview.get_settings().set_property(
            "enable-developer-extras",
            True
        )
        self.connect("destroy", Gtk.main_quit)
        self.connect("key-press-event", self.key)

    def key(self, webview, event):
        # Reload the webview when the F5 key is pressed
        if event.keyval == 65474:
            self.webview.reload()
        # Show the web inspector when the F12 key is pressed
        if event.keyval == 65481:
            inspector = self.webview.get_inspector()
            inspector.show()

    def add_script(self, webview, event):
        # Add a JavaScript function to the webview that can be called from the loaded webpage
        script = "function _run(run){fetch('/execute$'+run);}"
        if event == WebKit2.LoadEvent.FINISHED:
            self.webview.run_javascript(script)

    def viewer(self, window_state):
        # Set the window state based on the provided argument
        if window_state == "maximized":
            self.maximize()
            self.show()
        elif window_state == "fullscreen":
            self.fullscreen()
            self.show()
        elif window_state == "frameless":
            self.set_decorated(False)
            self.show()
        elif window_state == "framelesstop":
            self.set_decorated(False)
            self.set_keep_above(True)
            self.show()
        elif window_state == "maximizedframelesstop":
            self.set_decorated(False)
            self.set_keep_above(True)
            self.maximize()
            self.show()
        elif window_state == "alwaystop":
            self.set_keep_above(True)
            self.show()
        else:
            self.show()

    @staticmethod
    def run():
        # Start the Gtk main loop
        Gtk.main()

    @staticmethod
    def close_window(webview):
        # Quit the Gtk main loop when the webview is closed
        Gtk.main_quit()

    def title_changed(self, webview, title):
        # Set the window title and WM_CLASS property based on the webview's title
        title = self.webview.get_title()
        os.system(f"xprop -id $(xprop -root '\t$0' _NET_ACTIVE_WINDOW|cut -f2) -f WM_CLASS 8s -set WM_CLASS '{title}'")
        self.set_title(title)

    def load_url(self, url):
        # Load the specified URL in the webview
        self.webview.load_uri(url)

    def set_size(self, width, height, window_state, min_width, min_height):
        # Set the window size and position based on the provided arguments
        display = Gdk.Display.get_default()
        monitor = display.get_primary_monitor() if display else None
        if monitor:
            size = monitor.get_geometry()
            if width <= 0:
                width = size.width // 2
            if height <= 0:
                height = size.height // 2
        else:
            width = width if width > 0 else 800
            height = height if height > 0 else 600

        self.set_size_request(min_width, min_height)
        self.set_default_size(width, height)
        self.set_position(Gtk.WindowPosition.CENTER)
        if window_state == "fixed":
            self.set_resizable(False)

    def style(self, colorful):
        # Set the window and webview background color based on the provided argument
        if colorful == "black":
            self.override_background_color(
                Gtk.StateFlags.NORMAL,
                Gdk.RGBA(0, 0, 0, 1)
            )
            self.webview.set_background_color(Gdk.RGBA(0, 0, 0, 1))

        elif colorful == "transparent":
            screen = self.get_screen()
            visual = screen.get_rgba_visual()
            if visual is not None and screen.is_composited():
                self.set_visual(visual)
                self.override_background_color(
                    Gtk.StateFlags.NORMAL,
                    Gdk.RGBA(0, 0, 0, 0)
                )
                self.webview.set_background_color(Gdk.RGBA(0, 0, 0, 0))

        elif os.environ.get("XDG_CURRENT_DESKTOP") == "KDE":
            rgb = os.popen("kreadconfig5 --group WM --key activeBackground").read().split(",")

            if len(rgb) > 1:
                r, g, b = rgb if len(rgb) == 3 else rgb[:-1]
                r = float(int(r)/255)
                g = float(int(g)/255)
                b = float(int(b)/255)
                self.override_background_color(
                    Gtk.StateFlags.NORMAL,
                    Gdk.RGBA(r, g, b, 1)
                )
                self.webview.set_background_color(Gdk.RGBA(r, g, b, 1))
            else:
                color = self.get_style_context().get_background_color(Gtk.StateFlags.NORMAL)
                self.override_background_color(Gtk.StateFlags.NORMAL, color)
                self.webview.set_background_color(color)
        else:
            color = self.get_style_context().get_background_color(Gtk.StateFlags.NORMAL)
            self.override_background_color(Gtk.StateFlags.NORMAL, color)
            self.webview.set_background_color(color)
