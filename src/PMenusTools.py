import os
import xml.etree.ElementTree as etree

from PyQt4 import QtGui, QtCore

from PSettings import ICONS_S, ICONS_L, MENUDATA


class MenusTools(object):
    # call constructor of MenusTools

    def __init__(self, parent=None):

        self.parent = parent

    def createStatusBar(self):
        # create a status bar
        self.statusbar = self.parent.statusBar()
        self.statusbar.setFixedHeight(22)
        style = (""" QStatusBar {background-color:rgb(232,232,232); \
                border: 1px solid grey;}""")
        self.statusbar.setStyleSheet(style)
        self.statusbar.setSizeGripEnabled(False)

        self.statustip = QtGui.QLabel(self.statusbar.showMessage(
            'Ready.', 3000))

    def getMenuData(self):
        """get all menus and pulldowns from the external XML file"""

        menudata = list()

        xml_file = os.path.join(MENUDATA, 'PMenu.xml')
        xml = etree.parse(xml_file)
        menu_structure = xml.getroot()

        for menu in menu_structure.findall('Menubar'):
            mname = menu.attrib['name']
            items = menu.findall('Submenu')
            pulldowns = self.getPullDownData(items)
            menudata.append((mname, [s for s in pulldowns]))

        return tuple(menudata)

    def getPullDownData(self, items):

        pulldowns = list()
        for sub in items:
            sname = sub.attrib['name']
            if sname == 'Separator':
                pulldowns.append(('', '', '', '', self.onPass))
                continue
            tip = sub.attrib['tip']
            icon = sub.attrib['icon']
            shortcut = sub.attrib['short']
            handler = sub.attrib['handler']
            pulldowns.append((sname, tip, shortcut, icon, handler))

        return pulldowns

    def createMenus(self):
        """create the menubar and populate it automatically"""
        # create a menu bar
        self.menubar = QtGui.QMenuBar(self.parent)
        self.parent.setMenuBar(self.menubar)

        for eachMenu in self.getMenuData():
            name = eachMenu[0]
            menu = self.menubar.addMenu(name)

            pulldown = eachMenu[1]
            self.createPullDown(menu, pulldown)
        return

    def createPullDown(self, menu, eachPullDown):
        """create the submenu structure to method createMenus"""
        for name, tip, short, icon, handler in eachPullDown:

            if len(name) == 0:
                menu.addSeparator()
                continue

            icon = QtGui.QIcon(ICONS_S + icon)

            if 'aboutQt' not in handler:
                handler = 'self.parent.slots.' + handler

            action = QtGui.QAction(icon, name, self.parent,
                                   shortcut=short, statusTip=tip,
                                   triggered=eval(handler))
            menu.addAction(action)

    def getToolbarData(self):
        """get all menus and submenus from the external XML file"""

        xml_file = os.path.join(MENUDATA, 'PToolbar.xml')
        xml = etree.parse(xml_file)
        tool_structure = xml.getroot()

        tooldata = list()

        for toolbar in tool_structure.findall('Toolbar'):
            for tool in toolbar.findall('Tool'):
                if tool.attrib['handler'] == 'self.onPass':
                    tooldata.append(('', '', '', '', self.onPass))
                    continue
                tip = tool.attrib['tip']
                icon = tool.attrib['icon']
                handler = tool.attrib['handler']
                tooldata.append((tip, icon, handler))

        return tuple(tooldata)

    def createTools(self):
        """create the toolbar and populate it automatically
         from  method toolData
        """
        # create a tool bar
        self.toolbar = self.parent.addToolBar('Toolbar')

        for tip, icon, handler in self.getToolbarData():
            if len(tip) == 0:
                self.toolbar.addSeparator()
                continue
            icon = QtGui.QIcon(ICONS_L + icon)
            action = QtGui.QAction(
                icon, tip, self.parent, triggered=eval(
                    'self.parent.slots.' + handler))
            self.toolbar.addAction(action)

    def createDocks(self):
        self.parent.messagedock = QtGui.QDockWidget(self.parent)
        self.parent.messagedock. \
            setFeatures(QtGui.QDockWidget.DockWidgetMovable |
                        QtGui.QDockWidget.DockWidgetFloatable)
        self.parent.messagedock.setWindowTitle('Messages')
        # connect messagedock to slot
        self.parent.messagedock.topLevelChanged.connect(
            self.parent.slots.onLevelChanged)

        self.parent.messages = QtGui.QTextEdit(self.parent)
        self.parent.messages. \
            setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse |
                                    QtCore.Qt.TextSelectableByKeyboard)
        # connect messages to scrollhandler
        self.parent.messages.textChanged.connect(
            self.parent.slots.onTextChanged)

        self.parent.messagedock.setWidget(self.parent.messages)

        place = QtCore.Qt.BottomDockWidgetArea
        self.parent.addDockWidget(
            QtCore.Qt.DockWidgetArea(place), self.parent.messagedock)

    @QtCore.pyqtSlot()
    def onPass(self):
        pass
