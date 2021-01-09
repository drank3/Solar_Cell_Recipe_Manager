ui, mm = [None, None]



class Structure_Main_Logic(object):
    def __init__(self, uix, mmx, ST):
        global ui, mm
        ui = uix
        mm = mmx
        self.selected_layer = None
        self.ST = ST
        mm.Initialize_Materials()
        self.Enable_AP_Recipes(False)

    def Left_Click(self, select_btn):
        if select_btn.objectName() == "Add@Str_L":
            layer = self.Add_Layer()
            self.Fill_Materials(layer)
        elif select_btn.objectName().__contains__("Str@Layer"):
            self.Layer_Selected(select_btn)
        elif select_btn.objectName() == "Str@Block":
            select_btn = select_btn.parent()
            self.Layer_Selected(select_btn)
        else:
            print("unknown structure object")
            print(select_btn)

    def Add_Layer(self):
        layer = ui.SUI.Insert_New_Layer()
        self.ST.Add_Top_Layer()
        if self.selected_layer:
            ui.structure_viewer.focus_box.setParent(None)
            self.selected_layer = None
            self.Select_Material(None)
        return layer

    def Layer_Selected(self, layer):
        material = layer.material_edit.text()

        if not self.selected_layer:
            self.selected_layer = layer
            self.ST.current_layer_num = layer.num
            self.ST.current_layer_material = layer.material
            #drawing focus box around layer
            ui.SUI.Create_Focus_Box(layer)
            self.Select_Material(layer)

        else:
            if layer == self.selected_layer:
                self.selected_layer = None
                self.ST.current_layer_num = None
                self.ST.current_layer_material = None
                ui.structure_viewer.focus_box.setParent(None)
                self.Select_Material(None)
            else:
                self.selected_layer = layer
                self.ST.current_layer_num = layer.num
                self.ST.current_layer_material = layer.material
                ui.structure_viewer.focus_box.setParent(None)
                ui.SUI.Create_Focus_Box(layer)
                self.Select_Material(layer)

    def Fill_Materials(self, layer):
        materials = mm.Return_Materials()
        #Destroying a menu in case it already exists
        if layer.material_edit.menu():
            layer.material_edit.menu().setParent(None)
        for mat in materials:
            ui.SUI.Add_Material_Menu_Item(mat, layer)
        ui.SUI.Add_Material_Menu_Item("Add Material", layer)

        # Spent many hours in these couple of lines
        # It turns out lambda makes a sort of mini-function, so to preserve the text info
        # for materials when I was connecting the triggered signals I had to define them within the lamda,
        # otherwise the values would not be stored, now I know haha
        for action in layer.material_edit.menu().actions():
            if action.text() == "Add Material":
                action.triggered.connect(lambda: self.Add_Material())
            elif action.text() != "Add Material":
                text = action.text()
                action.triggered.connect(lambda text=text, layer=layer: self.Assign_Material(text, layer))

    def Add_Material(self):
        popup = ui.SUI.Popup_Material_Edit()
        popup.bt_cancel.clicked.connect(lambda: self.Popup_Material_Events("close", popup))
        popup.bt_enter.clicked.connect(lambda: self.Popup_Material_Events("enter", popup))
        popup.exec()

    def Popup_Material_Events(self, type, window):
        if type == "close":
            window.done(0)
        elif type == "enter":
            mm.Create_Material(window.t_e.text())
            window.done(1)
            self.Fill_All_Materials()

    def Fill_All_Materials(self):
        for layer in ui.SUI.layers:
            self.Fill_Materials(layer)

    def Assign_Material(self, material, layer):
        layer.material_edit.setText(material)
        layer.material = material
        info = mm.Load_Material(material)
        self.ST.Set_Layer_Material(layer.material, layer.num)
        self.ST.info[layer.num][layer.material] = info
        if layer == self.selected_layer:
            self.Select_Material(layer.material)

    def Select_Material(self, layer):
        if not layer:
            mm.Set_Existing_Material_Info(None, [])
            self.Enable_AP_Recipes(False)
        elif layer.material:
            info = self.ST.info[layer.num][layer.material]
            path = self.ST.info[layer.num]["Path"]
            mm.Set_Existing_Material_Info(info, path)
            self.Enable_AP_Recipes(True)



    def Load_Default_Materials(self):
        mm.Load_Default_Materials()
        self.Fill_All_Materials()

    def Save_Default_Materials(self):
        #TODO: Insert a popup warning here
        mm.Save_Default_Materials(self.ST)

    #TODO: Maybe add a tooltip or message on these windows that the material has not been selected
    def Enable_AP_Recipes(self, bool):

        ui.attribute_viewer.setEnabled(bool)
        ui.parameter_viewer.setEnabled(bool)

        for child in ui.parameter_viewer.children():
            if child.objectName().__contains__("frame"):
                child.setVisible(bool)

    def Clear_Structure_Window(self):
        self.selected_layer = None
        self.ST.current_layer_num = None
        self.ST.current_layer_material = None
        if hasattr(ui.structure_viewer, "focus_box"):
            ui.structure_viewer.focus_box.setParent(None)
        frame = ui.SUI.frame
        for child in frame.children():
            child.setParent(None)
        ui.SUI.layers = []

    def Load_Structure(self):
        self.Clear_Structure_Window()
        info = self.ST.Load_Structure()
        if info:
            for layer_info in info:
                material = [key for key in layer_info.keys() if key != "Path"][-1]
                layer = ui.SUI.Insert_New_Layer()
                layer.material_edit.setText(material)
                layer.material = material

    def Set_and_Show_Structure(self, structure_info):
        self.Clear_Structure_Window()
        self.ST.info = structure_info
        if structure_info:
            for layer_info in structure_info:
                material = [key for key in layer_info.keys() if key != "Path"][-1]
                layer = ui.SUI.Insert_New_Layer()
                layer.material_edit.setText(material)
                layer.material = material
                self.Enable_AP_Recipes(False)
                mm.updater.Clear_Par_and_Attr()
        else:
            #TODO: This case may never be necessary, but put in a null handler as well
            pass

    def Save_Structure(self):
        #TODO: Maybe add in a warning dialog HERE
        self.ST.Save_Structure()
