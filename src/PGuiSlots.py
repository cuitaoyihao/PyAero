import sys

from PyQt4 import QtGui, QtCore

import PyAero
import PAirfoil
import PGraphicsTest as gt
import PIconProvider
from PSettings import *


class Slots(object):

    def __init__(self, parent=None):

        self.parent = parent

    @QtCore.pyqtSlot()
    def onOpen(self):

        dialog = QtGui.QFileDialog()

        provider = PIconProvider.IconProvider()
        dialog.setIconProvider(provider)
        dialog.setNameFilter(DIALOGFILTER)
        dialog.setNameFilterDetailsVisible(True)
        dialog.setDirectory('data')
        dialog.setFileMode(QtGui.QFileDialog.ExistingFile)

        # open custom file dialog using custom icons
        if dialog.exec_():
            filename = dialog.selectedFiles()[0]
            selfilter = dialog.selectedFilter()

        # do nothing if CANCLE button was pressed
        try:
            filename
        except NameError:
            return

        if 'stl' in selfilter.toLower():  # method of QString object
            self.parent.postview.readStl(filename)
        else:
            self.loadAirfoil(filename, '#')

    @QtCore.pyqtSlot()
    def onOpenPredefined(self):
        self.loadAirfoil('predefined', '#')

    def loadAirfoil(self, name, comment):
        self.parent.airfoil = PAirfoil.Airfoil(self.parent)
        self.parent.airfoil.readContour(name, comment)
        self.fitAirfoilInView()

    @QtCore.pyqtSlot()
    def onPredefinedSTL(self):
        self.parent.postview.readStl('data/SATORI.stl')

    @QtCore.pyqtSlot()
    def fitAirfoilInView(self):
        if self.parent.airfoil:  # fit only when airfoil loaded
            dx = 0.05 * self.parent.airfoil.item.rect.width()
            rect = self.parent.airfoil.item.rect.adjusted(-dx, 0, dx, 0)
            self.parent.view.fitInView(rect, mode=QtCore.Qt.KeepAspectRatio)

            # cache view to be able to keep it during resize
            self.parent.view.getSceneFromView()

    @QtCore.pyqtSlot()
    def onViewAll(self):
        rect = self.parent.scene.itemsBoundingRect()
        self.parent.view.fitInView(rect, mode=QtCore.Qt.KeepAspectRatio)

    @QtCore.pyqtSlot()
    def toggleObjects(self):
        if self.parent.testitems:
            gt.deleteTestItems(self.parent.scene)
        else:
            gt.addTestItems(self.parent.scene)
        self.parent.testitems = not self.parent.testitems

    @QtCore.pyqtSlot()
    def onSave(self):
        (fname, thefilter) = QtGui.QFileDialog. \
            getSaveFileNameAndFilter(self.parent,
                                     'Save file', '.', filter=DIALOGFILTER)
        if not fname:
            return

        with open(fname, 'w') as f:
            f.write('This test worked for me ...')

    @QtCore.pyqtSlot()
    def onSaveAs(self):
        (fname, thefilter) = QtGui. \
            QFileDialog.getSaveFileNameAndFilter(
            self.parent, 'Save file as ...', '.',
            filter=DIALOGFILTER)
        if not fname:
            return
        with open(fname, 'w') as f:
            f.write('This test worked for me ...')

    @QtCore.pyqtSlot()
    def onPrint(self):
        dialog = QtGui.QPrintDialog()
        if dialog.exec_() == QtGui.QDialog.Accepted:
            self.parent.editor.document().print_(dialog.printer())

    @QtCore.pyqtSlot()
    def onPreview(self):
        printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)

        preview = QtGui.QPrintPreviewDialog(printer, self.parent)
        preview.paintRequested.connect(self.handlePaintRequest)
        preview.exec_()

    def handlePaintRequest(self, printer):
        printer.setOrientation(QtGui.QPrinter.Landscape)
        self.parent.view.render(QtGui.QPainter(printer))

    @QtCore.pyqtSlot()
    def toggleLogDock(self):
        """Switch message log window on/off"""

        sender = self.parent.sender().metaObject().className()

        if sender == 'QCheckBox':
            visible = self.parent.messagedock.isVisible()
            self.parent.messagedock.setVisible(not visible)
        # FIXME
        # FIXME: else is never called here, because when closing messagedock
        # FIXME: with 'X'clicked, no sender signal is emitted; closeEvent
        # FIXME: has to be overwritten in subclassed QDockWidget instead
        # FIXME
        else:
            checkbox = self.centralWidget().tools.cb1
            checkbox.setChecked(not checkbox.isChecked())

    @QtCore.pyqtSlot()
    def onMessage(self, msg):
        # move cursor to the end befor writing new message
        # so in case text inside the log window was selected before
        # the new text is pastes correct
        self.parent.messages.moveCursor(QtGui.QTextCursor.End)
        self.parent.messages.insertHtml(msg)

    @QtCore.pyqtSlot()
    def onExit(self):
        sys.exit(QtGui.qApp.quit())

    @QtCore.pyqtSlot()
    def onCalculator(self):
        pass

    @QtCore.pyqtSlot()
    def onBackground(self):
        if self.parent.bgview == 'gradient':
            self.parent.bgview = 'solid'
        else:
            self.parent.bgview = 'gradient'

        self.parent.view.setBackground(self.parent.bgview)

    @QtCore.pyqtSlot()
    def onUndo(self):
        pass

    @QtCore.pyqtSlot()
    def onLevelChanged(self):
        """Change size of message window when floating """
        if self.parent.messagedock.isFloating():
            self.parent.messagedock.resize(700, 300)

    @QtCore.pyqtSlot()
    def onTextChanged(self):
        """Move the scrollbar in the message log-window to the bottom.
        So latest messages are always in the view.
        """
        vbar = self.parent.messages.verticalScrollBar()
        if vbar:
            vbar.triggerAction(QtGui.QAbstractSlider.SliderToMaximum)

    def onTabChanged(self):
        tab = self.parent.centralwidget.tabs.currentIndex()
        if tab == 1:
            self.parent.centralwidget.tools.toolBox.setCurrentIndex(2)

    @QtCore.pyqtSlot()
    def onRedo(self):
        pass

    @QtCore.pyqtSlot()
    def onHelp(self):
        pass

    @QtCore.pyqtSlot()
    def onAbout(self):
        QtGui.QMessageBox. \
            about(self.parent, "About " + PyAero.__appname__,
                  "<b>" + PyAero.__appname__ +
                  "</b> is used for "
                  "2D airfoil contour analysis and CFD mesh generation.\
                  <br><br>"
                  "Version : " + PyAero.__version__ + "<br>"
                  "<b>" + PyAero.__appname__ + "</b> code under " +
                  PyAero.__license__ +
                  " license (c) " +
                  PyAero.__copyright__ + "<br><br>"
                  "email to: " + PyAero.__email__ + "<br>"
                  "Twitter: <a href='http://twitter.com/chiefenne'>\
                  @chiefenne</a><br><br>"
                  "<b>Aeropython</b> code under MIT license. \
                  (c) 2014 Lorena A. Barba, Olivier Mesnard<br>"
                  "Link to " +
                  "<a href='http://nbviewer.ipython.org/github/" +
                  "barbagroup/AeroPython/blob/master/lessons/" +
                  "11_Lesson11_vortexSourcePanelMethod.ipynb'> \
                  <b>Aeropython</b></a> in an iPython notebook.")
