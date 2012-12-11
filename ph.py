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
import rnio
import xml.etree.ElementTree as et

class Ph():
    """ Program handler
    
    """
    def __init__(self):
        """ Initialisation
        
        """
        self.cf = Config.Config(filename = 'Settings.ini')
        self.sdict = self.get_settings()
        #dictionary of all experiments
        self.exp = OrderedDict()
        #unique number of experiment /total number of experiments active
        self.ident = 1
        #my io module
        self.rnio = rnio.RnIo()
        
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
        
    def add_new_experiment(self, path, oldident = None):
        """ Create and add an new experiment
        
        path (str): path to experiment folder
        oldident (int): old identification number from old save
        
        """
        if oldident == None:
            _exp= experiment.Experiment(path, self.ident, sdict = self.sdict)
            self.exp[str(self.ident)] = _exp
        else:
            _exp= experiment.Experiment(path, oldident, sdict = self.sdict)
            self.exp[str(self.ident)] = _exp
            
            
        if oldident == None:
            self.ident += 1
        else:
            if oldident >= self.ident:
                self.ident = oldident
            else:
                self.ident += 1
                
            
        
    def _startup_experiments(self):
        """ Loads experiments from standard location
        
        """
        sfbxml = 'D:/Raimund Auswertung/Stephan/sfb.xml'
        
    def write_toXMLfile(self):
        """ Write all experiments to sfb xml file
        
        """
        sfbxml = self.sdict['sfbxml']
        self._make_sfbxmlfile(sfbxml)
        
        
    def _make_sfbxmlfile(self, sfbxml):
        """ Internal function for saving in xml file
        
        """
        #make xml root
        series = et.Element('Series')
        #für jedes experiment...
        for _exp in self.exp.itervalues():
            #create experiment element
            _exp_el = et.Element('Experiment')
            _exp_el.attrib['id'] = _exp.att['id']
            _exp_el.attrib['path'] = _exp.att['path']  
            #add description element
            _desc_el = et.Element('Description')
            _desc_el.text = _exp.att['description']
            _exp_el.append(_desc_el)
            #add parameteres
            #TODO add parameteres as necessary
            _param_el = et.Element('Parameters')
            for key, value in _exp.parameters.iteritems():
                _input_el = et.Element('Input')
                _input_el.attrib[key] = value
                _param_el.append(_input_el)
            _exp_el.append(_param_el)
            #add Measurements
            for name, bild in _exp.bd.iteritems():
                _measure_el = et.Element('Measurement')
                _measure_el.attrib['name'] = bild.att['name']
                _measure_el.attrib['phase'] = str(bild.att['phase'])
                _exp_el.append(_measure_el)
                
            
            
            #add experiment to series
            series.append(_exp_el)
            
        #write to xml file
        tree = et.ElementTree(series)
        tree.write(sfbxml)
        
    def read_sfbxmlfile(self):
        """ Read sfb xml file
        
        """
        sfbxml = self.sdict['sfbxml']
        #open elementtree
        tree = et.parse(sfbxml)
        series = tree.getroot()
        for _exp_el in series.findall('Experiment'):
            print _exp_el, _exp_el.tag, _exp_el.attrib
            _path = _exp_el.attrib['path']
            _id = _exp_el.attrib['id']
            self.add_new_experiment(str(_path), int(_id))
            #adding parameters to experiment
            for _para_el in _exp_el.findall('Parameters'):
                for _input_el in _para_el.findall('Input'):
                    for key, value in _input_el.attrib.iteritems():
                        self.exp[str(_id)].parameters[key] = value
                
            
        
        
    def convert_jpg(self):
        """ Convert images in Experiment to jpg
        
        """
        for exp in self.exp.itervalues():
            if 'convertet_to_jpg' in exp.data.keys():
                pass
            else:
                exp.convert_jpg()
        
    def calc_totalInt(self):
        """ Calculate total intensity for every image in every Experiment
        
        """
        for exp in self.exp.itervalues():
            if 'totalInt' in exp.data.keys():
                pass
            else:
                exp.calc_totalInt()
            
    def calc_flameHeight(self, nGauss = 2):
        """ Calculate flame height for every Experiment
        
        """
        for exp in self.exp.itervalues():
            if 'flammenhoehe' in exp.data.keys():
                pass
            else:
                exp.calc_flameHeight(nGauss)
        
if __name__ == "__main__":
    ph = Ph()
    ph.read_sfbxmlfile()