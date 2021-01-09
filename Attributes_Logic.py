from PySide2 import QtCore, QtGui, QtWidgets

ui, rp, param_path = [None, None, None]



class Attributes_Main_Logic(object):

    def __init__(self, uix, rpx, param_pathx):
        global ui, rp, param_path
        ui = uix
        rp = rpx
        param_path = param_pathx

        self.current_pos = ui.AUI.viewer

        ui.AUI.viewer.itemChanged.connect(self.Attr_and_Group_Creation)
        ui.AUI.viewer.itemSelectionChanged.connect(self.Selected)

    def Fill_Attrs(self):
        self.Clear_Attr_Window()
        try:
            if not param_path.attributes:
                raise TypeError("No attributes")
            else:
                try:
                    self.Clear_Attr_Window()
                except:
                    ui.AUI.Create_Frame(-1, "Attr", ui.AUI.attribute_viewer)



                count = 0;

                for attr in param_path.attributes.keys():
                    value = param_path.attributes[attr]

                    if str(type(value)) == "<class 'str'>":
                        ui.AUI.Insert_Item(attr, value, "Attr", self.current_pos)
                    elif str(type(param_path.attributes[attr])) == "<class 'dict'>":
                        item = ui.AUI.Insert_Item(attr, "", "Group", self.current_pos)
                        self.Group_Filling(param_path.attributes[attr], item)
                    else:
                        pass
                    count = count+1

                param_path.attributes = []
                ui.AUI.viewer.collapseAll()

        except Exception as e:
            print(e)
            if not ui.AUI.frame:
                #There is only one grid for the attribute window, and there will never be any more
                ui.AUI.Create_Frame(-1, "Attr", ui.attribute_viewer)

                #Keeps going invisible for some reason, had to reset Visibility to True
                ui.AUI.frame.setVisible(True)
            elif ui.AUI.frame:
                self.Clear_Attr_Window()

    def Group_Filling(self, group, parent):
        for key in group.keys():
            if str(type(group[key])) == "<class 'str'>":
                ui.AUI.Insert_Item(key, group[key], "Attr", parent)
            elif str(type(group[key])) == "<class 'dict'>":
                item = ui.AUI.Insert_Item(key, "", "Group", parent)
                self.Group_Filling(group[key], item)
            else:
                pass


    #Deletes Everything on the attribute window
    def Clear_Attr_Window(self):
        ui.AUI.viewer.clear()


    def Selected(self):
        item = ui.AUI.viewer.selectedItems()

        if item:
            self.current_pos = item[-1]
        elif not item:
            self.current_pos = ui.AUI.viewer



    #A Slightly modified reimplementation of Parameter_Creation for attributes
    def Attr_and_Group_Creation(self, item, col):
        try:
            if item.type == "Attr":
                attr = item
                if (not attr.previous_name) and (attr.text(0) != "Enter Name"):
                    rp.Attribute_Init(attr.text(0), attr.text(1), attr.path)
                    attr.previous_name = attr.text(0)
                elif (attr.previous_name is not None) and (attr.text(0) != attr.previous_name):
                    rp.Rename_Attribute(attr.previous_name, attr.text(0), attr.path)
                elif (attr.previous_name is not None) and (attr.text(0) == attr.previous_name):
                    rp.Attribute_Init(attr.text(0), attr.text(1), attr.path)

                if (attr.text(0) != "Enter Name") and (col == 0):
                    font = attr.font(0)
                    font.setItalic(False)
                    attr.setFont(0, font)
                elif (col == 1) and (attr.text(1) != "Enter Value"):
                    font = attr.font(1)
                    font.setItalic(False)
                    attr.setFont(1, font)

            elif item.type == "Group":
                group = item
                if (not group.previous_name) and (group.text(0) != "Enter Name"):
                    rp.Group_Init(group.text(0), group.path)
                    group.previous_name = group.text(0)
                elif (group.previous_name is not None) and (group.text(0) != group.previous_name):
                    rp.Rename_Attribute(group.previous_name, group.text(0), group.path)
                elif (group.previous_name is not None) and (group.text(0) == group.previous_name):
                    rp.Group_Init(group.text(0), group.path)

                if (group.text(0) != "Enter Group") and (col == 0):
                    font = group.font(0)
                    font.setItalic(False)
                    group.setFont(0, font)


        except Exception as e:
            print(e)






    def Delete(self, trigger):
        name = trigger.objectName()[5:-2]
        rp.Delete_Attribute(name)
        self.Fill_Attrs()



    def Left_Click(self, select_btn):

        if select_btn.objectName() == "Add@Attr_Variable":
            self.Add_Variable()
        elif select_btn.objectName() == "Add@Attr_Group":
            self.Add_Group()

    def Right_Click(self, select_btn, event):

        if select_btn.objectName().__contains__("AttrV@"):
            ui.AUI.Context_Menu(select_btn, event)

            try:
                ui.AUI.actionDelete.triggered.connect(lambda: self.Delete(ui.AUI.actionDelete.trigger))
            except Exception as e:
                print(["Context Menu Action Failed with log:" + e])

    def Add_Variable(self):
        parent = self.current_pos
        attr = ui.AUI.Insert_Item("Enter Name", "Enter Value", "Attr", parent)
        special_font = QtGui.QFont()
        special_font.setWeight(5)
        special_font.setItalic(True)

        attr.setFont(0, special_font)
        attr.setFont(1, special_font)




    def Add_Group(self):
        parent = self.current_pos
        attr = ui.AUI.Insert_Item("Enter Group", "", "Group", parent)
        special_font = QtGui.QFont()
        special_font.setWeight(5)
        special_font.setItalic(True)

        attr.setFont(0, special_font)
        attr.setFont(1, special_font)
