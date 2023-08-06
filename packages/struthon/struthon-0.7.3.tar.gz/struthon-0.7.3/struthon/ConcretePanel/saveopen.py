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

import os
import shelve

from PyQt5 import QtWidgets

savedir = os.path.dirname(__file__)#dir path for save and open

def saveproject(panel, load, progress=None):
    #----filename to save tkinter dialog
    global savedir
    
    filename = QtWidgets.QFileDialog.getSaveFileName(   caption = 'Save project as',
                                                        directory = os.path.join(savedir,panel.PanelName + '_scpdata'),
                                                        filter = "StruthonConcretePanel data' (*.dat)")[0]
    filename = str(filename)
    filename = os.path.splitext(filename)[0]

    if not filename == '':
        savedir = os.path.dirname(filename)
    #----
    if progress:
        progress.setValue(50)
    #----shelve file open
    db = shelve.open(filename)
    db.clear()
    #----writing panel and load object data to shelve file
    db['rcsteelname'] = panel.rcsteelname
    db['concretename'] = panel.concretename
    db['PanelName'] = panel.PanelName
    db['surfaceID'] = panel.surfaceID
    db['h'] = panel.h
    db['coord_Xp'] = panel.coord_Xp
    db['coord_Yp'] = panel.coord_Yp
    db['coord_Zp'] = panel.coord_Zp
    db['ap'] = panel.ap
    db['an'] = panel.an
    db['fip'] = panel.fip
    db['fin'] = panel.fin
    db['rysAp'] = panel.rysAp
    db['rysAn'] = panel.rysAn
    db['wlimp'] = panel.wlimp
    db['wlimn'] = panel.wlimn
    db['Anscale'] = panel.Anscale
    db['Apscale'] = panel.Apscale
    db['loadcasecontainer'] = load.loadcasecontainer
    #----
    if progress:
        progress.setValue(80)
    #----shelve file close
    db.close()
    #----
    if progress:
        progress.setValue(0)

def openproject(panel, load, progress=None):
    #----filename to open tkinter dialog
    global savedir

    filename = QtWidgets.QFileDialog.getOpenFileName(   caption = 'Open scpdata file',
                                                        directory = savedir,
                                                        filter = "StruthonConcretePanel data' (*.dat)")[0]
    filename = os.path.splitext(filename)[0]
    filename = str(filename)    
    
    if not filename == '':
        savedir = os.path.dirname(filename)
    #----
    if progress:
        progress.setValue(20)
    #----shelve file open
    db = shelve.open(filename)
    #----claring obiect data
    panel.clear_arrays_data()
    load.clear_arrays_data()
    #----reading data from shelve file and writing to panel and load object
    panel.rcsteelname = db['rcsteelname']
    panel.concretename = db['concretename']
    panel.PanelName = db['PanelName']
    panel.surfaceID = db['surfaceID']
    panel.h = db['h']
    panel.coord_Xp = db['coord_Xp']
    panel.coord_Yp = db['coord_Yp']
    panel.coord_Zp = db['coord_Zp']
    panel.ap = db['ap']
    panel.an = db['an']
    panel.fip =db['fip']
    panel.fin = db['fin']
    panel.rysAp = db['rysAp']
    panel.rysAn = db['rysAn']
    panel.wlimp = db['wlimp']
    panel.wlimn = db['wlimn']
    panel.Anscale[:] = db['Anscale'][:]
    panel.Apscale[:] = db['Apscale'][:]
    load.loadcasecontainer = db['loadcasecontainer']
    #----
    if progress:
        progress.setValue(80)
    #----shelve file close
    db.close()
    #----
    panel.calculate_flatten_coordinates()
    load.set_activeloadcase(load.get_loadcasenamelist()[0])
    #----
    if progress:
        progress.setValue(0)