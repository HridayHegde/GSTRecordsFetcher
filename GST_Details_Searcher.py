from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QTableView, QFileDialog, QMessageBox
from PyQt5.QtCore import QAbstractTableModel, Qt


from copy import deepcopy
import os

import apiInterface


global filepath
filepath = None

class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.instructions = QtWidgets.QPushButton(self.centralwidget)
        self.instructions.setGeometry(QtCore.QRect(730, 490, 41, 41))
        self.instructions.setObjectName("instructions")
        self.headlabel = QtWidgets.QLabel(self.centralwidget)
        self.headlabel.setGeometry(QtCore.QRect(140, 30, 521, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.headlabel.setFont(font)
        self.headlabel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.headlabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.headlabel.setLineWidth(1)
        self.headlabel.setMidLineWidth(0)
        self.headlabel.setAlignment(QtCore.Qt.AlignCenter)
        self.headlabel.setObjectName("headlabel")
        self.BrowseText = QtWidgets.QLineEdit(self.centralwidget)
        self.BrowseText.setGeometry(QtCore.QRect(290, 120, 331, 31))
        self.BrowseText.setObjectName("BrowseText")
        self.Browse = QtWidgets.QPushButton(self.centralwidget)
        self.Browse.setGeometry(QtCore.QRect(170, 120, 93, 31))
        self.Browse.setObjectName("Browse")
       
        self.getgstdetails = QtWidgets.QPushButton(self.centralwidget)
        self.getgstdetails.setGeometry(QtCore.QRect(340, 440, 131, 41))
        self.getgstdetails.setObjectName("getgstdetails")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(199, 180, 411, 251))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 409, 249))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.tableView = QtWidgets.QTableView(self.scrollAreaWidgetContents)
        self.tableView.setGeometry(QtCore.QRect(0, 0, 411, 251))
        self.tableView.setObjectName("tableView")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.Browse.clicked.connect(lambda: browsefile(self.BrowseText,self.tableView))
        self.instructions.clicked.connect(lambda: showinstructions(self.instructions))
        self.getgstdetails.clicked.connect(lambda: startsearch(self.getgstdetails))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.instructions.setText(_translate("MainWindow", "?"))
        self.headlabel.setText(_translate("MainWindow", "GST Details Searcher"))
        self.Browse.setText(_translate("MainWindow", "Browse"))
        self.getgstdetails.setText(_translate("MainWindow", "Get GST Details"))

def browsefile(BrowseText,tableView):
    global filepath
    temppathlist = QFileDialog.getOpenFileName(BrowseText.parent(), 'OpenFile')
    filepath = temppathlist[0]
    BrowseText.setText(filepath)
    try:
        df = pd.read_excel(filepath)
        model = pandasModel(df)
        tableView.setModel(model)

    except OSError as e:
        print(e)
        #browsefile(BrowseText,tableView)

def startsearch(self):
    global filepath
    
    if filepath==None:
        q = QMessageBox()
        q.setIcon(QMessageBox.Information)
        q.about(self,'Error', 'File not selected')
   
    else:
        df = pd.read_excel(filepath)
        rowlist = []
        for index,rows in df.iterrows():
            rowlist.append([rows[0],rows[1].replace(u'\xa0', u' ')])
        print(rowlist)
        status,message = apiInterface.getgstdata(rowlist)
        if status:
            #if not df == None:
                #showtableview(self,df)
            os.system(f'start {os.path.realpath("./Output")}')
        else:
            q = QMessageBox()
            q.setIcon(QMessageBox.Critical)
            q.about(self,'Error', message)

def showtableview(self,df):
    tabviewnew = QTableView(self)
    modelinternal = pandasModel(df)
    tabviewnew.setModel(modelinternal)


def showinstructions(self):
    x = QMessageBox()
    x.setIcon(QMessageBox.Information)
    x.about(self,'Instructions', '1. Use Template to create an excel file\n2. Delete the sample data given in the template\n3. Save the template as new file and browse to it using the below button\n4. Press Start Searcing to generate search data and wait till it completes\n5. After Completing Search the folder with the file will open automatically.\n6. You can find the output in the "Output" folder of the application, they are labled with date and time of generation.')
   

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
