# ------------------------------------------------------
# ---------------------- main.py -----------------------
# ------------------------------------------------------
import append_run_path
import mplwidget

from PyQt5.QtWidgets import*
# from PyQt5.uic import loadUi # for dev version
import qt_designer # for dist version
from PyQt5 import QtGui
from PyQt5 import QtCore

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

import numpy as np
import random

import cv2

# class MatplotlibWidget(QMainWindow): # for dev version
class MatplotlibWidget(qt_designer.Ui_MainWindow, QMainWindow): # for dist version
    
    def __init__(self):
        
        QMainWindow.__init__(self)
        
        # loadUi("qt_designer.ui",self) # for dev version
        self.setupUi(self) # for dist version

        self.setWindowTitle("PyQt5 & Matplotlib Example GUI")

        self.pushButton_generate_random_signal.clicked.connect(self.update_graph)

        self.pushButton_open_file.clicked.connect(self.open_img)

        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))


        rgb_color=(255, 255, 255)
        height, width = self.cv2label.width(), self.cv2label.height()
        cvimg = np.zeros((height, width, 3), np.uint8)
        color = tuple(reversed(rgb_color))
        cvimg[:] = color
        height, width = self.cv2label.height(), self.cv2label.width()
        pixmap = cv2pixmap(cvimg, width, height)
        self.cv2label.setPixmap(pixmap)

    def update_graph(self):

        fs = 500
        f = random.randint(1, 100)
        ts = 1/fs
        length_of_signal = 100
        t = np.linspace(0,1,length_of_signal)
        
        cosinus_signal = np.cos(2*np.pi*f*t)
        sinus_signal = np.sin(2*np.pi*f*t)

        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(t, cosinus_signal)
        self.MplWidget.canvas.axes.plot(t, sinus_signal)
        self.MplWidget.canvas.axes.legend(('cosinus', 'sinus'),loc='upper right')
        self.MplWidget.canvas.axes.set_title('Cosinus - Sinus Signal')
        self.MplWidget.canvas.draw()

    def open_img(self):
        fname = QFileDialog.getOpenFileName(self)
        cvimg = cv2.imread(fname[0])
        height, width = self.cv2label.height(), self.cv2label.width()
        pixmap = cv2pixmap(cvimg, width, height)
        self.cv2label.setPixmap(pixmap)

def cv2pixmap(cvimg, width, height):
    
    cvimg = cv2.resize(cvimg, 
                        dsize=(width, height), 
                        interpolation=cv2.INTER_AREA)
    
    height, width, channel = cvimg.shape
    bytesPerLine = 3 * width
    qtimg = QtGui.QImage(cvimg.data, 
                        width, 
                        height, 
                        bytesPerLine, 
                        QtGui.QImage.Format_RGB888).rgbSwapped()

    pixmap = QtGui.QPixmap.fromImage(qtimg)
    return pixmap


if __name__ == "__main__":
    app = QApplication([])
    window = MatplotlibWidget()
    window.show()
    app.exec_()