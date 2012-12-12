# -*- coding: utf-8 -*-

"""
Basic bild class for handling taken images.
"""
"""
logging info:
DEBUG	Detailed information, typically of interest only when diagnosing problems.
INFO	Confirmation that things are working as expected.
WARNING	An indication that something unexpected happened, or indicative of 
    some problem in the near future (e.g. ‘disk space low’). The software is 
    still working as expected.
ERROR	Due to a more serious problem, the software has not been able to perform 
    some function.
CRITICAL	A serious error, indicating that the program itself may be unable 
    to continue running.
"""

#standard library imports
import logging
#import sys
import os
import threading
import math

import multiprocessing as mp
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

#related third party imports
import numpy as np # NumPy (multidimensional arrays, linear algebra, ...)

#local application/library specific imports
import rnio
import fitter


#Scientific imports, idea taken from spyder

#import scipy as sp # SciPy (signal and image processing library)
#import matplotlib as mpl         # Matplotlib (2D/3D plotting library)
#import matplotlib.pyplot as plt  # Matplotlib's pyplot: MATLAB-like syntax
#from pylab import *              # Matplotlib's pylab interface
#ion()                            # Turned on Matplotlib's interactive mode



#Actual code
class Bild:
    """ Basic image class. All other images inherit from this class.
    
    Creates:
        bid (int) = bild id/number
    """
    lock = threading.Lock()
    bid_count = 0
    
    def __init__(self, pfad, **kwargs):
        """ Initialize attributes
        
        and example docstring
        Args:
            pfad (str): File path of image
        
        Kwargs:
            none (yet)
            
        Returns:
            nothing
            
        Creates:
            self.att (dic): empty dictionary for holding image attributes
            
        Raises:
            nothing
            
        Use me if you want to create an image
        
        """
        self.att = {} #attribute directory
        self.rnio = rnio.RnIo()
        self.fitter = fitter.Fitter()
        #checks if pfad is valid
        if os.path.exists(pfad) == True:
            self.pfad = str(pfad)
            logging.info('Image pfad was set: %s', pfad)
        
    def startup(self):
        """ Startup of bild instance. should be used at creation of bild
        
        """
        self.calc_name()
        with Bild.lock:
            self.att['bid'] = Bild.bid_count
            Bild.bid_count += 1
                            
        #setze/finde Dateiendung
        _end = self.pfad.split('.')
        _end = _end.pop()
        _endungen = ['bmp', 'jpg', 'fit', 'fits']
        if _end in _endungen:
            self.att['endung'] = _end
            logging.info('Bildendung erkannt')
        else:
            print 'Dateiendung nicht bekannt!'
    
    def calc_name(self):
        """ Set a name for the image.
        
        """
        pfad = self.pfad.replace('/','\\')
        namen = str(pfad).split(os.sep)
        name = namen.pop()
        self.att['name']=name
        _bn = name.rstrip('.fits')
        self.att['basisname'] = _bn
        _tmp = _bn.split('_')
        _tmp = _tmp.pop()
        try:
            self.att['phase'] = float(_tmp) * float(self.degree_image)
        except (TypeError):
            print 'Phase im Dateinamen nicht erkannt!'
        
    def open_image(self):
        """ Opens and returns an PIL image
        
        """
        _endl1 = ['bmp', 'jpg']
        _endl2 = ['fit', 'fits']
        if self.att['endung'] in _endl1:
            _arr = self.rnio.read_Image_nparray(self.pfad)
            return _arr
            logging.info('Bild geoeffnet')
        elif self.att['endung'] in _endl2:
            if hasattr(self, 'image'):
                return self.image
            else:
                _arr, _header = self.rnio.read_fits_nparray(self.pfad)
                #wenn fits image, behalte datei im arbeitsspeicher  
                self.image = _arr
                #plt.imshow(self.image)
                #plt.show()
                #save image
                """
                _fp = self.sdict['workspace']+'/originalImage/'
                if not os.path.exists(_fp):
                    os.makedirs(_fp)
                _fp += str(self.att['basisname']) +'.jpg'
                plt.imsave(_fp, self.image, origin = 'lower')
                """
                return self.image
        else:
            logging.error('Dateiendung konnte nicht geoeffnet werden')
            
        
        
    def create_array(self):
        """ Create and numpy array from open image
        
        Returns:
            np.array
            
        """
        #self.att['hoehe'] = np.array(self.open_image()).shape[0]
        #self.att['breite'] = np.array(self.open_image()).shape[1]
        _arr = self.open_image()
        #_arr = _arr[0,:,:]
        return _arr
        
    def convert_to_jpg(self):
        """ Convert and save the image as jpg
        
        """
        _arr = self.open_image()
        _fp = self.workspace+'/jpg/'
        if not os.path.exists(_fp):
                    os.makedirs(_fp)
        _fp += str(self.att['basisname']) +'.jpg'
        import scipy.misc
        scipy.misc.imsave(_fp, _arr)
        
    def calc_totalInt(self):
        """ Calculate total Pixel count of image
        
        """
        _arr = self.open_image()
        self.att['totalInt'] = _arr.sum()
        hoehe = _arr.shape[0]
        breite = _arr.shape[1]
        _apx = breite * hoehe
        self.att['mittelInt'] = self.att['totalInt'] / _apx
        
    def calc_flammenhoehe(self):
        """ Calculate flame height for image
        
        """
        #load needed Settings
        nullpunkt = int(self.zero)
        flammenmitte = int(self.flame_center)
        aufloesung = float(self.resolution)
        _arr = self.open_image()
        
        #nehme nur blauen farbkanal
        #if _arr.shape[2] > 1:
        #    _arr = _arr[:,:,2]
        
        #Check if nullpunkt and flammenmitte have valid values
        hoehe = _arr.shape[0]
        breite = _arr.shape[1]
        if nullpunkt < 0 or nullpunkt > hoehe:
            #print 'nullpunkt falsch'
            logging.error('Nullpunkt nicht innerhalb des Bildes')
        elif flammenmitte < 0 or flammenmitte > breite:
            #print 'flammenmitte falsch'
            logging.error('Flammenmitte nicht innerhalb des Bildes')

        #calculation
        #roi = arr[:,flammenmitte-breite:flammenmitte+breite]
        #roi = roi.sum(axis=1)
        _roi = _arr[:,flammenmitte]
        _posMax = np.argmax(_roi)
        #print _posMax
        self.att['flammenhoehe'] = (nullpunkt - _posMax) / aufloesung
        self.att['flammenhoeheIndex'] = _posMax

        
    def calc_flammenhoeheGauss(self, nGauss = 2):
        """ Calculate flame height with gauss fit
        
        """
        #load needed Settings
        nullpunkt = int(self.zero)
        flammenmitte = int(self.flame_center)
        aufloesung = float(self.resolution)
        _arr = self.open_image()
        
        #nehme nur blauen farbkanal
        #if _arr.shape[2] > 1:
        #    _arr = _arr[:,:,2]
        
        #Check if nullpunkt and flammenmitte have valid values
        hoehe = _arr.shape[0]
        breite = _arr.shape[1]
        if nullpunkt < 0 or nullpunkt > hoehe:
            #print 'nullpunkt falsch'
            logging.error('Nullpunkt nicht innerhalb des Bildes')
        elif flammenmitte < 0 or flammenmitte > breite:
            #print 'flammenmitte falsch'
            logging.error('Flammenmitte nicht innerhalb des Bildes')
        #Calculations
        _roi = _arr[:,flammenmitte]
        _guessMax = np.argmax(_roi)        
        # fitting process
        y = _roi
        _max = len(y)-1
        x = np.linspace(0,_max, len(y))
        n = nGauss #1 gauss
        b = 1
        a = [50]*n
        m = [_guessMax]*2 #da nur ein gaus nur ein eintrag
        s = [10]*n
        
        _fp = self.workspace+'/flammenHoeheGauss/'
        if not os.path.exists(_fp):
            os.makedirs(_fp)
        _fp += str(self.att['basisname'])
                
        b, a, m, s = self.fitter.multi_gauss_fit(x, y, n, b, a, m, s, 
                                                 plotflag = False, savefp = _fp)
        #print b, a, m, s
        #defining flame attributes
        m.sort()
        for i in xrange(nGauss):    
            self.att['flammenhoeheGauss'+str(i)] = (nullpunkt - m[i]) / aufloesung
            self.att['flammenhoeheGaussIndex'+str(i)] = m[i] #_posMax
            self.att['flammenhoeheGaussVarianz'+str(i)] = s[i] / aufloesung
        
    
    def calc_flammenbreite_single(self, work_q, result_q):
        """ Calculate the flame width by fitting two gauss
        
        roi (np.array): horizontale roi des bildes
        """
        while True:
            flammenmitte = int(self.flame_center)
            
            index, roi = work_q.get()
            guessleft = np.argmax(roi[:flammenmitte])
            guessright = np.argmax(roi[flammenmitte:]) + flammenmitte
            
            # fitting process
            y = roi
            _max = len(y)-1
            x = np.linspace(0,_max, len(y))
            n = 2 #2 gauss
            b = 10
            a = [50, 50]
            m = [guessleft, guessright] #da nur ein gaus nur ein eintrag
            s = [10, 10]
            
            b, a, m, s = self.fitter.multi_gauss_fit(x, y, n, b, a, m, s, plotflag = False)
            #print b, a, m, s
            #print m, a
            result_q.put([index, b, a, m, s])
            work_q.task_done()
            #return b, a, m, s
        
    
    def calc_flammenbreite(self):
        """ Calculate the flame width
        
        Creates:
            2D image
            
        """
        _arr = self.open_image()
        nullpunkt = int(self.zero)
        
        if 'flammenhoeheIndex' in self.att.keys():
            flammenhoehe = self.att['flammenhoeheIndex']
        else:
            self.calc_flammenhoehe()
            flammenhoehe = self.att['flammenhoeheIndex']
        
        #nehme nur blauen farbkanal
        #if _arr.shape[2] > 1:
        #    _arr = _arr[:,:,2]
            
        #schneide array zurecht:
        _arr = _arr[flammenhoehe:nullpunkt, :]
        
        #multiprocessing setup
        num_workers = mp.cpu_count() #number of worker processes
        work_q = mp.JoinableQueue() #work queue
        result_q = mp.Queue() #Queue for results
        
        #put tasks into work_q
        for i in xrange(_arr.shape[0]):
            _troi = _arr[i, :]
            _work = (i, _troi)
            work_q.put(_work)
            
            
        #setup workers
        workers = []
        for i in xrange(num_workers):
            workers.append(mp.Process(target=self.calc_flammenbreite_single, 
                                   args=(work_q, result_q)))
        
        #start workers                   
        for w in workers:
            #print w
            w.daemon = True
            w.start()
        work_q.join()
        
        
        #get results out of results_q
        _tarr = []
        n_result = result_q.qsize()
        for result in xrange(n_result):
            _t = result_q.get()
            _tarr.append(_t)
            
            
        #close queues
        work_q.close()
        result_q.close()
        result_q.join_thread()
        
        #terminate workers
        for w in workers:
            w.terminate()
            
        _tarr.sort() #returns sorted array
        
        _tarea = [] #calculate the area
        for item in _tarr:
            #print item[3]
            _tarea.append(item[3])
            
        #reconstruct image and display it
        _img = []
        for item in _tarr:
            _x = np.arange(0, _arr.shape[1], 1)
            _g1 = self.fitter.gauss(_x, item[1], item[2][0], item[3][0], item[4][0])
            _g2 = self.fitter.gauss(_x, item[1], item[2][1], item[3][1], item[4][1])
            _img.append(_g1+_g2)
        _img = np.array(_img)
        #plt.imshow(_img)
        #plt.show()

            
        print 'Finished calculating flame area for image' + str(self.att['name'])
        
        return _tarea
      
    def calc_flammenoberflaecheGauss(self):
        """ Calculate the flame area
        
        """
        aufloesung = float(self.resolution)
        
        _tarea = self.calc_flammenbreite()
        _tarea = np.array(_tarea)
        _left = _tarea[:,0]
        _right = _tarea[:,1]
        area = 0.0
        for i in xrange(len(_left)-1):
            area += math.sqrt((_left[i]-_left[i+1])**2 + 1)
            area += math.sqrt((_right[i]-_right[i+1])**2 + 1)
        area += _right[len(_right)-1] - _left[len(_left)-1]
        #print area / aufloesung
        self.att['flammenoberflaecheGauss'] = area / aufloesung
        
    def calc_flammenflaeche(self):
        """ Calculate flame area (simple)
        
        """
        aufloesung = float(self.resolution)
        aufloesung = (1./aufloesung)**2
        _arr = self.open_image()
        _arr = _arr.flat
        self.calc_totalInt()
        _mI = self.att['mittelInt']
        _sw = _mI
        _c = 0
        for item in _arr:
            if item > _sw:
                _c += 1
        _c = _c * aufloesung
        self.att['flammenflaeche'] = _c
        return _c
        
        