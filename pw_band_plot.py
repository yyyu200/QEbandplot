# -*- coding: utf-8 -*-
"""
@author: yyyu200@163.com
"""

import numpy as np
import re

def parse_filband(feig, npl=10):
    # feig : filband in bands.x input file
    # npl : number per line, 10 for bands.x, 6 for phonon

    f=open(feig,'r')
    lines = f.readlines()

    header = lines[0].strip()
    line = header.strip('\n')
    shape = re.split('[,=/]', line)
    nbnd = int(shape[1])
    nks = int(shape[3])
    eig = np.zeros((nks, nbnd), dtype=np.float32)

    dividend = nbnd
    divisor = npl
    div = nbnd // npl + 1 if nbnd % npl == 0 else nbnd // npl + 2 
    kinfo=[]
    for index, value in enumerate(lines[1:]):
        value = value.strip(' \n')
        quotient = index // div
        remainder = index % div

        if remainder == 0:
            kinfo.append(value)
        else:
            value = re.split('[ ]+', value)
            a = (remainder - 1) * npl
            b = a + len(value)
            eig[quotient][a:b] = value

    f.close()

    return eig, nbnd, nks, kinfo

def draw_band(bd_file, fig_file, do_find_gap, e_ref=0.0, nvband=0):
    eig, nbnd, nks, kinfo = parse_filband('bd.dat')
    
    ymin=-10  # y range in plot
    ymax=10
    lw=1.2 # line width

    import matplotlib as mpl
    mpl.use('Agg')
    import matplotlib.pyplot as plt
    p1=plt.subplot(1, 1, 1)
    F=plt.gcf()
    #F.set_size_inches([5,5])
    
    if nbnd <= nvband:
        print("warning: nvband ", nvband," should be less than the calculated band number ", nbnd)
    
    plt.xlim([0,nks-1]) # k-points
    plt.ylim([ymin,ymax])
    #plt.xlabel(r'$k (\AA^{-1})$',fontsize=16)
    plt.ylabel(r' E (eV) ',fontsize=16)
    
    if do_find_gap:
        if nbnd > nvband: # for insulators only, nvband can be found by gappw.sh(https://github.com/yyyu200/gappw)
            eig_vbm=max(eig[:,nvband-1])
            eig_cbm=min(eig[:,nvband])
            gap=eig_cbm-eig_vbm
            plt.title("Band gap= %.4f eV" % (gap))
            e_ref=eig_vbm
        elif nbnd==nvband: # cb not calculated, cannot find gap
            e_ref=max(eig[:,nvband-1])
        else:
            print("set nvband no less than", nbnd)
            assert None
    
    for i in range(nbnd):
        line1=plt.plot( eig[:,i]-e_ref,color='r',linewidth=lw ) 
    
    vlines= np.arange(0,nks,20) # positions of vertical lines, or specified by [0, 20, 40, ...]
    for vline in vlines:
        plt.axvline(x=vline, ymin=ymin, ymax=ymax,linewidth=lw,color='black')
    
    xlabeltext=[r'${\Gamma}$', 'X', 'M', r'${\Gamma}$', 'Z', 'R','A','Z','X','R','M','A']
    if len(xlabeltext)<len(vlines):
        for i in range(len(vlines)-len(xlabeltext)):
            xlabeltext.append('X')
    elif len(xlabeltext)>len(vlines):
        xlabeltext=xlabeltext[0:len(vlines)]
    
    assert len(xlabeltext)==len(vlines)
    
    plt.xticks( vlines, xlabeltext)
    
    plt.text(4, 8, 'SnO$_{2}$', fontsize=12, color='black', bbox=dict(facecolor='white',alpha=0.99,edgecolor='black') )
    plt.tight_layout()
    
    plt.savefig(fig_file, dpi=500)

if __name__ == '__main__':
    do_find_gap=True
    #e_ref=0.0 # set to fermi-level in scf output for metal, only applicable for do_find_gap=False
    nvband=26 # valence band number, only applicable for do_find_gap=True

    draw_band("bd.dat", "pwband.png", do_find_gap, nvband=nvband)
