from numpy import ones, empty
from mbase import package

class mfrch(package):
    'Recharge class'
    def __init__(self, model, nrchop=3, irchcb=0, rech=1e-3, irch=1, extension ='rch', unitnumber=19,external=True):
        '''
        external flag is used to control writing external arrays of constant values
        since this package has the potential to create a lot of external arrays
        '''
        package.__init__(self, model, extension, 'RCH', unitnumber) # Call ancestor's init to set self.parent, extension, name and unit number
        nrow, ncol, nlay, nper = self.parent.nrow_ncol_nlay_nper
        self.heading = '# RCH for MODFLOW, generated by Flopy.'
        self.url = 'rch.htm'
        self.nrchop = nrchop
        self.irchcb = irchcb
        self.external = external
        if self.external is False:
            load = True
        else:
            load = model.load
        self.rech = []
        self.irch = []
        if (not isinstance(rech, list)):
            rech = [rech]
        for a in rech:
            b = empty((nrow, ncol))
            b = self.assignarray(b , a,load=load )
            #print self.rech, b
            self.rech = self.rech + [b]
        if (not isinstance(irch, list)):
            irch = [irch]
        for a in irch:
            b = ones((nrow, ncol), dtype='int32')
            b = self.assignarray(b , a, load=load )
            self.irch = self.irch + [b]
        self.np = 0
        self.parent.add_package(self)
    def __repr__( self ):
        return 'Recharge class'
    def ncells( self):
        # Returns the  maximum number of cells that have recharge (developped for MT3DMS SSM package)
        nrow, ncol, nlay, nper = self.parent.nrow_ncol_nlay_nper
        return (nrow * ncol)
    def write_file(self):
        nrow, ncol, nlay, nper = self.parent.nrow_ncol_nlay_nper
        # Open file for writing
        f_rch = open(self.fn_path, 'w')
        f_rch.write('%s\n' % self.heading)
        f_rch.write('%10i%10i\n' % (self.nrchop, self.irchcb))
        for n in range(nper):
            comment = 'Recharge array for stress period ' + str(n + 1)
            if (n < len(self.rech)):
                inrech = 1
            else:
                inrech = -1
            if (n < len(self.irch)):
                inirch = 1
            else:
                inirch = -1
            f_rch.write('%10i%10i\n' % (inrech, inirch))
            comment = 'Recharge array for stress period ' + str(n + 1)
            if (n < len(self.rech)):
                if self.external:
                    self.parent.write_array( f_rch, self.rech[n], self.unit_number[0], True, 13, ncol, comment,ext_base='rech_'+str(n+1) )
                else:
                    self.parent.write_array( f_rch, self.rech[n], self.unit_number[0], True, 13, ncol, comment )
            comment = 'Recharge layers for stress period ' + str(n + 1)
            if ((n < len(self.irch)) and (self.nrchop == 2)):
                self.parent.write_array( f_rch, self.irch[n], self.unit_number[0], True, 13, ncol, comment,ext_base='irch_'+str(n+1) )
        f_rch.close()

