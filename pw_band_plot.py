# -*- coding: utf-8 -*-
"""
@author: yyyu200@163.com
"""

import numpy as np

feig=open('bd.dat')
ymin=-10
ymax=8
nband=26 # this is the valence band number, for insulators only

l=feig.readline()
nbnd=int(l.split(',')[0].split('=')[1])
nks=int(l.split(',')[1].split('=')[1].split('/')[0])

npl=10 # number per line
eig=np.zeros((nks,nbnd),dtype=float)
for i in range(nks):
    l=feig.readline()
    count=0
    if nbnd%npl==0:
        n=nbnd//npl
    else:
        n=nbnd//npl+1
    for j in range(n):
        l=feig.readline()
        for k in range(len(l.split())):
            eig[i][count]=l.split()[k]  # str to float
            count=count+1
            
feig.close()

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

p1=plt.subplot(1, 1, 1)

F=plt.gcf()
#F.set_size_inches([5,5])
lw=1.2 # line width

plt.xlim([0,nks-1]) # 201 points
plt.ylim([ymin,ymax])
#plt.xlabel(r'$k (\AA^{-1})$',fontsize=16)
plt.ylabel(r' E (eV) ',fontsize=16)

eig_vbm=max(eig[:,nband-1])
eig_cbm=min(eig[:,nband])
Gap=eig_cbm-eig_vbm

plt.title("Band gap="+str(Gap)+" eV")  # for insulators only
for i in range(nbnd):
    line1=plt.plot( eig[:,i]-eig_vbm,color='r',linewidth=lw ) 

vlines= np.arange(0,nks,20)
for vline in vlines:
    plt.axvline(x=vline, ymin=ymin, ymax=ymax,linewidth=lw,color='black')

plt.xticks( vlines, (r'${\Gamma}$', 'X', 'M', r'${\Gamma}$', 'Z',
           'R','A','Z','X','R','M','A') )

plt.text(180.0, 3, '$SnO_{2}$ rutile', fontsize=12, color='mediumvioletred')

plt.savefig('pwband.png',dpi=500)



