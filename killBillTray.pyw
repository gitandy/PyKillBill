import sys
import os
from PyQt4 import QtCore, QtGui
from resources import *

class Widget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        outlookAction = QtGui.QAction('Outlook', self)
        outlookAction.setIcon(QtGui.QIcon(':/images/outlook.png'))
        self.connect(outlookAction, QtCore.SIGNAL('triggered()'), self.__outlook)
            
        explorerAction = QtGui.QAction('Explorer', self)
        explorerAction.setIcon(QtGui.QIcon(':/images/file-manager.png'))
        self.connect(explorerAction, QtCore.SIGNAL('triggered()'), self.__explorer)

        tgitAction = QtGui.QAction('TGitCache', self)
        tgitAction.setIcon(QtGui.QIcon(':/images/tgit.png'))
        self.connect(tgitAction, QtCore.SIGNAL('triggered()'), self.__tgitcache)

        tsvnAction = QtGui.QAction('TSVNCache', self)
        tsvnAction.setIcon(QtGui.QIcon(':/images/tsvn.png'))
        self.connect(tsvnAction, QtCore.SIGNAL('triggered()'), self.__tsvncache)

        quitAction = QtGui.QAction('&Quit', self)
        quitAction.setIcon(QtGui.QIcon(':/images/exit.png'))
        self.connect(quitAction, QtCore.SIGNAL('triggered()'), app, QtCore.SLOT('quit()'))

        trayIconMenu = QtGui.QMenu(self)
        trayIconMenu.addAction(outlookAction)
        trayIconMenu.addAction(explorerAction)
        trayIconMenu.addSeparator()
        trayIconMenu.addAction(tgitAction)
        trayIconMenu.addAction(tsvnAction)
        trayIconMenu.addSeparator()
        trayIconMenu.addAction(quitAction)

        trayIcon = QtGui.QSystemTrayIcon(self)
        trayIcon.setContextMenu(trayIconMenu)
        trayIcon.setToolTip('Kill Bill')
        trayIcon.setIcon(QtGui.QIcon(':/images/tray.png'))
        trayIcon.show()

    def __outlook(self):
        self.kill('outlook.exe', True)

    def __explorer(self):
        self.kill('explorer.exe', True)

    def __tgitcache(self):
        self.kill('TGitCache.exe')

    def __tsvncache(self):
        self.kill('TSVNCache.exe')

    def kill(self, prog, restart=False):
        os.system('taskkill /f /im ' + prog)

        if restart:
            self.start(prog)

    def start(self, prog):
        os.system(prog)        

    def closeEvent(self, event):
        self.hide()
        event.ignore()


def main():
    global app
    app = QtGui.QApplication(sys.argv)
    w = Widget() 
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
