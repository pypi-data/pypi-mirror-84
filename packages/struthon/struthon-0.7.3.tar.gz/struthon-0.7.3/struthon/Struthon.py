'''
--------------------------------------------------------------------------
Copyright (C) 2015-2020 Lukasz Laba <lukaszlaba@gmail.com>

This file is part of Struthon.
Struthon free open source structural engineering design python applications.

Struthon is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

StruPy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Struthon; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
--------------------------------------------------------------------------

File changes:
- python3 compatibility checked
'''

import sys
import subprocess
import os
import time
import webbrowser

PATH = os.path.abspath(os.path.dirname(__file__))

PYTHON_ENGINE_PATH = sys.executable

from PyQt5 import QtWidgets

from mainwindow_ui import Ui_MainWindow

_appname = 'Struthon'
_version = '0.7.3'
_about = '''
-------------Licence-------------
Struthon is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

Struthon is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Foobar; if not, write to the Free Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA.

Copyright (C) 2015-2018 Lukasz Laba (e-mail : lukaszlab@o2.pl)
-------------Project info-------------
https://bitbucket.org/struthonteam/struthon
https://pypi.python.org/pypi/struthon
https://pypi.python.org/pypi/strupy
-------------Contact-------------
struthon@gmail.com
lukaszlab@o2.pl
'''

class MAINWINDOW(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #---Button clicked events
        self.ui.pushButton_SCMS.clicked.connect(self.run_SCMS)
        self.ui.pushButton_SCP.clicked.connect(self.run_SCP)
        self.ui.pushButton_SSSB.clicked.connect(self.run_SSSB)
        self.ui.pushButton_SSM.clicked.connect(self.run_SSM)
        self.ui.pushButton_SSBC.clicked.connect(self.run_SSBC)
        #---MenuBar events
        self.ui.actionAbout.triggered.connect(self.actionAbout)
        self.ui.actionProject_website.triggered.connect(self.actionWebsite)
    #----
    def run_SCMS(self):
        this_app_path = os.path.join(PATH, 'ConcreteMonoSection', 'ConcreteMonoSection.py')
        subprocess.Popen([PYTHON_ENGINE_PATH, this_app_path])

    def run_SCP(self):
        this_app_path = os.path.join(PATH, 'ConcretePanel', 'ConcretePanel.py')
        subprocess.Popen([PYTHON_ENGINE_PATH, this_app_path])

    def run_SSSB(self):
        this_app_path = os.path.join(PATH, 'SteelSectionBrowser', 'SteelSectionBrowser.py')
        subprocess.Popen([PYTHON_ENGINE_PATH, this_app_path])

    def run_SSM(self):
        this_app_path = os.path.join(PATH, 'SteelMember', 'SteelMember.py')
        subprocess.Popen([PYTHON_ENGINE_PATH, this_app_path])

    def run_SSBC(self):
        this_app_path = os.path.join(PATH, 'SteelBoltedConnection', 'SteelBoltedConnection.py')
        subprocess.Popen([PYTHON_ENGINE_PATH, this_app_path])

    #---
    def actionAbout(self):
        QtWidgets.QMessageBox.information(None, 'Info', _about)

    def actionWebsite(self):
        webbrowser.open('https://bitbucket.org/struthonteam/struthon')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MAINWINDOW()
    myapp.setWindowTitle(_appname + ' ' + _version)
    myapp.show()
    sys.exit(app.exec_())