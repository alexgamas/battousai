# -*- coding: utf-8 -*-

'''
BEGIN OF PROGRAM
----------------------------------------------------------------------------
AUTHOR     : Alex Gamas
MAIN GOAL  : Open an Image file and display this!
VERSION    : 0.1.2
USAGE TIPS :
----------------------------------------------------------------------------

'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import battousaiUtil as util
import sys

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
        self.childs = []
        self.x1 = min(point_1.x, point_2.x)
        self.y1 = min(point_1.y, point_2.y)
        self.x2 = max(point_1.x, point_2.x)
        self.y2 = max(point_1.y, point_2.y)
        self.h  = self.y2 - self.y1
        self.w  = self.x2 - self.x1
        self.color = color


class ImageDrawPanel(QGraphicsPixmapItem):
    #fieldMarkModeEnabled = False
    fieldMark = None
    
    def __init__(self, pixmap = None, parent = None, scene = None):
        self.p1 = None
        self.p2 = None
        
        super(ImageDrawPanel, self).__init__()
        self.x, self.y = -1, -1        

        self.pen = self.createPen(Qt.blue)
        
    def createPen(self, color = Qt.black):
        pen = QPen(Qt.SolidLine)
        pen.setColor(color)
        pen.setWidth(1)
        return pen
    '''
    def togleFieldMarkMode(self):
        self.fieldMarkModeEnabled = not self.fieldMarkModeEnabled
        if self.fieldMarkModeEnabled:
            self.pen.setColor(Qt.red)
            print "Field Mark Mode [ ON  ]"
        else:
            self.pen.setColor(Qt.blue)
            print "Field Mark Mode [ OFF ]"
        self.update()
    '''    
    def drawCross(self, painter, point):
        ''' melhorar a forma como gera a cruz 
            esta saindo da canvas quando perde o foco!
        '''
        painter.setPen(self.createPen(point.color))
        painter.drawLine(point.x, point.y - 100, point.x, point.y + 100)
        painter.drawLine(point.x - 100, point.y, point.x + 100, point.y)
    
    def drawSquare(self, painter, square):
        painter.setPen(self.createPen(square.color))
        painter.drawRect(square.x1, square.y1, square.w, square.h)

    '''
    def markPoint(self, x, y):
        if self.p1 == None:
            self.p1 = Point(x, y, self.pen.color())
        else:
            self.p2 = Point(x, y, self.pen.color())
    '''
    def cleanTempMarks(self):
        self.x = -1
        self.y = -1
        self.p1 = None
        self.p2 = None
    
    def cleanAll(self):
        if self.fieldMark != None:
            self.fieldMark.childs = None 
        self.fieldMark = None
        self.cleanTempMarks()
    
    def paint(self, painter, option, widget = None):               
        painter.drawPixmap(0, 0, self.pixmap())
        #painter.setPen(self.pen)
        
        
        if self.fieldMark != None:
            self.drawSquare(painter, self.fieldMark)
            for child in self.fieldMark.childs:
                self.drawSquare(painter, child)    
        
        
        ''' DRAW TIME
        '''
        if self.p1 != None:
            self.drawCross(painter, self.p1)
            
        if self.p2 != None:
            ''' THIS IS NOT GOOD!
            '''
            point_1 = Point(self.p1.x, self.p1.y, self.pen.color())
            point_2 = Point(self.p2.x, self.p2.y, self.pen.color())
            square = Square(point_2, point_1, self.pen.color())
            
            if self.fieldMark == None:
                self.fieldMark = square
            else:
                self.fieldMark.addChild(square)
                
            
            ''' LIMPAR
            '''            
            self.cleanTempMarks()
            ''' LIMPAR
            '''
            
            self.update()
            
            #self.drawCross(painter, self.p2)
        else:
            if self.x >= 0 and self.y >= 0:
                ponto_2 = Point(self.x, self.y, self.pen.color())
                self.drawSquare(painter, Square(self.p1, ponto_2, self.pen.color()))
            
        '''DRAW TIME
        '''
        #if self.fieldMark != None:
        #    self.drawSquare(painter, self.fieldMark)
        #    self.p1 = None
        #    self.p2 = None

    #def update(self, *args, **kwargs):
    #    if (self.fieldMarkModeEnabled):
    #        self.fieldMark = Square(self.p1, self.p2, self.pen.color())
    #    return QGraphicsPixmapItem.update(self, *args, **kwargs)
    
    def mousePressEvent (self, event):
        x = event.pos().x()
        y = event.pos().y()
        self.p1 = Point(x, y, self.pen.color())
        self.update()
        
    def mouseReleaseEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        self.p2 = Point(x, y, self.pen.color())
        self.update()
    
    def mouseMoveEvent (self, event):
        self.x = event.pos().x()
        self.y = event.pos().y()
        self.update()

class MainWindow(QMainWindow):
    _FILE_EXTENSIONS = ("bmp", "jpg", "png", "xpm")
    actualImagePos = 0
    index = 0
    outputFolder = None
    vecFile = None
    
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
        self.imagePanel.cleanAll()
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
    
            
    '''
    [filename] [# of objects] [[x y width height] [... 2nd object] ...]
    '''

    def recordVecData(self, pixmap, field):
        mainImage = pixmap.copy(field.x1, field.y1, field.w, field.h)
        
        if self.outputFolder == None:
            self.outputFolder = self.chooseDirectory(u"Selecione o diretório de saida!")

        vecFileName = "{outputFolder}/imagem_vec.vec".format(outputFolder = self.outputFolder)
        if self.vecFile == None:
            self.vecFile = file(vecFileName, "w")
        
        fieldString = ""
        detectionQty = 0
        imageField = "{:1.0f} {:1.0f} {:1.0f} {:1.0f}"

        filename = "imagem_{index:04}.png".format(index = self.index)
        imageFullPath = "{outputFolder}/{fname}".format(outputFolder = self.outputFolder, fname = filename)
        mainImage.save(imageFullPath, format = "PNG", quality = 100);

        if len(field.childs) == 0:
            detectionQty = 1
            fieldString = imageField.format(0, 0, field.w, field.h)
            self.vecFile.write("./{} {} {}\n".format(filename, detectionQty, fieldString))
        else:
            detectionQty = len(field.childs)
            for child in field.childs:
                fieldString = fieldString + " " + imageField.format(child.x1 - field.x1, child.y1 - field.y1, child.w, child.h)
            self.vecFile.write("./{} {} {}\n".format(filename, detectionQty, fieldString.strip()))
            
        
        
        self.index = self.index + 1
    
    def keyPressEvent(self, event):
        key = event.key()
        
        if key == Qt.Key_A:
            self.goToPrevImage()
        elif key == Qt.Key_D:
            self.goToNextImage()
        elif key == Qt.Key_C:
            self.imagePanel.cleanAll()
            self.imagePanel.update()
        elif key == Qt.Key_R:
            pixmap = self.pixmaps[self.actualImagePos]
            self.recordVecData(pixmap, self.imagePanel.fieldMark)
        
    
    def fileExtension(self, filename):
        return filename[filename.rfind("."):None][1:None]    
    
    def filterFiles(self, filenames, extensionFilter):
        filteredFiles = []
        for filename in filenames:
            if (self.fileExtension(filename) in extensionFilter):
                filteredFiles.append(filename)
        return filteredFiles
    
    def chooseDirectory(self, title):
        return str(QFileDialog.getExistingDirectory(self, title))
    
    def getImages(self):
        
        folder_name = self.chooseDirectory(u"Selecione o diretório de entrada das imagens...")
        
        files = self.filterFiles(util.listFiles(folder_name), self._FILE_EXTENSIONS)
        
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
        
    def closeEvent(self, event):
        if (self.vecFile != None) and (not self.vecFile.closed):
            self.vecFile.close()
            
            
if __name__ == "__main__":    
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.showMaximized()
    #mainWindow.show()
    sys.exit(app.exec_())

'''END OF PROGRAM
'''