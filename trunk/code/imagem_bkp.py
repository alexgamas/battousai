# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import battousaiUtil as util
import sys


'''
daniel_0001.png 3 1 3 49 55 1 3 49 55 1 3 49 55
daniel_0002.png 1 0 0 49 55

[filename] [# of objects] [[x y width height] [... 2nd object] ...]
[filename] [# of objects] [[x y width height] [... 2nd object] ...]
[filename] [# of objects] [[x y width height] [... 2nd object] ...]
'''
class Point():
    color = Qt.black
    x = 0
    y = 0
    
    def color(self): return self.color
    def x(self): return self.x
    def y(self): return self.y
    
    def __init__(self, x, y, color = Qt.black):
        self.x = x
        self.y = y
        self.color = color
        
class Square():
    
    FIELD = 0
    SELECTION = 1
    
    point_1 = Point(0, 0)
    point_2 = Point(0, 0)
    x1, x2, y1, y2, h, w = 0, 0, 0, 0, 0, 0
    color = Qt.black
    childs = []
    
    def addChild(self, square):
        self.childs.append(square)
        
    def type(self):
        if (len(self.childs) > 0):
            return self.FIELD
        else:
            return self.SELECTION
        
    def __init__(self, point_1, point_2, color = Qt.black):
        self.x1 = min(point_1.x, point_2.x)
        self.y1 = min(point_1.y, point_2.y)
        self.x2 = max(point_1.x, point_2.x)
        self.y2 = max(point_1.y, point_2.y)
        self.h  = self.y2 - self.y1
        self.w  = self.x2 - self.x1


class ImageDrawPanel(QGraphicsPixmapItem):
    fieldMarkModeEnabled = False
    fieldMark = None
    chieldFields = []
    
    def __init__(self, pixmap = None, parent = None, scene = None):
        self.p1 = None
        self.p2 = None
        
        super(ImageDrawPanel, self).__init__()
        self.x, self.y = -1, -1        

        self.pen = QPen(Qt.SolidLine)
        self.pen.setColor(Qt.blue)
        self.pen.setWidth(1)
    
    def togleFieldMarkMode(self):
        self.fieldMarkModeEnabled = not self.fieldMarkModeEnabled
        if self.fieldMarkModeEnabled:
            self.pen.setColor(Qt.red)
            print "Field Mark Mode [ ON  ]"
        else:
            self.pen.setColor(Qt.blue)
            print "Field Mark Mode [ OFF ]"
        self.update()
        
    def drawCross(self, painter, point):
        ''' melhorar a forma como gera a cruz 
            esta saindo da canvas quando perde o foco!
        '''
        painter.drawLine(point.x, point.y - 100, point.x, point.y + 100)
        painter.drawLine(point.x - 100, point.y, point.x + 100, point.y)
        
    
    def drawSquare(self, painter, square):
        painter.drawRect(square.x1, square.y1, square.w, square.h)
    
    def markPoint(self, x, y):
        if self.p1 == None:
            self.p1 = Point(x, y, self.pen.color())
        else:
            self.p2 = Point(x, y, self.pen.color())

    def paint(self, painter, option, widget = None):               
        painter.drawPixmap(0, 0, self.pixmap())                
        painter.setPen(self.pen)
        
        if self.x >= 0 and self.y >= 0:
            self.drawCross(painter, Point(self.x, self.y, Qt.yellow))
        
        if self.p1 != None:
            print "p1", self.p1
            self.drawCross(painter, self.p1)
            
        if self.p2 != None:
            print "p2", self.p2
            self.drawCross(painter, self.p2)
            
            
        
        if self.fieldMark != None:
            self.drawSquare(painter, self.fieldMark)
            self.p1 = None
            self.p2 = None

    def update(self, *args, **kwargs):
        if (self.fieldMarkModeEnabled):
            self.fieldMark = Square(self.p1, self.p2, self.pen.color())
        return QGraphicsPixmapItem.update(self, *args, **kwargs)
    
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
    _FILE_EXTENSIONS = ("bmp", "jpg", "png", "xpm")
    actualImagePos = 0
    
    
    def __init__(self):
        super(MainWindow, self).__init__()

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 800, 600)

        self.pixmaps = self.getImages()
        
        self.imagePanel = ImageDrawPanel(scene = self.scene)
        
        self.scene.addItem(self.imagePanel)
        self.view = QGraphicsView(self.scene)

        layout = QHBoxLayout()        
        layout.addWidget(self.view)
        self.widget = QWidget()
        self.widget.setLayout(layout)
        self.setCursor(Qt.CrossCursor)
        self.setCentralWidget(self.widget)
        self.setWindowTitle("Battousai")
        
        self.actualImagePos = 0
        self.setUpActualImage()
        
    
    def setUpActualImage(self):
        if (self.pixmaps != None):
            print "set-up img ... ", self.actualImagePos, " of ", len(self.pixmaps)
            self.imagePanel.setPixmap(self.pixmaps[self.actualImagePos])
            self.imagePanel.update()
        else:
            print "Nothing to set-up"
    
    def goToPrevImage(self):
        if (self.pixmaps != None):
            self.actualImagePos = self.actualImagePos - 1
            if self.actualImagePos < 0:
                self.actualImagePos = len(self.pixmaps) - 1
            self.setUpActualImage()
                
    def goToNextImage(self):
        if (self.pixmaps != None):
            self.actualImagePos = self.actualImagePos + 1 
            if self.actualImagePos >= len(self.pixmaps):
                self.actualImagePos = 0
            self.setUpActualImage()

    def goToFieldMarkMode(self):
        self.imagePanel.togleFieldMarkMode()
                  
    def keyPressEvent(self, event):
        key = event.key()
        
        if key == Qt.Key_A:
            self.goToPrevImage()
        elif key == Qt.Key_D:
            self.goToNextImage()
        elif key == Qt.Key_F:
            self.goToFieldMarkMode()
        
    
    def fileExtension(self, filename):
        return filename[filename.rfind("."):None][1:None]    
    
    def filterFiles(self, filenames, extensionFilter):
        filteredFiles = []
        for filename in filenames:
            if (self.fileExtension(filename) in extensionFilter):
                filteredFiles.append(filename)
        return filteredFiles
    
    def getImages(self):
        
        folder_name = QFileDialog.getExistingDirectory(self, "Selecione o diretório ...")
        files = self.filterFiles(util.listFiles(str(folder_name)), self._FILE_EXTENSIONS)
        
        if len(files) == 0:
            print u"A pasta selecionada não possui arquivos dos tipos: ", self._FILE_EXTENSIONS
            return None
        else:
            qtdImages = len(files)
            '''
            QProgressDialog(QWidget parent=None, Qt.WindowFlags flags=0)
            QProgressDialog(QString, QString, int, int, QWidget parent=None, Qt.WindowFlags flags=0)
            '''
            progressDialog =  QProgressDialog("Carregando imagens", "Cancelar", 0, qtdImages)
            progressDialog.setWindowModality(Qt.WindowModal)
            progressDialog.setCancelButton(None)
            progressDialog.setGeometry(100, 100, 400, 80)
            progressDialog.show()
            
            self.images = []
            idx = 0
            for fname in files:
                idx = idx + 1
                progressDialog.setValue(idx)
                self.images.append(QPixmap(fname))
            return self.images

if __name__ == "__main__":    
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.showMaximized()
    #mainWindow.show()
    sys.exit(app.exec_())
