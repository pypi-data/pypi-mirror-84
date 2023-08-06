from typing import List
from pystray import MenuItem, Menu
import pystray, sys, os
from PIL import Image
import time
from multiprocessing import Process, freeze_support, Queue
import justpy as jp
from humbletray import chromeapp

# from loguru import logger

q = Queue()

fig_name = "leaf.png"

# if getattr(sys, "frozen", False):
#     application_path = os.path.dirname(sys.executable)
# else:
#     try:
#         app_full_path = os.path.realpath(__file__)
#         application_path = os.path.dirname(app_full_path)
#     except NameError:
#         application_path = os.getcwd()

# fig_full_path = os.path.join(application_path, fig_name)
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


fig_full_path = resource_path(fig_name)


class SystrayIconMenu:
    def __init__(self, icon, menu=[], exit=None, schedule=None):
        self.icon = pystray.Icon("mon")
        self.icon.title = "Tooltip"
        self.icon.icon = Image.open(icon)
        self.schedule = schedule
        menu.append(("Exit", lambda: self.exit()))

        menu_items = []
        for name, action in menu:
            menu_items.append(MenuItem(name, action))
        self.icon.menu = Menu(*menu_items)

        if exit:
            self.exit = exit

    def action(self):
        print("action")

    def exit(self):
        self.icon.visible = False
        self.icon.stop()

    def setup(self, icon):
        icon.visible = True

        i = 0
        while icon.visible:
            # Some payload code
            if self.schedule:
                self.schedule.run_pending()
            print(i)
            i += 1

            time.sleep(5)

    def run(self):
        self.icon.run(self.setup)


class SystrayApp(object):
    def __init__(self, start_server, menu, icon, schedule=None):
        self.start_server = start_server
        self.menu = menu
        self.fig = icon
        self.schedule = schedule

    def run(self):
        freeze_support()
        server = Process(target=self.start_server, args=(q,))
        server.daemon = True
        server.start()

        def action():
            print("gui action")
            import atexit

            def clean_exit():
                # logger.debug("clean exit")
                app.exit()

            atexit.register(clean_exit)
            app = chromeapp.ChromeApp("http://localhost:8000", "humbletray", (800, 600), lockPort=None, chromeargs=[])

        menu = [("Open App", action)]

        icon = SystrayIconMenu(self.fig, menu, schedule=self.schedule)
        icon.run()

        server.terminate()
        server.join(timeout=1.0)


def run_gui(start_server, menu=None, fig=fig_full_path, schedule=None):
    # Todo(Ksmith): add scheduler integration
    app = SystrayApp(start_server, menu, fig, schedule)
    app.run()
