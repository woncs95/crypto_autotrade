import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 200, 300, 200)
        self.setWindowTitle("AlgoCrypto")
        self.setWindowIcon(QIcon("../dev/icon.jpg"))

        btn = QPushButton("버튼1", self)
        btn.clicked.connect(self.btn_clicked)
        btn.move(10, 10)


    def btn_clicked(self):
        print("버튼 클릭")
        pass

app = QApplication(sys.argv)
window=MyWindow()

File = open("../dev/SpyBot.qss", "r")

with File:
    qss = File.read()
    app.setStyleSheet(qss)
        # setup stylesheet

window.show()
app.exec_()


