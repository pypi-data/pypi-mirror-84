# -*- coding: utf-8 -*-
"""
| ----------------------------------------------------------------------------------------------------------------------
| Date                : November 2018
| Copyright           : © 2018 - 2020 by Tinne Cahy (Geo Solutions) and Ann Crabbé (KU Leuven)
| Email               : acrabbe.foss@gmail.com
| Acknowledgements    : Translated from Local Maximum Filter [C++ software]
|                       Ghent University, Laboratory of Forest Management and Spatial Information Techniques
|                       Lieven P.C. Verbeke
|
| This file is part of the QGIS Tree Density Calculator plugin and treedensitycalculator python package.
|
| This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
| License as published by the Free Software Foundation, either version 3 of the License, or any later version.
|
| This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
| warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
|
| You should have received a copy of the GNU General Public License (COPYING.txt). If not see www.gnu.org/licenses.
| ----------------------------------------------------------------------------------------------------------------------
"""
from os import path

from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMenu
from qgis.core import QgsApplication

from localmaxfilter.interfaces.localmaxfilter_provider import LocalMaxFilterProvider
from localmaxfilter.interfaces.local_max_filter_gui import LocalMaxFilterWidget
from localmaxfilter.images.resources_rc import qInitResources
qInitResources()


class LocalMaxFilterPlugin:
    """ QGIS Plugin Implementation """

    def __init__(self, iface):
        """
        :param QgsInterface iface: the interface instance which provides the hook to manipulate the QGIS GUI at run time
        """
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = path.dirname(__file__)

        # Add an empty menu to the Raster Menu
        self.main_menu = QMenu(title='Tree Density', parent=self.iface.rasterMenu())
        self.main_menu.setIcon(QIcon(':/logo'))
        self.iface.rasterMenu().addMenu(self.main_menu)
        self.provider = None

    def initGui(self):
        """ Create the menu entries and toolbar icons inside the QGIS GUI """

        # add action button to raster menu
        action = QAction(QIcon(':/logo'), 'Tree Density Calculator', self.iface.mainWindow())
        action.triggered.connect(lambda: LocalMaxFilterWidget().exec_())
        action.setStatusTip('Tree Density Calculator based on Brightness Image')
        self.main_menu.addAction(action)

        # add provider to processing toolbox
        self.provider = LocalMaxFilterProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        self.iface.rasterMenu().removeAction(self.main_menu.menuAction())
        QgsApplication.processingRegistry().removeProvider(self.provider)
