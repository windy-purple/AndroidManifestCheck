#author:windy_ll
import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import androidmanifestui
from maincode import checkcode
                
class MainAM(QMainWindow,androidmanifestui.Ui_MainWindow):

    code = None

    def __init__(self):
        QMainWindow.__init__(self)
        androidmanifestui.Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton_2.setEnabled(False)
        pix = QPixmap(str(os.path.join(sys.path[0])) + '\\img\\1.png')
        self.label_7.setPixmap(pix)
        self.label_8.setPixmap(pix)
        self.label_9.setPixmap(pix)
        self.label_10.setPixmap(pix)
        self.label_11.setPixmap(pix)
        self.pushButton.clicked.connect(self.checkstart)
        self.pushButton_2.clicked.connect(self.correctionstart)

    def checkstart(self):
        fn = QFileDialog.getOpenFileName(self,'选择AndroidManifest.xml文件','/','XML(*.xml)')
        self.textBrowser.setText(str(fn[0]))
        self.code = checkcode(str(fn[0]))
        self.code.check()
        self.updateimg()
        if self.code.flag == 0:
            self.pushButton_2.setEnabled(True)

    def correctionstart(self):
        self.code.correction()
        self.code.check()
        sys.exit(0)

    def updateimg(self):
        pixt = QPixmap(str(os.path.join(sys.path[0])) + '\\img\\2.png')
        pixf = QPixmap(str(os.path.join(sys.path[0])) + '\\img\\3.png')
        if self.code.checkresult['headermagic'] == 1:
            self.label_7.setPixmap(pixt)
        else:
            self.label_7.setPixmap(pixf)
        if self.code.checkresult['stringchunktype'] == 1:
            self.label_8.setPixmap(pixt)
        else:
            self.label_8.setPixmap(pixf)
        if self.code.checkresult['resourcechunktype'] == 1:
            self.label_9.setPixmap(pixt)
        else:
            self.label_9.setPixmap(pixf)
        if self.code.checkresult['startnamespacechunktype'] == 1:
            self.label_10.setPixmap(pixt)
        else:
            self.label_10.setPixmap(pixf)
        if self.code.checkresult['starttagtype'] == 1:
            self.label_11.setPixmap(pixt)
        else:
            self.label_11.setPixmap(pixf)
        
        
if __name__=='__main__':
    app = QApplication(sys.argv)
    md = MainAM()
    md.show()
    sys.exit(app.exec_())