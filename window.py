#python3.12 window.py
#pyinstaller --onefile window.py
import PySimpleGUI as gui
import logging
from time import sleep
from samase import Samase
import os

LOGFILE = "sezam.log"

def exists_localSamase(locals: dict) -> bool:
    if "localSamase" not in locals:
            print("Attempted to perform an operation without a directory selected!")
            return False
    else:
        return True

def exists_unpackSamase(locals: dict) -> bool:
    if "unpackSamase" not in locals:
            print("Attempted to perform an operation without a directory selected!")
            return False
    else:
        return True
    
#log setup
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', filename=LOGFILE, encoding='utf8', level = logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
logging.FileHandler(LOGFILE, mode = "w")

#window layout
layout = [[gui.Button("Select build directory"), gui.Text("Please select a path", key="curPath"), gui.Push(), gui.Checkbox("Run in x64", key="x64")],
          [gui.Button("Launch"), gui.Button("Build From")],
          [gui.Push()],
          [gui.Button("Select Executable to Unpack"), gui.Text("No exe selected", key="curExe"), gui.Push(), gui.Button("Unpack from")]
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
        clean_dir = directory[(directory.rfind("/")+1):]
        window["curPath"].update(value=clean_dir)
        localSamase=Samase(directory, None)
    if event == "Select Executable to Unpack":
        directory = gui.popup_get_file('Select path', initial_folder=os.getcwd(), file_types=(("Executable files", "*.exe"),))
        if directory == "":
            print("Nothing selected")
            continue
        clean_dir = directory[(directory.rfind("/")+1):]
        window["curExe"].update(value=clean_dir)
        unpackSamase=Samase(directory, None)
    if event == "Launch":
        if not exists_localSamase(locals()):
            continue
        localSamase.operation_type = 0
        localSamase.is64 = values["x64"]
        localSamase.operate()
    if event == "Build From":
        if not exists_localSamase(locals()):
            continue
        localSamase.operation_type = 1
        localSamase.is64 = values["x64"]
        localSamase.operate()
    if event == "Unpack from":
        if not exists_unpackSamase(locals()):
            continue
        assert unpackSamase.folder.endswith(".exe"), f"Expected executable to unpack, instead got {localSamase.folder}"
        unpackSamase.operation_type = 2
        localSamase.is64 = values["x64"]
        unpackSamase.operate()

    