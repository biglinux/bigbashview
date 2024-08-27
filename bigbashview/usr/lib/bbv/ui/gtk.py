import os
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("WebKit", "6.0")
from gi.repository import Gtk, WebKit, Gdk, Gio, GLib
from bbv.globaldata import ICON, TITLE, EXTERNAL_LINK, PROCESS


class Application(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="biglinux.bbv", flags=Gio.ApplicationFlags.NON_UNIQUE)
        GLib.set_application_name(PROCESS)

    def do_activate(self):
        Window(app=self)

class Window(Gtk.Window):
    def __init__(self, app):
        super().__init__(application=app)
        self.webview = WebKit.WebView()
        settings = self.webview.get_settings()
        settings.set_user_agent("BigBashView-Agent") # User-Agent Custom
        settings.set_enable_developer_extras(True) # Enable Web Inspector
        settings.set_enable_javascript(True)
        self.set_child(self.webview)
        
        # Definir o ícone da janela
        self.set_icon_name("big-logo")

        if TITLE:
            self.set_title(TITLE)
        else:
            self.webview.connect("notify::title", self.title_changed)

        if EXTERNAL_LINK:
            self.webview.connect("decide-policy", self.LinkOpener)

        self.webview.connect("load-changed", self.add_script)
        self.webview.connect("close", self.close_window)
        self.connect('close-request',self.close_window)

        # Criar um controlador de eventos para capturar teclas pressionadas
        key_controller = Gtk.EventControllerKey.new()
        self.webview.add_controller(key_controller)
        key_controller.connect("key-pressed", self.key)       

    def LinkOpener(self, web_view, decision, decision_type):
        """Intercepta navegações para abrir links externos no navegador padrão."""
        if decision_type == WebKit.PolicyDecisionType.NAVIGATION_ACTION:
            navigation_action = decision.get_navigation_action()
            request = navigation_action.get_request()
            uri = request.get_uri()
            if not uri.startswith("http://127.0.0.1"):
                if navigation_action.get_navigation_type() == WebKit.NavigationType.LINK_CLICKED:
                    # Abre links externos no navegador padrão do sistema
                    Gio.app_info_launch_default_for_uri(uri, None)
                    decision.ignore()
                    return False
            return True

    def key(self, controller, keyval, keycode, state):
        # Reload the webview when the F5 key is pressed
        if keyval == 65474:  # F5
            self.webview.reload()
        # Show the web inspector when the F12 key is pressed
        if keyval == 65481:  # F12
            inspector = self.webview.get_inspector()
            inspector.show()

    def add_script(self, webview, event):
        # Add a JavaScript function to the webview that can be called from the loaded webpage
        script = "function _run(run){fetch('/execute$'+run);}"
        if event == WebKit.LoadEvent.FINISHED:
            self.webview.evaluate_javascript(script, -1)

    def viewer(self, window_state):
        # Set the window state based on the provided argument
        if window_state == "maximized":
            self.maximize()
        elif window_state == "fullscreen":
            self.fullscreen()
        elif window_state == "frameless":
            self.set_decorated(False)
        elif window_state == "framelesstop":
            self.set_decorated(False)
            self.set_keep_above(True)
        elif window_state == "maximizedframelesstop":
            self.set_decorated(False)
            self.set_keep_above(True)
            self.maximize()
        elif window_state == "alwaystop":
            self.set_keep_above(True)
        self.present()

    def run(self):
        # Start the Gtk Application
        app = Application()
        app.run()

    def close_window(self, webview):
        # Quit the Gtk Application when the webview is closed
        self.close()
        os.kill(os.getpid(), 15)

    def title_changed(self, webview, title):
        # Set the window title
        title = self.webview.get_title()
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
        if window_state == "fixed":
            self.set_resizable(False)

    def style(self, colorful):
        # Set the window and webview background color based on the provided argument
        css_provider = Gtk.CssProvider()
        if colorful == "black":
            css_provider.load_from_string("window{background-color:rgba(0, 0, 0, 1);}")
            self.webview.set_background_color(Gdk.RGBA(0, 0, 0, 1))

        elif colorful == "transparent":
            css_provider.load_from_string("window{background-color:rgba(0, 0, 0, 0);}")
            self.webview.set_background_color(Gdk.RGBA(0, 0, 0, 0))

        elif os.environ.get("XDG_CURRENT_DESKTOP") == "KDE":
            rgb = os.popen("kreadconfig5 --group WM --key activeBackground").read().split(",")

            if len(rgb) > 1:
                r, g, b = rgb if len(rgb) == 3 else rgb[:-1]
                r = float(int(r)/255)
                g = float(int(g)/255)
                b = float(int(b)/255)
                self.webview.set_background_color(Gdk.RGBA(r, g, b, 1))
            else:
                color = Gdk.RGBA(1,1,1,1)
                style = "window{background-color:"+color.to_string()+";}"
                css_provider.load_from_string(style)
                self.webview.set_background_color(color)
        else:
            color = Gdk.RGBA(1,1,1,1)
            style = "window{background-color:"+color.to_string()+";}"
            css_provider.load_from_string(style)
            self.webview.set_background_color(color)

        style_context = self.get_style_context()
        style_context.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)