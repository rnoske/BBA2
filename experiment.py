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
    def __init__(self, path, ident):
        """ Initialisation
        
        path (str): path(folder) to experiment
        ident (int): identification number for each experiment
        
        """
        #Experiment attributes
        self.att = OrderedDict()
        self.att['tag'] = 'Experiment'
        self.att['path'] = path
        self.att['id'] = ident
        
        #Experiment parameters
        self.parameters = {}
        
        #Image dictionary
        self.bd = OrderedDict()
        #corresponding data
        self.data = {}
        
        #populate experiment
        self.populate_experiment()
        
    def add_parameter(self, name, value):
        """ Add parameter to parameter dictionary
        
        name (str): key
        value (any): value
        
        """
        self.parameters[name] = value
        
    def populate_experiment(self):
        """ Populate automatically the experiment
        
        """
        curdir = os.curdir()
        print curdir
        folder = curdir + '/fits'
        self._get_image_list(folder)
        
    def _get_image_list(self, folder):
        #get all files in folder
        
        #check if files are fit files
        
        #return list with fit files
        pass
        
        
    def add_image_bd(self, filepath):
        """ Adds image to bilderdict
        
        filepath (str): complete filepath to image
        
        """
        _Bild = bild.Bild(filepath)
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
        _fp = self.sdict['workspace']+'/Calculated Data/'
        if not os.path.exists(_fp):
            os.makedirs(_fp)
        if len(self.data) != 0:
            for key, value in self.data.iteritems():
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
        
    def convert_jpg(self):
        """ convert every image to jpg and save it
        
        """
        print 'Convertiere Bilder zu jpgs'
        for bild in self.bd.itervalues():
            bild.convert_to_jpg()
        self.data['convertet_to_jpg'] = True
        print 'Convertierung abgeschlossen!'
        
        
    def calc_totalInt(self):
        """ Calculate total Intensity for every image
        
        """
        _tInt = []
        _mInt = []
        for bild in self.bd.itervalues():
            bild.calc_totalInt()
            _tInt.append([int(bild.att['bid']), float(bild.att['totalInt'])])
            _mInt.append([int(bild.att['bid']), float(bild.att['mittelInt'])])
        self.data['totalInt'] = np.array(_tInt)
        self.data['mittelInt'] = np.array(_mInt)
        
    def calc_flameHeight(self, nGauss = 2):
        """ Calculate flame height for every image
        
        """
        print 'Startet calculating flame height'
        _fH = []
        _fHG = []
        for i, bild in enumerate(self.bd.itervalues()):
            bild.calc_flammenhoehe()
            bild.calc_flammenhoeheGauss(nGauss)
            _fH.append([int(bild.att['bid']), float(bild.att['flammenhoehe'])])
            _fHG.append([int(bild.att['bid']), 
                         float(bild.att['flammenhoeheGauss0'])])
            if nGauss == 2:
                _fHG[i].append(float(bild.att['flammenhoeheGauss1']))
                        #float(bild.att['flammenhoeheGaussVarianz'])])
        self.data['flammenhoehe'] = np.array(_fH)
        self.data['flammenhoehe Gauss'] = np.array(_fHG)
        print 'finished calculating flame height'
        
        