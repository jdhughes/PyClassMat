import re
import sys
import math
import numpy as np
import shapefile    
import MFArrayUtil as au

#--functions
def free_u1drel(length,file,rel_dir):
    line = file.readline().strip().split()
    data = []
    if line[0].upper() == 'CONSTANT':
        for l in range(length): data.append(float(line[1]))
    elif line[0].upper() == 'INTERNAL': 
        cnst = float(line[1])       
        for l in range(length):
            dline = f.readline().strip()
            data.append(float(dline) * cnst)
    elif line[0].upper() == 'EXTERNAL':
        raise NameError('External not supported')
    elif line[0].upper() == 'OPEN/CLOSE':
        cnst = float(line[2])
        f2 = open(rel_dir+line[1])
        for l in range(length):
            dline = f2.readline()
            #print dline,length
            data.append(float(dline.strip()) * cnst)
        f2.close
    else:
        raise TypeError('unrecognized keyword: '+line[0].upper())
    return data
#--get data from DIS file
def load_dis_file(file,rel_dir=''): 
    f = open(rel_dir+file,'r')
    off = re.compile('offset',re.IGNORECASE)
    offset = [0.0,0.0,0.0]
    #--read comment lines
    #--try to get the offset
    while True:
        line = f.readline()
        if line[0] != '#': break
        if off.search(line) != None:
            try:
                raw = line.strip().split('=')[-1].split(',')
                xedge = float(raw[0])
                yedge = float(raw[1])
                rotation = float(raw[2])
                offset = [xedge,yedge,rotation]
                print 'x-offset = %g y-offset = %g rotation = %g' % (xedge,yedge,rotation)
            except:
                print 'offset not found in dis file header...continuing'
    #--parse the first line
    raw = line.split()
    nlay, nrow, ncol, nper = int(raw[0]), int(raw[1]), int(raw[2]), int(raw[3])
    itmuni, lenunit = int(raw[4]), int(raw[5])  
    print 'nlay = {0} nrow = {1}, ncol = {2}'.format(nlay,nrow,ncol) 
    #--parse the laycbd line
    line = f.readline()
    raw = line.strip().split()
    if len(raw) != nlay:
        raise IndexError('need '+str(nlay)+' entries for dataset 2')
    laycbd = []
    for r in raw : laycbd.append(float(r))
    #--get delr and delc
    delr = free_u1drel(ncol,f,rel_dir) 
    delc = free_u1drel(nrow,f,rel_dir)
    #--close dis file
    f.close()
    #--return results       
    return offset,nlay,nrow,ncol,np.array(delr),np.array(delc)
#--rotate coordinates
def rotate(box,angle):
    new_box = []
    sin_phi = math.sin(angle*math.pi/180.0)
    cos_phi = math.cos(angle*math.pi/180.0)
    #print sin_phi,cos_phi
    for point in box:
        new_x = (point[0] * cos_phi) - (point[1] * sin_phi)
        new_y = (point[0] * sin_phi) + (point[1] * cos_phi)
        new_box.append([new_x,new_y])
    return new_box                                   
#--offset coordinates
def add_offset(box,offset):
    for point in box:
        point[0] += offset[0]
        point[1] += offset[1]
    return box
#--main script    
filename = '..\\data\\CoastalAquifer.dis'
offset,nlay,nrow,ncol,delr,delc = load_dis_file(filename)
#--flip the delc since we moved the orgin to lower left
delc = np.flipud( delc )
#--sum the lengths along the distance vectors
delr_cum = np.cumsum(delr)
delc_cum = np.cumsum(delc)
#--flip the delc since we moved the origin to lower left
delc_cum = np.flipud( delc_cum )
#--insert '0' in the first position 
xedge = np.hstack((0,delr_cum))
yedge = np.hstack((delc_cum,0))
#--read MODFLOW data from external files
ibound  = au.loadArrayFromFile(nrow,ncol,'..\\ref\\ibound.ref')
top     = au.loadArrayFromFile(nrow,ncol,'..\\ref\\top.ref')
#--create polygon shapefile of grid
wr = shapefile.Writer()
wr.field('row',fieldType='N',size=20)
wr.field('column',fieldType='N',size=20)
wr.field('delx',fieldType='N',size=20)
wr.field('dely',fieldType='N',size=20)
wr.field('cellnum',fieldType='N',size=20)
wr.field('ibound',fieldType='N',size=20)
wr.field('elev_m',fieldType='N',size=16,decimal=7)
#--create each polygon
cell_count = 0
for ir in range(0,nrow):
    for ic in range(0,ncol):
        #--calc the box points relative to the grid
        lowleft = [xedge[ic],yedge[ir]]     
        lowright = [xedge[ic+1],yedge[ir]]  
        upright = [xedge[ic+1],yedge[ir+1]] 
        upleft = [xedge[ic],yedge[ir+1]]            
        closeit = [xedge[ic],yedge[ir+1]-0.0001]            
        this_box = [upleft,upright,lowright,lowleft,closeit]
        #--if rotation is non-zero
        if offset[2] != 0.0:
            this_box = rotate(this_box,offset[2])
        #--add the offset in after the rotation
        this_box = add_offset(this_box,offset)
        ibt   = ibound[ir,ic]
        ttop  = top[ir,ic]
        wr.poly(parts=[this_box], shapeType=5)
        wr.record([ir+1,ic+1,delc[ir],delr[ic],cell_count+1,ibt,ttop])
        cell_count += 1
#--save polygon shapefile        
wr.save(target='..\\data\\CoastalAquifer_grid')
#--create extent polygon
wre = shapefile.Writer()
wre.field('domain',fieldType='N',size=20)
cell_count = 1
lowleft = [xedge[0],yedge[0]]     
lowright = [xedge[ncol],yedge[0]]  
upright = [xedge[ncol],yedge[nrow]] 
upleft = [xedge[0],yedge[nrow]]  
closeit =  [xedge[0],yedge[nrow]-0.0001]         
this_box = [upleft,upright,lowright,lowleft,closeit]
#--if rotation is non-zero
if offset[2] != 0.0:
    this_box = rotate(this_box,offset[2])
#--add the offset in after the rotation
this_box = add_offset(this_box,offset)
#--create extent polygon and save file        
wre.poly(parts=[this_box], shapeType=5)
wre.record([1])
wre.save(target='..\\data\\CoastalAquifer_grid_extent')
