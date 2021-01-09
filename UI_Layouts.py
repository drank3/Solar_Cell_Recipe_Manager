"""
This file maintains everything with relation to the window layout of the Recipe Manager applet. All Resizing
logic, default frame ratios, window initialization, and eventually layout design (pretty UI stuff) is located
here.


This class is **inherits** (in a stupid, backwards kind of way) from the better_Builder file. See there where it
is called
"""

from PySide2 import QtCore, QtGui, QtWidgets

attributes_default_width = .35
attribute_default_height = .65
batch_viewer_default_width = .20



class Layouts:

    def __init__(self, parent):
        self.parent = parent
        self.MainWindow = parent.MainWindow
        self.Default_Window_Initialization()
        self.Resizing(self.MainWindow)
        self.MainWindow.resizeEvent = self.Resizing

    def Default_Window_Initialization(self):

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.parent.parameter_viewer = QtWidgets.QScrollArea(self.parent.centralwidget)
        self.parent.parameter_viewer.setGeometry(QtCore.QRect((batch_viewer_default_width)*self.MainWindow.width()+1, attribute_default_height*self.MainWindow.height(), (1-batch_viewer_default_width)*self.MainWindow.width(), (1-attribute_default_height)*self.MainWindow.height()))
        self.parent.parameter_viewer.setSizePolicy(sizePolicy)
        self.parent.parameter_viewer.setWidgetResizable(True)
        self.parent.parameter_viewer.setObjectName("parameter_viewer")
        self.parent.parameter_viewer_widget_contents = QtWidgets.QWidget()
        self.parent.parameter_viewer_widget_contents.setGeometry(QtCore.QRect((batch_viewer_default_width)*self.MainWindow.width()+1, attribute_default_height*self.MainWindow.height(), (1-batch_viewer_default_width)*self.MainWindow.width(), (1-attribute_default_height)*self.MainWindow.height()))
        self.parent.parameter_viewer_widget_contents.setObjectName("parameter_viewer_widget_contents")
        self.parent.parameter_viewer.setWidget(self.parent.parameter_viewer_widget_contents)

        self.parent.attribute_viewer = QtWidgets.QScrollArea(self.parent.centralwidget)
        self.parent.attribute_viewer.setGeometry(QtCore.QRect((1-attributes_default_width)*self.MainWindow.width(), 0, attributes_default_width*self.MainWindow.width(), (attribute_default_height)*self.MainWindow.height()))
        self.parent.attribute_viewer.setWidgetResizable(True)
        self.parent.attribute_viewer.setObjectName("attribute_viewer")
        self.parent.attribute_viewer_widget_contents = QtWidgets.QWidget()
        self.parent.attribute_viewer_widget_contents.setGeometry(QtCore.QRect((1-attributes_default_width)*self.MainWindow.width(), 0, attributes_default_width*self.MainWindow.width(), (attribute_default_height)*self.MainWindow.height()))
        self.parent.attribute_viewer_widget_contents.setObjectName("attribute_viewer_widget_contents")
        self.parent.attribute_viewer.setWidget(self.parent.attribute_viewer_widget_contents)


        self.parent.batch_viewer = QtWidgets.QScrollArea(self.parent.centralwidget)
        self.parent.batch_viewer.setGeometry(QtCore.QRect(0, 0, batch_viewer_default_width*self.MainWindow.width(), self.MainWindow.height()))
        self.parent.batch_viewer.setWidgetResizable(True)
        self.parent.batch_viewer.setObjectName("batch_viewer")
        self.parent.batch_viewer_widget_contents = QtWidgets.QWidget()
        self.parent.batch_viewer_widget_contents.setGeometry(QtCore.QRect(0, 0, batch_viewer_default_width*self.MainWindow.width(), self.MainWindow.height()-40))
        self.parent.batch_viewer_widget_contents.setObjectName("batch_viewer_widget_contents")
        self.parent.batch_viewer.setWidget(self.parent.batch_viewer_widget_contents)


        self.parent.structure_viewer = QtWidgets.QScrollArea(self.parent.centralwidget)
        self.parent.structure_viewer.setGeometry(QtCore.QRect(1, 1, 1, 1))
        self.parent.structure_viewer.setWidgetResizable(True)
        self.parent.structure_viewer.setObjectName("structure_viewer")
        self.parent.structure_viewer_widget_contents = QtWidgets.QWidget()
        self.parent.structure_viewer_widget_contents.setGeometry(QtCore.QRect(0, 0, 1, 1))
        self.parent.structure_viewer_widget_contents.setObjectName("structure_viewer_widget_contents")
        self.parent.structure_viewer.setWidget(self.parent.structure_viewer_widget_contents)


    """
    This function is triggered whenever the mainWindow is resized and adjusts the two main scroll area sizes

    There are inbuilt functions to deal with these kind of scaling resizing events in Qt, but rather than
    spend the 30 minutes to figure out how to use them I thought coding them from scratch would be easier

    """
    def Resizing(self, event):

        mw_width = event.size().width()-1
        mw_height = event.size().height()-42


        attribute_viewer_x = (1-attributes_default_width)*mw_width
        attribute_viewer_y = 0
        attribute_viewer_width = attributes_default_width*mw_width
        attribute_viewer_height = (attribute_default_height)*mw_height
        self.parent.attribute_viewer.move(attribute_viewer_x, attribute_viewer_y)
        self.parent.attribute_viewer.resize(attribute_viewer_width, attribute_viewer_height)
        self.parent.attribute_viewer_widget_contents.resize(attribute_viewer_width, attribute_viewer_height)

        batch_viewer_x = 1
        batch_viewer_y = 0
        batch_viewer_width = batch_viewer_default_width*mw_width
        batch_viewer_height = mw_height
        self.parent.batch_viewer.resize(batch_viewer_width, batch_viewer_height)
        self.parent.batch_viewer_widget_contents.resize(batch_viewer_width, batch_viewer_height)
        self.parent.batch_viewer.move(batch_viewer_x, batch_viewer_y)

        structure_viewer_x = batch_viewer_width
        structure_viewer_y = 0
        structure_viewer_width = attribute_viewer_x-batch_viewer_width+batch_viewer_x+1
        structure_viewer_height = attribute_viewer_height
        self.parent.structure_viewer.resize(structure_viewer_width, structure_viewer_height)
        self.parent.structure_viewer_widget_contents.resize(structure_viewer_width, structure_viewer_height)
        self.parent.structure_viewer.move(structure_viewer_x, structure_viewer_y)

        parameter_viewer_x = (batch_viewer_width)
        parameter_viewer_y = attribute_default_height*mw_height-1
        parameter_viewer_width = mw_width - batch_viewer_width
        parameter_viewer_height = (batch_viewer_y+batch_viewer_height)-parameter_viewer_y
        self.parent.parameter_viewer.resize(parameter_viewer_width, parameter_viewer_height)
        self.parent.parameter_viewer_widget_contents.resize(parameter_viewer_width, parameter_viewer_height)
        self.parent.parameter_viewer.move(parameter_viewer_x, parameter_viewer_y)
