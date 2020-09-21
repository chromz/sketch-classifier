# Rodrigo Custodio, 15220

from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtOpenGL import QGLWidget
from PyQt5.QtGui import qRed, qGreen, qBlue
from PyQt5.QtCore import pyqtSlot, Qt
from sketch.ui import Ui_MainWindow
from sketch.canvas_area import CanvasArea
from os.path import isfile, exists

import numpy as np
import tensorflow as tf
import joblib


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Main gui of canvas
    """
    MODEL_FILE = "sketcher.ckpt"
    CLASSES_FILE = "classes.joblib"
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setFixedSize(1000, 1000)
        self.area = CanvasArea()
        self.render_height = 28
        self.render_width = 28
        self.canvas.setScene(self.area)
        self.canvas.setViewport(QGLWidget())
        self.canvas.setFixedSize(self.area.canvas_width,
                                 self.area.canvas_height)
        canvas_dim = self.canvas.contentsRect()
        self.area.setSceneRect(0, 0, canvas_dim.width(), canvas_dim.height())
        self.eraseCheckBox.stateChanged.connect(self.onEraseCheckBox)

        if not exists(self.MODEL_FILE) or not isfile(self.CLASSES_FILE):
            print("No neural network found create one using train script")
            quit()

        self.model = tf.keras.models.load_model(self.MODEL_FILE)
        self.model.summary()
        self.classes = joblib.load(self.CLASSES_FILE)
        print(self.classes)

        self.identifyButton.clicked.connect(self.on_identify_click)
        self.clearButton.clicked.connect(self.on_clear_click)
        self.show()

    @pyqtSlot()
    def onEraseCheckBox(self):
        self.area.toggleErase()

    @pyqtSlot()
    def on_identify_click(self):
        render_mat = np.zeros((self.render_width * self.render_height, 1))
        # Rescale image
        image = self.area.getImage().scaled(28, 28, Qt.KeepAspectRatio)
        width = image.width()
        height = image.height()
        for y in range(height):
            for x in range(width):
                color = image.pixel(x, y)
                pixel = np.array([qRed(color), qGreen(color), qBlue(color)])
                pixel = 255 - pixel
                greyscale = round(0.2126 * pixel[0] + 0.7152 * pixel[1] +
                                  0.0722 * pixel[2]) / 255
                render_mat[y * self.render_width + x][0] = greyscale
        img = render_mat.reshape(1, 28, 28, 1)
        # Show result
        prediction = self.model.predict(img)
        pred_class = self.classes[np.argmax(prediction)]

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText(f"It's a {pred_class}!")
        msg.setWindowTitle("Prediction:")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


    @pyqtSlot()
    def on_clear_click(self):
        self.area.clearDraw()
