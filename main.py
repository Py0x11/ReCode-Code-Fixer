from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QProgressBar, QLabel, QFrame, QHBoxLayout, QVBoxLayout
import time
from tkinter import *
from tkinter import messagebox
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.uic import loadUi
import sys
import os
import openai

n
try:
    key = open("API.txt", "r")
    openai.api_key = (key.read())
except FileNotFoundError:
    messagebox.showwarning(
        "API Key File Not Found", "API.txt Doesnt Exist")
    exit()
except openai.error.APIConnectionError:
    nb = messagebox.askretrycancel(
        "Server Down", "Either There is a Issue With the API or the Server is Down")
    if nb:
        pass
    if nb == False:
        exit()


class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('ReCode Code Error Fixer | Powered by OpenAI')
        self.setFixedSize(1100, 500)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.counter = 0
        self.n = 300  # total instance

        self.initUI()

        self.timer = QTimer()
        self.timer.timeout.connect(self.loading)
        self.timer.start(30)

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.frame = QFrame()
        layout.addWidget(self.frame)

        self.labelTitle = QLabel(self.frame)
        self.labelTitle.setObjectName('LabelTitle')

        # center labels
        self.labelTitle.resize(self.width() - 10, 150)
        self.labelTitle.move(0, 120)  # x, y
        self.labelTitle.setText('rECode')
        self.labelTitle.setAlignment(Qt.AlignCenter)

        self.labelDescription = QLabel(self.frame)
        self.labelDescription.resize(self.width() - 10, 50)
        self.labelDescription.move(0, self.labelTitle.height())
        self.labelDescription.setObjectName('LabelDesc')
        self.labelDescription.setAlignment(Qt.AlignCenter)

        self.progressBar = QProgressBar(self.frame)
        self.progressBar.resize(self.width() - 200 - 10, 50)
        self.progressBar.move(100, self.labelDescription.y() + 130)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setFormat('%p%')
        self.progressBar.setTextVisible(True)
        self.progressBar.setRange(0, self.n)
        self.progressBar.setValue(20)

        self.labelLoading = QLabel(self.frame)
        self.labelLoading.resize(self.width() - 10, 50)
        self.labelLoading.move(0, self.progressBar.y() + 70)
        self.labelLoading.setObjectName('LabelLoading')
        self.labelLoading.setAlignment(Qt.AlignCenter)
        self.labelLoading.setText('<strong>Starting Code AI</strong>')

    def loading(self):
        self.progressBar.setValue(self.counter)

        if self.counter == int(self.n * 0.3):
            self.labelLoading.setText(
                '<strong>Trained Models are Waking Up !!</strong>')
        elif self.counter == int(self.n * 0.6):
            self.labelLoading.setText(
                '<strong>Setting Up the Envoirment </strong>')
        elif self.counter >= self.n:
            self.timer.stop()
            self.close()

            time.sleep(1)

            self.myApp = MyApp()
            self.myApp.show()

        self.counter += 1


class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        loadUi("main.ui", self)
        self.current_path = None
        self.current_fontsize = 8
        self.setWindowTitle("Untitled")

        self.actionNew.triggered.connect(self.newFile)
        self.actionSave.triggered.connect(self.saveFile)
        self.actionSave_as.triggered.connect(self.saveFileAs)
        self.actionOpen.triggered.connect(self.openFile)
        self.actionUndo.triggered.connect(self.undo)
        self.actionRedo.triggered.connect(self.redo)
        self.actionCut.triggered.connect(self.cut)
        self.actionCopy.triggered.connect(self.copy)
        self.actionPaste.triggered.connect(self.paste)
        self.actionSet_Dark_Mode.triggered.connect(self.setDarkMode)
        self.actionSet_Light_Mode.triggered.connect(self.setLightMode)
        self.actionIncrease_Font_Size.triggered.connect(self.incFontSize)
        self.actionDecrease_Font_Size.triggered.connect(self.decFontSize)
        self.actionAbout_Creator.triggered.connect(self.about)
        self.ReviewCode.clicked.connect(self.Fix)

    def Fix(self):
        try:
            response = openai.Completion.create(
                model="code-davinci-002",
                prompt=f"##### Fix bugs in the below function\n \n### Buggy Python\n{self.textEdit.toPlainText()}\n### Fixed Python",
                temperature=0,
                max_tokens=182,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                stop=["###"]
            )
            resp = response["choices"][0]["text"]
            self.textEdit_2.setText(f" ### Fixed Code ### \n{resp}")
            if self.textEdit_2 == self.textEdit:
                elf.textEdit_2.setText(f"### No Problems Found ### \n{resp}")
            return resp
        except:
            openai.error

    def about(self):
        print("LOL")

    def newFile(self):
        self.textEdit.clear()
        self.setWindowTitle("Untitled")
        self.current_path = None

    def saveFile(self):
        if self.current_path is not None:
            # save the changes without opening dialog
            filetext = self.textEdit.toPlainText()
            with open(self.current_path, 'w') as f:
                f.write(filetext)
        else:
            self.saveFileAs()

    def saveFileAs(self):
        pathname = QFileDialog.getSaveFileName(
            self, 'Save file', 'D:\codefirst.io\PyQt5 Text Editor', 'Text files(*.txt)')
        filetext = self.textEdit.toPlainText()
        with open(pathname[0], 'w') as f:
            f.write(filetext)
        self.current_path = pathname[0]
        self.setWindowTitle(pathname[0])

    def openFile(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Open file', 'D:\codefirst.io\PyQt5 Text Editor', 'Text files (*.txt)')
        self.setWindowTitle(fname[0])
        with open(fname[0], 'r') as f:
            filetext = f.read()
            self.textEdit.setText(filetext)
        self.current_path = fname[0]

    def undo(self):
        self.textEdit.undo()

    def redo(self):
        self.textEdit.redo()

    def copy(self):
        self.textEdit.copy()

    def cut(self):
        self.textEdit.cut()

    def paste(self):
        self.textEdit.paste()

    def setDarkMode(self):
        self.setStyleSheet('''QWidget{
            background-color: rgb(33,33,33);
            color: #FFFFFF;
            }
            QTextEdit{
            background-color: rgb(46,46,46);
            }
            QMenuBar::item:selected{
            color: #000000
            } ''')

    def setLightMode(self):
        self.setStyleSheet("")

    def incFontSize(self):
        self.current_fontsize += 1
        self.textEdit.setFontPointSize(self.current_fontsize)

    def decFontSize(self):
        self.current_fontsize -= 1
        self.textEdit.setFontPointSize(self.current_fontsize)


if __name__ == '__main__':
    QApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = QApplication(sys.argv)
    app.setStyleSheet('''
        #LabelTitle {
            font-size: 60px;
            color: #93deed;
        }

        #LabelDesc {
            font-size: 30px;
            color: #c2ced1;
        }

        #LabelLoading {
            font-size: 30px;
            color: #e8e8eb;
        }

        QProgressBar {
            background-color: #ed134a;
            color: rgb(200, 200, 200);
            border-style: none;
            border-radius: 10px;
            text-align: center;
            font-size: 30px;
        }

        QProgressBar::chunk {
            border-radius: 10px;
            background-color: qlineargradient(spread:pad x1:0, x2:1, y1:0.511364, y2:0.523, stop:0 #00f4ff, stop:1 #f7ffff);
        }
    ''')

    splash = SplashScreen()
    splash.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
