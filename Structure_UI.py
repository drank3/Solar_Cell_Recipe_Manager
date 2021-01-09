from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtGui import QColor
import random


class Structure_Window(object):

    def __init__(self, structure_viewer):

        self.structure_viewer = structure_viewer

        self.layers = []
        self.layer_colors = None
        self.layer_colors = self.Layer_Color_Palette()
        self.Set_Header()
        self.Create_Frame()

        self.frame.resizeEvent = self.Frame_Centering
        self.Create_Insert_Layer_Button()
        self.layer_colors = self.Layer_Color_Palette()

    def Set_Header(self):
        self.header3 = QtWidgets.QLabel(self.structure_viewer)
        self.header3.setGeometry(QtCore.QRect(1, 1, 150, 50))
        image = QtGui.QImage("Structure Picture.png")
        image = image.smoothScaled(150, 50)
        pixs = QtGui.QPixmap.fromImage(image)
        self.header3.setPixmap(pixs)

    def Create_Frame(self):
        frame_h_offset = 25
        frame_v_offset = 30
        frame_width = self.structure_viewer.width() - 2*frame_h_offset
        frame_height = self.structure_viewer.height() - 50 - 2*frame_v_offset

        self.frame = QtWidgets.QFrame(self.structure_viewer)
        self.frame.setGeometry(QtCore.QRect(frame_h_offset, frame_v_offset+20, frame_width, frame_height))

        self.frame.setVisible(True)

    """This is just a temporary function for easy layer adding until I design a better way"""
    def Create_Insert_Layer_Button(self):

        font = QtGui.QFont()
        font.setPointSize(11)

        xPos = self.structure_viewer.width() - 100
        yPos = 15

        button = QtWidgets.QLabel(self.structure_viewer)
        button.setGeometry(QtCore.QRect(xPos, yPos, 40, 15))
        button.setText(" Insert Layer ")
        button.setObjectName("Add@Str_L")
        button.setFont(font)

        button.setFrameShape(QtWidgets.QFrame.Panel)
        button.setFrameShadow(QtWidgets.QFrame.Raised)
        button.setLineWidth(1)
        button.adjustSize()
        button.setVisible(True)

        return button

    def Insert_New_Layer(self):


        layer_height = 30
        layer_spacer = 9
        inital_layer_width = self.frame.width()*.7
        layer_material_separation = self.frame.width()*.1
        num = len(self.layers)


        self.layer_total_height = layer_height + layer_spacer
        self.layer_block_width = inital_layer_width
        self.layer_spacer = layer_spacer

        if len(self.layers) > 0:
            self.Move_Layers_Down()
        elif len(self.layers) == 0:
            layer_spacer = 0

        box = QtWidgets.QFrame(self.frame)
        box.setGeometry(QtCore.QRect(0, 0, self.frame.width(), layer_height+layer_spacer))
        box.setObjectName("Str@Layer_" + str(num))
        box.setLineWidth(0)
        box.setVisible(True)
        box.material = None
        box.num = num


        layer = Layer_Block(box)
        layer_width = inital_layer_width * .9**(len(self.layers))
        layer_yPos = len(self.layers) * (layer_height + layer_spacer)
        layer.setGeometry(QtCore.QRect(0, 0, layer_width, layer_height))

        #The next few lines are responsible for randomizing the color palette (after every 5 layers)
        #and creating the layer block itself
        if len(self.layers)%len(self.layer_colors) == 0 and len(self.layers) != 0:
            self.layer_colors = self.Layer_Color_Palette()
        layer.drawBlock(self.layer_colors[len(self.layers)%len(self.layer_colors)])

        box.layer_block = layer


        material = self.Create_Material_Edit(box)
        box.material_edit = material

        layer.setVisible(True)

        self.layers = self.layers + [box]
        self.frame.adjustSize()

        return box

    #This function creates a psuedo widget, didn't feel like defining this as its own class
    def Create_Material_Edit(self, parent):
        h_spacer = 10
        v_spacer = 5

        xPos = self.layer_block_width + h_spacer
        yPos = parent.y() + v_spacer

        widget = QtWidgets.QPushButton(parent)

        widget.setGeometry(xPos, yPos, 50, 15)
        if not parent.material:
            widget.setText("No Material Selected")
        else:
            widget.setText(parent.material)

        widget.adjustSize()
        widget.resize(widget.width()+15, widget.height()-2)
        widget.setVisible(True)
        return widget

    def Add_Material_Menu_Item(self, text, layer):
        parent = layer.material_edit
        if not parent.menu():
            menu = QtWidgets.QMenu()
            menu.addAction(text)
            parent.setMenu(menu)
            parent.menu().update()

        else:
            parent.menu().addAction(text)
            parent.menu().update()

    def Move_Layers_Down(self):
        layers = [layer for layer in self.frame.children() if layer.objectName().__contains__("Str@Layer") ]
        for layer in layers:
            layer.move(layer.x(), layer.y()+self.layer_total_height)

    def Frame_Centering(self, event):
        center_v_offset = 15
        new_height = self.frame.height()
        new_width = self.frame.width()

        xPos = (self.structure_viewer.width() - new_width)/2
        yPos = (self.structure_viewer.height() - new_height)/2 + center_v_offset

        self.frame.move(xPos, yPos)

    def Layer_Color_Palette(self):

        """default colors below"""
        color1 = QColor(33,176,192)
        color2 = QColor(8,76,97)
        color3 = QColor(219,58,52)
        color4 = QColor(255,200,87)
        color5 = QColor(50,48,49)
        #These colors were kind of just chosen at random, whatever looked decent
        #These are only necessary when a default color selection for a material has not been met
        colors = [color1, color2, color3, color4, color5]

        if not self.layer_colors:
            #If no color order has been set up yet
            mixed_colors = random.sample(colors, len(colors))
        else:
            #case to ensure that the first colors of the new list doesn't match the last of the old one
            #(no same color 2 times in a rpw)
            mixed_colors = random.sample(colors, len(colors))
            while mixed_colors[1] == self.layer_colors[-1]:
                mixed_colors = random.sample(colors, len(colors))
        return mixed_colors

    def Create_Focus_Box(self, layer):
        focus_box = QtWidgets.QFrame(layer.parent().parent())
        focus_box.setObjectName("Str@Focus")
        # how far the box is from the layer

        separation = 4
        # Very jarbled, but it is finding the relative position of layer in self.structure viewer
        # as a whole
        pos = layer.mapTo(self.structure_viewer, QtCore.QPoint(0, 0))
        xPos = (pos.x()) - separation
        yPos = (pos.y()) - separation
        width = layer.width() + 2*separation
        # The first layer doesn't have the layer spacer, but the rest need it subtracted from their height
        if int(layer.objectName()[-1]) > 0:
            height = layer.height() + 2*separation - self.layer_spacer
        else:
            height = layer.height() + 2*separation


        focus_box.setGeometry(QtCore.QRect(xPos, yPos, width, height))
        focus_box.setStyleSheet('''color: rgb(140, 140, 200);
                                   background-color: transparent;''')
        focus_box.setFrameShape(QtWidgets.QFrame.Box)
        focus_box.setLineWidth(2)
        focus_box.setVisible(True)
        # The frame kept blocking out the content underneath, so I had to stack it under self.frame
        focus_box.stackUnder(self.frame)
        self.structure_viewer.focus_box = focus_box

    # This function is a hot mess, but it works, sort of
    # Creates a popup dialog to enter the new material name
    #TODO: Make richtext stuff work for subscripts and Stuff
    #TODO: Make the top bar smaller, it is too big, and get rid of the question mark
    def Popup_Material_Edit(self):
        #if you want to change around the position of this popup, mess with xPos and yPos
        #I decided to just have it pop up in the middle of the application
        window = QtWidgets.QDialog()
        #These lines are meant to get hold of the mainwindow of the application, there is probably a better way to do it
        mw_pos = self.structure_viewer.parent().parent().pos()
        mw_width = self.structure_viewer.parent().parent().width()
        mw_height = self.structure_viewer.parent().parent().height()

        xPos = mw_pos.x() + mw_width/2
        yPos = mw_pos.y() + mw_height/2 -100

        window.setGeometry(xPos, yPos, 50, 50)

        label = QtWidgets.QLabel(window)
        label.setGeometry(10, 15, 15, 40)
        label.setText("Enter Material Name: ")
        label.font().setPointSize(14)
        label.adjustSize()

        initial_te_width = 130
        text_edit = QtWidgets.QLineEdit(window)
        text_edit.setGeometry(QtCore.QRect(label.x() + label.width() + 1, label.y() - 2, initial_te_width, label.height() + 4))
        text_edit.font().setPointSize(14)
        window.t_e = text_edit

        v_spacer = 15
        cancel = QtWidgets.QPushButton(window)
        cancel.setGeometry(QtCore.QRect(label.x(), label.y() + label.height() + v_spacer, 10, 10))
        cancel.setText("Cancel")
        cancel.font().setPointSize(12)
        cancel.adjustSize()

        window.bt_cancel = cancel


        enter = QtWidgets.QPushButton(window)
        enter.setGeometry(QtCore.QRect(cancel.x() + 150, cancel.y(), 10, 10))
        enter.setText("Add Material")
        enter.font().setPointSize(12)
        enter.adjustSize()
        window.bt_enter = enter

        window.adjustSize()
        enter.move(window.width()-enter.width()-cancel.x(), enter.y())

        window.move(xPos - window.width()/2, yPos - window.height()/2)
        window.resize(window.width() , window.height()-3)


        return window


#TODO: The rounded rectangles in this still look sloppy, I'll try a couple different rendering tricks later to see if this can be fixed
class Layer_Block(QtWidgets.QLabel):

    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("Str@Block")


    def drawBlock(self, color):

        self.path = QtGui.QPainterPath()

        self.path.addRoundedRect(QtCore.QRect(float(1.0), float(1.0), float(self.width() - 2.0), float(self.height()- 2.0)), 7.0, 7.0)

        self.pen = QtGui.QPen(QtCore.Qt.black, 1.0)
        self.color = color

        self.block = True
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        if self.block:
            painter.setPen(self.pen)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            painter.fillPath(self.path, self.color)
            painter.drawPath(self.path)
        painter.end()
