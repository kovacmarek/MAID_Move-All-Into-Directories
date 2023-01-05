from PyQt5 import QtCore, QtGui, QtWidgets
import SortFiles
from PySide2.QtWidgets import QFileDialog


files = None

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(340, 360)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:\\SSD\\SortFiles\\maid_icon.ico"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)      
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.executeButton = QtWidgets.QPushButton(self.centralwidget)
        self.executeButton.setGeometry(QtCore.QRect(224, 200, 81, 23))
        self.executeButton.setObjectName("executeButton")
        self.undoButton = QtWidgets.QPushButton(self.centralwidget)
        self.undoButton.setGeometry(QtCore.QRect(224, 240, 81, 23))
        self.undoButton.setObjectName("undoButton")
        self.cancelButton = QtWidgets.QPushButton(self.centralwidget)
        self.cancelButton.setGeometry(QtCore.QRect(224, 280, 81, 23))
        self.cancelButton.setObjectName("cancelButton")
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(20, 80, 161, 221))
        self.listView.setObjectName("listView")
        self.refreshButton = QtWidgets.QPushButton(self.centralwidget)
        self.refreshButton.setGeometry(QtCore.QRect(200, 80, 121, 51))
        self.refreshButton.setObjectName("refreshButton")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 40, 201, 21))
        self.lineEdit.setDragEnabled(False)
        self.lineEdit.setObjectName("lineEdit")
        self.browseButton = QtWidgets.QPushButton(self.centralwidget)
        self.browseButton.setGeometry(QtCore.QRect(240, 40, 81, 23))
        self.browseButton.setObjectName("browseButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 131, 16))
        self.label.setObjectName("label")
        self.outputLog = QtWidgets.QLabel(self.centralwidget)
        self.outputLog.setGeometry(QtCore.QRect(10, 320, 311, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.outputLog.setFont(font)
        self.outputLog.setAutoFillBackground(False)
        self.outputLog.setLineWidth(1)
        self.outputLog.setAlignment(QtCore.Qt.AlignCenter)
        self.outputLog.setWordWrap(False)
        self.outputLog.setObjectName("outputLog")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 340, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        model = QtGui.QStandardItemModel()

        def browse():
            self.lineEdit.setText(QFileDialog.getExistingDirectory(None, "choose folder",))

        def createListItem(n):
            item = QtGui.QStandardItem(n["name"])
            model.appendRow(item) 
            return n["name"]   

        def handleRefresh():
            global files
            files = None
            try:
                if(self.lineEdit.text() == ""):
                    self.outputLog.setText("You need to set the path first!")
                else:
                    # Delete list before creation
                    model.removeRows( 0, model.rowCount() )

                    # Create listview models
                    files = SortFiles.fetchFileTypes(self.lineEdit.text())
                    x = list(map(createListItem, files))
                    self.listView.setModel(model)
                    self.outputLog.setText("Refreshed!")
            except:
                if(self.lineEdit.text() == ""):
                    self.outputLog.setText("You need to set the path first!")
                else:
                    self.outputLog.setText("There are no files in this folder!")

        def handleExecute():
            global files
            try:
                if(files == None):
                    self.outputLog.setText("There are no files in this folder!") 
                else:
                    SortFiles.createFolders(self.lineEdit.text(), files)
                    SortFiles.moveFilesToFolders(self.lineEdit.text(), files)
                    self.outputLog.setText("Files successfuly sorted into folders!")
            except:
                if(self.lineEdit.text() == ""):
                    self.outputLog.setText("You need to set the path first!")
                else:
                    self.outputLog.setText("Error!")

        def handleUndo():
            global files
            try:
                SortFiles.moveFilesUndo(self.lineEdit.text(), files)
                self.outputLog.setText("Files moved to their original location!")
            except:
                if(self.lineEdit.text() == ""):
                    self.outputLog.setText("You need to set the path first!")
                else:
                    self.outputLog.setText("You've already moved all of them!") 

        self.browseButton.clicked.connect(browse)
        self.refreshButton.clicked.connect(handleRefresh)
        self.executeButton.clicked.connect(handleExecute)
        self.undoButton.clicked.connect(handleUndo)  
        self.cancelButton.clicked.connect(lambda: quit())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MAID"))
        self.executeButton.setText(_translate("MainWindow", "Execute"))
        self.undoButton.setText(_translate("MainWindow", "Undo"))
        self.cancelButton.setText(_translate("MainWindow", "Cancel"))
        self.refreshButton.setText(_translate("MainWindow", "Refresh"))
        self.browseButton.setText(_translate("MainWindow", "Browse"))
        self.label.setText(_translate("MainWindow", "Select folder to organize"))
        self.outputLog.setText(_translate("MainWindow", ""))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())



