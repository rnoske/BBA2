# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 15:38:42 2013

@author: rnoske
"""
import os
import numpy as np
import pandas as pd

def load_rmd(path, header=True):
    """ load rmd file
    
    path (str): complete filepath to .rmd file
    
    """
    if os.path.exists(path):
        print 'Pfad: ' + path + ' existiert!'
        
    with open(path, 'rb') as f:
        if header == True:
            _lenHeader = 2
            for line in xrange(_lenHeader):
                _row = f.readline()
                _header = _row.split()
                #_header.pop() #remove \n element
                print _header
        data = []
        for line in f.xreadlines():
            #print line
            line = line.split()
            _row = []
            for entry in line:
                _row.append(float(entry))
            data.append(_row)
        data = np.array(data)
        print data.shape[0], data.shape[1]
    
    
    

if __name__ == "__main__":
    fp = 'D:/Raimund Buero/Python/SpyDev/BBA2/test.mat.rmd'
    load_rmd(fp)