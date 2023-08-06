#/*##########################################################################
#
# The PyMca X-Ray Fluorescence Toolkit
#
# Copyright (c) 2004-2020 European Synchrotron Radiation Facility
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
__doc__ = """
Module to calculate a set of ROIs on a stack of data.
"""
import os
import numpy
import logging
import copy
from PyMca5.PyMcaIO import ConfigDict
from PyMca5.PyMcaIO.OutputBuffer import OutputBuffer as OutputBufferBase
from PyMca5.PyMcaCore import McaStackView


_logger = logging.getLogger(__name__)


class OutputBuffer(OutputBufferBase):

    def __init__(self, saveResiduals=False, saveFit=False, saveData=False,
                 diagnostics=False, saveFOM=False, **kwargs):
        super(OutputBuffer, self).__init__(**kwargs)
        self.fileProcessDefault = 'roi_sum'


class StackROIBatch(object):

    def __init__(self):
        self.config = ConfigDict.ConfigDict()

    def setConfiguration(self, configuration):
        self.config = ConfigDict.ConfigDict()
        self.config.update(configuration)

    def getConfiguration(self):
        return copy.deepcopy(self.config)

    def setConfigurationFile(self, ffile):
        configuration = ConfigDict.ConfigDict()
        configuration.read(ffile)
        self.setConfiguration(configuration)

    def batchROIMultipleSpectra(self, x=None, y=None, configuration=None,
                                net=True, xAtMinMax=False, index=None,
                                xLabel=None, outbuffer=None, save=True,
                                **outbufferinitargs):
        """
        This method performs the actual fit. The y keyword is the only mandatory input argument.

        :param x: 1D array containing the x axis (usually the channels) of the spectra.
        :param y: 3D array containing the data, usually [nrows, ncolumns, nchannels]
        :param weight: 0 Means no weight, 1 Use an average weight, 2 Individual weights (slow)
        :param net: 0 Means no subtraction, 1 Calculate
        :param xAtMinMax: if True, calculate X at maximum and minimum Y. Default is false.
        :param index: Index of dimension where to apply the ROIs.
        :param xLabel: Type of ROI to be used.
        :param outbuffer:
        :param save: set to False to postpone saving the in-memory buffers
        :return OutputBuffer:
        """
        data, x, index = self._parseData(x=x, y=y, index=index)
        roiList, config = self._prepareRoiList(configuration=configuration,
                                               xLabel=xLabel)

        # Calculation needs buffer for memory allocation (memory or H5)
        if outbuffer is None:
            outbuffer = OutputBuffer(**outbufferinitargs)
        with outbuffer.Context(save=save):
            outbuffer['configuration'] = config
            self._extractRois(data, x, index,
                              roiList=roiList,
                              roiDict=config["ROI"]["roidict"],
                              outbuffer=outbuffer,
                              xAtMinMax=xAtMinMax)
        return outbuffer

    def _extractRois(self, data, x, mcaAxis, roiList=None, roiDict=None,
                     outbuffer=None, xAtMinMax=False):
        nRois = len(roiList)
        nRows = data.shape[0]
        nColumns = data.shape[1]
        if xAtMinMax:
            roiShape = (nRois * 4, nRows, nColumns)
            names = [None] * 4 * nRois
        else:
            roiShape = (nRois * 2, nRows, nColumns)
            names = [None] * 2 * nRois

        # Helper variables for roi calculation
        idx = [None] * nRois  # indices along axis=index for each ROI
        xw = [None] * nRois  # x-values for each ROI
        iXMinList = [None] * nRois  # min(xw) for each ROI
        iXMaxList = [None] * nRois  # max(xw) for each ROI
        def idxraw(i): return i
        def idxnet(i): return i + nRois
        def idxmax(i): return i + 2 * nRois
        def idxmin(i): return i + 3 * nRois
        for j, roi in enumerate(roiList):
            if roi == "ICR":
                xw[j] = x
                idx[j] = numpy.arange(len(x))
                iXMinList[j] = idx[j][0]
                iXMaxList[j] = idx[j][-1]
            else:
                roiFrom = roiDict[roi]["from"]
                roiTo = roiDict[roi]["to"]
                idx[j] = numpy.nonzero((roiFrom <= x) & (x <= roiTo))[0]
                if len(idx[j]):
                    xw[j] = x[idx[j]]
                    iXMinList[j] = numpy.argmin(xw[j])
                    iXMaxList[j] = numpy.argmax(xw[j])
                else:
                    xw[j] = None
            names[idxraw(j)] = "ROI " + roi
            names[idxnet(j)] = "ROI " + roi + " Net"
            if xAtMinMax:
                roiType = roiDict[roi]["type"]
                names[idxmax(j)] = "ROI " + roi + (" %s at Max." % roiType)
                names[idxmin(j)] = "ROI " + roi + (" %s at Min." % roiType)

        # Allocate memory for result
        roidtype = numpy.float
        results = outbuffer.allocateMemory('roisum',
                                           shape=roiShape,
                                           dtype=roidtype,
                                           labels=names,
                                           dataAttrs=None,
                                           groupAttrs={'default': True},
                                           memtype='ram')

        # Allocate memory of partial result
        nMca = 2, 'MB'
        _logger.debug('Process spectra in chunks of {}'.format(nMca))
        datastack = McaStackView.FullView(data, mcaAxis=mcaAxis, nMca=nMca)
        for (resultidx, resultshape), chunk in datastack.items(keyType='select'):
            for j, roi in enumerate(roiList):
                # Calculate ROI sum
                if xw[j] is None:
                    # no points in the ROI       
                    rawSum = 0.0
                    netSum = 0.0
                else:
                    roichunk = chunk[:, idx[j]]
                    rawSum = roichunk.sum(axis=1, dtype=numpy.float)
                    deltaX = xw[j][iXMaxList[j]] - xw[j][iXMinList[j]]
                    left = roichunk[:, iXMinList[j]]
                    right = roichunk[:, iXMaxList[j]]
                    deltaY = right - left
                    if abs(deltaX) > 0.0:
                        slope = deltaY / float(deltaX)
                        background = left * len(xw[j]) + slope * \
                                    (xw[j] - xw[j][iXMinList[j]]).sum(dtype=numpy.float)
                        netSum = rawSum - background
                    else:
                        netSum = 0.0
                    rawSum = rawSum.reshape(resultshape)
                    netSum = netSum.reshape(resultshape)
                results[idxraw(j)][resultidx] = rawSum  # ROI sum
                results[idxnet(j)][resultidx] = netSum  # ROI sum minus linear background
                # Calculate x-value of the minimum and maximum within the ROI
                if xAtMinMax:
                    if xw[j] is None:
                        # what can be the Min and the Max when there is nothing in the ROI?
                        _logger.warning("No Min. Max for ROI <%s>. Empty ROI" % roi)
                    else:
                        maxImage = xw[j][numpy.argmax(roichunk, axis=1)]
                        results[idxmax(j)][resultidx] = maxImage.reshape(resultshape)
                        minImage = xw[j][numpy.argmin(roichunk, axis=1)]
                        results[idxmin(j)][resultidx] = minImage.reshape(resultshape)

    def _parseData(self, x=None, y=None, index=None):
        if y is None:
            raise RuntimeError("y keyword argument is mandatory!")
        if hasattr(y, "info") and hasattr(y, "data"):
            data = y.data
            mcaIndex = y.info.get("McaIndex", -1)
        else:
            data = y
            mcaIndex = -1
        if index is None:
            index = mcaIndex
        if index < 0:
            index = len(data.shape) - 1

        #workaround a problem with h5py
        try:
            if index in [0]:
                testException = data[0:1]
            else:
                if len(data.shape) == 2:
                    testException = data[0:1, -1]
                elif len(data.shape) == 3:
                    testException = data[0:1, 0:1, -1]
        except AttributeError:
            txt = "%s" % type(data)
            if 'h5py' in txt:
                _logger.info("Implementing h5py workaround")
                import h5py
                data = h5py.Dataset(data.id)
            else:
                raise

        # only usual spectra case supported
        if index != (len(data.shape) - 1):
            raise IndexError("Only stacks of spectra supported")
        if len(data.shape) != 3:
            txt = "For the time being only "
            txt += "three dimensional arrays supported"
            raise NotImplementedError(txt)
        if len(data.shape) != 3:
            txt = "For the time being only "
            txt += "three dimensional arrays supported"
            raise NotImplementedError(txt)

        # make sure to get x data
        if x is None:
            x = numpy.arange(data.shape[index]).astype(numpy.float32)
        elif x.size != data.shape[index]:
            raise NotImplementedError("All the spectra should share same X axis")
        #data = numpy.transpose(data, (1,0,2))
        return data, x, index

    def _prepareRoiList(self, configuration=None, xLabel=None):
        # read the current configuration
        if configuration is not None:
            self.setConfiguration(configuration)
        config = self.getConfiguration()

        # prepare roi list
        roiList0 = config["ROI"]["roilist"]
        if type(roiList0) not in [type([]), type((1,))]:
            roiList0 = [roiList0]

        # operate only on compatible ROIs
        roiList = []
        roiDict = config["ROI"]["roidict"]
        for roi in roiList0:
            roiType = roiDict[roi]["type"]
            if xLabel is None:
                roiList.append(roi)
            elif roi.upper() == "ICR":
                roiList.append(roi)
            elif xLabel.lower() == roiType.lower():
                roiList.append(roi)
            else:
                _logger.info("ROI <%s> ignored")
        return roiList, config


def getFileListFromPattern(pattern, begin, end, increment=None):
    if type(begin) == type(1):
        begin = [begin]
    if type(end) == type(1):
        end = [end]
    if len(begin) != len(end):
        raise ValueError(\
            "Begin list and end list do not have same length")
    if increment is None:
        increment = [1] * len(begin)
    elif type(increment) == type(1):
        increment = [increment]
    if len(increment) != len(begin):
        raise ValueError(\
            "Increment list and begin list do not have same length")
    fileList = []
    if len(begin) == 1:
        for j in range(begin[0], end[0] + increment[0], increment[0]):
            fileList.append(pattern % (j))
    elif len(begin) == 2:
        for j in range(begin[0], end[0] + increment[0], increment[0]):
            for k in range(begin[1], end[1] + increment[1], increment[1]):
                fileList.append(pattern % (j, k))
    elif len(begin) == 3:
        raise ValueError("Cannot handle three indices yet.")
        for j in range(begin[0], end[0] + increment[0], increment[0]):
            for k in range(begin[1], end[1] + increment[1], increment[1]):
                for l in range(begin[2], end[2] + increment[2], increment[2]):
                    fileList.append(pattern % (j, k, l))
    else:
        raise ValueError("Cannot handle more than three indices.")
    return fileList


def prepareDataStack(fileList):
    if (not os.path.exists(fileList[0])) and \
        os.path.exists(fileList[0].split("::")[0]):
        # odo convention to get a dataset form an HDF5
        fname, dataPath = fileList[0].split("::")
        # compared to the ROI imaging tool, this way of reading puts data
        # into memory while with the ROI imaging tool, there is a check.
        if 0:
            import h5py
            h5 = h5py.File(fname, "r")
            dataStack = h5[dataPath][:]
            h5.close()
        else:
            from PyMca5.PyMcaIO import HDF5Stack1D
            # this way reads information associated to the dataset (if present)
            if dataPath.startswith("/"):
                pathItems = dataPath[1:].split("/")
            else:
                pathItems = dataPath.split("/")
            if len(pathItems) > 1:
                scanlist = ["/" + pathItems[0]]
                selection = {"y":"/" + "/".join(pathItems[1:])}
            else:
                selection = {"y":dataPath}
                scanlist = None
            print(selection)
            print("scanlist = ", scanlist)
            dataStack = HDF5Stack1D.HDF5Stack1D([fname],
                                                selection,
                                                scanlist=scanlist)
    else:
        from PyMca5.PyMca import EDFStack
        dataStack = EDFStack.EDFStack(fileList, dtype=numpy.float32)
    return dataStack


def main():
    import glob
    import sys
    import getopt
    _logger.setLevel(logging.DEBUG)
    options = ''
    longoptions = ['cfg=', 'outdir=',
                   'tif=', 'edf=', 'csv=', 'h5=', 'dat=',
                   'filepattern=', 'begin=', 'end=', 'increment=',
                   'outroot=', 'outentry=', 'outprocess=',
                   'overwrite=', 'multipage=']
    try:
        opts, args = getopt.getopt(
                     sys.argv[1:],
                     options,
                     longoptions)
    except:
        _logger.error(sys.exc_info()[1])
        sys.exit(1)
    outputDir = None
    outputRoot = ""
    fileEntry = ""
    fileProcess = ""
    filepattern = None
    begin = None
    end = None
    increment = None
    tif = 0
    edf = 0
    csv = 0
    h5 = 1
    dat = 0
    overwrite = 1
    multipage = 0
    for opt, arg in opts:
        if opt in ('--cfg'):
            configurationFile = arg
        elif opt in '--begin':
            if "," in arg:
                begin = [int(x) for x in arg.split(",")]
            else:
                begin = [int(arg)]
        elif opt in '--end':
            if "," in arg:
                end = [int(x) for x in arg.split(",")]
            else:
                end = int(arg)
        elif opt in '--increment':
            if "," in arg:
                increment = [int(x) for x in arg.split(",")]
            else:
                increment = int(arg)
        elif opt in '--filepattern':
            filepattern = arg.replace('"', '')
            filepattern = filepattern.replace("'", "")
        elif opt in '--outdir':
            outputDir = arg
        elif opt == '--outroot':
            outputRoot = arg
        elif opt == '--outentry':
            fileEntry = arg
        elif opt == '--outprocess':
            fileProcess = arg
        elif opt in ('--tif', '--tiff'):
            tif = int(arg)
        elif opt == '--edf':
            edf = int(arg)
        elif opt == '--csv':
            csv = int(arg)
        elif opt == '--h5':
            h5 = int(arg)
        elif opt == '--dat':
            dat = int(arg)
        elif opt == '--overwrite':
            overwrite = int(arg)
        elif opt == '--multipage':
            multipage = int(arg)
    if filepattern is not None:
        if (begin is None) or (end is None):
            raise ValueError(
                "A file pattern needs at least a set of begin and end indices")
    if filepattern is not None:
        fileList = getFileListFromPattern(filepattern, begin, end,
                                          increment=increment)
    else:
        fileList = args
    if len(fileList):
        dataStack = prepareDataStack(fileList)
    else:
        print("OPTIONS:", longoptions)
        sys.exit(0)
    if outputDir is None:
        print("RESULTS WILL NOT BE SAVED: No output directory specified")
    worker = StackROIBatch()
    worker.setConfigurationFile(configurationFile)
    outbuffer = OutputBuffer(outputDir=outputDir,
                             outputRoot=outputRoot,
                             fileEntry=fileEntry,
                             fileProcess=fileProcess,
                             tif=tif, edf=edf, csv=csv,
                             h5=h5, dat=dat,
                             multipage=multipage,
                             overwrite=overwrite)
    with outbuffer.saveContext():
        worker.batchROIMultipleSpectra(y=dataStack,
                                       outbuffer=outbuffer)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
