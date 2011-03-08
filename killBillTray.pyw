import sys
import os
from PyQt4 import QtCore, QtGui
from resources import *

class Widget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        
        self._signalMapper = QtCore.QSignalMapper(self)
        self._trayIconMenu = QtGui.QMenu(self)

        actions_cfg = (
            {'Title': 'Restart Outlook',
             'Icon': ':/images/outlook.png',
             'Restart': True,
             'Exe': 'outlook.exe'},
            {'Title': 'Restart Explorer',
             'Icon': ':/images/file-manager.png',
             'Restart': True,
             'Exe': 'explorer.exe'},
            {'Title': 'Kill TGitCache',
             'Icon': ':/images/tgit.png',
             'Restart': False,
             'Exe': 'TGitCache.exe'},
            {'Title': 'Kill TSVNCache',
             'Icon': ':/images/tsvn.png',
             'Restart': False,
             'Exe': 'TSVNCache.exe'})

        self._restart = {}

        for act_cfg in actions_cfg:
            self._restart[act_cfg['Exe']] = self._init_action(act_cfg)

        self.connect(self._signalMapper, QtCore.SIGNAL('mapped(const QString &)'), self.kill)

        quitAction = QtGui.QAction('&Quit', self)
        quitAction.setIcon(QtGui.QIcon(':/images/exit.png'))
        self.connect(quitAction, QtCore.SIGNAL('triggered()'), app, QtCore.SLOT('quit()'))

        self._trayIconMenu.addSeparator()
        self._trayIconMenu.addAction(quitAction)

        trayIcon = QtGui.QSystemTrayIcon(self)
        trayIcon.setContextMenu(self._trayIconMenu)
        trayIcon.setToolTip('Kill Bill')
        trayIcon.setIcon(QtGui.QIcon(':/images/tray.png'))
        trayIcon.show()

    def _init_action(self, cfg):
        action = QtGui.QAction(cfg['Title'], self)
        action.setIcon(QtGui.QIcon(cfg['Icon']))
        self._signalMapper.setMapping(action, cfg['Exe'])
        self.connect(action, QtCore.SIGNAL('triggered()'), self._signalMapper, QtCore.SLOT('map()'))
        self._trayIconMenu.addAction(action)

        return cfg['Restart']

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
