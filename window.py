# python3.12 window.py
# pyinstaller --onefile window.py
# pyinstaller window.spec
import PySimpleGUI as gui
import logging
import samase
import os
from utilities import log_print
from const import LOGFILE, SEL_DIR, DIR_HINT, START, BUILD, STR_64, SEL_UNPK, DO_UNPK, SEL_POPUP, SEL_ERR, UNPK_HINT, WINDOW_NAME, SECTION_1, SECTION_2

def assert_path(path: str | None, message: str = "Attempted to perform an operation without a directory selected!") -> bool:
    if path == "" or path is None:
        log_print(message)
        return False
    return True

class Window():
    def __init__(self):
        self.local_samase = ""
        self.unpack_samase = ""
        self.original_directory = os.getcwd()

        layout = [[gui.Push(), gui.Text(SECTION_1, font=("Helvetica", 12, "bold")), gui.Push()],
                [gui.Button(SEL_DIR), gui.Text(DIR_HINT, key="curPath"), gui.Push(), gui.Checkbox(STR_64, key="x64")],
                [gui.Push(), gui.Button(START), gui.Button(BUILD), gui.Push()],
                [gui.Push()],
                [gui.Push(), gui.Text(SECTION_2, font=("Helvetica", 12, "bold"), tooltip="The exe will be unpacked to /target/ in this directory"), gui.Push()],
                [gui.Button(SEL_UNPK), gui.Text(UNPK_HINT, key="curExe")],
                [gui.Push(), gui.Button(DO_UNPK, tooltip="WARNING! Overwrites target folder contents"), gui.Push()]
        ]
        self.window = gui.Window(WINDOW_NAME, layout, resizable=True)

    def run(self):
        while True:
            event, values = self.window.read()
            if event == gui.WIN_CLOSED:
                log_print("Exiting sezam, bye!")
                break
            log_print(f"\033[0;30mExecuting event: {event}...\033[0;0m")
            if event == SEL_DIR:
                directory: str | None = gui.popup_get_folder(SEL_POPUP, initial_folder=os.getcwd())
                log_print(f"Selected directory: {directory}")
                if not assert_path(directory, SEL_ERR):
                    continue
                clean_dir = directory[(directory.rfind("/")+1):] # TODO: use appropriate function from os.path
                self.window["curPath"].update(value=clean_dir)
                self.local_samase = directory
            if event == SEL_UNPK:
                directory: str | None = gui.popup_get_file(SEL_POPUP, initial_folder=os.getcwd(), file_types=(("Executable files", "*.exe"),))
                log_print(f"Selected executable: {directory}")
                if not assert_path(directory, SEL_ERR):
                    continue
                clean_dir = directory[(directory.rfind("/")+1):]
                self.window["curExe"].update(value=clean_dir)
                self.unpack_samase = directory
            if event == START:
                if not assert_path(self.local_samase):
                    continue
                log_print(f"Trying to launch a session from {self.local_samase}...")
                samase.run(self.local_samase, values["x64"])
            if event == BUILD:
                if not assert_path(self.local_samase):
                    continue
                log_print(f"Trying to pack an executable from {self.local_samase}...")
                samase.build(self.local_samase, values["x64"])
            if event == DO_UNPK:
                if not assert_path(self.unpack_samase):
                    continue
                if not self.unpack_samase.endswith(".exe"):
                    log_print(f"Expected executable to unpack, instead got {self.local_samase}!")
                    continue
                samase.unpack(self.unpack_samase, values["x64"], first_dir=self.original_directory)

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', filename=LOGFILE, encoding='utf8', level = logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
    logging.FileHandler(LOGFILE, mode = "w")

    window = Window()
    window.run()
    