# -*- coding: utf-8 -*-
"""
| ----------------------------------------------------------------------------------------------------------------------
| Date                : August 2018
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
import os

from osgeo import gdal
from qgis.PyQt.QtWidgets import QDialog, QFileDialog, QDialogButtonBox
from qgis.gui import QgsFileWidget
from qgis.core import QgsProviderRegistry, QgsMapLayerProxyModel, QgsRasterLayer, QgsProject, QgsVectorLayer
from qgis.utils import iface
from qgis.PyQt.uic import loadUi

from localmaxfilter.interfaces import run_algorithm_local_max_filter


class LocalMaxFilterWidget(QDialog):
    """ QDialog to interactively set up the Local Max Filter input and output. """

    def __init__(self):
        super(LocalMaxFilterWidget, self).__init__()
        loadUi(os.path.join(os.path.dirname(__file__), 'local_max_filter.ui'), self)

        # parameters
        excluded_providers = [p for p in QgsProviderRegistry.instance().providerList() if p not in ['gdal']]
        self.imageComboBox.setExcludedProviders(excluded_providers)
        self.imageComboBox.setFilters(QgsMapLayerProxyModel.RasterLayer)
        self.imageAction.triggered.connect(self._image_browse)
        self.imageButton.setDefaultAction(self.imageAction)

        excluded_providers = [p for p in QgsProviderRegistry.instance().providerList() if p not in ['ogr']]
        self.maskComboBox.setExcludedProviders(excluded_providers)
        self.maskComboBox.setFilters(QgsMapLayerProxyModel.VectorLayer)
        self.maskAction.triggered.connect(self._vector_browse)
        self.maskButton.setDefaultAction(self.maskAction)

        # set snap_distance maximum to half of the window size
        self.SNAPSpinBox.setMaximum(self.windowSpinBox.value()/2)
        self.windowSpinBox.valueChanged.connect(self._spinbox_value_changed)

        self.outputFileWidget.lineEdit().setReadOnly(True)
        self.outputFileWidget.lineEdit().setPlaceholderText('[Create temporary layer]')
        self.outputFileWidget.setStorageMode(QgsFileWidget.SaveFile)

        # Open in QGIS?
        try:
            iface.activeLayer
        except AttributeError:
            self.openCheckBox.setChecked(False)
            self.openCheckBox.setDisabled(True)

        # run or cancel
        self.OKClose.button(QDialogButtonBox.Ok).setText("Run")
        self.OKClose.accepted.connect(self._run_local_max_filter)
        self.OKClose.rejected.connect(self.close)

        # widget variables
        self.image = None
        self.mask = None

    def log(self, text):
        # append text to log window
        self.logBrowser.append(str(text) + '\n')
        # open the widget on the log screen
        self.tabWidget.setCurrentIndex(self.tabWidget.indexOf(self.tab_log))

    def _image_browse(self):
        """ Browse for an image raster file. """
        path = QFileDialog.getOpenFileName(filter=QgsProviderRegistry.instance().fileRasterFilters())[0]
        try:
            if len(path) > 0:
                gdal.UseExceptions()
                layer = QgsRasterLayer(path, os.path.basename(path), 'gdal')
                assert layer.isValid()
                QgsProject.instance().addMapLayer(layer, True)
                self.imageComboBox.setLayer(layer)
        except AssertionError:
            self.log("'" + path + "' not recognized as a supported file format.")
        except Exception as e:
            self.log(e)

    def _vector_browse(self):
        """ Browse for a vector file. """
        path = QFileDialog.getOpenFileName(filter=QgsProviderRegistry.instance().fileVectorFilters())[0]
        try:
            if len(path) > 0:
                gdal.UseExceptions()
                layer = QgsVectorLayer(path, os.path.basename(path), 'ogr')
                assert layer.isValid()
                QgsProject.instance().addMapLayer(layer, True)
                self.maskComboBox.setLayer(layer)
        except AssertionError:
            self.log("'" + path + "' not recognized as a supported file format.")
        except Exception as e:
            self.log(e)

    def _spinbox_value_changed(self, value):
        self.SNAPSpinBox.setMaximum(value/2)

    def _run_local_max_filter(self):
        """ Read all parameters and pass them on to the LocalMaxFilter class. """

        try:
            # Only temp file possible when result is opened in QGIS
            if not self.openCheckBox.isChecked() and len(self.outputFileWidget.filePath()) == 0:
                raise Exception("If you won't open the result in QGIS, you must select a base file name for output.")

            # Get parameters
            if not self.imageComboBox.currentLayer():
                raise Exception("Choose a correct image file.")
            else:
                image_path = self.imageComboBox.currentLayer().source()
            window = self.windowSpinBox.value()
            if self.maskComboBox.currentLayer():
                mask_path = self.maskComboBox.currentLayer().source()
            else:
                mask_path = None
            snap_distance = self.SNAPSpinBox.value()
            output_path = self.outputFileWidget.filePath()
            voronoi = self.VoronoiCheckBox.isChecked()

            result = run_algorithm_local_max_filter(image_path=image_path, window=window,
                                                    update_progress_bar=self.progressBar.setValue,
                                                    log_function=self.log,
                                                    mask_path=mask_path,
                                                    output_base_path=output_path,
                                                    snap_distance=snap_distance,
                                                    voronoi=voronoi)

            # Open result in QGIS
            if self.openCheckBox.isChecked():
                # point layer
                output_point_path = result[0]
                output_point_name, _ = os.path.splitext(os.path.basename(output_point_path))
                output_point_layer = QgsVectorLayer(output_point_path, name=output_point_name)
                QgsProject.instance().addMapLayer(output_point_layer, True)

                # mask layer
                if mask_path:
                    output_mask_path = result[1]
                    output_mask_name, _ = os.path.splitext(os.path.basename(output_mask_path))
                    output_mask_layer = QgsVectorLayer(output_mask_path, name=output_mask_name)
                    QgsProject.instance().addMapLayer(output_mask_layer, True)

                # voronoi layer
                if voronoi:
                    output_voronoi_path = result[2]
                    output_voronoi_name, _ = os.path.splitext(os.path.basename(output_voronoi_path))
                    output_voronoi_layer = QgsVectorLayer(output_voronoi_path, name=output_voronoi_name)
                    QgsProject.instance().addMapLayer(output_voronoi_layer, True)

        except Exception as e:
            self.log(e)


def _run():
    from qgis.core import QgsApplication
    from qgis.analysis import QgsNativeAlgorithms
    app = QgsApplication([], True)
    app.initQgis()
    from processing.core.Processing import Processing
    Processing.initialize()
    QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

    z = LocalMaxFilterWidget()
    z.show()

    app.exec_()


if __name__ == '__main__':
    _run()
