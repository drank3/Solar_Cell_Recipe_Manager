from PySide2 import QtCore, QtGui, QtWidgets
from UI_Layouts import Layouts
import Attributes_UI
import Parameters_UI
import Structure_UI
import Batch_UI




class Central_UI(object):

#TODO: Windows kind of stutter when resizing, maybe use global pos instead of local ones when moving stuff
#TODO: ScrollArea Stuff
#TODO: Make fonts look nicer
#TODO: Make Attr window look nicer
#TODO: Redesign the header images, maybe add color schemes to them and give a trail
#TODO: Buttons look gross, fix them (pwpnt has some good bevel options I guess)
#TODO: Add in that feature to change the ratio between the two scroll areas

    def __init__(self):
        #I kind of understand this super line, its just making sure that QtWidget init is not overridden
        super(QtWidgets.QWidget).__init__()


        self.MainWindow = QtWidgets.QMainWindow()

        self.setupUi()
        self.Main_Menus()



        self.MainWindow.show()



    def setupUi(self):


        #Setting the base window up, most of this is uninteresting/redundant
        self.MainWindow.setObjectName("self.MainWindow")
        self.MainWindow.resize(1100, 700)
        self.MainWindow.setFixedSize(1100, 700)
        self.MainWindow.move(800, 100)


        #self.MainWindow.showMaximized()
        self.MainWindow.setWindowTitle("Recipe Manager")


        icon = QtGui.QIcon("Icon.png")
        self.MainWindow.setWindowIcon(icon)



        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        font.setWeight(50)
        self.MainWindow.setFont(font)
        self.MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.MainWindow.setAutoFillBackground(False)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)


        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        Layouts(self)

        self.AUI = Attributes_UI.Attributes_Window(self.attribute_viewer)
        self.PUI = Parameters_UI.Parameters_Window(self.parameter_viewer)
        self.SUI = Structure_UI.Structure_Window(self.structure_viewer)
        self.BUI = Batch_UI.Batch_Window(self.batch_viewer)



        self.MainWindow.setCentralWidget(self.centralwidget)


        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)



        #Passing the function with the actual amount of children the scrollbox has
        #Creating the first frame (to build up a new recipe)
        self.PUI.Create_Grid(0, "Par", self.parameter_viewer)




    def Main_Menus(self):
        self.menubar = QtWidgets.QMenuBar(self.MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1692, 21))
        self.menubar.setObjectName("menubar")
        self.MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)

        """ Stuff for the file menu option"""
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuFile.setTitle("File")
        self.menubar.addAction(self.menuFile.menuAction())

        self.actionOpen = QtWidgets.QAction(self.MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(self.MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionExport_to_CSV = QtWidgets.QAction(self.MainWindow)
        self.actionExport_to_CSV.setObjectName("actionExport_to_CSV")
        self.actionSave_As = QtWidgets.QAction(self.MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionExport = QtWidgets.QAction(self.MainWindow)
        self.actionExport.setObjectName("actionExport")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addAction(self.actionExport)

        self.actionExport_to_CSV.setText("Export to CSV")
        self.actionSave_As.setText("Save As")
        self.actionExport.setText("Export Recipe")
        self.actionSave.setText("Save")
        self.actionOpen.setText("Open")


        """Stuff for the View menu option"""
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuView.setTitle("View")
        self.menubar.addAction(self.menuView.menuAction())


        """Stuff for the Devices menu option"""
        self.menuDevices = QtWidgets.QMenu(self.menubar)
        self.menuDevices.setObjectName("menuDevices")
        self.menubar.addAction(self.menuDevices.menuAction())
        self.menuDevices.setTitle("Devices")

        self.actionImport_Devices = QtWidgets.QAction(self.menuDevices)
        self.actionImport_Devices.setObjectName("actionImport_Devices")
        self.actionImport_Devices.setText("Import New Devices")
        self.menuDevices.addAction(self.actionImport_Devices)

        self.actionSave_All_Device_Data = QtWidgets.QAction(self.menuDevices)
        self.actionSave_All_Device_Data.setObjectName("actionSave_All_Device_Data")
        self.actionSave_All_Device_Data.setText("Save All Device Data")
        self.menuDevices.addAction(self.actionSave_All_Device_Data)

        self.actionSet_Selected_Device_Structure = QtWidgets.QAction(self.menuDevices)
        self.actionSet_Selected_Device_Structure.setObjectName("actionSet_Selected_Device_Structure")
        self.actionSet_Selected_Device_Structure.setText("Set Selected Device Structure")
        self.menuDevices.addAction(self.actionSet_Selected_Device_Structure)


        """Stuff for the Materials menu option"""
        self.menuMaterials = QtWidgets.QMenu(self.menubar)
        self.menuMaterials.setObjectName("menuMaterials")
        self.menubar.addAction(self.menuMaterials.menuAction())
        self.menuMaterials.setTitle("Materials")

        self.actionLoad_Default_Materials = QtWidgets.QAction(self.menuMaterials)
        self.actionLoad_Default_Materials.setObjectName("actionLoad_Default_Materials")
        self.actionLoad_Default_Materials.setText("Load Default Materials")
        self.menuMaterials.addAction(self.actionLoad_Default_Materials)

        self.actionSave_Default_Materials = QtWidgets.QAction(self.menuMaterials)
        self.actionSave_Default_Materials.setObjectName("actionSave_Default_Materials")
        self.actionSave_Default_Materials.setText("Save Default Materials")
        self.menuMaterials.addAction(self.actionSave_Default_Materials)


        """Stuff for the Structures menu Option"""
        self.menuStructures = QtWidgets.QMenu(self.menubar)
        self.menuStructures.setObjectName("menuStructures")
        self.menubar.addAction(self.menuStructures.menuAction())
        self.menuStructures.setTitle("Structures")

        self.actionLoad_Structure = QtWidgets.QAction(self.menuStructures)
        self.actionLoad_Structure.setObjectName("actionLoad_Structure")
        self.actionLoad_Structure.setText("Load Structure")
        self.menuStructures.addAction(self.actionLoad_Structure)

        self.actionSave_Structure = QtWidgets.QAction(self.menuStructures)
        self.actionSave_Structure.setObjectName("actionSave_Structure")
        self.actionSave_Structure.setText("Save Structure")
        self.menuStructures.addAction(self.actionSave_Structure)







if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    nice = Central_UI()

    sys.exit(app.exec_())
