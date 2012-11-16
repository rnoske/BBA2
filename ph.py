# -*- coding: utf-8 -*-

"""
Program Handler!
"""

import collections
import os
import multiprocessing as mp

import numpy as np
import matplotlib.pyplot as plt

import bild
import Config

class Ph():
    """ Program handler
    
    """
    def __init__(self):
        """ Initialisation
        
        """
        self.cf = Config.Config(filename = 'Settings.ini')
        self.bd = collections.OrderedDict()
        self.data = {}
        
    #Settingsui handling
    def get_settings(self, section = 'FlameParameters'):
        """ Return an dictionaray of current Settings
        
        """
        self.cf.getConfigOptions(section) #reads config
        return self.cf.cfgdict #created dictionaray
        
    def set_settings(self, cfgdict, section = 'FlameParameters'):
        """ Save the dictionary to file
        
        """
        self.cf.writeConfigOptions(section, cfgdict)
        
    #Program Handling
    def del_image_dict(self):
        """ Deletes dictionary entrys
        
        """
        self.bd = collections.OrderedDict()
        
    def add_image_bd(self, filepath):
        """ Adds image to bilderdict
        
        filepath (str): complete filepath to image
        
        """
        _Bild = bild.Bild(filepath)
        _name = _Bild.att['name']
        self.bd[_name] = _Bild
        
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
        
    def calc_flameArea(self):
        """ Calculate the flame area for every image
        
        """
        print 'Starting calculating Flame area gauss'
        _fA = []
        for bild in self.bd.itervalues():
            bild.calc_flammenoberflaecheGauss()
            _fA.append([int(bild.att['bid']), 
                        float(bild.att['flammenoberflaecheGauss'])])
        self.data['Flammenoberflaeche Gauss'] = np.array(_fA)
        print 'Finished calculating Flame area gauss'
    
    def worker_flameArea(self, work_q, result_q):
            bild = work_q.get()
            print bild.att['name']
            bild.calc_flammenflaeche()
            result_q.put(bild)
            work_q.task_done()
            
    def calc_flameAreaCounting(self):
        """ Calculate the flame area as function of the number of pixel 
        over threshold
        
        """
        print 'Starting calculating counting flame area'
        _fA = []
        for bild in self.bd.itervalues():
            bild.calc_flammenflaeche()
            _fA.append([int(bild.att['bid']), 
                        float(bild.att['flammenflaeche'])])
        self.data['Flammenflaeche'] = np.array(_fA)
        print 'Finished calculating counting flame area'