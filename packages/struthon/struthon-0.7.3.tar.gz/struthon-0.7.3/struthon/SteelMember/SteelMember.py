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
from __future__ import division

import sys
import time
import copy

from PyQt5 import QtCore, QtGui, QtWidgets

import strupy.units as u
from strupy.steel.SteelElement import SteelElement
from strupy.steel. SteelElementSolver import SteelElementSolver
from strupy.steel.SteelElementLoad import SteelElementLoad
from strupy.x_graphic.PyqtSceneCreator2D import PyqtSceneCreator2D

from mainwindow_ui import Ui_MainWindow
import infotext
import reports
import saveopen
import paramvalues

u.xvalueformat("%5.2f")

class MAINWINDOW(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # QT events
        self.ui.pushButton_calculate.clicked.connect(self.pushButton_calculate)
        self.ui.pushButton_BrowseSection.clicked.connect(self.pushButton_BrowseSection)
        #---------
        self.ui.pushButton_FindSections.clicked.connect(self.pushButton_FindSections)
        self.ui.listWidget_typelist.clicked.connect(self.typeselected)
        self.ui.listWidget_sectnamelist.clicked.connect(self.sectnameselected)
        self.ui.pushButton_ApllySelected.clicked.connect(self.pushButton_ApllySelected)
        #---------
        self.ui.pushButton_loadAllON.clicked.connect(self.pushButton_loadAllON)
        self.ui.pushButton_loadAllOFF.clicked.connect(self.pushButton_loadAllOFF)
        self.ui.pushButton_loadAddCase.clicked.connect(self.pushButton_loadAddCase)
        self.ui.pushButton_loadEditSelected.clicked.connect(self.pushButton_loadEditSelected)
        self.ui.pushButton_loadDelAll.clicked.connect(self.pushButton_loadDelAll)
        self.ui.pushButton_loadDelSelected.clicked.connect(self.pushButton_loadDelSelected)
        self.ui.pushButton_loadSeletedON.clicked.connect(self.pushButton_loadSeletedON)
        self.ui.pushButton_loadSeletedOFF.clicked.connect(self.pushButton_loadSeletedOFF)
        #---------
        self.ui.listWidget_loadcases.clicked.connect(self.loadcases_setLoadCaseItem)
        #---------
        self.ui.pushButton_zoom_in.clicked.connect(self.pushButton_zoom_in)
        self.ui.pushButton_zoom_out.clicked.connect(self.pushButton_zoom_out)
        #---------
        self.ui.pushButton_set_wlim_ratio.clicked.connect(set_wlim_ratio)
        self.ui.pushButton_set_alpha_yk.clicked.connect(set_alpha_yk)
        self.ui.pushButton_set_alpha_zk.clicked.connect(set_alpha_zk)
        #----MenuBar File
        self.ui.actionSave_project.triggered.connect(self.actionSave)
        self.ui.actionOpen_project.triggered.connect(self.actionOpen)
        #---MenuBar Option
        self.ui.actionReport_language.triggered.connect(set_language)
        #---MenuBar Help
        self.ui.actionAbout.triggered.connect(self.actionAbout)
        #---seting window title
        self.setWindowTitle(infotext.appname + ' ' + infotext.version)

    #------------

    def actionSave(self):
        ui_loadfromdate()
        ui_loadtodate()
        saveopen.saveproject(element, load, self.ui.progressBar)
        self.ui.progressBar.setValue(0)
        
    def actionOpen(self):  
        saveopen.openproject(element, load, self.ui.progressBar)
        self.ui.progressBar.setValue(0)
        ui_loadtodate()
        CheckSection()
    
    #------------

    def actionAbout(self):
        QtWidgets.QMessageBox.information(None, 'Info', infotext.about)

    #------------
    
    def loadcases_setLoadCaseItem(self):
        setLoadCaseItem ()
    
    #------------    
    
    def pushButton_calculate(self):
        self.busy(True)
        ui_loadfromdate()
        ui_loadtodate()
        CheckSection()
        HideSectionBrowserList()
        myapp.ui.progressBar.setValue(0)
        self.busy(False)
        
    #------------

    def pushButton_BrowseSection(self):
        ui_loadfromdate ()
        BrowseSection()
        ui_loadtodate ()
        HideSectionBrowserList()
        
    def pushButton_FindSections(self):
        self.busy(True)
        HideSectionBrowserList()
        ui_loadfromdate ()
        FindSections()
        ui_loadtodate()
        self.busy(False)
    
    def typeselected(self):
        ui_typeselected()

    def sectnameselected(self):
        ui_sectnameselected()
        
    def pushButton_ApllySelected(self):
        self.busy(True)
        if self.ui.listWidget_sectnamelist.currentItem():
            secnameselected=self.ui.listWidget_sectnamelist.currentItem().text()
            self.ui.lineEdit_SectionFigure.setText(secnameselected)
            ui_loadfromdate ()
            ui_loadtodate ()
            CheckSection()
            HideSectionBrowserList()
            HideSectionBrowserList()
        self.busy(False)

    #------------

    def pushButton_loadAllON(self):
        load.caseactiv_all()
        ui_loadtodate()
        HideSectionBrowserList()
        
    def pushButton_loadAllOFF(self):
        load.caseactiv_any()
        ui_loadtodate ()
        HideSectionBrowserList()

    def pushButton_loadAddCase(self):
        ui_loadfromdate ('Add')
        ui_loadtodate ()
        HideSectionBrowserList()
        
    def pushButton_loadEditSelected(self):
        ui_loadfromdate ('Edit')
        ui_loadtodate ()
        HideSectionBrowserList()

    def pushButton_loadDelAll(self):
        load.clear_loadcase()
        ui_loadtodate ()
        HideSectionBrowserList()
        
    def pushButton_loadDelSelected(self):
        load.delete_loadcase(loadcaseItemSelected)
        ui_loadtodate () 
        HideSectionBrowserList()    
        
    def pushButton_loadSeletedON(self):
        load.caseactiv_oncase(loadcaseItemSelected)
        ui_loadtodate ()
        HideSectionBrowserList()
        
    def pushButton_loadSeletedOFF(self):
        load.caseactiv_offcase(loadcaseItemSelected)
        ui_loadtodate ()
        HideSectionBrowserList()

    #------------
        
    def pushButton_zoom_in(self):
        viev_unit_change(-0.5*u.mm)

    def pushButton_zoom_out(self):
        viev_unit_change(+0.5*u.mm)

    #------------

    def busy(self, is_busy=True):
        if is_busy:
            QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        else:
            QtWidgets.QApplication.restoreOverrideCursor()

def set_language():
    global language
    #---
    current_language_index = reports.available_languages.index(language)
    language = QtWidgets.QInputDialog.getItem(None, 'Report language', 'Select language', reports.available_languages, current_language_index, False)[0]
    language = str(language)
    #---
    ui_loadtodate()
    CheckSection()
    
def set_wlim_ratio():
    choice = str(QtWidgets.QInputDialog.getItem(None, 'SLS parameter definition', 'Selcect wlim_ratio value, w_lim=w_lim_ratio*L', paramvalues.wlim_ratio.keys(), 0, False)[0])
    element.w_lim_ratio = paramvalues.wlim_ratio[choice]
    #---
    ui_loadtodate()
    CheckSection()

def set_alpha_yk():
    choice = str(QtWidgets.QInputDialog.getItem(None, 'SLS parameter definition', 'Selcect alpha_yk value, w_yk = alpha_yk*M_zk*L^2/(E*Iz)', paramvalues.alpha_k.keys(), 0, False)[0])
    element.alpha_yk = paramvalues.alpha_k[choice]
    #---
    ui_loadtodate()
    CheckSection()

def set_alpha_zk():
    choice = str(QtWidgets.QInputDialog.getItem(None, 'SLS parameter definition', 'Selcect alpha_zk value, w_zk = alpha_zk*M_yk*L^2/(E*Iy)', paramvalues.alpha_k.keys(), 0, False)[0])
    element.alpha_zk = paramvalues.alpha_k[choice]
    #---
    ui_loadtodate()
    CheckSection()
    
def ui_loadtodate ():
    #section properties
    myapp.ui.lineEdit_SectionMark.setText(element.Mark)
    myapp.ui.lineEdit_SectionFigure.setText(element.sectname)
    myapp.ui.comboBox_SteelGrade.setCurrentIndex(myapp.ui.comboBox_SteelGrade.findText(element.steelgrade))
    myapp.ui.lineEdit_L.setText(str((element.L/u.m).asNumber()))
    myapp.ui.lineEdit_k_ycr.setText(str(element.k_ycr))
    myapp.ui.lineEdit_k_zcr.setText(str(element.k_zcr))
    myapp.ui.lineEdit_k_LT.setText(str(element.k_LT))
    myapp.ui.lineEdit_alpha_yk.setText(str(round(element.alpha_yk, 4)))
    myapp.ui.lineEdit_alpha_zk.setText(str(round(element.alpha_zk, 4)))
    myapp.ui.lineEdit_w_lim_ratio.setText(str(round(element.w_lim_ratio, 4)))
    myapp.ui.lineEdit_gamm_F.setText(str(load.gamma_F))
    #reports
    scrol_value = myapp.ui.textBrowser_ElementProperties.verticalScrollBar().value()
    myapp.ui.textBrowser_ElementProperties.clear()
    myapp.ui.textBrowser_ElementProperties.append(reports.ElementnPropertiesReport(element, language))
    myapp.ui.textBrowser_ElementProperties.verticalScrollBar().setValue(scrol_value)
    #---
    scrol_value = myapp.ui.textBrowser_SectionResistance.verticalScrollBar().value()
    myapp.ui.textBrowser_SectionResistance.clear()
    myapp.ui.textBrowser_SectionResistance.append(reports.SectionResistanceReport(element, language))
    myapp.ui.textBrowser_SectionResistance.verticalScrollBar().setValue(scrol_value)
    #---
    scrol_value = myapp.ui.textBrowser_ElementResistance.verticalScrollBar().value()
    myapp.ui.textBrowser_ElementResistance.clear()
    myapp.ui.textBrowser_ElementResistance.append(reports.ElementResistanceReport(element, language))
    myapp.ui.textBrowser_ElementResistance.verticalScrollBar().setValue(scrol_value)
    #--Element drawing
    ui_drawingsection()
    #--Drawing info
    myapp.ui.label_DrawInfo2.clear()
    myapp.ui.label_DrawInfo2.setText(reports.OneLineResistanceReport(element, language))
    #loadcases list
    myapp.ui.listWidget_loadcases.clear()
    myapp.ui.listWidget_loadcases.addItems(secloadcasaslist())
    
def ui_loadfromdate (loadcase=0):
    global element
    global language
    #section properties
    element.Mark = str(myapp.ui.lineEdit_SectionMark.text())
    element.set_sectionfrombase(str(myapp.ui.lineEdit_SectionFigure.text()))
    element.set_steelgrade(myapp.ui.comboBox_SteelGrade.currentText())
    element.L =string_to_value((myapp.ui.lineEdit_L.text()))*u.m
    element.k_ycr = string_to_value((myapp.ui.lineEdit_k_ycr.text()))
    element.k_zcr = string_to_value((myapp.ui.lineEdit_k_zcr.text()))
    element.k_LT = string_to_value((myapp.ui.lineEdit_k_LT.text()))
    load.gamma_F = string_to_value((myapp.ui.lineEdit_gamm_F.text()))
    element.w_lim_ratio = string_to_value((myapp.ui.lineEdit_w_lim_ratio.text()))
    element.alpha_yk = string_to_value(eval(str(myapp.ui.lineEdit_alpha_yk.text())))
    element.alpha_zk = string_to_value((myapp.ui.lineEdit_alpha_zk.text()))
    #section loads
    if loadcase != 0:
        Name=str(myapp.ui.lineEdit_Name.text())
        #-----
        N_Ed = string_to_value((myapp.ui.lineEdit_N_Ed.text()))*u.kN
        M_yEd = string_to_value((myapp.ui.lineEdit_M_yEd.text()))*u.kNm
        M_zEd = string_to_value((myapp.ui.lineEdit_M_zEd.text()))*u.kNm
        V_yEd = string_to_value((myapp.ui.lineEdit_V_yEd.text()))*u.kN
        V_zEd = string_to_value((myapp.ui.lineEdit_V_zEd.text()))*u.kN
        T_Ed = string_to_value((myapp.ui.lineEdit_T_Ed.text()))*u.kNm
        stabilitycheck = myapp.ui.checkBox_stability.isChecked()
        deflectioncheck = myapp.ui.checkBox_deflection.isChecked()
        print(stabilitycheck)
        if loadcase=='Add':
            load.add_loadcase({"Name": Name, "N_Ed": N_Ed, "M_yEd": M_yEd, "M_zEd": M_zEd, "V_yEd": V_yEd, "V_zEd": V_zEd, "T_Ed": T_Ed, "stabilitycheck": stabilitycheck, "deflectioncheck": deflectioncheck})
        if loadcase=='Edit':
            load.edit_loadcase(loadcaseItemSelected, {"Name": Name, "N_Ed": N_Ed, "M_yEd": M_yEd, "M_zEd": M_zEd, "V_yEd": V_yEd, "V_zEd": V_zEd, "T_Ed": T_Ed , "stabilitycheck": stabilitycheck, "deflectioncheck": deflectioncheck})
    
def setLoadCaseItem ():
    global loadcaseItemSelected
    loadcaseItemSelected=int(myapp.ui.listWidget_loadcases.currentItem().text()[0])
    myapp.ui.lineEdit_Name.setText(load.Name[loadcaseItemSelected])
    myapp.ui.lineEdit_N_Ed.setText(str((load.N_Ed[loadcaseItemSelected]/u.kN).asNumber()))
    myapp.ui.lineEdit_M_yEd.setText(str((load.M_yEd[loadcaseItemSelected]/u.kNm).asNumber()))
    myapp.ui.lineEdit_M_zEd.setText(str((load.M_zEd[loadcaseItemSelected]/u.kNm).asNumber()))
    myapp.ui.lineEdit_V_yEd.setText(str((load.V_yEd[loadcaseItemSelected]/u.kN).asNumber()))
    myapp.ui.lineEdit_V_zEd.setText(str((load.V_zEd[loadcaseItemSelected]/u.kN).asNumber()))
    myapp.ui.lineEdit_T_Ed.setText(str((load.T_Ed[loadcaseItemSelected]/u.kN).asNumber()))
    myapp.ui.checkBox_stability.setChecked(load.stabilitycheck[loadcaseItemSelected])
    myapp.ui.checkBox_deflection.setChecked(load.deflectioncheck[loadcaseItemSelected])

def CheckSection():
    global result
    result = solv.check_element_for_load(element, load)
    #------
    scrol_value = myapp.ui.textBrowser_ElementCheckResults.verticalScrollBar().value()
    myapp.ui.textBrowser_ElementCheckResults.clear()
    myapp.ui.textBrowser_ElementCheckResults.append(reports.CheckSectionReport(element, load, result, language))
    myapp.ui.textBrowser_ElementCheckResults.verticalScrollBar().setValue(scrol_value)
    #------
    scrol_value = myapp.ui.textBrowser_SummaryReport.verticalScrollBar().value()
    myapp.ui.textBrowser_SummaryReport.clear()
    myapp.ui.textBrowser_SummaryReport.append(reports.SummaryReport(element, load, result, language))
    myapp.ui.textBrowser_SummaryReport.verticalScrollBar().setValue(scrol_value)
    #------
    myapp.ui.label_DrawInfo1.clear()
    myapp.ui.label_DrawInfo1.setText(reports.OneLineCheckSectionReport(element, load, result, language))
    if result[0]: myapp.ui.label_DrawInfo1.setStyleSheet('color: green')
    else: myapp.ui.label_DrawInfo1.setStyleSheet('color: red')

#---------------------------------------------------------------------------------
    
def BrowseSection():
    figure = element._SteelSection__base.ui_get_sectionparameters()['sectionname']
    element.set_sectionfrombase(figure)
    #------
    ui_loadtodate()
    CheckSection()

def FindSections():
    global sectionlist
    global tmpelement
    global tmpload
    global isfrom
    global isto
    global sectiongrouptocalculate
    isfrom_inComboBox = string_to_value(myapp.ui.comboBox_Find_from.currentText())
    isto_inComboBox = string_to_value(myapp.ui.comboBox_Find_to.currentText())
    if not (tmpelement.steelgrade == element.steelgrade) & (tmpload.get_loadcases() == load.get_loadcases()) & (isfrom_inComboBox==isfrom) & (isto_inComboBox==isto) & (sectiongrouptocalculate == str(myapp.ui.comboBox_sectiongroups.currentText())):
        ClearFoundSectionList()
        tmpelement = copy.deepcopy(element)
        tmpload = copy.deepcopy(load)
        #-------
        isfrom = isfrom_inComboBox
        isto = isto_inComboBox
        sectiongrouptocalculate = str(myapp.ui.comboBox_sectiongroups.currentText())
        #-------
        progress=0
        number_of_secion=len(element._SteelSection__base.get_database_sectionlist())
        #-------
        for i in element._SteelSection__base.get_database_sectionlist():
            figure = element._SteelSection__base.get_sectionparameters(i)['figure']
            if element._SteelSection__base.get_figuregroupname(figure) == sectiongrouptocalculate or sectiongrouptocalculate == 'All' : 
                tmpelement.set_sectionfrombase(i)
                localresult = solv.check_element_for_load(tmpelement, tmpload)
                if localresult[0]:
                    if isfrom <= max(localresult[4]) <= isto :
                        sectionlist.append(i)
            progress += 1
            myapp.ui.progressBar.setValue(100 * progress/number_of_secion)
        myapp.ui.progressBar.setValue(0)
    ui_reloadlists()

def ui_reloadlists():
    global typelist
    global sectionlist
    sectionlist=sorted(list(set(sectionlist))) 
    typesinsomeseclist=[element._SteelSection__base.get_sectionparameters(i)['figure'] for i in sectionlist]    
    typelist=sorted(list(set(typesinsomeseclist)))
    myapp.ui.listWidget_sectnamelist.clear()
    myapp.ui.listWidget_sectnamelist.addItems(sectionlist)
    myapp.ui.listWidget_typelist.clear()
    myapp.ui.listWidget_typelist.addItems(typelist)

def ui_typeselected():
    selectedtype = myapp.ui.listWidget_typelist.currentItem().text()
    #--------
    myapp.ui.textBrowser_FindSectionResults.clear()
    myapp.ui.textBrowser_SummaryReport.clear()
    myapp.ui.listWidget_sectnamelist.clear()
    basename = element._SteelSection__base.get_database_name()
    myapp.ui.textBrowser_FindSectionResults.append(basename)
    selectedtype_description = element._SteelSection__base.get_database_sectiontypesdescription()[str(selectedtype)]
    myapp.ui.textBrowser_FindSectionResults.append(selectedtype_description)
    for i in sectionlist:
        if element._SteelSection__base.get_sectionparameters(i)['figure']==selectedtype:
            myapp.ui.listWidget_sectnamelist.addItem(i)

def ui_sectnameselected():
    global tmpelement
    global tmpload
    #---Scroll
    scrol_value = myapp.ui.textBrowser_FindSectionResults.verticalScrollBar().value()
    #---Report clear
    myapp.ui.textBrowser_FindSectionResults.clear()
    #---What selected
    selectedsectname = str(myapp.ui.listWidget_sectnamelist.currentItem().text())
    selectedtype = element._SteelSection__base.get_sectionparameters(selectedsectname)['figure']
    basename = element._SteelSection__base.get_database_name()
    selectedtype_description = element._SteelSection__base.get_database_sectiontypesdescription()[str(selectedtype)]
    #---Report title
    myapp.ui.textBrowser_FindSectionResults.append(basename)
    myapp.ui.textBrowser_FindSectionResults.append(selectedtype_description)
    myapp.ui.textBrowser_FindSectionResults.append(selectedsectname + ' selected')
    #---Checking selected section for load
    tmpelement = copy.deepcopy(element)
    tmpelement.set_sectionfrombase(selectedsectname)
    localresult = solv.check_element_for_load(tmpelement, tmpload)
    #---Check report
    myapp.ui.textBrowser_FindSectionResults.append(reports.CheckSectionReport(tmpelement, tmpload, localresult, language))
    #---Scroll
    myapp.ui.textBrowser_FindSectionResults.verticalScrollBar().setValue(scrol_value)
    
def ClearFoundSectionList():
    global typelist
    global sectionlist
    typelist=[]
    sectionlist=[]
    HideSectionBrowserList()
    
def HideSectionBrowserList():
    myapp.ui.listWidget_sectnamelist.clear()
    myapp.ui.listWidget_typelist.clear()
    myapp.ui.textBrowser_FindSectionResults.clear()

def ui_drawingsection():
    sectionscene.clearScene()
    element.draw_contour(sectionscene, element.sectname)
    sectionscene.ShowOnGraphicsViewObiect()
    
def viev_unit_change(value=u.mm):
    sectionscene.change_unit(value)
    ui_drawingsection()

def secloadcasaslist ():
    u.xvalueformat("%9.2f")
    list=[]
    for i in range(len(load.Name)):
        list.append(str(i) + ', ' + str(load.Name[i]) + ',' + str(load.N_Ed[i]) + ','+str(load.M_yEd[i]) + ',' + str(load.M_zEd[i]) + ',' + str(load.V_yEd[i]) + ' , ' + str(load.V_zEd[i]) + ',' + str(load.T_Ed[i]) + ',          ' + str(load.stabilitycheck[i]) + ',             '+ str(load.deflectioncheck[i]) + ',             ' + str(load.caseactiv[i]))
    u.xvalueformat("%5.2f")
    return list
    
def string_to_value(valuestring):
    valuestring = str(valuestring)
    valuestring = valuestring.replace(',', '.')
    value = eval(valuestring)
    return value

if __name__ == "__main__":
    element = SteelElement()
    load = SteelElementLoad()
    solv = SteelElementSolver()
    loadcaseItemSelected=0
    language = reports.available_languages[0]
    result = None
    #---
    element.set_sectionbase_speedmode(1)
    #----
    tmpelement = SteelElement()
    tmpelement.steelgrade = None
    tmpload = SteelElementLoad()
    tmpload.caseactiv_any()
    isfrom = None
    isto = None
    sectiongrouptocalculate = None
    typelist=[]
    sectionlist=[]
    #----
    app = QtWidgets.QApplication(sys.argv)
    myapp = MAINWINDOW()
    sectionscene = PyqtSceneCreator2D()
    sectionscene.set_GraphicsViewObiect(myapp.ui.graphicsView)
    sectionscene.set_unit(0.3*u.cm)
    myapp.ui.comboBox_SteelGrade.addItems(element.get_availablesteelgrade())
    myapp.ui.comboBox_sectiongroups.addItems(['All'] + [element._SteelSection__base.get_database_sectiongroups()[i] for i in sorted(element._SteelSection__base.get_database_sectiongroups().keys())])
    #----
    element.set_sectionfrombase()
    CheckSection()
    ui_loadtodate()
    
    element.set_sectionbase_databasename('UK')
    #----
    myapp.show()
    sys.exit(app.exec_())