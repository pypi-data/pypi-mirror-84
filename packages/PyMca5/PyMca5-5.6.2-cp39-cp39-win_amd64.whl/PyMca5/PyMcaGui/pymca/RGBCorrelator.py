#!/usr/bin/env python
#/*##########################################################################
# Copyright (C) 2004-2020 V.A. Sole, European Synchrotron Radiation Facility
#
# This file is part of the PyMca X-ray Fluorescence Toolkit developed at
# the ESRF by the Software group.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#############################################################################*/
__author__ = "V.A. Sole - ESRF Data Analysis"
__contact__ = "sole@esrf.fr"
__license__ = "MIT"
__copyright__ = "European Synchrotron Radiation Facility, Grenoble, France"
import sys
import os
import numpy
from PyMca5.PyMcaGui.pymca import RGBCorrelatorWidget
qt = RGBCorrelatorWidget.qt
if hasattr(qt, 'QString'):
    QString = qt.QString
else:
    QString = str
from PyMca5.PyMcaGui import RGBCorrelatorGraph
from PyMca5.PyMcaGui import QPyMcaMatplotlibSave
USE_MASK_WIDGET = False
if USE_MASK_WIDGET:
    from PyMca5.PyMcaGui import MaskImageWidget
    
MATPLOTLIB = True

class RGBCorrelator(qt.QWidget):

    sigRGBCorrelatorSignal = qt.pyqtSignal(object)
    sigMaskImageWidgetSignal = qt.pyqtSignal(object)

    def __init__(self, parent=None, graph=None, bgrx=True, image_shape=None):
        qt.QWidget.__init__(self, parent)
        self.setWindowTitle("PyMca RGB Correlator")
        self.setWindowIcon(qt.QIcon(qt.QPixmap(RGBCorrelatorGraph.IconDict['gioconda16'])))
        self.mainLayout = qt.QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(6)
        self.splitter   = qt.QSplitter(self)
        self.splitter.setOrientation(qt.Qt.Horizontal)
        self.controller = RGBCorrelatorWidget.RGBCorrelatorWidget(self.splitter, image_shape=image_shape)
        self._y1AxisInverted = False
        self._imageBuffer = None
        self._matplotlibSaveImage = None
        standaloneSaving = True
        if graph is None:
            if MATPLOTLIB:
                standaloneSaving = False
            if USE_MASK_WIDGET:
                self.graphWidgetContainer = MaskImageWidget.MaskImageWidget(self.splitter,
                                            selection=True,
                                            imageicons=True,
                                            standalonesave=standaloneSaving,
                                            profileselection=False,
                                            polygon=True)
                self.graphWidget = self.graphWidgetContainer.graphWidget
            else:
                self.graphWidget = RGBCorrelatorGraph.RGBCorrelatorGraph(self.splitter,
                                            standalonesave=standaloneSaving)
            if not standaloneSaving:
                self.graphWidget.saveToolButton.clicked.connect( \
                         self._saveToolButtonSignal)
                self._saveMenu = qt.QMenu()
                self._saveMenu.addAction(QString("Standard"),    self.graphWidget._saveIconSignal)
                self._saveMenu.addAction(QString("Matplotlib") , self._saveMatplotlibImage)
            self.graph = self.graphWidget.graph
            #add flip Icon
            self.graphWidget.hFlipToolButton.clicked.connect( \
                         self._hFlipIconSignal)
            self._handleGraph    = True
        else:
            self.graph = graph
            self._handleGraph = False
        #self.splitter.setStretchFactor(0,1)
        #self.splitter.setStretchFactor(1,1)
        self.mainLayout.addWidget(self.splitter)

        self.reset    = self.controller.reset
        self.addImage = self.controller.addImage
        self.removeImage = self.controller.removeImage
        self.addImageSlot = self.controller.addImageSlot
        self.removeImageSlot = self.controller.removeImageSlot
        self.replaceImageSlot = self.controller.replaceImageSlot
        self.setImageShape = self.controller.setImageShape
        self.update   = self.controller.update
        self.transposeImages   = self.controller.transposeImages
        self.controller.sigRGBCorrelatorWidgetSignal.connect( \
                     self.correlatorSignalSlot)
        self.controller.sigMaskImageWidgetSignal.connect( \
                     self.maskImageSlot)

    def _hFlipIconSignal(self):
        if self._handleGraph:
            if self.graph.isYAxisInverted():
                self.graph.invertYAxis(False)
            else:
                self.graph.invertYAxis(True)
            self.graph.replot()
            #this is not needed
            #self.controller.update()
            return

    def setSelectionMask(self, *var, **kw):
        self.controller.setSelectionMask(*var, **kw)

    def maskImageSlot(self, ddict):
        self.sigMaskImageWidgetSignal.emit(ddict)

    def correlatorSignalSlot(self, ddict):
        if 'image' in ddict:
            # keep the image buffer as an array
            self._imageBuffer = ddict['image']
            size = ddict['size']
            self._imageBuffer.shape = size[1],size[0],4
            self._imageBuffer[:,:,3] = 255
            self.graph.addImage(self._imageBuffer)
            self.graph.replot()

    def _saveToolButtonSignal(self):
        self._saveMenu.exec_(self.cursor().pos())

    def _saveMatplotlibImage(self):
        if self._matplotlibSaveImage is None:
            self._matplotlibSaveImage = QPyMcaMatplotlibSave.SaveImageSetup(None,
                                                                            None)
            self._matplotlibSaveImage.setWindowTitle("Matplotlib RGBCorrelator")

        #Qt is BGR while the others are RGB ...
        # This is not any longer a problem because we do not use PyQwt
        self._matplotlibSaveImage.setPixmapImage(self._imageBuffer, bgr=False)
        self._matplotlibSaveImage.show()
        self._matplotlibSaveImage.raise_()

    def closeEvent(self, event):
        ddict = {}
        ddict['event'] = "RGBCorrelatorClosed"
        ddict['id']    = id(self)
        self.controller.close()
        if self._matplotlibSaveImage is not None:
            self._matplotlibSaveImage.close()
        self.sigRGBCorrelatorSignal.emit(ddict)
        qt.QWidget.closeEvent(self, event)

    def show(self):
        if self.controller.isHidden():
            self.controller.show()
        qt.QWidget.show(self)

def test():
    import logging
    app = qt.QApplication([])
    app.lastWindowClosed.connect(app.quit)
    if 0:
        graphWidget = RGBCorrelatorGraph.RGBCorrelatorGraph()
        graph = graphWidget.graph
        w = RGBCorrelator(graph=graph)
    else:
        w = RGBCorrelator()
        w.resize(800, 600)
    import getopt
    from PyMca5.PyMcaCore.LoggingLevel import getLoggingLevel
    options = ''
    longoptions = ["logging=", "debug="]
    opts, args = getopt.getopt(
                    sys.argv[1:],
                    options,
                    longoptions)

    logging.basicConfig(level=getLoggingLevel(opts))
    filelist=args
    if len(filelist):
        try:
            import DataSource
            DataReader = DataSource.DataSource
        except:
            import EdfFileDataSource
            DataReader = EdfFileDataSource.EdfFileDataSource
        for fname in filelist:
            source = DataReader(fname)
            for key in source.getSourceInfo()['KeyList']:
                dataObject = source.getDataObject(key)
                w.addImage(dataObject.data, os.path.basename(fname)+" "+key)
    else:
        print("This is a just test method using 100 x 100 matrices.")
        print("Run PyMcaPostBatch to have file loading capabilities.")
        array1 = numpy.arange(10000)
        array2 = numpy.resize(numpy.arange(10000), (100, 100))
        array2 = numpy.transpose(array2)
        array3 = array1 * 1
        w.addImage(array1)
        w.addImage(array2)
        w.addImage(array3)
        w.setImageShape([100, 100])
    w.show()
    app.exec_()

if __name__ == "__main__":
    test()

