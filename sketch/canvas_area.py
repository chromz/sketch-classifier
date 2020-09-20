# Rodrigo Custodio

from PyQt5.QtWidgets import QGraphicsScene, QGraphicsLineItem
from PyQt5.QtGui import QColor, QPen, QBrush, QTransform, QImage, QPainter
from PyQt5.QtCore import Qt


class CanvasArea(QGraphicsScene):
    """
    Custom canvas widget to paint
    """
    def __init__(self, *args, **kwargs):
        super(CanvasArea, self).__init__(*args, **kwargs)
        # Hardcoded because reasons
        self.canvas_width = 560
        self.canvas_height = 560
        self.erasing = False
        self.transform = QTransform()
        self.grid_color = QColor(209, 209, 209)
        self.gridPen = QPen(self.grid_color)
        self.gridPen.setWidth(2)
        self.gridPen.setStyle(Qt.DotLine)
        self.defaultColor = QColor(0, 0, 0)
        self.defaultPen = QPen(self.defaultColor)
        self.defaultBrush = QBrush(self.defaultColor)

    def mousePressEvent(self, event):
        self.drawCoords(event.scenePos())

    def mouseMoveEvent(self, event):
        self.drawCoords(event.scenePos())

    def getImage(self):
        image = QImage(self.sceneRect().size().toSize(), QImage.Format_RGB888)
        image.fill(QColor(255, 255, 255))
        painter = QPainter(image)
        painter.setRenderHint(QPainter.Antialiasing)
        self.render(painter)
        return image

    def clearDraw(self):
        self.clear()
        # self.drawGrid()

    def toggleErase(self):
        self.erasing = not self.erasing

    def setColor(self, color):
        self.defaultPen.setColor(color)
        self.defaultBrush.setColor(color)

    def drawCoords(self, coords):
        if (not self.erasing):
            self.addEllipse(coords.x(), coords.y(), 10, 10, self.defaultPen,
                            self.defaultBrush)
        else:
            item = self.itemAt(coords, self.transform)
            if (item is None or type(item) == QGraphicsLineItem):
                return
            self.removeItem(item)
