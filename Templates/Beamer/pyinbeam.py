'''
Created on Sep 23, 2010

@author: langevin
'''

import numpy

def binaryread(file, vartype, shape=(1), charlen=16):
    """Read text, a scalar value, or an array of values from a binary file.
       file is an open file object
       vartype is the return variable type: str, numpy.int32, numpy.float32, 
           or numpy.float64
       shape is the shape of the returned array (shape(1) returns a single value)
           for example, shape = (nlay, nrow, ncol)
       charlen is the length of the text string.  Note that string arrays cannot
           be returned, only multi-character strings.  Shape has no affect on strings.
    """
    import struct
    
    #store the mapping from type to struct format (fmt)
    typefmtd = {numpy.int32:'i', numpy.float32:'f', numpy.float64:'d'}
        
    #read a string variable of length charlen
    if vartype is str:
        result = file.read(charlen*1)
        
    #read other variable types
    else:
        fmt = typefmtd[vartype]
        #find the number of bytes for one value
        numbytes = vartype(1).nbytes
        #find the number of values
        nval = numpy.core.fromnumeric.prod(shape)
        fmt = str(nval) + fmt
        s = file.read(numbytes * nval)
        result = struct.unpack(fmt, s)
        if nval == 1:
            result = vartype(result[0])
        else:
            result = numpy.array(result, dtype=vartype)
            result = numpy.reshape(result, shape)
    return result