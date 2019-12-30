'''
Author: Jichao Li
Date:   April, 2018

Preprocessing UIUC airfoils
Step 3: Select Data. Remove non-smooth airfoils.

Remove the airfoils with more than one max thickness locations.
'''
import numpy as np
from scipy import interpolate
import math
import os
from pyspline import pySpline
from scipy.interpolate import UnivariateSpline

# read airfoils names
namelist =[]
f = open('name_step2.txt','r')
while True:
  filename=f.readline()
  if filename:
    namelist.append(filename.rstrip())
  else:
    break
f.close()


def recreate(thiscurve):
    '''
    Recreate an uniform sharp TE airfoil.
    The uniform airfoil has [0,0] and [1,0] inside as LE and TE, respectively.
    '''
    # recreate a normal airfoil to the new stencil
    N  = 201
    Nf = int((N-1)/2) + 1
    theta = np.linspace(.0000,2*np.pi,N)
    xnew  = np.cos(theta)
    for i in xrange(N):
        xnew[i] = (xnew[i] + 1.0)/2.0
    reairfoil = np.zeros((N,2))
    
    LEs = 0.0
    tck, u = interpolate.splprep([thiscurve[:,0],thiscurve[:,1]], s=0)
    for i in xrange(thiscurve.shape[0]):
        if thiscurve[i,0] == 0.0:
            LEs = u[i]
            break
    
    def findy(sa,sb,xtemp):
        # find the s value in [sa,sb], and make the x value of this s equals xtemp
        # return the y value of this s
        xfind = 0.0
        upper = sb
        lower = sa
        pa = interpolate.splev(sa, tck)
        pb = interpolate.splev(sb, tck)
        xa = pa[0]# curve.getValue(lower)[0]
        xb = pb[0]# curve.getValue(upper)[0]
        eplison = 1.e-8

        if abs(xa - xtemp) < eplison:
           return pa[1],sa
        if abs(xb - xtemp) < eplison:
           return pb[1],sb

        while (abs(xfind - xtemp) > eplison):
           news = (upper + lower)/2.0
           pnew = interpolate.splev(news, tck)
           xnew = pnew[0]
           if abs(xtemp - xnew) < eplison:
               return pnew[1],news
           
           if (xtemp - xnew)*(xtemp - xa) > 0.0:
               lower = news
           else:
               upper = news
        return  pnew[1],news

    #upper surface
    s1 = 0.0
    startp = interpolate.splev(s1, tck)
    for i in xrange(Nf-1):    
        # find along the curve
        mysa = s1
        mysb = min(s1+0.3,LEs-1.e-15)
        reairfoil[i,0] = abs(xnew[i])
        ytemp,s1 = findy(mysa,mysb,xnew[i])
        reairfoil[i,1] = ytemp
    #LE, reset the leading edge to be (0,0)
    reairfoil[Nf-1,0] = 0.0
    reairfoil[Nf-1,1] = 0.0

    #lower surface
    s1 = LEs + 1.e-15
    endp = interpolate.splev(1.0, tck)
    for i in xrange(Nf,N):    
        mysa = s1
        mysb = min(s1+0.3,1.0)
        reairfoil[i,0] = abs(xnew[i])
        ytemp,s1 = findy(mysa,mysb,xnew[i])
        reairfoil[i,1] = ytemp  
    #TE [1,0]
    reairfoil[-1,0] = 1.0
    reairfoil[-1,1] = 0.0
    reairfoil[0,0] = 1.0
    reairfoil[0,1] = 0.0
    
    return reairfoil
    

def checkthick(aa):
    '''
    check if an airfoil has multiple max-thickness points
    '''
    airfoil = recreate(aa)
    N = airfoil.shape[0]
    Nf = int((N+1)/2)    
    thickline = np.zeros((Nf,3))
    
    for i in xrange(Nf):
        thickline[i,0] = airfoil[Nf-1-i,0]
        thickline[i,1] = airfoil[Nf-1-i,1] - airfoil[N - Nf + i,1]
    
    spl = UnivariateSpline(thickline[1:-1,0],thickline[1:-1,1], k=3, s=0.0)
    # count how many times it changes
    ncount = 0
    knon = 1.e-3
    symbol = 1.0
    for i in xrange(1,Nf-1):
        # compute the derivative
        deltx = 1.e-6
        y2 = spl(thickline[i,0]+deltx)
        y1 = spl(thickline[i,0]-deltx)
        dydx = (y2-y1)/(2.0*deltx)
        thickline[i,2] = dydx
        if dydx*symbol < 0.0:
            if abs(dydx) > knon:
                ncount += 1
                symbol = -1.0*symbol
    print ncount
    if ncount > 1:
        return False
    else:
        return True

fname=open('name_step3.txt','w')
fdis = open('discarded_step3.txt','w')

for iair in xrange(len(namelist)):
    filename = namelist[iair]
    aa = np.loadtxt('uniform/'+filename)
    print filename
    if checkthick(aa):
        fname.write(filename+'\n')
    else:
        fdis.write(filename+'\n')
fname.close()
fdis.close()

