# -*- coding: utf-8 -*-

""" My Input and Output IO clas/file

"""
#standard library imports
import os
import logging
#related third party imports
import numpy as np
from PIL import Image as PILImage
#local application/library specific imports


class RnIo():
    """ My IO class
    
    """
    
    def __init__(self, workspace = ''):
        """ IO initialisation
        
        """
        self.workspace = workspace
    
    def write_nparray_csv(self, nparray, header = [], 
                            speichername = 'test.csv', 
                            delimiter = ';'):
        """ Write 2D nparray to ascii file
        
        nparray (nparray): 2D numpy data array
        header (arr): 1D python array of header
        speichername (str): name of file to write
        delimiter (str): delimiter which shall be used
        
        """
        #Assertions
        try:
            assert(isinstance(nparray, np.ndarray))
            assert(isinstance(header, list))
            assert(isinstance(speichername, str))
            assert(isinstance(delimiter, str))
        except AssertionError:
            logging.error('ein paramter hat nicht das passende format')
        
        #Code
        filepath = self.workspace + speichername
        with open(filepath, 'wb') as f:
            #check if header exists
            if len(header) > 0:
                _row = ''
                for entry in header:
                    _row += str(entry) + delimiter
                _row += '\n'
                f.write(_row)
                    
            for y in xrange(nparray.shape[0]):
                _row = ''
                for x in xrange(nparray.shape[1]):
                    _row += str(nparray[y, x]) + delimiter
                _row += '\n'
                f.write(_row)
                
    def read_csv_nparray(self, name = 'test.csv', 
                         header = False, 
                         delimiter = ';'):
        """ Reads csv file
        
        name (str): file name of file e.g. test.csv
        header (bool): if file has 1 line header set as True
        delimiter: delimiter of file
        
        Returns:
            header (arr)
            nparray
        
        """
        _header = []
        _arr = []
        filepath = self.workspace + name
        with open(filepath, 'rb') as f:
            #read header
            if header == True:
                _row = f.readline()
                _header = _row.split(delimiter)
                _header.pop() #remove \n element
                
            #read data
            for line in f.xreadlines():
                line = line.split(delimiter)
                line.pop() #remove new line char
                try:
                    line = [float(x) for x in line] #convert string to float
                except ValueError:
                    logging.error("""coud no convert string to float, wrong data
                    format ist given back!""")
                _arr.append(line)

        _arr = np.array(_arr)          
        return _header, _arr
                
    def write_nparray_Image(self, nparray, name = 'test.bmp', normiert = True):
        """ Write an 2D/3D nparray as an Image
        
        nparray (numpy arra): 2D/3D Numpy array
        name (str): filename of image
        normiert (bool): if true the Image will be normalized
        
        """
        filepath = self.workspace + name
        _image = PILImage.fromarray(nparray)
        
        if normiert == True:
            from PIL import ImageOps
            _image = ImageOps.autocontrast(_image, cutoff=0)
            
        _image.save(filepath)
        
    def read_Image_nparray(self, filepath):
        """ Reads Image with PIL and converts it to numpy array
        
        filepath (str): complete filepath to Image
        
        """
        #with open(filepath, 'rb') as _fp:
            #_fp = open(filepath, 'rb')
        img = PILImage.open(filepath)
            #_img = _img.convert('L')
            #_fp.close()
        #_arr = np.array(img)
        arr = np.array(img)
        return arr
    
                
    def read_fits_nparray(self, name = 'test.fit', number = 0):
        """ Read .fits file from iStar camera
        
        name (str): file name
        number (int): number of hdulist (usually 0)
        
        Returns:
            _header (pyfits.header.Header): dictionary type something
            _arr (numpy.ndarray): numpy array
        
        """
        import pyfits
        _file =self. workspace + name
        _fits = pyfits.open(_file)
        _header = _fits[number].header
        _arr = _fits[number].data
        _arr = _arr[0,:,:] #da nur 2D Array
        return _arr, _header
        


if __name__ == "__main__":
    """
    a = [[1,2,3], [4,5,6]]
    a = np.array(a)
    h = ['bla', 'blub', 'bloeb']
    myIO = RnIo()
    myIO.write_nparray_csv(a, header = h, delimiter = ';')
    nh, na = myIO.read_csv_nparray(header = True)
    print nh
    print na
    """
    #myIO= RnIo()
    #_h, _arr = myIO.read_fits_nparray()
    #print _h['temp'], _arr
    #print _arr.shape
    
    
    fp1 = 'C:/Python/testbilder/25927 11-16-19.bmp'
    fp2 = 'C:\Python\testbilder\25927 11-16-19.bmp'
    myIO = RnIo()
    myarr = myIO.read_Image_nparray(fp1)
