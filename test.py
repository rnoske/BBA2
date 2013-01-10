# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import scipy.ndimage as spimg

#related third party imports
import numpy as np # NumPy (multidimensional arrays, linear algebra, ...)

#local application/library specific imports
import rnio
import fitter

def open_image(pfad):
    """ Opens and returns an PIL image
    
    """
    myrnio = rnio.RnIo()
    _arr, _header = myrnio.read_fits_nparray(pfad)
    #_arr = _arr[350:650, 425:675]
    
    _arr = spimg.interpolation.rotate(_arr, -0.95+90, order = 5, reshape=False)
    _arr = _arr[1024-650:1024-350, 425:675]
    
    return _arr
    
if __name__ == "__main__":
    base = 'D:/Raimund Auswertung/Stephan/ukd0lg-08_12_b/UG11/fits'
    fp = base + '/08_11_Fri Jan  4 2013_14.39.34_0.fits'
    
    #fp2 = 'D:/Raimund Buero/Python/SpyDev/gridfit/3cm.fits'
    fp2 = 'D:/Raimund Buero/Python/SpyDev/gridfit/full.fits'
    #fp2 = 'D:/Raimund Buero/Python/SpyDev/gridfit/rot-full.fits'
    #fp2 = 'D:/Raimund Buero/Python/SpyDev/gridfit/rot-sub.fits'
    
    #flame = open_image(fp)
    
    arr = open_image(fp2)
    #arr = arr[425:675, 350:650]
    #arr = arr[350:650, 425:675]
    
    print arr.shape
    

    
    #plt.cla()
    #plt.clf()
    #plt.imshow(flame)
    #plt.colorbar()
    #plt.savefig('flame.jpg')
    #plt.show()
    
    plt.cla()
    plt.clf()
    plt.imshow(arr)
    plt.colorbar()
    plt.savefig('arr4.jpg')
    plt.show()