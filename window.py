# TODO: turn into run.bat and build.bat (or .sh for linux?)
# python3.12 window.py
# pyinstaller --onefile window.py
# pyinstaller window.spec
import PySimpleGUI as gui
import logging
import samase
import os

LOGFILE = "sezam.log"

# TODO: supply intelligent defaults
local_samase = ""
unpack_samase = ""

def pathSet(value: str) -> bool:
    if value == "":
        print("Attempted to perform an operation without a directory selected!")
        return False
    return True
    
# Log setup
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', filename=LOGFILE, encoding='utf8', level = logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
logging.FileHandler(LOGFILE, mode = "w")

# Window layout
layout = [[gui.Button("Select build directory"), gui.Text("Please select a path", key="curPath"), gui.Push(), gui.Checkbox("Run in x64", key="x64")],
          [gui.Push(), gui.Button("Launch"), gui.Button("Build From"), gui.Push()],
          [gui.Push()],
          [gui.Button("Select .exe to Unpack"), gui.Text("No exe selected", key="curExe")],
          [gui.Push(), gui.Button("Unpack from"), gui.Push()]
]

window = gui.Window("Sezam", layout, resizable=True)
while True:
    event, values = window.read()
    if event == gui.WIN_CLOSED:
        break
    if event == "Select build directory":
        directory = gui.popup_get_folder('Select path', initial_folder=os.getcwd())
        if directory == "":
            print("Nothing selected")
            continue
        clean_dir = directory[(directory.rfind("/")+1):] # TODO: use appropriate function from os.path
        window["curPath"].update(value=clean_dir)
        local_samase = directory
    if event == "Select Executable to Unpack":
        directory = gui.popup_get_file('Select path', initial_folder=os.getcwd(), file_types=(("Executable files", "*.exe"),))
        if directory == "":
            print("Nothing selected")
            continue
        clean_dir = directory[(directory.rfind("/")+1):]
        window["curExe"].update(value=clean_dir)
        unpack_samase = directory
    if event == "Launch":
        if not pathSet(local_samase):
            continue
        samase.run(local_samase, values["x64"])
    if event == "Build From":
        if not pathSet(local_samase):
            continue
        samase.build(local_samase, values["x64"])
    if event == "Unpack from":
        if not pathSet(unpack_samase):
            continue
        # on assumption that the user must select .exe file in the popup
        assert unpack_samase.endswith(".exe"), f"Expected executable to unpack, instead got {local_samase}"
        samase.build(unpack_samase, values["x64"])

    