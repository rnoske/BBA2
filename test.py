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
    
    #_arr = spimg.interpolation.rotate(_arr, -0.95+90, order = 5, reshape=False)
    #_arr = _arr[1024-650:1024-350, 425:675]
    
    return _arr
    
if __name__ == "__main__":
    base = 'E:/Raimund Auswertung/Stephan/ukd0lg-08_12-sb/fits'
    fp = base + '/08_12_14.41.10_21.fits'
    
    _arr = open_image(fp)
    
    import scipy.ndimage.filters as spfilter
    _arr = spfilter.median_filter(_arr, size = (3,3))
    
    print _arr.min()
    _arr -= _arr.min()
    
    from scipy import ndimage
    _com = ndimage.measurements.center_of_mass(_arr)
    print _com
    
    """
    s0 = _arr.sum(axis=1)
    x = np.arange(len(s0))
    
    s0 = (s0-s0.min())
    s0 = s0/s0.max()
    
    s0_s = s0.sum()
    s0_t  = 0
    for i in xrange(len(s0)):
        s0_t += (s0[i]) * i
    
    cog = s0_t/s0_s
    print cog
    
    
    cs = np.cumsum(s0)

    
    _tmean = s0.sum() / 2
    _tsum = 0
    for i in xrange(len(s0)):
        _tsum += s0[i]
        if _tsum >= _tmean:
            print i
            break
            
            
    
    plt.plot(x, s0)
    plt.show()
    """
    
    """
    plt.cla()
    plt.clf()
    plt.imshow(arr)
    plt.colorbar()
    plt.savefig('arr4.jpg')
    plt.show()
    """