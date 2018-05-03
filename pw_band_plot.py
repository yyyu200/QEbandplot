# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 11:45:32 2016

@author: Think
"""

import numpy as np

feig=open('bd.dat')

l=feig.readline()
nbnd=int(l.split(',')[0].split('=')[1])
nks=int(l.split(',')[1].split('=')[1].split('/')[0])

eig=np.zeros((nks,nbnd),dtype=float)
for i in range(nks):
    l=feig.readline()
    count=0
    for j in range(nbnd//10+1):
        l=feig.readline()
        for k in range(len(l.split())):
            eig[i][count]=l.split()[k]
            count=count+1
            
feig.close()

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

p1=plt.subplot(1, 1, 1)

F=plt.gcf()
#F.set_size_inches([5,5])
lw=1.2 # line width
#plt.rcParams['axes.linewidth']=lw
#plt.rcParams['axes.labelpad']=1
#plt.rcParams['axes.labelsize']='large'
#plt.rcParams['font.family']='sans-serif'
#plt.rcParams['figure.subplot.wspace']=0
#plt.rcParams['legend.fontsize']='small'
#plt.rcParams['xtick.labelsize']='x-large'
#plt.rcParams['ytick.labelsize']='x-large'
#plt.rcParams['savefig.transparent']=True
#plt.rcParams['font.sans-serif']='Times New Roman'

plt.xlim([0,220]) # 201 points
ymin=-10
ymax=8
plt.ylim([ymin,ymax])
#plt.xlabel(r'$k (\AA^{-1})$',fontsize=16)
plt.ylabel(r' E (eV) ',fontsize=16)
#plt.title('Potential(eV)')
#plt.axes().set_aspect(5000)

nband=26
eig_vbm=max(eig[:,nband-1])
eig_cbm=min(eig[:,nband])
Gap=eig_cbm-eig_vbm

plt.title("Band gap="+str(Gap)+" eV")
for i in range(nbnd):
    line1=plt.plot( eig[:,i]-eig_vbm,color='r',linewidth=lw ) #'#9400D3'

i=20
while i<220:
    plt.axvline(x=i, ymin=ymin, ymax=ymax,linewidth=lw,color='black')
    i=i+20

plt.xticks( np.arange(0,140,20), (r'${\Gamma}$', 'X', 'M', r'${\Gamma}$', 'Z',
           'R','A','Z','X','R','M','A') )

plt.savefig('pwband.pdf',dpi=500)


