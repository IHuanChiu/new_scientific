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
from time import localtime, asctime
from array import array
import logging
from logger import log
from random import gauss
import numpy as np
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/macro/utils/')
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/macro/scripts/')
from countHit import Level1Hit, Level2Hit, findpoint, matchhit
from printInfo import checkTree
from slimming import DisableBranch
from div import createRatioCanvas
from utils.cuts import PreEventSelection, findx2yshift, findadccut
import enums
from utils.helpers import ProgressBar

gROOT.ProcessLine(
"struct RootStruct {\
   Int_t      trigger;\
   Int_t      nhit;\
   Int_t       npoint;\
   Int_t      nsignalx_lv1;\
   Int_t      nsignaly_lv1;\
   Int_t      nsignalx_lv2;\
   Int_t      nsignaly_lv2;\
   Double_t  energy_p[128];\
   Double_t  energy_n[128];\
   Double_t     adc_p[128];\
   Double_t     adc_n[128];\
   Int_t       axis_x[128];\
   Int_t       axis_y[128];\
   Double_t    weight[128];\
   Double_t    E_p[512];\
   Double_t    E_n[512];\
   Double_t    E_p_lv1[128];\
   Double_t    E_n_lv1[128];\
   Double_t    E_p_lv2[128];\
   Double_t    E_n_lv2[128];\
   Double_t    DeltaE[512];\
   Int_t       Poi_x[512];\
   Int_t       Poi_y[512];\
   Int_t       Poi_x_lv1[128];\
   Int_t       Poi_y_lv1[128];\
   Int_t       Poi_x_lv2[128];\
   Int_t       Poi_y_lv2[128];\
};"
); 

from ROOT import RootStruct
struct = RootStruct()

def getlineEnergy(energyFile, channel): 
    return energyFile.Get('spline_%s'%(channel))

def getTSpline(self,fname, ef):
    f = ROOT.TFile(fname) 
    line = list()
    for ch in range(0, 256): 
       line.append(getlineEnergy(ef, ch))
       if ch < 128:#x
          if ch < 10: hist_name = "hist_cmn" + "00" + str(ch) 
          elif ch < 100:  hist_name = "hist_cmn" + "0" + str(ch) 
          else : hist_name = "hist_cmn" + str(ch)
          hist = f.Get(hist_name) 
          self.hx.Add(hist)
       else:#y
          hist_name = "hist_cmn" + str(ch)
          hist = f.Get(hist_name) 
          self.hy.Add(hist)
    return line

def array2tree(name, tree):
    a = "adc{}"[0].format(0) 
    print(e.GetBranch(a))

    
def makentuple(signal, point, hitx_lv2, hity_lv2, hitx_lv1, hity_lv1):
    for n in range(1,len(signal)+1):          
       struct.adc_p[n-1]        = signal[n].adc_p
       struct.adc_n[n-1]        = signal[n].adc_n
       struct.energy_p[n-1]     = signal[n].energy_p
       struct.energy_n[n-1]     = signal[n].energy_n
       struct.axis_x[n-1]       = signal[n].x
       struct.axis_y[n-1]       = signal[n].y
       struct.weight[n-1]       = signal[n].weight
    for n in range(1,len(point)+1):          
       struct.E_p[n-1]        = point[n].energy_p
       struct.E_n[n-1]        = point[n].energy_n
       struct.Poi_x[n-1]      = point[n].x
       struct.Poi_y[n-1]      = point[n].y
       struct.DeltaE[n-1]     = point[n].deltaE
    for n in range(1,len(hitx_lv1)+1):          
       struct.E_p_lv1[n-1]        = hitx_lv1[n].energy
       struct.Poi_x_lv1[n-1]      = hitx_lv1[n].position
    for n in range(1,len(hity_lv1)+1):          
       struct.E_n_lv1[n-1]        = hity_lv1[n].energy
       struct.Poi_y_lv1[n-1]      = hity_lv1[n].position
    for n in range(1,len(hitx_lv2)+1):          
       struct.E_p_lv2[n-1]        = hitx_lv2[n].energy
       struct.Poi_x_lv2[n-1]      = hitx_lv2[n].position
    for n in range(1,len(hity_lv2)+1):          
       struct.E_n_lv2[n-1]        = hity_lv2[n].energy
       struct.Poi_y_lv2[n-1]      = hity_lv2[n].position

class tran_process():
      def __init__(self,
                   ifile=None,
                   tree=None,
                   event_list=None,
                   efile=None
                   ):
          # config
          self.ifile = ifile
          self.tree   = tree
          self.event_list = event_list
           
          # members
          Efile = ROOT.TFile(efile, 'read')
          self.hist_list = []
          self.tree_list = []
          self.h2_lv1 = ROOT.TH2D("hist_level1","level1 hit channel",20,0,20,20,0,20)
          self.h2_lv1.SetDirectory(0)
          self.h2_lv1.GetXaxis().SetTitle("X")
          self.h2_lv1.GetYaxis().SetTitle("Y")
          self.h2_lv2 = ROOT.TH2D("hist_level2","level2 hit channel",20,0,20,20,0,20)
          self.h2_lv2.SetDirectory(0)
          self.h2_lv2.GetXaxis().SetTitle("X")
          self.h2_lv2.GetYaxis().SetTitle("Y")
          self.hx = ROOT.TH1D("hist_cmn_pside","p-side adc - cmn",1024,-50.5,973.5)
          self.hy = ROOT.TH1D("hist_cmn_nside","n-side adc - cmn",1024,-50.5,973.5)
          self.hx.SetDirectory(0)
          self.hy.SetDirectory(0)
          self.h2_cutflow_x = ROOT.TH2D("hist_cutflow_x","remained hit after the selections",3,0,3,128,0,128)
          self.h2_cutflow_y = ROOT.TH2D("hist_cutflow_y","remained hit after the selections",3,0,3,128,0,128)
          self.h2_cutflow_x.SetDirectory(0)
          self.h2_cutflow_y.SetDirectory(0)
          h2_Label = ["Raw","Level 1","Level 2"]
          self.h2_cutflow_x.GetYaxis().SetTitle("number of hits")
          self.h2_cutflow_y.GetYaxis().SetTitle("number of hits")
          for i in range(len(h2_Label)): 
             self.h2_cutflow_x.GetXaxis().SetBinLabel(i+1,h2_Label[i])
             self.h2_cutflow_y.GetXaxis().SetBinLabel(i+1,h2_Label[i])
          self.h1_event_cutflow = ROOT.TH1D("hist_event_cutflow","events after the selections",5,0,5)
          self.h1_event_cutflow.SetDirectory(0)
          h1_Label = ["Raw","trigger","Level 1","Level 2", "photon"]
          for i in range(len(h1_Label)):
             self.h1_event_cutflow.GetXaxis().SetBinLabel(i+1,h1_Label[i])   

          self.tout = TTree('tree','tree') 
          self.tout.SetDirectory(0)
          self.tout.Branch( 'trigger', struct, 'trigger/I:nhit:npoint:nsignalx_lv1:nsignaly_lv1:nsignalx_lv2:nsignaly_lv2' ) 
 
          self.tout.Branch( 'energy_p', AddressOf( struct, 'energy_p' ),    'energy_p[nhit]/D' )
          self.tout.Branch( 'energy_n', AddressOf( struct, 'energy_n' ),    'energy_n[nhit]/D' )
          self.tout.Branch( 'adc_p', AddressOf( struct, 'adc_p' ),          'adc_p[nhit]/D' )
          self.tout.Branch( 'adc_n', AddressOf( struct, 'adc_n' ),          'adc_n[nhit]/D' )
          self.tout.Branch( 'x', AddressOf( struct, 'axis_x' ),             'x[nhit]/I' )
          self.tout.Branch( 'y', AddressOf( struct, 'axis_y' ),             'y[nhit]/I' )
          self.tout.Branch( 'weight', AddressOf( struct, 'weight' ),        'weight[nhit]/D' )

          self.tout.Branch( 'E_p', AddressOf( struct, 'E_p' ),    'E_p[npoint]/D' )
          self.tout.Branch( 'E_n', AddressOf( struct, 'E_n' ),    'E_n[npoint]/D' )
          self.tout.Branch( 'E_p_lv1', AddressOf( struct, 'E_p_lv1' ),    'E_p_lv1[nsignalx_lv1]/D' )
          self.tout.Branch( 'E_n_lv1', AddressOf( struct, 'E_n_lv1' ),    'E_n_lv1[nsignaly_lv1]/D' )
          self.tout.Branch( 'E_p_lv2', AddressOf( struct, 'E_p_lv2' ),    'E_p_lv2[nsignalx_lv2]/D' )
          self.tout.Branch( 'E_n_lv2', AddressOf( struct, 'E_n_lv2' ),    'E_n_lv2[nsignaly_lv2]/D' )
          self.tout.Branch( 'DeltaE', AddressOf( struct, 'DeltaE' ),   'DeltaE[npoint]/D' )

          self.tout.Branch( 'Poi_x', AddressOf( struct, 'Poi_x' ),        'Poi_x[npoint]/I' )
          self.tout.Branch( 'Poi_y', AddressOf( struct, 'Poi_y' ),        'Poi_y[npoint]/I' )
          self.tout.Branch( 'Poi_x_lv1', AddressOf( struct, 'Poi_x_lv1' ),        'Poi_x[nsignalx_lv1]/I' )
          self.tout.Branch( 'Poi_y_lv1', AddressOf( struct, 'Poi_y_lv1' ),        'Poi_y[nsignaly_lv1]/I' )
          self.tout.Branch( 'Poi_x_lv2', AddressOf( struct, 'Poi_x_lv2' ),        'Poi_x[nsignalx_lv2]/I' )
          self.tout.Branch( 'Poi_y_lv2', AddressOf( struct, 'Poi_y_lv2' ),        'Poi_y[nsignaly_lv2]/I' )

          self.coef_R = 1 # random to ADC to avoid quantum phenomenon
          if not enums.IsRandom : self.coef_R = 0

          self.line = getTSpline(self, ifile, Efile) 
          self.cut_p, self.cut_n = findadccut(self.line)
      #    coef_a, coef_b = findx2yshift(self.hx, self.hy)

          self.hist_list.append(self.h2_lv1)
          self.hist_list.append(self.h2_lv2)
          self.hist_list.append(self.hx)
          self.hist_list.append(self.hy)
          self.hist_list.append(self.h2_cutflow_x)
          self.hist_list.append(self.h2_cutflow_y)
          self.hist_list.append(self.h1_event_cutflow)

          self.tree_list.append(self.tout)

          self.drawables = self.hist_list + self.tree_list
          print ("init : ")

      def tran_adc2e(self):
          self.h1_event_cutflow.Fill(0,self.tree.GetEntries())         

          print ("run : ")
          for ie in range(skimmingtree.GetN()):
             print ("run : ",ie)

             self.tree.GetEntry(self.event_list.GetEntry(ie))

             self.h1_event_cutflow.Fill(1)
             self.h2_cutflow_x.Fill(0, 128)
             self.h2_cutflow_y.Fill(0, 128)

             hitx_lv1, hity_lv1 = Level1Hit(self.tree, self.line, self.cut_p, self.cut_n, self.coef_R) # cut adc & save info.
             self.h2_lv1.Fill(len(hitx_lv1),len(hity_lv1))
             self.h2_cutflow_x.Fill(1, len(hitx_lv1))
             self.h2_cutflow_y.Fill(1, len(hity_lv1))
             if len(hitx_lv1) is 0 or len(hity_lv1) is 0: return 0
             self.h1_event_cutflow.Fill(2)

             hitx_lv2, hity_lv2, madx, mady = Level2Hit(hitx_lv1, hity_lv1) # merge adjacent signal
             self.h2_lv2.Fill(len(hitx_lv2),len(hity_lv2))
             self.h2_cutflow_x.Fill(2, len(hitx_lv2))
             self.h2_cutflow_y.Fill(2, len(hity_lv2))
             if len(hitx_lv2) is 0 or len(hity_lv2) is 0: return 0
             self.h1_event_cutflow.Fill(3)
      
             point = findpoint(hitx_lv2, hity_lv2, madx, mady)
             hit_signal = matchhit(len(hitx_lv2), len(hity_lv2), point)
             if len(hit_signal) > 128 or len(hit_signal) is 0: return 0 # huge hit channel (over max size of leaf) or no signal   
             self.h1_event_cutflow.Fill(4)

             # varaibles of ntuple 
             struct.nsignalx_lv1 = len(hitx_lv1)
             struct.nsignaly_lv1 = len(hity_lv1)
             struct.nsignalx_lv2 = len(hitx_lv2)
             struct.nsignaly_lv2 = len(hity_lv2)
             struct.npoint = len(hitx_lv2)*len(hity_lv2)
             struct.nhit = len(hit_signal)
             struct.trigger = self.tree.integral_livetime
             makentuple(hit_signal,point,hitx_lv2, hity_lv2,hitx_lv1, hity_lv1)
             self.tout.Fill()

          return self.drawables


"""       
def tran(args):
    
    fout = ROOT.TFile( args.output, 'recreate' )
    f = ROOT.TFile(args.input)   
    tree = f.Get("eventtree")
    slinename = "../run/auxfile/spline_calibration.root"
    Efile = ROOT.TFile(slinename, 'read') # not always open

    h2_lv1 = ROOT.TH2D("hist_level1","level1 hit channel",20,0,20,20,0,20)
    h2_lv1.GetXaxis().SetTitle("X")
    h2_lv1.GetYaxis().SetTitle("Y")
    h2_lv2 = ROOT.TH2D("hist_level2","level2 hit channel",20,0,20,20,0,20)
    h2_lv2.GetXaxis().SetTitle("X")
    h2_lv2.GetYaxis().SetTitle("Y")
    hx = ROOT.TH1D("hist_cmn_pside","p-side adc - cmn",1024,-50.5,973.5)
    hy = ROOT.TH1D("hist_cmn_nside","n-side adc - cmn",1024,-50.5,973.5)
    h2_cutflow_x = ROOT.TH2D("hist_cutflow_x","remained hit after the selections",3,0,3,128,0,128)
    h2_cutflow_y = ROOT.TH2D("hist_cutflow_y","remained hit after the selections",3,0,3,128,0,128)
    h2_Label = ["Raw","Level 1","Level 2"]
    h2_cutflow_x.GetYaxis().SetTitle("number of hits")
    h2_cutflow_y.GetYaxis().SetTitle("number of hits")
    for i in range(len(h2_Label)): 
       h2_cutflow_x.GetXaxis().SetBinLabel(i+1,h2_Label[i])
       h2_cutflow_y.GetXaxis().SetBinLabel(i+1,h2_Label[i])
    h1_event_cutflow = ROOT.TH1D("hist_event_cutflow","events after the selections",5,0,5)
    h1_Label = ["Raw","trigger","Level 1","Level 2", "photon"]
    for i in range(len(h1_Label)):
       h1_event_cutflow.GetXaxis().SetBinLabel(i+1,h1_Label[i])
   
    log().info("Starting Job: %s"%(asctime(localtime()))) 

    coef_R = 1 # random to ADC to avoid quantum phenomenon
    if not enums.IsRandom : coef_R = 0

    ti = time.time()

    fout.cd()
    tout = TTree('tree','tree') 
    tout.Branch( 'trigger', struct, 'trigger/I:nsignalx_lv1:nsignaly_lv1:nsignalx_lv2:nsignaly_lv2:npoint:nhit' ) 
    tout.Branch( 'energy_p', AddressOf( struct, 'energy_p' ),    'energy_p[nhit]/D' )
    tout.Branch( 'energy_n', AddressOf( struct, 'energy_n' ),    'energy_n[nhit]/D' )
    tout.Branch( 'adc_p', AddressOf( struct, 'adc_p' ),          'adc_p[nhit]/D' )
    tout.Branch( 'adc_n', AddressOf( struct, 'adc_n' ),          'adc_n[nhit]/D' )
    tout.Branch( 'x', AddressOf( struct, 'axis_x' ),             'x[nhit]/I' )
    tout.Branch( 'y', AddressOf( struct, 'axis_y' ),             'y[nhit]/I' )
    tout.Branch( 'mergehit_x', AddressOf( struct, 'mergehit_x' ),'mergehit_x[nhit]/I' )
    tout.Branch( 'mergehit_y', AddressOf( struct, 'mergehit_y' ),'mergehit_y[nhit]/I' )
    tout.Branch( 'weight', AddressOf( struct, 'weight' ),        'weight[nhit]/D' )

    tout_p = TTree('pointtree','pointtree') 
    tout_p.Branch( 'npoint', pointstruct, 'npoint/I' ) 
    tout_p.Branch( 'energy_p', AddressOf( pointstruct, 'E_p' ),    'energy_p[npoint]/D' )
    tout_p.Branch( 'energy_n', AddressOf( pointstruct, 'E_n' ),    'energy_n[npoint]/D' )
    tout_p.Branch( 'x', AddressOf( pointstruct, 'Poi_x' ),        'x[npoint]/I' )
    tout_p.Branch( 'y', AddressOf( pointstruct, 'Poi_y' ),        'y[npoint]/I' )
    tout_p.Branch( 'DeltaE', AddressOf( pointstruct, 'DeltaE' ),   'DeltaE[npoint]/D' )

    line = list()
    for ch in range(0, 256): 
       line.append(getlineEnergy(Efile, ch))

       if ch < 128:#x
          if ch < 10: hist_name = "hist_cmn" + "00" + str(ch) 
          elif ch < 100:  hist_name = "hist_cmn" + "0" + str(ch) 
          else : hist_name = "hist_cmn" + str(ch)
          hist = f.Get(hist_name) 
          hx.Add(hist)
       else:#y
          hist_name = "hist_cmn" + str(ch)
          hist = f.Get(hist_name) 
          hy.Add(hist)

    cut_p, cut_n = findadccut(line)
#    coef_a, coef_b = findx2yshift(hx, hy)

    tree = DisableBranch(tree)
    skimmingtree = PreEventSelection(args.input, tree)
    
    h1_event_cutflow.Fill(0,tree.GetEntries())
    h1_event_cutflow.Fill(1,skimmingtree.GetN())
    prog = ProgressBar(ntotal=skimmingtree.GetN(),text="Processing ntuple",init_t=ti)

    for ie in range(skimmingtree.GetN()):
       nevproc=ie
       prog.update(nevproc)
       #if ie%5000 is 0 : print("event running : ", ie , " time : ", time.time() - ti)
       tree.GetEntry(skimmingtree.GetEntry(ie))
       h2_cutflow_x.Fill(0, 128)
       h2_cutflow_y.Fill(0, 128)

       hitx_lv1, hity_lv1 = Level1Hit(tree, line, cut_p, cut_n, coef_R) # cut adc & save info.
       h2_lv1.Fill(len(hitx_lv1),len(hity_lv1))
       h2_cutflow_x.Fill(1, len(hitx_lv1))
       h2_cutflow_y.Fill(1, len(hity_lv1))
       if len(hitx_lv1) is 0 or len(hity_lv1) is 0: continue
       h1_event_cutflow.Fill(2)

       hitx_lv2, hity_lv2, madx, mady = Level2Hit(hitx_lv1, hity_lv1) # merge adjacent signal
       h2_lv2.Fill(len(hitx_lv2),len(hity_lv2))
       h2_cutflow_x.Fill(2, len(hitx_lv2))
       h2_cutflow_y.Fill(2, len(hity_lv2))
       if len(hitx_lv2) is 0 or len(hity_lv2) is 0: continue
       h1_event_cutflow.Fill(3)
      
       point = findpoint(hitx_lv2, hity_lv2, madx, mady)
       hit_signal = matchhit(len(hitx_lv2), len(hity_lv2), point)
       if len(hit_signal) > 512 or len(hit_signal) is 0: continue # huge hit channel (over max size of leaf) or no signal   
       h1_event_cutflow.Fill(4)

       # ntuple for each point
       pointstruct.npoint = len(hitx_lv2)*len(hity_lv2)
       makepointtree(point)
       tout_p.Fill()
       
       # varaibles of ntuple 
       struct.nsignalx_lv1 = len(hitx_lv1)
       struct.nsignaly_lv1 = len(hity_lv1)
       struct.nsignalx_lv2 = len(hitx_lv2)
       struct.nsignaly_lv2 = len(hity_lv2)
       struct.npoint = len(hitx_lv2)*len(hity_lv2)
       struct.nhit = len(hit_signal)
       struct.trigger = tree.integral_livetime
       makentuple(hit_signal)
       tout.Fill()

    prog.finalize()
    tf = time.time()
    dt = tf - ti
    checkTree(tout,tree)
    log().info("Info. processing time: %.1f s"%(dt))
    
    cv = createRatioCanvas("cv",1600,800)
    cv.Divide(2,1)
    cv.cd(1).SetRightMargin(0.18)
    h2_cutflow_x.Draw("colz TEXT0")
    cv.cd(2).SetRightMargin(0.18)
    h2_cutflow_y.Draw("colz TEXT0")
    
    cv.Write()
    hx.Write()
    hy.Write()
    h2_lv1.Write()
    h2_lv2.Write()
    h2_cutflow_x.Write()
    h2_cutflow_y.Write()
    h1_event_cutflow.Write()
    tout.Write()
    tout_p.Write()

    fout.Close()
    Efile.Close()

    if __name__ is not "__main__": return tout
"""

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("input", type=str, default="../rawdata/calibration_data/20200225a_am241_5plus.root", help="Input File Name")
    parser.add_argument("--output", type=str, default="../run/root/tranadc_dsd", help="Input File Name")
    parser.add_argument("--channel", default=False, action="store_true", help="number of CPU")
    parser.add_argument("--adc", default=False, action="store_true", help="log progess")
    args = parser.parse_args()

    tran( args)

