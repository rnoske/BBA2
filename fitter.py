# -*- coding: utf-8 -*-

#Fitting class!
import numpy as np
from scipy.optimize import leastsq
import matplotlib.pyplot as plt
from multiprocessing import Pool, Process

class Fitter():
    """ Class for fitting data
    
    """
    
    def create_testdata(self):
        """ creates two gaussion functions as testdata
        
        Returns:
            np.array testdata
        
        """
        # Setting up test data
        def norm(x, mean, sd):
          norm = []
          for i in range(x.size):
              norm += [1.0/(sd*np.sqrt(2*np.pi))*np.exp(-(x[i] - mean)**2/(2*sd**2))]
          return np.array(norm)
        
        mean1, mean2 = 0, -2
        std1, std2 = 0.5, 1 
        
        x = np.linspace(-20, 20, 500)
        y_real = norm(x, mean1, std1) + norm(x, mean2, std2)
        return x, y_real
        
    def beispiel(self):
        """ Testbeispiel. Muss mit creat_testdata zusammen funktionieren!
        
        """
        def norm(x, mean, sd):
            norm = []
            for i in range(x.size):
                norm += [1.0/(sd*np.sqrt(2*np.pi))*np.exp(-(x[i] - mean)**2/(2*sd**2))]
            return np.array(norm)
        x, y_real = self.create_testdata()
        # Solving
        m, dm, sd1, sd2 = [5, 10, 1, 1]
        p = [m, dm, sd1, sd2] # Initial guesses for leastsq
        y_init = norm(x, m, sd1) + norm(x, m + dm, sd2) # For final comparison plot
        
        def res(p, y, x):
            m, dm, sd1, sd2 = p
            m1 = m
            m2 = m1 + dm
            y_fit = norm(x, m1, sd1) + norm(x, m2, sd2)
            err = y - y_fit
            return err
        
        plsq = leastsq(res, p, args = (y_real, x))        
        y_est = norm(x, plsq[0][0], plsq[0][2]) + norm(x, plsq[0][1], plsq[0][3])
        
        plt.plot(x, y_real, label='Real Data')
        plt.plot(x, y_init, 'r.', label='Starting Guess')
        plt.plot(x, y_est, 'g.', label='Fitted')
        plt.legend()
        plt.show()
        
        return plsq
        
    def gauss_norm(self, x, mean, sd):
        norm = []
        for i in range(x.size):
            norm += [1.0/(sd*np.sqrt(2*np.pi))*np.exp(-(x[i] - mean)**2/(2*sd**2))]
        return np.array(norm)
        
    def multi_gauss_fit_norm(self, x, y, n, m, s, plotflag = False):
        """ Fit n Gauss functions do data
        
        x (np.array): numpy array with x-axis
        y (np.array): numpy array with data
        n (int): number of Gauss functions to fit
        m (np.array): m[0]= initial mean value for first gauss
                    m[n]= differenzes to mean before    
        s (np.array): array of standard deviations
        plotflag (bool): if true an graph is plottet
        
        Example:
            n = 2
            m = [5., 5.]
            s = [1, 1]
            x, y_real = myfitter.create_testdata()
            multiGaussFit(x, y_real, n, m, s)
            
        """    
        # Initial fit
        y_init = self.gauss_norm(x, m[0], s[0])
        for i in xrange(1, n):
            y_init += self.gauss_norm(x, m[i]+m[i-1], s[i])
                
        def res(p, y, x):
            #initialisation of paramters
            m = []
            s = []
            for i in xrange(n):
                m.append(p[i])
                s.append(p[i+n])
            absm = []
            for i in xrange(n):
                if i == 0:
                    absm.append(m[i])
                elif i >= 1:
                    absm.append(m[i] + m[i-1])
            #generation fit function
            y_fit = self.gauss_norm(x, absm[0], s[0])
            for i in xrange(1,n):
                y_fit += self.gauss_norm(x, absm[i], s[i]) 
            err = y - y_fit
            return err
        #parameter magic, notwendig um paramter für leastsq zu bekommen
        p = []
        for item in m:
            p.append(item)
        for item in s:
            p.append(item)
        p = np.array(p)
        param, success = leastsq(res, p, args = (y, x))
        #print param
        
        
        
        #plotting
        if plotflag == True:
            #result function
            y_est = self.gauss_norm(x, param[0], param[n])
            for i in xrange(1, n):
                y_est += self.gauss_norm(x, param[i+0], param[i+2])
            
            plt.plot(x, y, label='Real Data')
            plt.plot(x, y_init, 'r.', label='Starting Guess')
            plt.plot(x, y_est, 'g.', label='Fitted')
            plt.legend()
            plt.show()
        
        return param
        
        
    def gauss(self, x, b, a, mean, sd):
        """
        gauss = []
        for i in range(x.size):
            gauss.append(b+a*np.exp(-((x[i]-mean)/sd)**2))
        return np.array(gauss)
        """
        return b+a*np.exp(-((x-mean)/sd)**2)
      
    def multi_gauss_fit(self, x, y, n, b, a, m, s, plotflag = True, savefp = ''):
        """ Fit n Gauss functions do data
        
        x (np.array): numpy array with x-axis
        y (np.array): numpy array with data
        n (int): number of Gauss functions to fit
        b (int): offset of gauss functions
        a (np.array): preexponential factors
        m (np.array): m[0]= initial mean value for first gauss
                    m[n]= initial guess for mean value, diffrent from norm 
                    gauss fit
        s (np.array): array of standard deviations
        plotflag (bool): if true an graph is plottet
        savefp (str): Filepath to save to; saved if str != ''
        
        Example:
            n = 2
            m = [5., 5.]
            s = [1, 1]
            x, y_real = myfitter.create_testdata()
            multiGaussFit(x, y_real, n, m, s)
            
        Returns:
            b, a, m, s
            
        """           
        def res(p, y, x):
            #initialisation of paramters
            b = p[0]
            a = []
            m = []
            s = []
            for i in xrange(n):
                a.append(p[i+1]) #+1 because 0 is offset b
                m.append(p[i+1+n]) #3 because 3 params
                s.append(p[i+1+(2*n)])
                #print a, m, s
              
            #generation fit function
            y_fit = self.gauss(x, b, a[0], m[0], s[0])
            for i in xrange(1,n):
                y_fit += self.gauss(x, b, a[i], m[i], s[i])
            err = y - y_fit
            return err
        #parameter magic, notwendig um paramter für leastsq zu bekommen
        p = []
        p.append(b)
        for item in a:
            p.append(item)
        for item in m:
            p.append(item)
        for item in s:
            p.append(item)
        p = np.array(p)
        param, success = leastsq(res, p, args = (y, x))
        #print param
        
        #result function
        b = param[0]
        a = []
        m = []
        s = []
        for i in xrange(n):
            a.append(param[i+1]) #+1 because 0 is offset b
            m.append(param[i+1+n]) #3 because 3 params
            s.append(param[i+1+(2*n)])
            #print a, m, s     
        
        #plotting
        #generation fit function
        y_est = self.gauss(x, b, a[0], m[0], s[0])
        for i in xrange(1,n):
            y_est += self.gauss(x, b, a[i], m[i], s[i])
        
        plt.cla()
        plt.plot(x, y, 'bo', label='Real Data')
        plt.plot(x, y_est, 'g-', label='Fitted')
        plt.legend()
        if savefp != '':
            _fp = savefp +'.jpg'
            plt.savefig(_fp)
            _data = []
            for i in xrange(len(x)):
                _data.append([x[i], y[i], y_est[i]])
            _data = np.array(_data)
            _fp = savefp+'.txt'
            np.savetxt(_fp, _data, delimiter=';')
        if plotflag == True:
            plt.show()
        
        return b, a, m, s
      
    def multi_beispiel(self):
        jobs = []
        n = 2
        for i in xrange(n):
            p = Process(target=self.beispiel)
            jobs.append(p)
            p.start()
        
        p.join()
        
        for j in jobs:
            print '%s.exitcode = %s' % (j.name, j.exitcode)
        
        
        
if __name__ == "__main__":
    myfitter = Fitter()
    #myfitter.multi_beispiel()
    
    n = 2
    b = 0.
    a = [1., 1.]
    m = [-5., 0.]
    s = [1., 1.]
    x, y_real = myfitter.create_testdata()
    param = myfitter.multi_gauss_fit(x, y_real, n, b, a, m, s)
    