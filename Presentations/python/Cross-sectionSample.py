    ix = 23
    ax = ztf.add_subplot(3,2,2)
    text(0.0,1.01,'Production well 1 (row 18)',\
         horizontalalignment='left',verticalalignment='bottom',size=7,transform=ax.transAxes)
    t = np.copy( top[ix,:] )
    h = np.copy(  hd[ix,:] )
    h[35:] = 0.0
    z = np.copy(  zs[ix,:] )
    z[35:] = 0.0
    zt = np.copy(  z_steady[ix,:] )
    f  = ax.fill_between(xcell,y1=h,y2=z,color='#40d3f7')
    s  = ax.fill_between(xcell,y1=z,y2=-25.,color='#F76541')
    ax.plot(xcell,zt,linestyle=':',color='#FFA500')
    ax.plot(xcell,t,'k-',zorder=100)
    ax.plot([xcell[30],xcell[30]],[t[30],h[30]],linestyle='solid',color='0.5',linewidth=2)
    ax.plot([xcell[30],xcell[30]],[h[30],-25.],'k-',linewidth=2)
    ax.plot(xcell[0:36],h[0:36],'b-',linewidth=0.5)
    #--plot limits
    ax.set_xlim(xmin,xmax)
    ax.set_ylim(-20,5)
    ylabel('Elevation (m)')
