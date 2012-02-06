# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
#import PyQt4
import battousaiUtil as util
import sys

class ImageDrawPanel(QGraphicsPixmapItem):
    def __init__(self, pixmap=None, parent=None, scene=None):
        
       
        self.p1 = None
        self.p2 = None
        
        super(ImageDrawPanel, self).__init__()
        self.x, self.y = -1, -1        
        self.radius = 10

        self.pen = QPen(Qt.SolidLine)
        self.pen.setColor(Qt.blue)
        self.pen.setWidth(1)
        
        #self.brush = QBrush(Qt.yellow)
    
    def drawCross(self, painter, x, y):
        painter.drawLine(self.x, self.y - 100, self.x, self.y + 100)
        painter.drawLine(self.x - 100, self.y, self.x + 100, self.y)
    
    def markPoint(self, x, y):
        if self.p1 == None:
            self.p1 = (x, y)
        else:
            self.p2 = (x, y)

    def paint(self, painter, option, widget = None):               
        painter.drawPixmap(0, 0, self.pixmap())                
        painter.setPen(self.pen)
        #painter.setBrush(self.brush)
        
        if self.p1 != None:
            pass   
        
        if self.x >= 0 and self.y >= 0:
            self.drawCross(painter, self.x, self.y)

    def mousePressEvent (self, event):
        print 'mouse pressed'
        self.x = event.pos().x()
        self.y = event.pos().y()            
        self.update()
        
    def mouseReleaseEvent(self, event):
        print 'mouse released'
        self.x = event.pos().x()
        self.y = event.pos().y()
        self.markPoint(self.x, self.y)
        
        self.update()
    
    def mouseMoveEvent (self, event):
        print 'mouse moving'
        self.x = event.pos().x()
        self.y = event.pos().y()            
        self.update()        

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 800, 600)

        pixmap=self.openImage()        
        self.imagePanel = ImageDrawPanel(scene = self.scene)
        self.imagePanel.setPixmap(pixmap)
        self.scene.addItem(self.imagePanel)

        self.view = QGraphicsView(self.scene)

        layout = QHBoxLayout()        
        layout.addWidget(self.view)

        self.widget = QWidget()
        self.widget.setLayout(layout)
        
        self.setCursor(Qt.CrossCursor)
        
        self.setCentralWidget(self.widget)
        self.setWindowTitle("Battousai")

    def keyPressEvent(self, *args, **kwargs):
        
        return QMainWindow.keyPressEvent(self, *args, **kwargs)
    
    def openImage(self):
        
        folder_name = QFileDialog.getExistingDirectory(self, "Selecione o diretório ...")
        
        self.files = util.listFiles(str(folder_name))
        
        fname = QFileDialog.getOpenFileName(self, "Abrir Imagem... ", ".", "Image Files (*.bmp *.jpg *.png *.xpm)")
        if fname.isEmpty(): return None
        return QPixmap(fname)        


if __name__ == "__main__":    
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
