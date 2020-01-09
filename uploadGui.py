import sys, os
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

import requests  
import json

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Upload tasks'
        self.left = 10
        self.top = 10
        self.width = 500
        self.height = 140
        self.initUI()
        self.tasks = {}

        tokenFile = open("token.txt", "r")
        self.token = tokenFile.readline().strip('\n')
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(200, 58)
        self.textbox.resize(280,20)
        
        # Create a button in the window
        self.buttonSet = QPushButton('Upload set of tasks', self)
        self.buttonSet.move(20,15)
        self.buttonSet.resize(150, 45)

        self.buttonSingle = QPushButton('Upload single task', self)
        self.buttonSingle.move(20,75)
        self.buttonSingle.resize(150, 45)

        # connect button to function on_click
        self.buttonSet.clicked.connect(self.upload_set_on_click)
        self.buttonSingle.clicked.connect(self.upload_single_on_click)
        self.show()
    
    @pyqtSlot()
    def upload_set_on_click(self):
        folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        QMessageBox.question(self, 'Message - pythonspot.com', folder, QMessageBox.Ok, QMessageBox.Ok)
        tasks = os.listdir(folder)
        tasks.remove(".DS_Store")
        for task in tasks:
            print(task)
            self.addTask(folder, task)
        self.textbox.setText(folder)

    def upload_single_on_click(self):
        folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        pos = folder.rfind("/")
        #print("pos: ", pos, " len: ", len(folder))
        task = folder[pos+1:len(folder)]
        self.addTask(folder[:pos], task)

    def addTask(self, folder, task):
        print(folder, " ", task)

        if task in self.tasks:
            print(task, " task has already been uploaded")
        else:
            boolGroups = os.listdir(folder+"/"+task)
            boolGroups.remove(".DS_Store")
            features = {"folder":folder}
            for group in boolGroups:
                features[group] = []

            self.tasks[task] = features
            for group in boolGroups:
                self.addImages(folder, task, group)
        #print(self.tasks)

    
    def addImages(self,folder,task, group):
        dataFolder = os.path.join(folder, task, group)
        images = os.listdir(dataFolder)
        url = "http://127.0.0.1:8000/practice"
        for image in images:
            self.tasks[task][group].append(image)
            data = {'category':task, 'in_category':group, 'token':self.token}
            f = open(os.path.join(dataFolder,image), 'rb')
            files = {
                    'photo': f,
                    #'Content-Type': 'image/jpeg' # commenting out did nothing
                }
            r=requests.post(url, data=data , files=files)
            got_response = r.text
            print(got_response)
            print(r.status_code)

    def testDirPrint(self, folder):
        for dirpath, dirnames, filenames in os.walk(folder):
            print(dirpath)
            print(dirnames)
            print(filenames)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())