import os
import os.path
import sys
import ConfigParser
from PyQt4 import QtCore, QtGui
from resources import *

__version__ = '0.1'
__author_name__ = 'Andreas Schawo'
__author_email__ = 'andreas@schawo.de'
__copyright__ = 'Copyright (c) 2011-2012, Andreas Schawo, All rights reserved'
__license__ = '''Copyright (c) 2011-2012, Andreas Schawo <andreas@schawo.de>

All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

   1. Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.
   2. Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.
   3. Neither the name of the authors nor the names of its contributors may
      be used to endorse or promote products derived from this software without
      specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHORS 'AS IS' AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.'''


class Widget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        
        self._signalMapper = QtCore.QSignalMapper(self)
        self._trayIconMenu = QtGui.QMenu(self)

        self._restart = {}

        self._action_cfg = self._read_config()
        for act_cfg in self._action_cfg:
            self._restart[act_cfg['Exe']] = self._init_action(act_cfg)
            
        self.connect(self._signalMapper, QtCore.SIGNAL('mapped(const QString &)'), self.kill)

        aboutAction = QtGui.QAction('&About', self)
        aboutAction.setIcon(QtGui.QIcon(':/images/info.png'))
        self.connect(aboutAction, QtCore.SIGNAL('triggered()'), self.showAbout)

        quitAction = QtGui.QAction('&Quit', self)
        quitAction.setIcon(QtGui.QIcon(':/images/exit.png'))
        self.connect(quitAction, QtCore.SIGNAL('triggered()'), app, QtCore.SLOT('quit()'))

        self._trayIconMenu.addSeparator()
        self._trayIconMenu.addAction(aboutAction)
        self._trayIconMenu.addAction(quitAction)

        self._trayIcon = QtGui.QSystemTrayIcon(self)
        self._trayIcon.setContextMenu(self._trayIconMenu)
        self._trayIcon.setToolTip('Kill Bill')
        self._trayIcon.setIcon(QtGui.QIcon(':/images/tray.png'))
        self._trayIcon.show()

    def _init_action(self, cfg):
        action = QtGui.QAction(cfg['Title'], self)
        action.setIcon(QtGui.QIcon(cfg['Icon']))
        self._signalMapper.setMapping(action, cfg['Exe'])
        self.connect(action, QtCore.SIGNAL('triggered()'), self._signalMapper, QtCore.SLOT('map()'))
        self._trayIconMenu.addAction(action)

        return {'Restart': cfg['Restart'],
                'RestartProg': os.path.join(cfg['Path'], cfg['Exe']),
                'RestartParameter': cfg['Parameter']}

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

                    if config.has_option(act, 'path'):
                        act_cfg['Path'] = config.get(act, 'path')
                    else:
                        act_cfg['Path'] = ''

                    if config.has_option(act, 'parameter'):
                        act_cfg['Parameter'] = config.get(act, 'parameter')
                    else:
                        act_cfg['Parameter'] = ''

                    actions_cfg += (act_cfg,)
                except Exception, e:
                    print e

        return sorted(actions_cfg, lambda x, y: cmp(x['Priority'], y['Priority']))

    def kill(self, prog):
        prog = str(prog)
        
        os.system('taskkill /f /im ' + prog)

        if self._restart[prog]['Restart']:
            args = [prog] + self._restart[prog]['RestartParameter'].split()

            os.spawnv(os.P_NOWAIT, self._restart[prog]['RestartProg'], args)        

    def showAbout(self):
        self._trayIcon.showMessage(self.tr("About"), __copyright__ + "\n\n" + self.tr("Kill Bill") + "\n" + self.tr("Version") + ": " + __version__)


def main():
    global app
    app = QtGui.QApplication(sys.argv)
    w = Widget() 
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
