import tkinter as tk
from tkinter import filedialog
import csv
import json
import os




#This class is primarily a data storage object, and as such, I've tried to keep is as simple as possible
#All higher-level logical functions are handled by Device_Manager
class Devices_Info(object):

    def __init__(self):
        self.info = {"Batches": {}, "Unsorted Devices": {}}

    def Add_Batch(self, batch_name):
        self.info["Batches"][batch_name] = {}

    def Add_Device(self, device_name, batch_name):
        if not batch_name:
            self.info["Unsorted Devices"][device_name] = {}
        else:
            self.info["Batches"][batch_name][device_name] = {}

    def Set_Device_Structure(self, structure, device_name, batch_name):
        if not batch_name:
            self.info["Unsorted Devices"][device_name] = structure.info
        else:
            self.info["Batches"][batch_name][device_name] = structure.info

    def Return_Structure_Info(self, device_name, batch_name):
        if batch_name:
            return self.info["Batches"][batch_name][device_name]
        else:
            return self.info["Unsorted Devices"][device_name]



devices_info = Devices_Info()

class Device_Manager(object):

    def __init__(self, structure):
        self.devices = devices_info
        self.structure = structure
    def Import_New_Devices(self):
        raw_dev_info = []
        all_batches = {}
        root = tk.Tk()
        root.withdraw()
        save_dir = os.getcwd()
        filename = filedialog.askopenfilename(initialdir = save_dir, title = "Import New Devices", filetypes = (("CSV", "*.csv*"), ("All files", "*.*")))
        try:
            with open(filename, 'r') as file:
                temp = csv.reader(file, delimiter=',')
                raw_dev_info = [row for row in temp]
            for device in raw_dev_info:
                batch_name = device[0]
                device_name = device[1]

                if not batch_name:
                    devices_info.Add_Device(device_name, None)
                else:
                    if batch_name in devices_info.info["Batches"]:
                        devices_info.Add_Device(device_name, batch_name)
                    else:
                        devices_info.Add_Batch(batch_name)
                        devices_info.Add_Device(device_name, batch_name)
            return True
        except:
            print("Devices import aborted")
            return false
    def Set_Device_Structure_To_Current(self, device_name, batch_name):
        self.devices.Set_Device_Structure(self.structure, device_name, batch_name)

    def Save_All_Device_Data(self):
        root = tk.Tk()
        root.withdraw()
        save_dir = os.getcwd()
        filename = filedialog.asksaveasfilename(initialdir = save_dir, title = "Save Devices Data", filetypes = (("Device Recipe Files", "*.rcpd*"), ("All files", "*.*")))
        try:
            if filename[-5:] == ".rcpd":
                print("overwritten old file with filename:"+filename)
                with open(filename[:-5] + ".rcpd", 'w') as file:
                    json.dump(self.devices.info, file)
            else:
                with open(filename + ".rcpd", 'w') as file:
                    json.dump(self.devices.info, file)
            return True
        except Exception as e:
            print(e)
            return False
