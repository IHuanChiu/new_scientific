#!/usr/bin/env python    
#-*- coding:utf-8 -*-   
"""
This module provides the transformation from adc to energy.
"""
__author__    = "I-Huan CHIU"
__email__     = "ichiu@chem.sci.osaka-u.ac.jp"
__created__   = "2019-11-08"
__copyright__ = "Copyright 2019 I-Huan CHIU"
__license__   = "GPL http://www.gnu.org/licenses/gpl.html"

# modules
import sys,os,random,math,ROOT
from ROOT import TFile, TTree, TCut, TChain, TSelector
from ROOT import gROOT, AddressOf
ROOT.gROOT.SetBatch(1)
import argparse
import math
from multiprocessing import Pool, cpu_count
import time
from array import array
#from logger import log
import logging
from random import gauss
#import numpy as np
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/macro/utils/')
from countHit import defineHit, matchhit, mergehit
from printInfo import checkTree
from slimming import DisableBranch

gROOT.ProcessLine(
"struct RootStruct {\
   Int_t      trigger;\
   Int_t      nhit;\
   Int_t      nhitx;\
   Int_t      nhity;\
   Int_t      nmergehitx;\
   Int_t      nmergehity;\
   Double_t  energy_p[2048];\
   Double_t  energy_n[2048];\
   Double_t     adc_p[2048];\
   Double_t     adc_n[2048];\
   Int_t       axis_x[2048];\
   Int_t       axis_y[2048];\
   Double_t    weight[2048];\
};" 
); 
from ROOT import RootStruct
struct = RootStruct()

def getSpline(energyFile, channel): 
    return energyFile.Get('spline_%s'%(channel))

def array2tree(name, tree):
    a = "adc{}"[0].format(0) 
    print(e.GetBranch(a))

def PreEventSelection(tree):
#    cut = TCut("integral_livetime > 500 && integral_livetime < 1500")
    cut = TCut("1")
    cv = ROOT.TCanvas("","")
    tree.Draw(">>elist", cut) 
    elist = gROOT.FindObject("elist")
    return elist
    
def makentuple(nhit, signal):
    for n in range(1,nhit+1):          
       struct.adc_p[n-1]    = signal[n].adc_p
       struct.adc_n[n-1]    = signal[n].adc_n
       struct.energy_p[n-1] = signal[n].energy_p
       struct.energy_n[n-1] = signal[n].energy_n
       struct.axis_x[n-1]   = signal[n].x
       struct.axis_y[n-1]   = signal[n].y
       struct.weight[n-1]   = signal[n].weight

def findx2yshift(h_x, h_y):
    g1x = ROOT.TF1("g1x","gaus",100,300)
    g2x = ROOT.TF1("g2x","gaus",650,800)
    g1y = ROOT.TF1("g1y","gaus",100,300)
    g2y = ROOT.TF1("g2y","gaus",650,850)
    h_x.Fit("g1x","QR")
    h_x.Fit("g2x","QR+")
    h_y.Fit("g1y","QR")
    h_y.Fit("g2y","QR+")
    mean1_x, mean2_x = g1x.GetParameter(1), g2x.GetParameter(1)
    mean1_y, mean2_y = g1y.GetParameter(1), g2y.GetParameter(1)

    a = (g2y.GetParameter(1) - g1y.GetParameter(1))/(g2x.GetParameter(1) - g1x.GetParameter(1))
    b = g1y.GetParameter(1) - (a * g1x.GetParameter(1))

    return a, b
         
def findadccut(line):
    adccut_p, adccut_n = [],[]
    energycut = 10.
    for ch in range(0, 128): 
       cut_flag = 0
       for iadc in range(20,500):
          if (line[ch].Eval(iadc) > energycut) and (cut_flag is 0): 
             adccut_p.append(iadc)
             cut_flag = 1
       if cut_flag is 0: adccut_p.append(100)# not find a good cut value for adc
    for ch in range(0, 128): 
       cut_flag = 0
       for iadc in range(20,500):
          if (line[ch+128].Eval(iadc) > energycut) and (cut_flag is 0): 
             adccut_n.append(iadc)
             cut_flag = 1
       if cut_flag is 0: adccut_n.append(100)# not find a good cut value for adc
    return adccut_p, adccut_n   


def tran(args, IsRandom = False):
    __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
    ROOT.gROOT.LoadMacro( __location__+'/AtlasStyle/AtlasStyle.C')
    ROOT.SetAtlasStyle()
    
    fout = ROOT.TFile( args.output, 'recreate' )
    f = ROOT.TFile(args.input)   
    tree = f.Get("eventtree")
    slinename = "../run/auxfile/spline_calibration.root"
    Efile = ROOT.TFile(slinename, 'read') # not always open
    
    coef_R = 1 # random to ADC to avoid quantum phenomenon
    if not IsRandom : coef_R = 0
    print("Random number setting : ", coef_R) 

    ti = time.time()

    fout.cd()
    tout = TTree('tree','tree') 
    tout.Branch( 'trigger', struct, 'trigger/I:nhit:nhitx:nhity:nmergehitx:nmergehity' ) 
    tout.Branch( 'energy_p', AddressOf( struct, 'energy_p' ), 'energy_p[nhit]/D' )#max hit : 128
    tout.Branch( 'energy_n', AddressOf( struct, 'energy_n' ), 'energy_n[nhit]/D' )
    tout.Branch( 'adc_p', AddressOf( struct, 'adc_p' ),       'adc_p[nhit]/D' )
    tout.Branch( 'adc_n', AddressOf( struct, 'adc_n' ),       'adc_n[nhit]/D' )
    tout.Branch( 'x', AddressOf( struct, 'axis_x' ),          'x[nhit]/I' )
    tout.Branch( 'y', AddressOf( struct, 'axis_y' ),          'y[nhit]/I' )
    tout.Branch( 'weight', AddressOf( struct, 'weight' ),       'weight[nhit]/D' )

    line = list()
    hx = ROOT.TH1D()
    hy = ROOT.TH1D()
    for ch in range(0, 256): 
       line.append(getSpline(Efile, ch))
       if ch < 128:#x
          if ch < 10: hist_name = "hist_cmn" + "00" + str(ch) 
          elif ch < 100:  hist_name = "hist_cmn" + "0" + str(ch) 
          else : hist_name = "hist_cmn" + str(ch)
          hist = f.Get(hist_name) 
          if(ch is 0): hx = hist.Clone()
          else: hx.Add(hist)
       else:#y
          hist_name = "hist_cmn" + str(ch)
          hist = f.Get(hist_name) 
          if(ch is 128): hy = hist.Clone()
          else: hy.Add(hist)
    cut_p, cut_n = findadccut(line)
    coef_a, coef_b = findx2yshift(hx, hy)

    tree = DisableBranch(tree)
    skimmingtree = PreEventSelection(tree)
    
    print("total events : ",skimmingtree.GetN(), " / ", tree.GetEntries(), " (by PreEventSelection)")
    for ie in range(skimmingtree.GetN()):
       if ie%5000 is 0 : print("event running : ", ie , " time : ", time.time() - ti)
       tree.GetEntry(skimmingtree.GetEntry(ie))
       n_hit_x, n_hit_y, hitx, hity = defineHit(tree, line, cut_p, cut_n, coef_a, coef_b, coef_R)
       if n_hit_x is 0 or n_hit_y is 0: continue
       m_nx, m_ny, n_hit_all, pre_signal = mergehit(n_hit_x, n_hit_y, hitx, hity)
       n_hit, signal = matchhit(m_nx, m_ny, n_hit_all, pre_signal)
       if n_hit > 2048: continue # huge hit channel (over max size of leaf)     

       # varaibles of ntuple 
       struct.nhitx = n_hit_x
       struct.nhity = n_hit_y
       struct.nmergehitx = m_nx
       struct.nmergehity = m_ny
       struct.nhit = n_hit
       struct.trigger = tree.integral_livetime
       makentuple(n_hit, signal)
       tout.Fill()

    tf = time.time()
    dt = tf - ti
    print("Ntuple processing time: %.1f s"%(dt))
    checkTree(tout,tree)
    print("Info. processing time: %.1f s"%(dt))

    tout.Write()
    fout.Close()
    Efile.Close()

    if __name__ is not "__main__": return tout
   
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("input", type=str, default="../rawdata/calibration_data/20200225a_am241_5plus.root", help="Input File Name")
    parser.add_argument("--output", type=str, default="../run/root/tranadc_dsd.root", help="Input File Name")
    parser.add_argument("--channel", default=False, action="store_true", help="number of CPU")
    parser.add_argument("--adc", default=False, action="store_true", help="log progess")
    args = parser.parse_args()

    tran( args , True)

