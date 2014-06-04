# -*- coding: utf-8 -*-
"""
Created on Thu May  8 02:46:29 2014

@author: argentum
"""

from PyQt4 import QtGui, QtCore
#from math import sqrt
from PIL import Image
from PIL import ImageQt
from PIL import ImageEnhance

class Window(QtGui.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.view = View(self)
        self.view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.view.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.btnLoad = QtGui.QPushButton('Load', self)
        self.btnClearView = QtGui.QPushButton('Clear View', self)
        self.btnPlot = QtGui.QPushButton('Plot', self)
        self.btnQuit = QtGui.QPushButton('Quit', self)
        self.lcdBrightness = QtGui.QLCDNumber(self)
        
        
        #Slider Brightness
        self.slrBrightness = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.slrBrightness.setTickPosition (QtGui.QSlider.TicksBelow)
        self.slrBrightness.setMinimum(1)
        self.slrBrightness.setMaximum(100)
        self.slrBrightness.setValue(50)
        self.slrBrightness.setTickInterval(1)
        self.slrBrightness.setDisabled(True)
        #Slider Contrast
        self.slrContrast = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.slrBrightness.setTickPosition (QtGui.QSlider.TicksBelow)
        self.slrContrast.setMinimum(1)
        self.slrContrast.setMaximum(100)
        self.slrContrast.setValue(50)
        self.slrContrast.setTickInterval(1)
        self.slrContrast.setDisabled(True)
        #CONSTRUCTION
        #layout's
        self.lytVert = QtGui.QVBoxLayout()
        self.lytHorButtons = QtGui.QHBoxLayout()
        self.lytHorView = QtGui.QHBoxLayout()
        #add to layout's
        self.lytHorButtons.addWidget(self.lcdBrightness)
        self.lytHorButtons.addWidget(self.btnLoad)
        self.lytHorButtons.addWidget(self.btnClearView)
        self.lytHorButtons.addWidget(self.btnPlot)
        self.lytHorButtons.addWidget(self.btnQuit)
        self.lytHorView.addWidget(self.view)
        #self.lytHorView.addWidget(self.slrContrast)
        self.lytVert.addLayout(self.lytHorView)
        self.lytVert.addWidget(self.slrBrightness)
        self.lytVert.addWidget(self.slrContrast)
        self.lytVert.addLayout(self.lytHorButtons)
        self.setLayout(self.lytVert)
        #SLOT's
        self.btnClearView.clicked.connect(self.handleClearView)
        self.btnLoad.clicked.connect(self.handleLoad)
        self.connect(self.btnQuit, QtCore.SIGNAL("clicked()"), QtGui.qApp.quit)
        self.connect(self.slrBrightness, QtCore.SIGNAL('valueChanged(int)'),
                     self.lcdBrightness, QtCore.SLOT('display(int)') )
        self.connect(self.slrBrightness, QtCore.SIGNAL('valueChanged(int)'),
                     self.updateBrightnessContrast)
        self.connect(self.slrContrast, QtCore.SIGNAL('valueChanged(int)'),
                     self.updateBrightnessContrast)
        #CONSTANT's
        self.coordinates=[]

    #FUNCTION's
    def handleClearView(self):
        self.view.scene.clear()
        self.view.lines=[]
        self.slrBrightness.setDisabled(True)
        self.slrContrast.setDisabled(True)
        #self.view.setSceneRect(0, 0, 0, 0)
    def handleLoad(self):
        if len(self.view.lines) > 0:
            self.view.scene.clear()
            self.view.lines = []
        else:
            self.view.scene.clear()
            
        self.fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/home/argentum/Python_work')
        print("Loaded file:")        
        print(self.fname)
        self.imgPath = str(self.fname)
        self.img=Image.open(self.imgPath) #Load image!!!     
        w, h = self.img.size
        self.imgQ = ImageQt.ImageQt(self.img)
        pixMap = QtGui.QPixmap.fromImage(self.imgQ)
        self.pixItem = QtGui.QGraphicsPixmapItem(pixMap)
        self.view.scene.addItem(self.pixItem)
        self.view.fitInView(QtCore.QRectF(0, 0, w, h), QtCore.Qt.KeepAspectRatio)
        self.view.scene.update()
        self.slrBrightness.setDisabled(False)
        self.slrContrast.setDisabled(False)
    
    def updateBrightnessContrast(self, evnt):
        if len(self.view.lines) > 0:
            self.coordinates=[]
            for i in range(len(self.view.lines)):
                l=self.view.lines[i]
                lF=l.line()
                curCoord=[lF.x1(), lF.y1(), lF.x2(), lF.y2()]           
                self.coordinates.append(curCoord)
            self.view.lines = []      
        sliderBrightnessValue = self.slrBrightness.value()
        sliderContrastValue = self.slrContrast.value()
        self.curBr=float(sliderBrightnessValue)/50.0
        self.curCt=float(sliderContrastValue)/50.0
#        print("Brightness: "),
#        print(self.curBr)
#        print("Contrast: "),
#        print(self.curCt)
        self.view.scene.clear()
        
        curImageStateBr=self.img
        enhancerBr = ImageEnhance.Brightness(curImageStateBr)
        curImageStateBr = enhancerBr.enhance(self.curBr)
        curImageStateCt = curImageStateBr
        enhancerCt = ImageEnhance.Contrast(curImageStateCt)
        curImageStateCt = enhancerCt.enhance(self.curCt)
        self.imgQ = ImageQt.ImageQt(curImageStateCt)
        pixMap = QtGui.QPixmap.fromImage(self.imgQ)
        self.pixItem = QtGui.QGraphicsPixmapItem(pixMap)
        self.view.scene.addItem(self.pixItem)
        self.view.scene.update()
        if len(self.coordinates) > 0:
            self.view.redrawLines(self.coordinates)        


class View(QtGui.QGraphicsView):
    def __init__(self, parent):
        QtGui.QGraphicsView.__init__(self, parent)
        self.scene=QtGui.QGraphicsScene(self)
        self.setScene(self.scene)
        self.lines = []

    def mousePressEvent(self, event):
        self._start = event.pos()

    def mouseReleaseEvent(self, event):
        start = QtCore.QPointF(self.mapToScene(self._start))
        end = QtCore.QPointF(self.mapToScene(event.pos()))
        curLine = QtGui.QGraphicsLineItem(QtCore.QLineF(start, end))
        self.scene.addItem(curLine)
        self.lines.append(curLine)
        print("Number of lines: "),
        print(len(self.lines))

    def redrawLines(self, coordinates):
        if len(coordinates) > 0:
            for i in range(len(coordinates)):
                curCoord=coordinates[i]
                x1, y1, x2, y2 = curCoord
                curLine=QtGui.QGraphicsLineItem(x1, y1, x2, y2)
                self.scene.addItem(curLine)
                self.lines.append(curLine)

        
if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.resize(700, 700)
    window.show()
    sys.exit(app.exec_())