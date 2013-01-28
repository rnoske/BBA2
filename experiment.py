# -*- coding: utf-8 -*-

#standard library imports
import logging
import os
from collections import OrderedDict

#related third party imports
import numpy as np # NumPy (multidimensional arrays, linear algebra, ...)
import matplotlib.pyplot as plt

#local application/library specific imports
import bild


class Experiment():
    """ Experiment class
    
    """
    def __init__(self, path, ident, **kwargs):
        """ Initialisation
        
        path (str): path(folder) to experiment
        ident (int): identification number for each experiment
        
        """
        #Experiment attributes
        self.att = OrderedDict()
        self.att['tag'] = 'Experiment'
        self.att['path'] = str(path)
        self.att['id'] = str(ident)
        self.att['name'] = str(self._calc_name())
        self.att['description'] = 'single experiment'
        
        #Experiment parameters
        self.parameters = {}
        self._read_parameters()
        
        #Image dictionary
        self.bd = OrderedDict()
        #corresponding data
        self.data = {}
        
        #populate experiment
        self.populate_experiment()
        
    def _calc_name(self):
        """ Extract name out of file path
        
        """
        _path = self.att['path']
        namen = str(_path).split(os.sep)
        name = namen.pop()
        return name
        
    def add_parameter(self, name, value, unit=None):
        """ Add parameter to parameter dictionary
        
        name (str): key
        value (any): value
        unit (str): unit corresponding to value
        
        """
        _param = {}
        _param['name'] = name
        _param['value'] = value
        _param['unit'] = unit
        #print _param
        self.parameters[_param['name']] = _param
        
    def _read_parameters(self):
        """ Read parameters from Paramter.cfg file
        
        """
        #read parameter file
        _fp = self.att['path'] + '/' + 'Parameter.cfg'
        with open(_fp) as f:
            content = f.readlines()
        #analyse content and add parameters
        _nparams = ((len(content)+1)/4)
        for i in xrange(_nparams):
            _n = content[i*4].rstrip('\n')
            _u = content[i*4+1].rstrip('\n')
            _v = content[i*4+2].rstrip('\n')
            self.add_parameter(_n, _v, _u)
                
        
    def populate_experiment(self):
        """ Populate automatically the experiment
        
        """
        curdir = self.att['path'] #os.getcwd()
        folder = curdir + '/fits'
        _fitfiles = self._get_image_list(folder)
        for _fitfile in _fitfiles:
            _fp = folder + '/' + _fitfile
            self.add_image_bd(_fp)
        
    def _get_image_list(self, folder):
        #get all files in folder
        _items = os.listdir(folder)        
        #check if files are fit files
        _fitfiles = []
        for item in _items:
            _end = item.split('.')
            _end = _end.pop()
            _endungen = ['fits']
            if _end in _endungen:
                _fitfiles.append(item)
            else:
                print 'Dateiendung nicht .fit!'
        
        #return list with fit files
        return _fitfiles
        
        
    def add_image_bd(self, filepath):
        """ Adds image to bilderdict
        
        filepath (str): complete filepath to image
        
        """
        _Bild = bild.Bild(filepath)
        #set necessary parameter for image
        _Bild.zero =self.parameters['Zero']['value']
        _Bild.resolution =self.parameters['Resolution']['value']
        _Bild.flame_center =self.parameters['Flame center']['value']
        _Bild.workspace =self.att['path']
        _Bild.degree_image =self.parameters['Degree per image']['value']
        
        _Bild.startup()
        
        _name = _Bild.att['name']
        self.bd[_name] = _Bild
        
    def del_image_dict(self):
        """ Deletes dictionary entrys
        
        """
        self.bd = OrderedDict()
        
    def setImageSettings(self, sdict):
        """ Set Image Settings for each Bild class instance
        
        sdict (dict): Settings dictionaray
        
        """
        self.sdict = sdict
        for k, v in self.bd.iteritems():
            v.sdict = sdict
            
    def get_imageName_list(self):
        """ Return list of bd keys
        
        """
        return self.bd.keys()
        
    def save_ResultData(self):
        """ Save all acquired Data
        
        """
        print 'Saving calculated results!'
        if len(self.data) != 0:
            for key, value in self.data.iteritems():
                _fp = self.att['path']+'/Calculated Data/'
                if not os.path.exists(_fp):
                    os.makedirs(_fp)
                #print key, value
                _fp += key
                #save as text file
                _fpd = _fp + '.txt'
                np.savetxt(_fpd, value, delimiter=';')
                #save as plot
                colour = ['bo', 'ro', 'go', 'b+', 'r+', 'g+']
                plt.cla()
                for n in xrange(1, value.shape[1]):
                    plt.plot(value[:, 0], value[:, n], colour[n-1], label=str(n))
                plt.legend()
                _fpp = _fp + '.jpg'
                plt.savefig(_fpp)
        print 'Finished saving calculated results!'
        
    def convert_jpg(self):
        """ convert every image to jpg and save it
        
        """
        print 'Convertiere Bilder zu jpgs, tif und eps'
        for bild in self.bd.itervalues():
            bild.convert_to_jpg()
            bild.convert_to_tiff()
            #bild.convert_to_eps()
            bild.convert_to_pdf()
        #self.data['convertet_to_jpg'] = True
        print 'Convertierung abgeschlossen!'
        
        
    def calc_totalInt(self):
        """ Calculate total Intensity for every image
        
        """
        _tInt = []
        _mInt = []
        _com =  []
        for bild in self.bd.itervalues():
            bild.calc_totalInt()
            bild.calc_com()
            _tInt.append([int(bild.att['phase']), float(bild.att['totalInt'])])
            _mInt.append([int(bild.att['phase']), float(bild.att['mittelInt'])])
            _com.append([int(bild.att['phase']), float(bild.att['CoM 1']), float(bild.att['CoM 0'])])
        self.data['totalInt'] = np.array(_tInt)
        self.data['mittelInt'] = np.array(_mInt)
        self.data['CoM'] = np.array(_com)
        
        #temporary calc-histogram call
        #self.calc_histogram()
        
    def calc_histogram(self):
        """ Calculate the Intensity histogram for every image
        
        """
        print 'Calculating Histogram for all images'
        for bild in self.bd.itervalues():
            bild.calc_histogram()
        print 'Finished calculating histograms'
        
    def calc_flameHeight(self, nGauss = 2):
        """ Calculate flame height for every image
        
        """
        print 'Startet calculating flame height'
        _fH = []
        _fHG0 = []
        _fHG1 = []
        for i, bild in enumerate(self.bd.itervalues()):
            bild.calc_flammenhoehe()
            bild.calc_flammenhoeheGauss(nGauss)
            _fH.append([int(bild.att['phase']), 
                        float(bild.att['flammenhoehe']), 
                        float(bild.att['flammenhoeheIndex'])])
            _fHG0.append([int(bild.att['phase']), 
                         float(bild.att['flammenhoeheGauss0']),
                         float(bild.att['flammenhoeheGaussAmplitude0']), 
                        float(bild.att['flammenhoeheGaussVarianz0']), 
                        float(bild.att['flammenhoeheGaussIndex0'])])
            if nGauss == 2:
                _fHG1.append([int(bild.att['phase']), 
                         float(bild.att['flammenhoeheGauss1']),
                         float(bild.att['flammenhoeheGaussAmplitude1']), 
                        float(bild.att['flammenhoeheGaussVarianz1']), 
                        float(bild.att['flammenhoeheGaussIndex1'])])
        self.data['flammenhoehe'] = np.array(_fH)
        self.data['flammenhoehe Gauss 0'] = np.array(_fHG0)
        if nGauss == 2:
            self.data['flammenhoehe Gauss 1'] = np.array(_fHG1)
        print 'finished calculating flame height'
        
        