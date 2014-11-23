#!/usr/bin/env python

'''
Created on Feb 16, 2013

@author: Toshiba
'''
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future_builtins import *


import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import helpform,Frame,splashScreen,time

import qrc_resources


__version__ = "0.3 Alpha"

class SystemTrayIcon(QSystemTrayIcon):
   
    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        menu = QMenu(parent)
        self.actionExit = QAction("Exit", self)
        self.actionAbout = QAction("About CPNSA", self)
        
        menu.addAction(self.actionAbout)
        menu.addSeparator()
        menu.addAction(self.actionExit)
        
        self.connect(self.actionAbout, SIGNAL("triggered()"), self.about)
        self.connect(self.actionExit, SIGNAL("triggered()"), self.exit)  
        
        traySignal = "activated(QSystemTrayIcon::ActivationReason)"
        
        self.connect(self, SIGNAL(traySignal), self.icon_activated)
        self.setContextMenu(menu)
       
    def exit(self):
        w = QWidget()
        reply = QMessageBox.question(w, 'Confirm Action',"Are you sure to exit?", QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:           
            window.close()
            
    def about(self):            
        window.helpAbout()

    def icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            if window.windowState() != Qt.WindowMaximized:
                window.showMaximized()
            else:
                window.showNormal()
                window.showMaximized()
            window.setFocus(True)
            window.show()
        
        
class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.tabWidget = QTabWidget()
        self.setCentralWidget(self.tabWidget)
        fileNewAction = self.createAction("&New", self.fileNew,
                QKeySequence.New, "filenew", "Create a New project")
        fileOpenAction = self.createAction("&Open...", self.fileOpen,
                QKeySequence.Open, "fileopen",
                "Open an existing NBird file")
        fileSaveAction = self.createAction("&Save", self.fileSave,
                QKeySequence.Save, "filesave", "Save nbb file")
        fileSaveAsAction = self.createAction("Save &As...",
                self.fileSaveAs, icon="filesaveas",
                tip="Save Nbird using a new filename")
        fileSaveAllAction = self.createAction("Save A&ll",
                self.fileSaveAll, icon="filesave",
                tip="Save all the files")
        fileCloseTabAction = self.createAction("Close &Tab",
                self.fileCloseTab, 'Ctrl+W', "filequit",
                "Close the active tab")
        fileQuitAction = self.createAction("&Quit", self.close,
                "Ctrl+Q", "filequit", "Close the application")
        helpHelpAction = self.createAction(self.tr("&Help"),
                self.helpHelp, QKeySequence.HelpContents)
        
        helpAboutAction = self.createAction(
                self.tr("&About Mareula"), self.helpAbout)
        QShortcut(QKeySequence.PreviousChild, self, self.prevTab)
        QShortcut(QKeySequence.NextChild, self, self.nextTab)
        fileMenu = self.menuBar().addMenu("&File")
        self.addActions(fileMenu, (fileNewAction, fileOpenAction,
                fileSaveAction, fileSaveAsAction, fileSaveAllAction,
                fileCloseTabAction, None, fileQuitAction))
        editMenu = self.menuBar().addMenu("&Edit")
        
        helpMenu = self.menuBar().addMenu(self.tr("&Help"))
        self.addActions(helpMenu, ( helpHelpAction, helpAboutAction))
        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolbar")
        self.addActions(fileToolbar, (fileNewAction, fileOpenAction,
                                      fileSaveAction))
        settings = QSettings()
        self.restoreGeometry(
                settings.value("MainWindow/Geometry").toByteArray())
        self.restoreState(
                settings.value("MainWindow/State").toByteArray())

        self.status = self.statusBar()
        self.status.setSizeGripEnabled(False)
        self.status.showMessage("Ready", 5000)

        self.setWindowTitle("CPNSA")
        QTimer.singleShot(0, self.loadFiles)
           
    def helpAbout(self):
        QMessageBox.about(self,
                self.tr("CPNSA"),
                (self.tr("""<b>CPNSA</b> v %1
                <p>Copyright &copy; 2013 Tantawi Ltd. 
                All rights reserved.
                <p>Generic modular intgerated solution.
                """).arg(__version__)))
        
    def helpHelp(self):
        form = helpform.HelpForm("index.html", self)
        form.show()
    
   
    def createAction(self, text, slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/{0}.png".format(icon)))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action

    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def closeEvent(self, event):
        failures = []
        for i in range(self.tabWidget.count()):
            toplogyEdit = self.tabWidget.widget(i)
            if toplogyEdit.isModified():
                try:
                    toplogyEdit.save()
                    
                except IOError, e:
                    failures.append(unicode(e))
        if (failures and
            QMessageBox.warning(self, "CPNSA -- Save Error",
                    "Failed to save{0}\nQuit anyway?".format(
                    "\n\t".join(failures)),
                    QMessageBox.Yes|QMessageBox.No) ==
                    QMessageBox.No):
            event.ignore()
            return
        settings = QSettings()
        settings.setValue("MainWindow/Geometry",
                          QVariant(self.saveGeometry()))
        settings.setValue("MainWindow/State",
                          QVariant(self.saveState()))
        files = QStringList()
        for i in range(self.tabWidget.count()):
            toplogyEdit = self.tabWidget.widget(i)
            
            if not toplogyEdit.filename.startsWith("new"):
                files.append(toplogyEdit.filename)
        settings.setValue("CurrentFiles", QVariant(files))
        while self.tabWidget.count():
            toplogyEdit = self.tabWidget.widget(0)
            toplogyEdit.close()
            self.tabWidget.removeTab(0)
        self.newProject.closeAll()
        
    def prevTab(self):
        last = self.tabWidget.count()
        current = self.tabWidget.currentIndex()
        if last:
           
            last -= 1
            current = last if current == 0 else current - 1
            self.tabWidget.setCurrentIndex(current)

    def nextTab(self):
        last = self.tabWidget.count()
        current = self.tabWidget.currentIndex()
        if last:
            last -= 1
            current = 0 if current == last else current + 1
            self.tabWidget.setCurrentIndex(current)


    def loadFiles(self):
        if len(sys.argv) > 1:
            count = 0
            for filename in sys.argv[1:]:
                filename = QString(filename)
                if QFileInfo(filename).isFile():
                    self.loadFile(filename)
                    QApplication.processEvents()
                    count += 1
                    if count >= 10: # Load at most 10 files
                        break
        else:
            settings = QSettings()
            files = settings.value("CurrentFiles").toStringList()
            for filename in files:
                filename = QString(filename)
                if QFile.exists(filename):
                    self.loadFile(filename)
                    QApplication.processEvents()


    def fileNew(self):
        self.newProject = Frame.InnerTab()
        self.tabWidget.addTab(self.newProject, self.newProject.windowTitle())
        self.tabWidget.setCurrentWidget(self.newProject)
        
    def fileOpen(self):
        filename = QFileDialog.getOpenFileName(self,
                "CPNSA -- Open File")
        if not filename.isEmpty():
            for i in range(self.tabWidget.count()):
                toplogyEdit = self.tabWidget.widget(i)
                if toplogyEdit.filename == filename:
                    self.tabWidget.setCurrentWidget(toplogyEdit)
                    break
            else:
                self.loadFile(filename)


    def loadFile(self, filename):
        toplogyEdit =Frame.InnerTab(filename)
        if toplogyEdit is None or not isinstance(toplogyEdit,Frame.InnerTab):
            return True
        try:
            toplogyEdit.load()
        except (IOError, OSError), e:
            QMessageBox.warning(self,
                    "CPNSA -- Load Error",
                    "Failed to load {0}: {1}".format(filename, e))
            toplogyEdit.close()
            del toplogyEdit
        else:
            self.tabWidget.addTab(toplogyEdit, toplogyEdit.windowTitle())
            self.tabWidget.setCurrentWidget(toplogyEdit)


    def fileSave(self):
        toplogyEdit = self.tabWidget.currentWidget()
        if toplogyEdit is None or not isinstance(toplogyEdit,Frame.InnerTab):
            return True
        try:
            toplogyEdit.save()
            self.tabWidget.setTabText(self.tabWidget.currentIndex(),
                    QFileInfo(toplogyEdit.filename).fileName())
            return True
        except (IOError, OSError), e:
            QMessageBox.warning(self,
                    "CPNSA -- Save Error",
                    "Failed to save {0}: {1}".format(toplogyEdit.filename, e))
            return False


    def fileSaveAs(self):
        toplogyEdit = self.tabWidget.currentWidget()
        if toplogyEdit is None or not isinstance(toplogyEdit,Frame.InnerTab):
            return True
        filename = QFileDialog.getSaveFileName(self,
                "CPNSA -- Save File As", toplogyEdit.filename,
                "Nbird (*.nbb *.*)")
        if not filename.isEmpty():
            toplogyEdit.filename = filename
            return self.fileSave()
        return True

    def fileSaveAll(self):
        errors = []
        for i in range(self.tabWidget.count()):
            toplogyEdit = self.tabWidget.widget(i)
            if toplogyEdit.isModified():
                try:
                    toplogyEdit.save()
                except (IOError, OSError), e:
                    errors.append("{0}: {1}".format(toplogyEdit.filename, e))
        if errors:
            QMessageBox.warning(self, "CPNSA -- "
                    "Save All Error",
                    "Failed to save\n{0}".format("\n".join(errors)))

    def fileCloseTab(self):
        toplogyEdit = self.tabWidget.currentWidget()
        if toplogyEdit is None or not isinstance(toplogyEdit,Frame.InnerTab):
            return True
        
        toplogyEdit.close()
        self.tabWidget.removeTab(self.tabWidget.currentIndex())

def show_splash(app, path):
    image = QPixmap(path)
    splash = splashScreen.SplashScreen(image)
    font = QFont(splash.font())
    font.setPointSize(font.pointSize() + 5)
    splash.setFont(font)
    splash.show()
    QApplication.processEvents()
    for count in range(1, 10):
        splash.showMessage(splash.tr('Processing %1...').arg(count),
                           Qt.AlignCenter, Qt.black)
        app.processEvents()
        QThread.msleep(1000)
    splash.hide()
    splash.close()



def main():
    
    
    app = QApplication(sys.argv)
    #show_splash(app,"images/icon.png")
    app.setWindowIcon(QIcon("images/icon.png"))
    app.setOrganizationName("CPNSA")
    app.setOrganizationDomain("cpnsa.com")
    app.setApplicationName("CPNSA")
    
    global window
    window = MainWindow()
    w = QWidget()
    trayIcon = SystemTrayIcon(QIcon("images/icon.png"), w )
    trayIcon.show()
    trayIcon.setToolTip("CPNSA")
    trayIcon.showMessage("CPNSA","CPNSA has started!")
    
    window.showMaximized()
    window.show()
    
    window.fileNew()
    #splashz.finish(window)
    app.exec_()
if __name__ == "__main__": main()
    