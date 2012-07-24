#--2d real array utilities 
#--for reading, writing and plotting
#--ASCII 2-D MODFLOW real arrays

#--libraries
import numpy as np
import os
import math
import sys
import pylab
from pylab import *                      
from matplotlib import colors, cm
import time

#import blnUtil
#reload(blnUtil)


def mapBndCellsArray(nrow,ncol,bndcells,**kwargs):  
    try:
        parm = kwargs['parm']
    except:
        parm = ''
    array = np.zeros((nrow,ncol),dtype='double')-1.0e+30
    for cells in range(0,len(bndcells)): 
        if cmp(parm,'stage') == 0:
            array[(bndcells[cells].row)-1,(bndcells[cells].column)-1] = bndcells[cells].stage
        elif cmp(parm,'rate') == 0:
            array[(bndcells[cells].row)-1,(bndcells[cells].column)-1] = bndcells[cells].rate
        elif cmp(parm,'concen') == 0:
            array[(bndcells[cells].row)-1,(bndcells[cells].column)-1] = bndcells[cells].concen
        elif cmp(parm,'cond') == 0:
            array[(bndcells[cells].row)-1,(bndcells[cells].column)-1] = bndcells[cells].cond
        elif cmp(parm,'int') == 0:
            array[(bndcells[cells].row)-1,(bndcells[cells].column)-1] = 1
        else:        
            try:
                array[(bndcells[cells].row)-1,(bndcells[cells].column)-1] = bndcells[cells].stage
            except:
                try:
                    array[(bndcells[cells].row)-1,(bndcells[cells].column)-1] = bndcells[cells].rate
                except:
                    try:
                        array[(bndcells[cells].row)-1,(bndcells[cells].col)-1] = bndcells[cells].concen
                    except:
                        raise TypeError 
    return array




def loadArrayFromFile(nrow,ncol,file):
    '''
    read 2darray from file
    file(str) = path and filename
    '''
    try:
        file_in = open(file,'r')
        openFlag = True
    except:
#       assert os.path.exists(file)
        file_in = file
        openFlag = False
    
    data = np.zeros((nrow*ncol),dtype='double')-1.0E+10
    d = 0
    while True:
        line = file_in.readline()
        if line is None or d == nrow*ncol:break
        raw = line.strip('\n').split()
        for a in raw:
            try:
                data[d] = float(a)
            except:
                print 'error casting to float on line: ',line
                sys.exit()
            if d == (nrow*ncol)-1:
                assert len(data) == (nrow*ncol)
                data.resize(nrow,ncol)
                return(data) 
            d += 1  
    file_in.close()
    data.resize(nrow,ncol)
    return(data)

def loadRealArrayFromBinaryFile(nrow,ncol,file,realbyte=4):
    '''
    read 2darray from file
    file(str) = path and filename
    '''
    if realbyte == 4:
        dtype_np = np.float
        tsize    = np.float32
    elif realbyte == 8:
        dtype_np = np.double    
        tsize    = np.float64
    try:
        f = open(file,'rb')
    except:
#       assert os.path.exists(file)
        f = file
        return False, np.zeros( (nrow,ncol), dtype_np )
    
    data=np.fromfile(file=f, dtype=tsize, count=nrow*ncol)
    data.shape=(nrow,ncol)
    f.close()
    return True, data

def loadSurferGrdFromFile(file):
    '''
    read 2darray from file
    file(str) = path and filename
    '''
    try:
        file_in = open(file,'r')
        openFlag = True
    except:
#       assert os.path.exists(file)
        file_in = file
        openFlag = False
    
    line = file_in.readline()  #dssa
    line = file_in.readline()  #ncol nrow
    raw = line.split()
    try:
        ncol = int( raw[0] )
        nrow = int( raw[1] )
    except:
        print 'error parsing ncol and nrow on line:\n  ',line
        sys.exit()
    line = file_in.readline()  #xmin xmax
    raw = line.split()
    try:
        xmin = float( raw[0] )
        xmax = float( raw[1] )
    except:
        print 'error parsing xmin and xmax on line:\n  ',line
        sys.exit()
    line = file_in.readline()  #ymin ymax
    raw = line.split()
    try:
        ymin = float( raw[0] )
        ymax = float( raw[1] )
    except:
        print 'error parsing ymin and ymax on line:\n  ',line
        sys.exit()
    line = file_in.readline()  #zmin zmax
    raw = line.split()
    try:
        zmin = float( raw[0] )
        zmax = float( raw[1] )
    except:
        print 'error parsing zmin and zmax on line:\n  ',line
        sys.exit()
    
    #calculate cell size and offset
    dx = ( xmax - xmin ) / float( ncol - 1 )
    dy = ( ymax - ymin ) / float( nrow - 1 )
    x0 = xmin - 0.5 * dx
    y0 = ymin - 0.5 * dy
    offset   = [ x0, y0 ]
    cellsize = [ dx, dy ]
    
    data = np.zeros((nrow*ncol),dtype='double')-1.0E+10
    d = 0
    while True:
        line = file_in.readline()
        if line is None or d == nrow*ncol:break
        raw = line.strip('\n').split()
        for a in raw:
            try:
                data[d] = float(a)
            except:
                print 'error casting to float on line: ',line
                sys.exit()
            if d == (nrow*ncol)-1:
                assert len(data) == (nrow*ncol)
                data.resize(nrow,ncol)
                #return nrow,ncol,data
                exit
            d += 1  

    file_in.close()
    #print nrow, ncol

    data.resize(nrow,ncol)
    #invert data to modflow orientation
    data = np.flipud(data)
    #mask where less than zmin
    data = np.ma.masked_less( data, zmin )
    #mask where greater than zmax
    data = np.ma.masked_greater( data, zmax )
    return nrow,ncol,offset,cellsize,data


def ref2grd(file,ref,nrow,ncol,offset,delt,nodata=-999):
    f = open(file,'w')
    f.write('ncols '+str(ncol)+'\n')
    f.write('nrows '+str(nrow)+'\n')
    f.write('xllcorner '+str(offset[0])+'\n')
    f.write('yllcorner '+str(offset[1])+'\n')
    f.write('cellsize '+str(delt)+'\n')
    f.write('nodata_value {0}\n'.format( nodata ))
    writeArrayToFile(ref,f,nWriteCol=ncol) 
    f.close()
    return
        

    
def writeArrayToFile(array,file,**kwargs):
    '''
    write 2-d array to file
    nWriteCol(int) = number of columns in output file array
    oFormat(str) = output format ex: {0:12.4E}
    file(str) = path and filename
    '''
    
    #--get keyword arguments
    try:
        nWriteCol = kwargs['nWriteCol']
    except:
        nWriteCol = 10
    
    try:
        oFormat = kwargs['oFormat']
        if len(oFormat) == 1:
            if cmp(oFormat,'i') == 0 or cmp(oFormat,'I') == 0:
                oFormat = '{0:3.0f}'
    except:
        oFormat = '{0:14.6E}'
    
    
    assert len(np.shape(array)) == 2
    nrow,ncol = np.shape(array)
    #--check for line return flag at end each column
    if ncol%nWriteCol == 0:
        lineReturnFlag = False
    else:
        lineReturnFlag = True   
        
    #--try to open file, if fail, file is an open fileobj       
    try:
        file_out = open(file,'w')
        openFlag = True
    except:
        file_out = file
        openFlag = False
            
    #--write the array                      
    for a in range(0,nrow):
        for b in range(0,ncol):
            try:
                file_out.write(oFormat.format(float(array[a][b])))
            except:
                print 'NAN at row,col: ',a,b,array[a][b]
                sys.exit()
            if (b+1)%nWriteCol == 0.0 and b != 0:
                file_out.write('\n')
        if lineReturnFlag == True:
            file_out.write('\n')
    if openFlag == True:        
        file_out.close()
    return True




#--generic plot of 2d array with grid
def plotArray(array,rowDim,colDim,**kwargs):
    #--get keyword arguments
    try:
        title = kwargs['title']
    except:
        title = ''

    try:
        cBarLoc,cBarLabel = kwargs['cBarLoc'],kwargs['cBarLabel']
    except:
        cBarLoc,cBarLabel = [0.25,0.025,0.5,0.025],''
    try:
        cbticks = kwargs['cbticks']
        cbticks_len = len( cbticks )
    except:
        cbticks = None
        cbticks_len = 0
    
    
    try:
        xOff,yOff = kwargs['offset'][0],kwargs['offset'][1]
    except:
        xOff,yOff = 0.0,0.0     
    try:
        max = kwargs['max']
    except:
        max = np.max(array)
    
    try:
        min = kwargs['min']
    except:
        min = np.min(array)
    print 'min,max',min,max
    try:
        figuresize = kwargs['figuresize']
    except:
        if np.shape(array)[0] > np.shape(array)[1]:
            figuresize = (8.5,11)
        else:
            figuresize = (11,8.5)
    
    try:
        gridFlag = kwargs['gridFlag']
    except:
        gridFlag = False
        
    try:
        outputFlag = kwargs['outputFlag']
    except:
        try:
            outputFlag = kwargs['output']
        except:
            outputFlag = 'show'
    
    cmap='jet'
    
    #--get contour array
    try:
        con_array = kwargs['con_array']
        con_len = len(con_array)
        con_text = []
        for c in con_array:
            ct = '{0:15.7g}'.format( c ).strip()
            con_text.append( ct )
    except:
        con_array = []
        con_len = 0
        con_text = []
        
    #--get bln lines and index array
    try:
        blnlines = kwargs['bln']
#       blnPoints,blnIdx = blnUtil.loadBlnFile(blnlines)
        blnPoints,blnIdx = loadBlnFile(blnlines)
    except:
        blnPoints = []
        blnIdx = []
    
    #-- get generic points to plot
    try:
        genPoints = kwargs['gpts']
    except:
        genPoints = []
    
    try:
        fig = kwargs['fig']
    except:
        fig = pylab.figure(figsize=(figuresize))
    
    try:
        Aspect = kwargs['Aspect']
    except:
        Aspect = 'auto'

    try:
        ax = kwargs['ax']
    except:
        ax = pylab.subplot(111,aspect=Aspect)

    try:
        isample = kwargs['isample']
    except:
        isample = 1
    
    try:
        LogTransform = kwargs['LogTransform']
    except:
        LogTransform = False
    
    try:
        plotColorBar = kwargs['plotColorBar']
    except:
        plotColorBar = True
    
    
                        
    #--array params
    nrow,ncol = np.shape(array)
    
    #--log transform
    if LogTransform == True:
        mask = ma.getmask( array )
        for i in range(0,nrow):
            for j in range(0,ncol):
                if mask[i,j] == False:
                    array[i,j] = math.log10( array[i,j] )
        if con_len > 0:
            for i in range(0,con_len):
                con_array[i] = math.log10( float( con_array[i] ) )
        try:
            max = math.log10( kwargs['max'] )
        except:
            max = math.ceil( np.max(array) )
        try:
            min = math.log10( kwargs['min'] )
        except:
            min = math.floor( np.min(array) )
        if cbticks_len > 0:
            cbticks = array( cb_ticks )
            t = copy( cbticks )
            for i in range(0,cbticks_len):
                t[i] = math.log10( t[i] )
            cbticks = copy( t )
        else:
           cbticks = arange(min,max+1,1)
        print 'revised min,max',min,max

    #--set x and y dimensions       
    try:
        x = np.arange(xOff,xOff+(ncol*colDim)+colDim,colDim)
        xmin,xmax = xOff,xOff+(ncol*colDim)
    except:
        try:            
            f_in = open(colDim,'r')
            x = np.zeros((1),dtype='float')
            for line in f_in:
                raw = line.split()
                for a in range(0,len(raw)):
                    x = np.append(x,float(raw[a]))
            x = np.delete(x,[0])
            xmin,xmax = np.min(x),np.max(x)                         
        except:
            assert np.shape(colDim)[0] == ncol+1
            x = colDim
            xmin,xmax = np.min(x),np.max(x)
            
    try:
        y = np.arange(yOff,yOff+(nrow*rowDim)+rowDim,rowDim)
        ymin,ymax = yOff,yOff+(nrow*rowDim)
    except:
        try:            
            f_in = open(rowDim,'r')
            y = np.zeros((1),dtype='float')
            for line in f_in:
                raw = line.split()
                for a in range(0,len(raw)):
                    y = np.append(y,float(raw[a]))
            y = np.delete(y,[0])
            ymin,ymax = np.min(y),np.max(y)                         
        except:
            assert np.shape(rowDim)[0] == nrow+1
            y = rowDim
            ymin,ymax = np.min(y),np.max(y)
    
                
    array = np.flipud(array)
    #fig = figure(figsize=figuresize)
    #ax = subplot(1,1,1,aspect='equal')
    ax.set_title(title)     
            
    #--define meshgrid
    X,Y = np.meshgrid(x,y)
    
    #--set up color map
    numColors = 128
    palette = cm.get_cmap(cmap,numColors)
    palette.set_over('w')
    palette.set_under('w')
    palette.set_bad('w')
    
    
    #--mask
#   array = ma.masked_where(array<min,array)
#   array = ma.masked_where(array>max,array)
    
    #-- plot array
    c = ax.pcolor(X[::isample,::isample],Y[::isample,::isample],array[::isample,::isample],vmin=min,vmax=max,cmap=palette,alpha=0.5,edgecolors='None')
    
    #-- plot grid if gridFlag
    if gridFlag:
        row = 0
        while row < nrow:
            plot([xmin,xmax],[y[row],y[row]],'k-',linewidth=0.1)
            row += 1    
        col = 0
        while col < ncol:
            plot([x[col],x[col]],[ymin,ymax],'k-',linewidth=0.1)
            col += 1
    #print xmin,xmax,ymin,ymax
    
    
    #--plot BLN lines
    if len(blnPoints) > 0:
        for a in range(1,np.shape(blnIdx)[0]):
            #print blnIdx[a-1]
            ax.plot(blnPoints[blnIdx[a-1]:blnIdx[a],0],blnPoints[blnIdx[a-1]:blnIdx[a],1],'k-',lw=2.0)
                
    #--plot generic points
    if len(genPoints) > 0:
    
        #try:
        ax.plot(genPoints[:,0],genPoints[:,1],'k+')
        #except:
        #   print 'error plotting generic points...'
    
    #--plot contours
    if con_len > 0:
        cs = ax.contour(x[:-1],y[:-1],array,con_array,colors='k')
        fmt = {}
        for l,s in zip( cs.levels, con_text ):
            fmt[l] = s
        ax.clabel(cs,inline=1,fmt=fmt)
        
    #--plot color bar
    if plotColorBar:
        cax=axes(cBarLoc)
        fig.colorbar(c,cax=cax,orientation='horizontal',ticks=cbticks)                                       
        cax.set_title(cBarLabel) 
        if LogTransform == True:
            lt1 = cax.get_xticklabels()
            lt2 = []
            for t in lt1:
                rv = float ( t.get_text() )
                v = math.pow( 10., rv )
                if rv >= 6.0:
                    t = '{0:10.3e}'.format( v ).strip()
                elif rv >= 0.0 :
                    t = '{0:10.0f}'.format( v ).strip()
                elif rv >= -1.0:
                    t = '{0:10.1f}'.format( v ).strip()
                elif rv >= -2.0:
                    t = '{0:10.2f}'.format( v ).strip()
                elif rv >= -3.0:
                    t = '{0:10.3f}'.format( v ).strip()
                else:
                    t = '{0:10.3e}'.format( v ).strip()
                lt2.append( t )
            cax.set_xticklabels( lt2 )

    ax.set_xlim(xmin,xmax)
    ax.set_ylim(ymin,ymax)

    if outputFlag == 'save':
        if title == '':
            title = str(time.time())
        plotname=title+'.png'
        savefig(plotname,orientation='portrait',format='png',dpi=150)
    elif outputFlag == 'show':
        show()
    elif outputFlag == None:
        #print 'no output produced...'
        return ax
    else:
        try:
            fmt = outputFlag.split('.')[-1]
        
        except:
            print 'unable to parse outputFlag for output format type: ',outputFlag
        savefig(outputFlag,orientation='portrait',format=fmt,dpi=150)
    close(fig)
    return


def loadBlnFile(file):
    
    data = np.array([0,0,0])
    dataIdx = np.array([0])
    f_in = open(file,'r')
    while True:
        try:
            points = int(f_in.readline().strip('\n').split(',')[0])
        except:
            break               
        for a in range(0,points):
            point = f_in.readline().strip('\n').split(',')
            data = np.vstack((data,[float(point[0]),float(point[1]),float(point[2])]))
        dataIdx = np.append(dataIdx,dataIdx[-1]+points)
    data = np.delete(data,0,axis=0)
    return(data,dataIdx) 

def UpscaleArray(nrow0,ncol0,array,iscale):
    nrow1 = nrow0 / iscale
    ncol1 = ncol0 / iscale 
    upscale = np.zeros( (nrow1,ncol1), np.float )
    for irow in range(0,nrow1):
        for jcol in range(0,ncol1):
            i0 = irow * iscale
            i1 = min( nrow0 - 1, (irow+1)*iscale )
            j0 = jcol * iscale
            j1 = min( ncol0 - 1, (jcol+1)*iscale )
            slice = array[i0:i1,j0:j1]
            upscale[irow,jcol] = np.mean( slice )
    return upscale


#--generic image plotting function
def plotimage( d, **kwargs ):
    try:
        vmin = kwargs['vmin']
    except:
        vmin = np.min( d )
    try:
        vmax = kwargs['vmax']
    except:
        vmax = np.max( d )
    try:
        text = kwargs['text']
    except:
        text = 'None'
    try:
        fout = kwargs['fout']
    except:
        fout = 'temp.png'
    try:
        interpolation = kwargs['interpolation']
    except:
        interpolation = 'none'
    try:
        addcolorbar = kwargs['addcolorbar']
        if addcolorbar.lower() != 'vertical' and addcolorbar.lower() != 'horizontal':
            addcolorbar = 'None'
    except:
        addcolorbar = 'None'
    try:
        polyline_list = kwargs['polyline']
        IsPolyline = True
    except:
        polyline_list = []
        IsPolyline = False
    try:
        im_extent = kwargs['extent']
    except:
        im_extent = None
        
    #--plot data
    fig = plt.figure()
    ax = fig.add_subplot(111,aspect=1)
    dv = ax.imshow(d,vmin=vmin,vmax=vmax,interpolation=interpolation,extent=im_extent)
    if IsPolyline == True:
        polyline_plot( ax, polyline_list )
    if addcolorbar != 'None':
        cb = colorbar(dv,orientation=addcolorbar,ticks=[vmin,vmax])
        if addcolorbar.lower() == 'vertical':
            cb.ax.set_yticklabels( (vmin,vmax), size=6 )
        else:
            cb.ax.set_xticklabels( (vmin,vmax), size=6 )
    xticks( size=6 )
    yticks( size=6 )
    if text != 'None':
        ax.text(0.0, 1.01,text,size=8,horizontalalignment='left', verticalalignment='bottom', transform = ax.transAxes)
    fig.savefig(fout,dpi=150)
    close(fig)
    return

#--generic pcolor plotting function
def plotgrid( x, y, d, **kwargs ):
    try:
        vmin = kwargs['vmin']
    except:
        vmin = np.min( d )
    try:
        vmax = kwargs['vmax']
    except:
        vmax = np.max( d )
    try:
        text = kwargs['text']
    except:
        text = 'None'
    try:
        fout = kwargs['fout']
    except:
        fout = 'temp.png'
    try:
        addcolorbar = kwargs['addcolorbar']
        if addcolorbar.lower() != 'vertical' and addcolorbar.lower() != 'horizontal':
            addcolorbar = 'None'
    except:
        addcolorbar = 'None'
    try:
        polyline_list = kwargs['polyline']
        IsPolyline = True
    except:
        polyline_list = []
        IsPolyline = False
    #--plot data
    fig = plt.figure()
    ax = fig.add_subplot(111,aspect=1)
    dv = ax.pcolor(x, y[::-1], np.flipud(d),vmin=vmin,vmax=vmax)
    if IsPolyline == True:
        polyline_plot( ax, polyline_list )
    if addcolorbar != 'None':
        cb = colorbar(dv,orientation=addcolorbar,ticks=[vmin,vmax])
        if addcolorbar.lower() == 'vertical':
            cb.ax.set_yticklabels( (vmin,vmax), size=6 )
        else:
            cb.ax.set_xticklabels( (vmin,vmax), size=6 )
    ax.set_xlim(x.min(),x.max())
    ax.set_ylim(y.min(),y.max())
    xticks( size=6 )
    yticks( size=6 )
    if text != 'None':
        ax.text(0.0, 1.01,text,size=8,horizontalalignment='left', verticalalignment='bottom', transform = ax.transAxes)
    fig.savefig(fout,dpi=150)
    close(fig)
    return

def polyline_plot( ax, polyline_list ):
    for line in polyline_list:
        ax.plot(line[0,:],line[1,:],'k-')
    return
            