# -*- coding: utf-8 -*-
"""
| ----------------------------------------------------------------------------------------------------------------------
| Date                : April 2020
| Copyright           : © 2020 by Ann Crabbé (KU Leuven)
| Email               : acrabbe.foss@gmail.com
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
dense_name = 'treedensitycalculator'  # used for distributing your package on pip or qgis, no spaces
long_name = 'Tree Density Calculator'  # what users see in the QGIS plugin repository and on the RTD toc
pdf_title = 'Tree Density Calculator Documentation'  # the front page title on the read the docs PDF version

author = 'Ann Crabbé'  # your name
author_email = 'acrabbe.foss@gmail.com'  # your contact information
author_copyright = '© 2018 - 2020 by Ann Crabbé'  # a copyright, typical "© [start year] - [end year] by [your name]"
short_version = '1.5'  # 2 numbers, update with each new release
long_version = '1.5.6'  # 3 numbers, update with each new release

bitbucket_home = 'https://bitbucket.org/kul-reseco/localmaxfilter'
bitbucket_src = 'https://bitbucket.org/kul-reseco/localmaxfilter/src'
bitbucket_issues = 'https://bitbucket.org/kul-reseco/localmaxfilter/issues'

read_the_docs = 'https://treedensitycalculator.readthedocs.io'

keywords = ['forestry', 'tree density', 'remote sensing', 'sliding window', 'local maxima']

qgis_min_version = '3.6'

short_description = 'The Tree Density Calculator is designed to calculate tree densities based on local maxima.'
long_description = 'The Tree Density Calculator is a QGIS plugin and command line interface package designed to ' \
                    'calculate tree densities based on brightness images, using the local maximum in a sliding window.'

qgis_metadata_icon = 'images/logo.png'
qgis_category = 'Raster'
processing_provider = True
