# Least squares class for minuit minimizer
# Derek Fujimoto
# Oct 2020

cimport cython
cimport numpy as np
from scipy.misc cimport derivative 

cpdef class LeastSquares:
    
    # data arrays
    cdef double[:] x
    cdef double[:] y
    cdef double[:] dx
    cdef double[:] dy
    
    # function to fit
    cdef object fn

    def __init__(self, fn, double[:] x, double[:] y, dy=None, dx=None):
        self.fn = fn
        self.x = x
        self.y = y
        
        if dy is None:
            self.dy = np.zeros(len(x))
        else:
            self.dy = dy
            
        if dx is None:
            self.dx = np.zeros(len(x))
        else:
            self.dx = dx
            
    def __call__(self,*pars):
        
        fprime = 
