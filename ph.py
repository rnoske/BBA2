# -*- coding: utf-8 -*-

"""
Program Handler!
"""

from collections import OrderedDict
import os
import multiprocessing as mp

import numpy as np
import matplotlib.pyplot as plt

import experiment
import Config

class Ph():
    """ Program handler
    
    """
    def __init__(self):
        """ Initialisation
        
        """
        self.cf = Config.Config(filename = 'Settings.ini')
        self.exp = OrderedDict()
        self.ident = 0
        
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
        
    def add_experiment(self, experiment):
        """ Add an experiment
        
        experiment (experiment): experiment object
        
        """
        self.exp[experiment.att[str(self.ident)]] = experiment
        self.ident += 1
        
    def add_new_experiment(self, path):
        """ Create and add an new experiment
        
        path (str): path to experiment folder
        
        """
        exp = experiment.Experiment(path, self.ident)
        self.exp[experiment.att[str(self.ident)]] = exp
        self.ident += 1
        
    def convert_jpg(self):
        """ Convert images in Experiment to jpg
        
        """
        for i, exp in self.exp.itervalues():
            if 'convertet_to_jpg' in exp.data.keys():
                pass
            else:
                exp.convert_jpg()
        
    def calc_totalInt(self):
        """ Calculate total intensity for every image in every Experiment
        
        """
        for i, exp in self.exp.itervalues():
            if 'totalInt' in exp.data.keys():
                pass
            else:
                exp.calc_totalInt()
            
    def calc_flameHeight(self, nGauss = 2):
        """ Calculate flame height for every Experiment
        
        """
        for i, exp in self.exp.itervalues():
            if 'flammenhoehe' in exp.data.keys():
                pass
            else:
                exp.calc_flameHeight(nGauss)
        
    