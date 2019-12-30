'''
Author: Jichao Li
Date:   April, 2018

Preprocessing UIUC airfoils
Step 2: Uniform Data. Sharpen airfoils' trailing edges and uniform them.


After the procession of the first step, all airfoils start from the trailing edge and end at the trailing edge.
But,
some airfoils are associated with a blunt trailing edge;
Some are with a non-0 angle of attack.
Some are not uniform.

We do these procedures in this step:
- Define the trailing edge by 
  1. if the two are the same, just use it
  2. if they are different which means it is a blunt TE airfoil, find the TE by increasing the two lines
- Uniform it and re-generate it into a uniform format with 301 points
'''
import numpy as np
from scipy import interpolate
import math
import os
from pyspline import pySpline
from scipy.interpolate import UnivariateSpline

# read airfoils names
namelist =[]
f = open('name_step1.txt','r')
while True:
  filename=f.readline()
  if filename:
    namelist.append(filename.rstrip())
  else:
    break
f.close()


def line(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C

def intersection(L1, L2):
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x,y
    else:
        return False


nBlunt = 0
nunBlunt = 0
nleft = 0     # the crossing point is left on both TE
nrightfar = 0  # the crossing point is right on both TE and too far from either TE
fardist = 0.1
ncannot = 0  # can't find the crossing point

os.system('mkdir uniform')


def modifydata(aa):
    '''
    Modify a closed sharp TE airfoil.
    Four steps:
    1. interpolate a curve
    2. find the LE
    3. rotate and scale the curve
    4. reset the points on the curve  
    '''    
    
    # step 1
    try:
        tck, u = interpolate.splprep([aa[:,0],aa[:,1]], s=0)
    except:
        try:
            # maybe there two same points together
            aax=[]
            aay=[]
            for i in xrange(aa.shape[0]):
                if i>0:
                    if aa[i,0] == aa[i-1,0] and aa[i,1] == aa[i-1,1]:
                        pass
                    else:
                        aax.append(aa[i,0])
                        aay.append(aa[i,1])
                else:
                    aax.append(aa[i,0])
                    aay.append(aa[i,1])
            tck, u = interpolate.splprep([aax,aay], s=0)                     
        except:
            f = open('fault.plt','w')            
            for i in xrange(aa.shape[0]):
                f.write('%.15f %.15f\n'%(aa[i,0],aa[i,1]))
            f.close()
            stop 
    # step 2: find LE
    TE = aa[0,:].copy()
    tol = 1.0
    smd = 0.5
    shalf = 0.4
    largedis = 0.0
    while (tol > 1.e-15):
        nseed = 100
        seeds = np.zeros(nseed)
        distance = np.zeros(nseed)
        for i in xrange(nseed):
            tseed = smd - shalf + 2.0*shalf*i/(nseed - 1.0) 
            tp    =  interpolate.splev(tseed, tck)
            seeds[i]    = tseed
            distance[i] = np.linalg.norm(tp-TE)
        index = np.argmax(distance)
        smd = seeds[index]
        thisdis = distance[index]    
        tol = abs(thisdis - largedis)
        largedis = thisdis
        shalf = shalf/(nseed - 1.0)
    LEs = smd
    LE  = interpolate.splev(LEs, tck)

    nhalfpts = 151
    npts = nhalfpts*2-1
    thiscurve = np.zeros((npts,2))

    theta = np.linspace(.0000,2*np.pi,npts)
    xb = 0.5
    #xnew  = np.cos(theta)
    xnew  = np.cos(theta)*np.sqrt(1.0/(np.cos(theta)*np.cos(theta) + xb*xb*np.sin(theta)*np.sin(theta)))
    for i in xrange(npts):
        xnew[i] = (xnew[i] + 1.0)/2.0
    #upper surface
    for i in xrange(nhalfpts):
        tseed = LEs*(1.0-xnew[i])
        tp = interpolate.splev(tseed, tck)
        thiscurve[i,0] = tp[0]
        thiscurve[i,1] = tp[1]
    #lower surface
    for i in xrange(1,nhalfpts):
        tseed = LEs + (1.0 - LEs)*(1.0-xnew[i])
        tp = interpolate.splev(tseed, tck)
        thiscurve[nhalfpts-1+i,0] = tp[0]
        thiscurve[nhalfpts-1+i,1] = tp[1]
    
    # step 3: make it uniform
    length = np.linalg.norm(LE-TE)
    costheta = (TE[0] - LE[0])/length
    sintheta = -1.0*(LE[1] - TE[1])/length    
    # step 3.1: shift
    for i in xrange(npts):
        thiscurve[i,0] = thiscurve[i,0] - LE[0]
        thiscurve[i,1] = thiscurve[i,1] - LE[1]
    
    # step 3.2: rotate
    for i in xrange(npts):
        xtemp          = thiscurve[i,0]
        ytemp          = thiscurve[i,1]
        thiscurve[i,0] = xtemp*costheta + ytemp*sintheta
        thiscurve[i,1] = -1.0*xtemp*sintheta + ytemp*costheta
    
    # step 3.3: scale
    for i in xrange(npts):
        xtemp          = thiscurve[i,0]
        ytemp          = thiscurve[i,1]
        thiscurve[i,0] = xtemp/length
        thiscurve[i,1] = ytemp/length
    #return thiscurve
    # Set the LE and TE be [0,0] and [1,0] now in case of Machine accuracy limination
    thiscurve[nhalfpts-1,0] = 0.0
    thiscurve[nhalfpts-1,1] = 0.0
    thiscurve[0,0] = 1.0
    thiscurve[0,1] = 0.0
    thiscurve[-1,0] = 1.0
    thiscurve[-1,1] = 0.0
    #print 'recreat'
    # recreate airfoils
    return thiscurve
    

fname=open('name_step2.txt','w')
fdis = open('discarded_step2.txt','w')

for iair in xrange(3):#len(namelist)):
    filename = namelist[iair]
    aa = np.loadtxt('rewrite/'+filename)
    
    if aa[0,0] == aa[-1,0] and aa[0,1] == aa[-1,1]:
        # Sharp TE airfoils
        fname.write(filename+'\n')
        newdata = modifydata(aa)
        
        # Rewrite the modified airfoil to the **uniform** folder
        f = open('uniform/'+filename,'w')
        for i in xrange(newdata.shape[0]):
            f.write('%.15f %.15f\n'%(newdata[i,0],newdata[i,1]))
        f.close()
        
    else:
        # Blunt LE airfoils
        
        # Compute the crossing point
        L1 = line(aa[0,:],aa[1,:])
        L2 = line(aa[-1,:],aa[-2,:])
        R = intersection(L1, L2)
        if R:
            if (R[0] < aa[1,0]) or  (R[0] < aa[-2,0]):
                #nleft += 1
                # The crossing point is on the left of the Trailing Edge section
                fdis.write(filename+'\n')
            elif (R[0] > aa[0,0] and R[0] > aa[-1,0]) and ( (R[0]-aa[-1,0]) > fardist or (R[0]-aa[0,0]) > fardist ):
                #nrightfar += 1 
                # The crossing point is too far away from the Trailing Edge section
                fdis.write(filename+'\n')
            if R[0] > aa[1,0] and R[0] > aa[-2,0] and  abs(R[0] - aa[0,0]) < fardist and abs(R[0] - aa[-1,0]) < fardist:
                fname.write(filename+'\n')
                newaa = aa.copy()
                newaa[0,0] = R[0]
                newaa[0,1] = R[1]
                newaa[-1,0] = R[0]
                newaa[-1,1] = R[1]
                newdata = modifydata(newaa)
                # Rewrite the modified airfoil to the **uniform** folder
                f = open('uniform/'+filename,'w')
                for i in xrange(newdata.shape[0]):
                    f.write('%.15f %.15f\n'%(newdata[i,0],newdata[i,1]))
                f.close()
        else:
            #ncannot += 1
            #No single intersection point detected"
            fdis.write(filename+'\n')
fname.close()
fdis.close()

