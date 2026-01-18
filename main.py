from tkinter import filedialog, messagebox
from os import getcwd, system, path
import tkinter as tk
import subprocess, sys

BLANK_WORLD_PATH = f"{getcwd()}\\mc3ds\\data\\blankworld"
print(BLANK_WORLD_PATH)
DEP_LIST = ["dissect.cstruct", "anvil-new", "click", "nbtlib", "p_tqdm"]

def startConversion(worldName:str):
    system(f'py -m 3dschunker -c "{folder_path}" -w "{worldName}"')


def getWorldName(byteData:bytes):
    from mc3ds.nbt import NBT
    return str(NBT(byteData).get("LevelName"))

def getWorld():
    global folder_path, levelDatPath
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_entry.config(state=tk.NORMAL)
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder_path)
        folder_entry.config(state=tk.DISABLED)
        levelDatPath = f"{folder_path}/level.dat"

def testModules():
    try: import dissect.cstruct, click, nbtlib, p_tqdm
    except ImportError:
        answer = messagebox.askyesno("Module Notice", "3DS-Chunker needs some Modules to opperate.\nMay it install them now?")
        if answer:
            for module in DEP_LIST:system(f'pip install {module}')
            messagebox.showinfo("Notice", "You will need to Re-Run the GUI.\nRequired modules have been installed.")
            sys.exit(1)
        else:sys.exit(1)

def beforeConvert():
    testModules()
    if not folder_entry.get():
        messagebox.showerror("ERROR - Generic", "No PATH to the World was Set.\nPlease select a World to Convert.")
        return
    if not path.exists(f"{folder_entry.get()}\\db\\vdb"):
        messagebox.showerror("ERROR - Generic", f"The World PATH is Invalid.\nOnly select the top-most directory of the World.")
        return
    with open(levelDatPath, 'rb+') as f:
        worldName = getWorldName(f.read())
    startConversion(worldName)

try:from mc3ds.nbt import NBT
except ModuleNotFoundError: print("success");testModules()


root = tk.Tk()
root.title("3DS Chunker (World Converter) - GUI")
root.geometry("600x200")
root.resizable(False, False)
root.config(background='black')

frame = tk.Frame(root)
frame.config(background='black')
frame.pack(pady=20, padx=10)
folder_entry = tk.Entry(frame, width=80)
folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
import_button = tk.Button(frame, text="...", command=getWorld, border=0)
import_button.pack(side=tk.RIGHT, padx=5)

bottom_frame = tk.Frame(root, bg='black')
bottom_frame.pack(side=tk.BOTTOM, pady=10)
center_button = tk.Button(bottom_frame, text="Convert 3DS to Java", command=beforeConvert)
center_button.pack(side=tk.BOTTOM, pady=10)

root.mainloop()