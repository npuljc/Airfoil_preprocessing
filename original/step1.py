'''
Author: Jichao Li
Date:   April, 2018

Preprocessing UIUC airfoils
Step 1: Format Data. Remove unnesessary texts from the files and eliminate incomplete airfoils.
'''

import os
import numpy as np

# read airfoils names
namelist =[]
f = open('uiuc_airfoil_names.txt','r')
while True:
  filename=f.readline()
  if filename:
    namelist.append(filename.rstrip())
  else:
    break
f.close()

'''
Most of the airfoils files are in this format:
------------
 Title
 x1 y1
 x2 y2
  ...
 xn yn
------------
We're going to remove the title if they have one.
Manaual check is required for few airfoils.
'''

checked = True#False

if not checked:
    # Copy all airfoils to **rewrite** folder
    os.system('mkdir rewrite')
    os.system('cp coord_seligFmt/* rewrite/')

    print 'These files require your manual check:'
    for i in range(len(namelist)):
        filename = namelist[i]
        # Remove lines if they have ABC/abc. E/e are OK because some data contains them, e.g. 1.e-2
        os.system('sed -i "/[A-D,F-Z,a-d,f-z]/d" ./rewrite/{0}'.format(filename))
        try:
            mydata = np.loadtxt('rewrite/'+filename)
        except:
            # Remove the first line if the data cannot be loaded
            os.system('sed -i "1d" ./rewrite/{0}'.format(filename))
            try:
                mydata = np.loadtxt('rewrite/'+filename)
            except:
                # These airfoils require manual check
                os.system('cp coord_seligFmt/{0} rewrite/{0}'.format(filename))
                print 'rewrite/'+filename
    print '\n#########################################################################################################################'
    print 'During your check, please remove whatever characters that are not desired. \nAfter that, please reset the check flag and rerun this script.'
    print '#########################################################################################################################\n'
else:
    pass

def checksequence(data):
    '''
    Check if an airfoil is in this sequence: TE -> upper surface -> LE -> lower surface -> TE
    '''
    flagStart = False
    flagEnd   = False
    
    if abs(data[1,0]) > abs(data[1,0] - 0.1):
        flagStart = True
    if abs(data[-1,0]) > abs(data[-1,0] - 0.1):
        flagEnd   = True
    
    return (flagStart and flagEnd)


for i in range(len(namelist)):
    filename = namelist[i]
    mydata = np.loadtxt('rewrite/'+filename)
    if checksequence(mydata):
        pass
    else:
        print filename,'The sequence is not desired. Please modify it.'

print '\n#########################################################################################################################'
print 'Please the modify those airfoils file if you can. \nAfter that, please reset the modified flag and rerun this script.'
print '#########################################################################################################################\n'

modified=True#False

def checkcompleteness(data):
    '''
    Check if an airfoil is kind of complete.
    '''
    if abs(data[0,0] - data[-1,0])/(max(data[:,0])-min(data[:,0])) < 0.05:
        return True
    else:
        return False    

if modified:
    fname = open('name_step1.txt','w')
    fdis = open('discarded_step1.txt','w')
    for i in range(len(namelist)):
        filename = namelist[i]
        mydata = np.loadtxt('rewrite/'+filename)
        if checkcompleteness(mydata):
            fname.write(filename+'\n')
        else:
            print filename,'is not complete and will be discarded.'
            fdis.write(filename+'\n')
    fname.close()
    fdis.close()           
            
