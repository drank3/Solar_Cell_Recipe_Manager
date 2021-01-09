import tkinter as tk
from tkinter import filedialog
import json
import os

class Structure(object):
    def __init__(self):
        #Note that the layer number starts from 0, not 1, in accordance to python list indexing
        self.current_layer_num = None
        self.current_layer_material = None
        #temp_storage is an attribute used to temporarily store structure information, which is useful when clicking through devices
        self.temp_storage = None
        self.info = []

    def Add_Top_Layer(self):
        self.info = self.info + [None]


    def Set_Layer_Material(self, material, num):
        self.info[num] = {material: {}}
        self.info[num]["Path"] = []

    def Load_Structure(self):
        root = tk.Tk()
        root.withdraw()
        filename = filedialog.askopenfilename(initialdir = os.getcwd(), title = "Load Structure", filetypes = (("Recipe File", "*.rcp*"),  ("All files", "*.*")))
        try:
            with open(filename, 'r') as file:
                info = json.load(file)
            self.info = info
            self.temp_storage = info
            return info
        except:
            print("Structure Load Aborted")
            return False

    def Save_Structure(self):
        root = tk.Tk()
        root.withdraw()
        save_dir = os.getcwd()
        filename = filedialog.asksaveasfilename(initialdir = save_dir, title = "Save Structure", filetypes = (("Recipe Files", "*.rcp*"), ("All files", "*.*")))
        if filename[-4:] == ".rcp":
            print("overwritten old file with filename:"+filename)
            with open(filename[:-4] + ".rcp", 'w') as file:
                json.dump(self.info, file)
        else:
            with open(filename + ".rcp", 'w') as file:

                json.dump(self.info, file)
