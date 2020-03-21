from PyQt5 import QtCore, QtGui, QtWidgets
import difflib
import os
import sys

class MainUI():
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(497, 224)
        MainWindow.setMinimumSize(QtCore.QSize(497, 224))
        MainWindow.setMaximumSize(QtCore.QSize(497, 224))
        self.openfiledialog = QtWidgets.QFileDialog(MainWindow)
        self.pushButton = QtWidgets.QPushButton(MainWindow)
        self.pushButton.setGeometry(QtCore.QRect(80, 110, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.openFileNameDialog)
        self.pushButton_2 = QtWidgets.QPushButton(MainWindow)
        self.pushButton_2.setGeometry(QtCore.QRect(320, 110, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.openFileNameDialog2)
        self.pushButton_3 = QtWidgets.QPushButton(MainWindow)
        self.pushButton_3.setGeometry(QtCore.QRect(200, 170, 93, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.difference)
        self.lineEdit = QtWidgets.QLineEdit(MainWindow)
        self.lineEdit.setGeometry(QtCore.QRect(40, 70, 181, 22))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(MainWindow)
        self.lineEdit_2.setGeometry(QtCore.QRect(270, 70, 181, 22))
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "amdiff"))
        self.pushButton.setText(_translate("MainWindow", "Browse"))
        self.pushButton_2.setText(_translate("MainWindow", "Browse"))
        self.pushButton_3.setText(_translate("MainWindow", "Diff"))

    def openFileNameDialog(self):
        self.openfiledialog.setNameFilter("Any ascii file (*)");
        self.openfiledialog.setDirectory(os.path.dirname(os.path.realpath(__file__)))
        if self.openfiledialog.exec():
            actualfile = self.openfiledialog.selectedFiles();
        self.lineEdit.setText(actualfile[0])

    def openFileNameDialog2(self):
        self.openfiledialog.setNameFilter("Any ascii file (*)");
        self.openfiledialog.setDirectory(os.path.dirname(os.path.realpath(__file__)))
        if self.openfiledialog.exec():
            actualfile = self.openfiledialog.selectedFiles();
        self.lineEdit_2.setText(actualfile[0])

    def difflib_parser(self, a, b):
        difflib_matcher = difflib.SequenceMatcher(None, a, b)
        def process_tag(tag, i1, i2, j1, j2):
            if tag == 'replace':
                return '<span style="text-decoration:line-through;background-color:#ff94d0;">' + difflib_matcher.a[i1:i2] + '</span> -> <span style="background-color:#60f516;">' + difflib_matcher.b[j1:j2] + '</span>'
            if tag == 'delete':
                return '<span style="background-color:#ff94d0;">-' + difflib_matcher.a[i1:i2] + '</span>'
            if tag == 'equal':
                return difflib_matcher.a[i1:i2]
            if tag == 'insert':
                return '<span style="background-color:#60f516;">+' + difflib_matcher.b[j1:j2] + '</span>'
        return ''.join(process_tag(*t) for t in difflib_matcher.get_opcodes())

    def difference(self):
        global file1, diff

        file1 = self.lineEdit.text()
        file2 = self.lineEdit_2.text()
        path = os.path.dirname(os.path.realpath(__file__))
        diff = f"{path}/temp.txt"

        with open(file1, "r") as tmp_file1:
            o = tmp_file1.readlines()
        with open(file2, "r") as tmp_file2:
            d = tmp_file2.readlines()
        with open(diff, "w") as diff_file:
            for x in range(len(o)):
                diff_file.write(self.difflib_parser(o[x],d[x]))

        tmp_file1.close()
        tmp_file2.close()
        diff_file.close()
        Window.show()
        w.display_diff()

class DifferenceUI(MainUI):
    def __init__(self):
        super().__init__()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1497, 890)
        MainWindow.setMinimumSize(QtCore.QSize(1497, 890))
        MainWindow.setMaximumSize(QtCore.QSize(1497, 890))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setFamily("Trebuched MS")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setFont(font)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 731, 821))
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setFont(font)
        self.textEdit_2.setGeometry(QtCore.QRect(750, 10, 731, 821))
        self.textEdit_2.setObjectName("textEdit_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def display_diff(self):
        global file1, diff

        with open(file1, "r") as tmp_file1:
            o = tmp_file1.readlines()
            for x in range(len(o)):
                self.textEdit.append(o[x])
            self.textEdit_2.toHtml()
        tmp_file1.close()

        with open(diff, "r") as tmp_diff:
            d = tmp_diff.readlines()
            for x in range(len(d)):
                self.textEdit_2.append(d[x])
            self.textEdit_2.toHtml()
        tmp_diff.close()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Difference"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MainUI()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.retranslateUi(MainWindow)
    Window = QtWidgets.QMainWindow()
    w = DifferenceUI()
    w.setupUi(Window)
    w.retranslateUi(Window)
    sys.exit(app.exec_())
