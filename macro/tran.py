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
#sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/macro/utils/')
#sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/macro/scripts/')
from utils.printInfo import checkTree
from utils.slimming import DisableBranch
from utils.countHit import Level1HitAll, Level2Hit, findcluster, ClusterCategory, matchLv2, Level1Hit
from utils.cuts import PreEventSelection, findx2yshift, findadccut
from utils.hits import database, rawdata_eventtree
import enums
from utils.helpers import ProgressBar

gROOT.ProcessLine(
"struct RootStruct {\
   Int_t      trigger;\
   Int_t      unixtime;\
   Int_t      initUT;\
   Int_t      nhit;\
   Int_t      ncluster;\
   Int_t      nsignalx_lv1;\
   Int_t      nsignaly_lv1;\
   Int_t      nsignalx_lv2;\
   Int_t      nsignaly_lv2;\
   Double_t  energy_p[128];\
   Double_t  energy_n[128];\
   Double_t     adc_p[128];\
   Double_t     adc_n[128];\
   Double_t    axis_x[128];\
   Double_t    axis_y[128];\
   Double_t    type[128];\
   Double_t       E_p[512];\
   Double_t       E_n[512];\
   Double_t   E_p_lv1[128];\
   Double_t   E_n_lv1[128];\
   Double_t   E_p_lv2[128];\
   Double_t   E_n_lv2[128];\
   Double_t   Nstrips_p_lv2[128];\
   Double_t   Nstrips_n_lv2[128];\
   Double_t     Poi_x[512];\
   Double_t     Poi_y[512];\
   Double_t Poi_x_lv1[128];\
   Double_t Poi_y_lv1[128];\
   Double_t Poi_x_lv2[128];\
   Double_t Poi_y_lv2[128];\
   Double_t    DeltaE[512];\
   Double_t Nstrips_x[512];\
   Double_t Nstrips_y[512];\
};"
); 

from ROOT import RootStruct
struct = RootStruct()

def getlineEnergy(energyFile, name, channel): 
    if "spline_maxbin" in name : return energyFile.Get('Calline%s'%(channel))
    # return energyFile.Get('spline_%s'%(channel)) #TODO calibration data is not good enough
    else:       
       if channel is 240: return energyFile.Get('spline_%s'%(239))
       elif channel >= 154 and channel <= 165:  return energyFile.Get('spline_%s'%(153))
       elif channel >= 219 and channel <= 225:  return energyFile.Get('spline_%s'%(218))
       else: return energyFile.Get('spline_%s'%(channel))
       

def getTSpline(self,fname, efname, dblist):
    f = ROOT.TFile(fname) 
    line = list()
    if efname:
       ef = ROOT.TFile(efname, 'read')
       for ch in range(0, 256): 
          line.append(getlineEnergy(ef, efname, ch))
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
       ef.Close()
    else:
       for ch in range(0, 256):
          func=dblist[ch].calfunc.Clone()
          line.append(func)
    return line       

def Getdatabase():
    databasename = "/Users/chiu.i-huan/Desktop/new_scientific/macro/auxfile/database.root"
    f = ROOT.TFile(databasename)
    dbtree = f.Get("dbtree") 
    mdatabase = []
    for m in dbtree:
       func = m.calfunc.Clone()
       D = database(m.detid,m.asicid,m.asicch,m.posx,m.posy,m.widthx,m.widthy,m.ethre,func)
       mdatabase.append(D) # List for id 
    f.Close()
    return mdatabase
    
def makentuple(signal, cluster, hitx_lv2, hity_lv2, hitx_lv1, hity_lv1):
    for n in range(1,len(signal)+1):          
       struct.adc_p[n-1]        = signal[n].adc_p
       struct.adc_n[n-1]        = signal[n].adc_n
       struct.energy_p[n-1]     = signal[n].energy_p
       struct.energy_n[n-1]     = signal[n].energy_n
       struct.axis_x[n-1]       = signal[n].x
       struct.axis_y[n-1]       = signal[n].y
       struct.type[n-1]       = signal[n].type
    for n in range(1,len(cluster)+1): # make cluster for adjacent channels
       struct.E_p[n-1]        = cluster[n].energy_p # energy sum of cluster
       struct.E_n[n-1]        = cluster[n].energy_n
       struct.Poi_x[n-1]      = cluster[n].x # position with max. energy
       struct.Poi_y[n-1]      = cluster[n].y
       struct.DeltaE[n-1]     = cluster[n].deltaE
       struct.Nstrips_x[n-1]  = cluster[n].nstrips_x # number of level-1 hits in cluster
       struct.Nstrips_y[n-1]  = cluster[n].nstrips_y
    for n in range(1,len(hitx_lv1)+1):          
       struct.E_p_lv1[n-1]        = hitx_lv1[n].energy
       struct.Poi_x_lv1[n-1]      = hitx_lv1[n].position
    for n in range(1,len(hity_lv1)+1):          
       struct.E_n_lv1[n-1]        = hity_lv1[n].energy
       struct.Poi_y_lv1[n-1]      = hity_lv1[n].position
    for n in range(1,len(hitx_lv2)+1):          
       struct.E_p_lv2[n-1]        = hitx_lv2[n].energy
       struct.Nstrips_p_lv2[n-1]  = hitx_lv2[n].nstrips
       struct.Poi_x_lv2[n-1]      = hitx_lv2[n].position
    for n in range(1,len(hity_lv2)+1):          
       struct.E_n_lv2[n-1]        = hity_lv2[n].energy
       struct.Nstrips_n_lv2[n-1]  = hity_lv2[n].nstrips
       struct.Poi_y_lv2[n-1]      = hity_lv2[n].position

def GetEventTree(tree, adccut, coef_R, dtype):
    m_rawdata_list = []
    nasic = 4
    if "CdTe" in dtype: nstrip = 64
    else : nstrip = 32
    index = 0
    for idet in range(2):
       for iasic in range(nasic):
          for istrip in range(nstrip):
             if "CdTe" in dtype and not istrip%2: continue # skip even strips in shimafuji-1 data
             m_rawdata = rawdata_eventtree()
             m_rawdata.detid      = idet # 0 is p-side(x), 1 is n-side(y)
             m_rawdata.asicid     = iasic+idet*4 # 0~3 is p-side, 4~7 is n-side
             m_rawdata.stripid    = index # 0 ~ 255
             m_rawdata.upperbound = 1000.
             m_rawdata.coef_R     = coef_R
             m_rawdata.adccut     = adccut[index]

             if (idet*nasic+iasic) is 0: 
                m_rawdata.adc    = tree.adc0[istrip]
                m_rawdata.cmn    = tree.cmn0
                m_rawdata.adcm   = tree.adc0[istrip] - tree.cmn0
             elif (idet*nasic+iasic) is 1: 
                m_rawdata.adc    = tree.adc1[istrip]
                m_rawdata.cmn    = tree.cmn1
                m_rawdata.adcm   = tree.adc1[istrip] - tree.cmn1
             elif (idet*nasic+iasic) is 2: 
                m_rawdata.adc    = tree.adc2[istrip]
                m_rawdata.cmn    = tree.cmn2
                m_rawdata.adcm   = tree.adc2[istrip] - tree.cmn2
             elif (idet*nasic+iasic) is 3: 
                m_rawdata.adc    = tree.adc3[istrip]
                m_rawdata.cmn    = tree.cmn3
                m_rawdata.adcm   = tree.adc3[istrip] - tree.cmn3
             elif (idet*nasic+iasic) is 4: 
                m_rawdata.adc    = tree.adc4[istrip]
                m_rawdata.cmn    = tree.cmn4
                m_rawdata.adcm   = tree.adc4[istrip] - tree.cmn4
             elif (idet*nasic+iasic) is 5: 
                m_rawdata.adc    = tree.adc5[istrip]
                m_rawdata.cmn    = tree.cmn5
                m_rawdata.adcm   = tree.adc5[istrip] - tree.cmn5
             elif (idet*nasic+iasic) is 6:
                m_rawdata.adc    = tree.adc6[istrip]
                m_rawdata.cmn    = tree.cmn6
                m_rawdata.adcm   = tree.adc6[istrip] - tree.cmn6
             elif (idet*nasic+iasic) is 7: 
                m_rawdata.adc    = tree.adc7[istrip]
                m_rawdata.cmn    = tree.cmn7
                m_rawdata.adcm   = tree.adc7[istrip] - tree.cmn7
             
             index += 1
             if m_rawdata.adcm < m_rawdata.adccut : continue 
             m_rawdata_list.append(m_rawdata)# info. for the selected strips
    return m_rawdata_list

class tran_process():
      def __init__(self,
                   ifile=None,
                   tree=None,
                   event_list=None,
                   efile=None,
                   dtype=None,
                   ecut=None,
                   deltae=None,
                   initUT=None
                   ):
          # config
          self.ifile      = ifile
          self.tree       = tree
          self.event_list = event_list
          self.dtype      = dtype
          self.ecut       = ecut
          self.deltae     = deltae
          self.efile      = efile
          self.initUT     = initUT
           
          # members
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
          self.h1_lv2_x_nstrips = ROOT.TH1D("p-side_n","p-side nstrips of level2hit",20,0,20)
          self.h1_lv2_x_nstrips.SetDirectory(0)
          self.h1_lv2_y_nstrips = ROOT.TH1D("n-side_n","n-side nstrips of level2hit",20,0,20)
          self.h1_lv2_y_nstrips.SetDirectory(0)
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
#          self.h1_event_cutflow = ROOT.TH1D("hist_event_cutflow","events after the selections",5,0,5)
#          self.h1_event_cutflow.SetDirectory(0)
#          h1_Label = ["Raw","trigger","Level 1","Level 2", "photon"]
#          for i in range(len(h1_Label)):
#             self.h1_event_cutflow.GetXaxis().SetBinLabel(i+1,h1_Label[i])   

          self.tout = TTree('tree','tree') 
          self.tout.SetDirectory(0)
          self.tout.Branch( 'intvar', struct, 'trigger/I:unixtime:initUT:nhit:ncluster:nsignalx_lv1:nsignaly_lv1:nsignalx_lv2:nsignaly_lv2' )  

          self.tout.Branch( 'energy_p', AddressOf( struct, 'energy_p' ),  'energy_p[nhit]/D' )
          self.tout.Branch( 'energy_n', AddressOf( struct, 'energy_n' ),  'energy_n[nhit]/D' )
          self.tout.Branch( 'adc_p',    AddressOf( struct, 'adc_p' ),     'adc_p[nhit]/D' )
          self.tout.Branch( 'adc_n',    AddressOf( struct, 'adc_n' ),     'adc_n[nhit]/D' )
          self.tout.Branch( 'x',        AddressOf( struct, 'axis_x' ),    'x[nhit]/D' )
          self.tout.Branch( 'y',        AddressOf( struct, 'axis_y' ),    'y[nhit]/D' )
          self.tout.Branch( 'type',        AddressOf( struct, 'type' ),   'type[nhit]/D' )

          self.tout.Branch( 'E_p',     AddressOf( struct, 'E_p' ),        'E_p[ncluster]/D' )
          self.tout.Branch( 'E_n',     AddressOf( struct, 'E_n' ),        'E_n[ncluster]/D' )
          self.tout.Branch( 'E_p_lv1', AddressOf( struct, 'E_p_lv1' ),    'E_p_lv1[nsignalx_lv1]/D' )
          self.tout.Branch( 'E_n_lv1', AddressOf( struct, 'E_n_lv1' ),    'E_n_lv1[nsignaly_lv1]/D' )
          self.tout.Branch( 'E_p_lv2', AddressOf( struct, 'E_p_lv2' ),    'E_p_lv2[nsignalx_lv2]/D' )
          self.tout.Branch( 'E_n_lv2', AddressOf( struct, 'E_n_lv2' ),    'E_n_lv2[nsignaly_lv2]/D' )
          self.tout.Branch( 'Nstrips_p_lv2', AddressOf( struct, 'Nstrips_p_lv2' ),    'Nstrips_p_lv2[nsignalx_lv2]/D' )
          self.tout.Branch( 'Nstrips_n_lv2', AddressOf( struct, 'Nstrips_n_lv2' ),    'Nstrips_n_lv2[nsignaly_lv2]/D' )

          self.tout.Branch( 'Poi_x',     AddressOf( struct, 'Poi_x' ),    'Poi_x[ncluster]/D' )
          self.tout.Branch( 'Poi_y',     AddressOf( struct, 'Poi_y' ),    'Poi_y[ncluster]/D' )
          self.tout.Branch( 'Poi_x_lv1', AddressOf( struct, 'Poi_x_lv1' ),'Poi_x_lv1[nsignalx_lv1]/D' )
          self.tout.Branch( 'Poi_y_lv1', AddressOf( struct, 'Poi_y_lv1' ),'Poi_y_lv1[nsignaly_lv1]/D' )
          self.tout.Branch( 'Poi_x_lv2', AddressOf( struct, 'Poi_x_lv2' ),'Poi_x_lv2[nsignalx_lv2]/D' )
          self.tout.Branch( 'Poi_y_lv2', AddressOf( struct, 'Poi_y_lv2' ),'Poi_y_lv2[nsignaly_lv2]/D' )

          self.tout.Branch( 'DeltaE',  AddressOf( struct, 'DeltaE' ),     'DeltaE[ncluster]/D' )
          self.tout.Branch( 'Nstrips_x', AddressOf( struct, 'Nstrips_x' ),'Nstrips_x[ncluster]/D' )
          self.tout.Branch( 'Nstrips_y', AddressOf( struct, 'Nstrips_y' ),'Nstrips_y[ncluster]/D' )

          self.coef_R = 1 # random to ADC to avoid quantum phenomenon
          if not enums.IsRandom : self.coef_R = 0
          self.dblist = Getdatabase()

          self.line = getTSpline(self, ifile, self.efile, self.dblist) 
          self.cut = findadccut(self.line, self.dtype, self.ecut)
      #    coef_a, coef_b = findx2yshift(self.hx, self.hy)

          self.hist_list.append(self.h2_lv1)
          self.hist_list.append(self.h2_lv2)
          self.hist_list.append(self.hx)
          self.hist_list.append(self.hy)
          self.hist_list.append(self.h2_cutflow_x)
          self.hist_list.append(self.h2_cutflow_y)
          self.hist_list.append(self.h1_lv2_x_nstrips)
          self.hist_list.append(self.h1_lv2_y_nstrips)
#          self.hist_list.append(self.h1_event_cutflow)
          self.tree_list.append(self.tout)

          self.drawables = self.hist_list + self.tree_list

      def tran_adc2e(self,ie):
          hitx_lv2, hity_lv2, cluster, hit_signal = {},{},{},{}
          self.tree.GetEntry(self.event_list.GetEntry(ie))

          self.h2_cutflow_x.Fill(0, 128)
          self.h2_cutflow_y.Fill(0, 128)

#          rawdata_list = GetEventTree(self.tree, self.cut, self.coef_R, self.dtype)
#          hitx_lv1, hity_lv1 = Level1HitAll(rawdata_list, self.line, self.dblist)
          hitx_lv1, hity_lv1 = Level1Hit(self.tree, self.cut, self.coef_R, self.dblist, self.efile, self.line, self.dtype)#Slow
          self.h2_lv1.Fill(len(hitx_lv1),len(hity_lv1))
          self.h2_cutflow_x.Fill(1, len(hitx_lv1))
          self.h2_cutflow_y.Fill(1, len(hity_lv1))

          if len(hitx_lv1) is not 0 and len(hity_lv1) is not 0:
             hitx_lv2, hity_lv2 = Level2Hit(hitx_lv1, hity_lv1) # merge adjacent signal
             self.h2_lv2.Fill(len(hitx_lv2),len(hity_lv2))
             self.h2_cutflow_x.Fill(2, len(hitx_lv2))
             self.h2_cutflow_y.Fill(2, len(hity_lv2))
             for _mx in hitx_lv2 : self.h1_lv2_x_nstrips.Fill(hitx_lv2[_mx].nstrips)
             for _my in hity_lv2 : self.h1_lv2_y_nstrips.Fill(hity_lv2[_my].nstrips)

          if len(hitx_lv2) is not 0 and len(hity_lv2) is not 0:   
             cluster = findcluster(hitx_lv2, hity_lv2)#Slow
#             hit_signal = ClusterCategory(cluster)#Slow
             hit_signal = matchLv2(hitx_lv2, hity_lv2, self.deltae)

          if len(hitx_lv2)*len(hity_lv2) > 512: return 0 # huge hit channel 
          if len(hit_signal) is 0: return 0 # skip 0 hit events

          # varaibles of ntuple 
          struct.nsignalx_lv1 = len(hitx_lv1)
          struct.nsignaly_lv1 = len(hity_lv1)
          struct.nsignalx_lv2 = len(hitx_lv2)
          struct.nsignaly_lv2 = len(hity_lv2)
          struct.ncluster = len(hitx_lv2)*len(hity_lv2)
          struct.nhit = len(hit_signal)
          struct.trigger  = self.tree.integral_livetime
          struct.unixtime = self.tree.unixtime
          struct.initUT   = int(self.initUT)
          makentuple(hit_signal,cluster,hitx_lv2, hity_lv2,hitx_lv1, hity_lv1)
          self.tout.Fill()

