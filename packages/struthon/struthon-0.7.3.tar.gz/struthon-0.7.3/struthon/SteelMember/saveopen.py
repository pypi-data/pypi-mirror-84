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

def saveproject(element, load, progress=None):
    global savedir
    #----asking for filename with default as element.Mark

    filename = QtWidgets.QFileDialog.getSaveFileName(   caption = 'Save project as',
                                                    directory = os.path.join(savedir,element.Mark + '_ssmdata'),
                                                    filter = "StruthonSteelMember data' (*.dat)")[0]
                                                    
    filename = str(filename)
    filename = os.path.splitext(filename)[0]
    #----
    if not filename == '': savedir = os.path.dirname(filename)
    #----
    if progress:
        progress.setValue(50)
    #----shelve file open
    db = shelve.open(filename)
    db.clear()
    #----writing element data to shelve file
    db['Mark'] = element.Mark
    db['sectname'] = element.sectname
    db['steelgrade'] = element.steelgrade
    db['L'] = element.L
    db['k_ycr'] = element.k_ycr
    db['k_zcr'] = element.k_zcr
    db['k_LT'] = element.k_LT
    db['alpha_yk'] = element.alpha_yk
    db['alpha_zk'] = element.alpha_zk
    db['w_lim_ratio'] = element.w_lim_ratio
    db['comment'] = element.comment

    #----writing load data to shelve file
    db['Name'] = load.Name
    db['M_yEd'] = load.M_yEd
    db['M_zEd'] = load.M_zEd
    db['T_Ed'] = load.T_Ed
    db['N_Ed'] = load.N_Ed
    db['V_yEd'] = load.V_yEd
    db['V_zEd'] = load.V_zEd
    db['caseactiv'] = load.caseactiv
    db['stabilitycheck'] = load.stabilitycheck    
    db['deflectioncheck'] = load.deflectioncheck
    
    #----writing other data to shelve file
    db['gamma_F'] = load.gamma_F
    
    #----
    if progress:
        progress.setValue(80)
    #----shelve file close
    db.close()
    #----
    if progress:
        progress.setValue(0)
    
def openproject(element, load, progress=None):
    global savedir
    #----asking for filename
    filename = QtWidgets.QFileDialog.getOpenFileName(   caption = 'Open ssmdata file',
                                                    directory = savedir,
                                                    filter = "StruthonSteelMember data' (*.dat)")[0]

    filename = os.path.splitext(filename)[0]
    filename = str(filename)
    if not filename == '': savedir = os.path.dirname(filename)
    #----
    if progress:
        progress.setValue(20)
    #----shelve file open
    db = shelve.open(filename)
    #----claring load object data
    load.clear_loadcase()
    #----reading data from shelve file and writing to element object
    print(db)
    if 'Mark' in db: element.Mark = db['Mark']
    if 'sectname' in db: element.set_sectionfrombase(db['sectname'])
    if 'steelgrade' in db: element.set_steelgrade(db['steelgrade'])
    if 'L' in db: element.L = db['L'] 
    if 'k_ycr' in db: element.k_ycr = db['k_ycr']
    if 'k_zcr' in db: element.k_zcr = db['k_zcr'] 
    if 'k_LT' in db: element.k_LT = db['k_LT']
    
    if 'alpha_yk' in db: element.alpha_yk = db['alpha_yk']
    if 'alpha_zk' in db: element.alpha_zk = db['alpha_zk'] 
    if 'w_lim_ratio' in db: element.w_lim_ratio = db['w_lim_ratio'] 
    if 'comment' in db: element.comment = db['comment'] 

    #----reading data from shelve file and writing load object
    if 'Name' in db: load.Name = db['Name']
    if 'M_yEd' in db: load.M_yEd = db['M_yEd']
    if 'M_zEd' in db: load.M_zEd = db['M_zEd']
    if 'T_Ed' in db: load.T_Ed = db['T_Ed']
    if 'N_Ed' in db: load.N_Ed = db['N_Ed']
    if 'V_yEd' in db: load.V_yEd = db['V_yEd']
    if 'V_zEd' in db: load.V_zEd = db['V_zEd']
    if 'caseactiv' in db: load.caseactiv = db['caseactiv']
    if 'stabilitycheck' in db: load.stabilitycheck  = db['stabilitycheck']    
    if 'deflectioncheck' in db: load.deflectioncheck  = db['deflectioncheck']

    #reading data from shelve file and writing other data
    if 'gamma_F' in db: load.gamma_F  = db['gamma_F'] 
    
    #----
    if progress:
        progress.setValue(80)
    #----shelve file close
    db.close()
    #----
    if progress:
        progress.setValue(0)