import os
import sys
import ConfigParser
from PyQt4 import QtCore, QtGui
from resources import *

class Widget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        
        self._signalMapper = QtCore.QSignalMapper(self)
        self._trayIconMenu = QtGui.QMenu(self)

        self._restart = {}

        for act_cfg in self._read_config():
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

    def _read_config(self):
        actions_cfg = ()
        
        config = ConfigParser.RawConfigParser()
        config.read('KillBill.ini')
        actions = config.sections()

        for act in actions:
            if config.has_option(act, 'exe'):
                try:
                    act_cfg = {}
                    act_cfg['Title'] = act
                    act_cfg['Exe'] = config.get(act, 'exe')

                    if config.has_option(act, 'restart'):
                        act_cfg['Restart'] = config.getboolean(act, 'restart')
                    else:
                        act_cfg['Restart'] = False

                    if config.has_option(act, 'icon'):
                        act_cfg['Icon'] = config.get(act, 'icon')
                    else:
                        act_cfg['Icon'] = ':/images/default.png'

                    if config.has_option(act, 'priority'):
                        act_cfg['Priority'] = config.getint(act, 'priority')
                    else:
                        act_cfg['Priority'] = 10

                    actions_cfg += (act_cfg,)
                except Exception, e:
                    print e

        return sorted(actions_cfg, lambda x, y: cmp(x['Priority'], y['Priority']))

    def kill(self, prog):
        prog = str(prog)
        
        os.system('taskkill /f /im ' + prog)

        if self._restart[prog]:
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
