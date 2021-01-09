from PySide2 import QtCore, QtGui, QtWidgets
global all_batches

ui, dm, SL = [None, None, None]

class Batch_Main_Logic(object):

    def __init__(self, uix, dmx, SLx):
        global ui, dm, SL
        ui = uix
        dm = dmx
        SL = SLx
        ui.BUI.batch_tree.itemSelectionChanged.connect(lambda: self.Device_Selected())
        self.devices = dm.devices
        self.loaded = False


    def Import_Devices(self):
        global all_batches
        all_batches = dm.Import_New_Devices()

        for batch in self.devices.info["Batches"].keys():
            b_parent = ui.BUI.Insert_Item(batch, "Batch", ui.BUI.batch_tree)
            b_parent.status = 0
            for device in self.devices.info["Batches"][batch].keys():
                item = ui.BUI.Insert_Item(device, "Device", b_parent)
                item.status = 0
        for device in self.devices.info["Unsorted Devices"].keys():
            ui.BUI.Insert_Item(device, "Unsorted Device", ui.BUI.batch_tree)

    def Set_Selected_Device_Structure(self):
        dm.structure.temp_storage = dm.structure.info
        checked_items = self.Find_Checked()
        unsorted_devices = [x for x in checked_items if x.type == "Unsorted Device"]
        batch_devices = [x for x in checked_items if x.type == "Device"]

        for item in unsorted_devices:
            device = item.text(0)
            dm.Set_Device_Structure_To_Current(device, None)
            ui.BUI.Change_Item_Color(item, "blue")
            item.status = 1
            item.setCheckState(0, QtCore.Qt.CheckState.Unchecked)

        for item in batch_devices:
            batch = item.parent().text(0)
            device = item.text(0)
            dm.Set_Device_Structure_To_Current(device, batch)
            ui.BUI.Change_Item_Color(item, "blue")
            item.status = 1
            item.setCheckState(0, QtCore.Qt.CheckState.Unchecked)
        self.Manual_Autotristation()
        self.Unselect_All()

    #This returns a list of all checked items in the batch tree viewer
    def Find_Checked(self):
        checked = []
        root = ui.BUI.batch_tree.invisibleRootItem()

        for i in range(root.childCount()):
            top_item = root.child(i)
            #This catches the unsorted devices
            if top_item.childCount() == 0:
                if top_item.checkState(0) == QtCore.Qt.Checked:
                    checked += [top_item]
            elif top_item.childCount() > 0:
                #This segment catches the devices inside a batch
                for g in range(top_item.childCount()):
                    child = top_item.child(g)
                    if child.checkState(0) == QtCore.Qt.Checked:
                        checked += [child]
                #This line catches all of the batches
                if top_item.checkState(0) == QtCore.Qt.Checked:
                    checked += [top_item]

        return(checked)

    def Manual_Autotristation(self):
        root = ui.BUI.batch_tree.invisibleRootItem()
        for i in range(root.childCount()):
            top_item = root.child(i)
            count = 0
            statuses = []
            if top_item.childCount() > 0:
                #This segment catches the devices inside a batch
                for g in range(top_item.childCount()):
                    child = top_item.child(g)
                    statuses += [child.status]

                if all(status == 1 for status in statuses):
                    ui.BUI.Change_Item_Color(top_item, "blue")
                elif all(status == 2 for status in statuses):
                    ui.BUI.Change_Item_Color(top_item, "green")

    def Save_All_Device_Data(self):

        result = dm.Save_All_Device_Data()
        if result:
            print("Save completed successfully")
        else:
            print("Save operation failed")

    def Load_Device_Data(self):
        pass

    def Unselect_All(self):
        item_list = ui.BUI.batch_tree.selectedItems()
        for item in item_list:
            item.setSelected(False)

    def Device_Selected(self):
        selection = ui.BUI.batch_tree.selectedItems()
        #This feature is giving me some trouble, excluding it for now
        if len(selection) == 0:
            pass
            """
            SL.Set_and_Show_Structure(dm.structure.temp_storage)
            """
        else:
            """
            print(selection[0].status)
            item = selection[0]
            if item.status == 1 or item.status == 2:
                if item.type == "Unsorted Device":
                    print("ok bro")
                elif item.type == "Device":
                    device = item.text(0)
                    batch = item.parent().text(0)
                    print("device: " + device + ",  Batch: " + batch)
                    structure_info = dm.devices.Return_Structure_Info(device, batch)
                    SL.Set_and_Show_Structure(structure_info)

            elif item.status == 0:
                SL.Set_and_Show_Structure(dm.structure.temp_storage)
            """
