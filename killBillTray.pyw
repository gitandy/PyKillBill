import sys
import os
from PyQt4 import QtCore, QtGui
from resources import *

class Widget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        
        signalMapper = QtCore.QSignalMapper(self)

        self._restart = {}

        outlookAction = QtGui.QAction('Outlook', self)
        outlookAction.setIcon(QtGui.QIcon(':/images/outlook.png'))
        self._restart['outlook.exe'] = True
        signalMapper.setMapping(outlookAction, 'outlook.exe')
        self.connect(outlookAction, QtCore.SIGNAL('triggered()'), signalMapper, QtCore.SLOT('map()'))
    
        explorerAction = QtGui.QAction('Explorer', self)
        explorerAction.setIcon(QtGui.QIcon(':/images/file-manager.png'))
        self._restart['explorer.exe'] = True
        signalMapper.setMapping(explorerAction, 'explorer.exe')
        self.connect(explorerAction, QtCore.SIGNAL('triggered()'), signalMapper, QtCore.SLOT('map()'))

        tgitAction = QtGui.QAction('TGitCache', self)
        tgitAction.setIcon(QtGui.QIcon(':/images/tgit.png'))
        self._restart['TGitCache.exe'] = False
        signalMapper.setMapping(tgitAction, 'TGitCache.exe')
        self.connect(tgitAction, QtCore.SIGNAL('triggered()'), signalMapper, QtCore.SLOT('map()'))

        tsvnAction = QtGui.QAction('TSVNCache', self)
        tsvnAction.setIcon(QtGui.QIcon(':/images/tsvn.png'))
        self._restart['TSVNCache.exe'] = False
        signalMapper.setMapping(tsvnAction, 'TSVNCache.exe')
        self.connect(tsvnAction, QtCore.SIGNAL('triggered()'), signalMapper, QtCore.SLOT('map()'))

        quitAction = QtGui.QAction('&Quit', self)
        quitAction.setIcon(QtGui.QIcon(':/images/exit.png'))
        self.connect(quitAction, QtCore.SIGNAL('triggered()'), app, QtCore.SLOT('quit()'))

        self.connect(signalMapper, QtCore.SIGNAL('mapped(const QString &)'), self.kill)

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

    def kill(self, prog):
        prog = str(prog)
        
        os.system('taskkill /f /im ' + prog)

        if self._restart[prog]:
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
