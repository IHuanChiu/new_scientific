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
from random import gauss
import numpy as np
from utils.printInfo import checkTree
from utils.slimming import DisableBranch
from utils.countHit import Level1HitArray, Level2Hit, findcluster, ClusterCategory, matchLv2, Level1Hit
from utils.cuts import PreEventSelection, findx2yshift, findadccut
from utils.hits import database, rawdata_eventtree
import enums
from utils.helpers import ProgressBar

gROOT.ProcessLine(
"struct RootStruct {\
   Int_t      trigger;\
   Int_t      livetime;\
   Int_t      unixtime;\
   Int_t      nhit;\
   Int_t      ncluster;\
   Int_t      nsignalx_lv1;\
   Int_t      nsignaly_lv1;\
   Int_t      nsignalx_lv2;\
   Int_t      nsignaly_lv2;\
   Double_t  energy[128];\
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
   Int_t   Nstrips_p_lv2[128];\
   Int_t   Nstrips_n_lv2[128];\
   Double_t     Poi_x[512];\
   Double_t     Poi_y[512];\
   Double_t Poi_x_lv1[128];\
   Double_t Poi_y_lv1[128];\
   Double_t Poi_x_lv2[128];\
   Double_t Poi_y_lv2[128];\
   Double_t    DeltaE[512];\
   Double_t Nstrips_x[512];\
   Double_t Nstrips_y[512];\
   Double_t Stripid_x_lv1[128];\
   Double_t Stripid_y_lv1[128];\
};"
); 

from ROOT import RootStruct
struct = RootStruct()

def getlineEnergy(energyFile,channel): 
    if "spline_maxbin" in energyFile.GetName() : return energyFile.Get('Calline%s'%(channel))
    elif "spline_calibration.root" in energyFile.GetName(): # For Si-detector calibration
       if channel == 240: return energyFile.Get('spline_%s'%(239))
       if channel >= 154 and channel <= 165:  return energyFile.Get('spline_%s'%(153))
       if channel >= 219 and channel <= 225:  return energyFile.Get('spline_%s'%(218))
       if channel == 127:  return energyFile.Get('spline_%s'%(126))
       return energyFile.Get('spline_%s'%(channel))
    elif "m5c400v.root" in energyFile.GetName(): # watanabe file 
       if channel < 10: cal_name = "calfunc_" + "00" + str(channel) 
       elif channel < 100:  cal_name = "calfunc_" + "0" + str(channel) 
       else : cal_name = "calfunc_" + str(channel)
       return energyFile.Get(cal_name)
    else: 
       return energyFile.Get('graph_%s'%(channel))
       #return energyFile.Get('spline_%s'%(channel))
       #return energyFile.Get('fline_%s'%(channel))
 
def getTSpline(efname,dblist):
    line = list()
    if efname:
       ef = ROOT.TFile(efname, 'read')
       for ch in range(0, 256): 
          line.append(getlineEnergy(ef,ch))
       ef.Close()
    else:
       for ch in range(0, 256):
          func=dblist[ch].calfunc.Clone()
          line.append(func)
    return line       

def getResponse():
    _response_list=dict()
    _file=ROOT.TFile("/Users/chiu.i-huan/Desktop/new_scientific/imageAna/macro/auxfile/epi2_epi1_caldata.root")
    _response_list.update({"p1n1":_file.Get("graph2d_1_1")})
    _response_list.update({"p1n2":_file.Get("graph2d_1_2")})
    _response_list.update({"p1n3":_file.Get("graph2d_1_3")})
    _response_list.update({"p2n1":_file.Get("graph2d_2_1")})
    _response_list.update({"p2n2":_file.Get("graph2d_2_2")})
    _response_list.update({"p2n3":_file.Get("graph2d_2_3")})
    _response_list.update({"p3n1":_file.Get("graph2d_3_1")})
    _response_list.update({"p3n2":_file.Get("graph2d_3_2")})
    _response_list.update({"p3n3":_file.Get("graph2d_3_2")})
    _response_list.update({"p4n1":_file.Get("graph2d_4_1")})
    _response_list.update({"p4n2":_file.Get("graph2d_4_2")})
    _response_list.update({"p4n3":_file.Get("graph2d_4_2")})
    for _n in _response_list:
       _response_list[_n].SetDirectory(0)
    return _response_list

def Getdatabase():
    databasename = "/Users/chiu.i-huan/Desktop/new_scientific/imageAna/macro/auxfile/database.root"
    f = ROOT.TFile(databasename)
    dbtree = f.Get("dbtree") 
    mdatabase = []
    for m in dbtree:
       func = m.calfunc.Clone()
       D = database(m.detid,m.asicid,m.asicch,m.stripid,m.posx,m.posy,m.widthx,m.widthy,m.ethre,func)
       mdatabase.append(D) # List for asicid (0-7) -> asicch (0-62)
    f.Close()
    return mdatabase
    
def makentuple(signal, cluster, hitx_lv2, hity_lv2, hitx_lv1, hity_lv1):
    for n in range(1,len(signal)+1):          
       struct.adc_p[n-1]        = signal[n].adc_p
       struct.adc_n[n-1]        = signal[n].adc_n
       struct.energy[n-1]       = signal[n].energy
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
       struct.Stripid_x_lv1[n-1]  = hitx_lv1[n].stripid
    for n in range(1,len(hity_lv1)+1):          
       struct.E_n_lv1[n-1]        = hity_lv1[n].energy
       struct.Poi_y_lv1[n-1]      = hity_lv1[n].position
       struct.Stripid_y_lv1[n-1]  = hity_lv1[n].stripid
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
    if "FEC1" in dtype: 
       nasic = 4 # nasic for one side
       nstrip = 64 # nchannel for one ASIC
    elif "FEC2" in dtype: 
       nasic = 2
       nstrip = 64
    else:
       nasic = 4
       nstrip = 32
    index = 0
    for idet in range(2):
       for iasic in range(nasic):
          for istrip in range(nstrip):
             if "FEC1" in dtype and not istrip%2: continue # skip even strips in shimafuji-1 data
             m_rawdata = rawdata_eventtree()
             m_rawdata.detid      = idet # 0 is p-side(x), 1 is n-side(y)
             m_rawdata.asicid     = iasic+idet*nasic # p-side & n-side
             m_rawdata.stripid    = index # 0 ~ 255
             m_rawdata.upperbound = 1024 # limit for ADC
             m_rawdata.coef_R     = coef_R
             m_rawdata.adccut     = adccut[index]

             if (idet*nasic+iasic) == 0: 
                m_rawdata.adc    = tree.adc0[istrip]
                m_rawdata.cmn    = tree.cmn0
                m_rawdata.adcm   = tree.adc0[istrip] - tree.cmn0
             elif (idet*nasic+iasic) == 1: 
                m_rawdata.adc    = tree.adc1[istrip]
                m_rawdata.cmn    = tree.cmn1
                m_rawdata.adcm   = tree.adc1[istrip] - tree.cmn1
             elif (idet*nasic+iasic) == 2: 
                m_rawdata.adc    = tree.adc2[istrip]
                m_rawdata.cmn    = tree.cmn2
                m_rawdata.adcm   = tree.adc2[istrip] - tree.cmn2
             elif (idet*nasic+iasic) == 3: 
                m_rawdata.adc    = tree.adc3[istrip]
                m_rawdata.cmn    = tree.cmn3
                m_rawdata.adcm   = tree.adc3[istrip] - tree.cmn3
             elif (idet*nasic+iasic) == 4: 
                m_rawdata.adc    = tree.adc4[istrip]
                m_rawdata.cmn    = tree.cmn4
                m_rawdata.adcm   = tree.adc4[istrip] - tree.cmn4
             elif (idet*nasic+iasic) == 5: 
                m_rawdata.adc    = tree.adc5[istrip]
                m_rawdata.cmn    = tree.cmn5
                m_rawdata.adcm   = tree.adc5[istrip] - tree.cmn5
             elif (idet*nasic+iasic) == 6:
                m_rawdata.adc    = tree.adc6[istrip]
                m_rawdata.cmn    = tree.cmn6
                m_rawdata.adcm   = tree.adc6[istrip] - tree.cmn6
             elif (idet*nasic+iasic) == 7: 
                m_rawdata.adc    = tree.adc7[istrip]
                m_rawdata.cmn    = tree.cmn7
                m_rawdata.adcm   = tree.adc7[istrip] - tree.cmn7
             
             index += 1
             if m_rawdata.adcm < m_rawdata.adccut : continue 
             m_rawdata_list.append(m_rawdata)# info. for the selected strips
    return m_rawdata_list

class tran_process():
      def __init__(self,
                   tree=None,
                   event_list=None,
                   efile=None,
                   dtype=None,
                   ecut=None,
                   deltae=None
                   ):
          # ==================================
          # config 
          # ==================================
          self.tree       = tree
          self.event_list = event_list
          self.dtype      = dtype
          self.ecut       = ecut
          self.deltae     = deltae
          self.efile      = efile
           
          # ==================================
          # members
          # ==================================
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
          #self.hx = ROOT.TH1D("hist_cmn_pside","p-side adc - cmn",1024,-50.5,973.5)
          #self.hy = ROOT.TH1D("hist_cmn_nside","n-side adc - cmn",1024,-50.5,973.5)
          #self.hx.SetDirectory(0)
          #self.hy.SetDirectory(0)
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

          # ==================================
          # tree
          # ==================================
          self.tout = TTree('tree','tree') 
          self.tout.SetDirectory(0)
          self.tout.Branch( 'intvar', struct, 'trigger/I:livetime:unixtime:nhit:ncluster:nsignalx_lv1:nsignaly_lv1:nsignalx_lv2:nsignaly_lv2' )  
          #  === match hit (case-1, case-2 ...) ===
          self.tout.Branch( 'energy', AddressOf( struct, 'energy' ),  'energy[nhit]/D' )
          self.tout.Branch( 'energy_p', AddressOf( struct, 'energy_p' ),  'energy_p[nhit]/D' )
          self.tout.Branch( 'energy_n', AddressOf( struct, 'energy_n' ),  'energy_n[nhit]/D' )
          self.tout.Branch( 'adc_p',    AddressOf( struct, 'adc_p' ),     'adc_p[nhit]/D' )
          self.tout.Branch( 'adc_n',    AddressOf( struct, 'adc_n' ),     'adc_n[nhit]/D' )
          self.tout.Branch( 'x',        AddressOf( struct, 'axis_x' ),    'x[nhit]/D' )
          self.tout.Branch( 'y',        AddressOf( struct, 'axis_y' ),    'y[nhit]/D' )
          self.tout.Branch( 'type',        AddressOf( struct, 'type' ),   'type[nhit]/D' )

          #  === Lv1: raw data with base energy cut; Lv2: merged hit ===
          self.tout.Branch( 'E_p_lv1', AddressOf( struct, 'E_p_lv1' ),    'E_p_lv1[nsignalx_lv1]/D' )
          self.tout.Branch( 'E_n_lv1', AddressOf( struct, 'E_n_lv1' ),    'E_n_lv1[nsignaly_lv1]/D' )
          self.tout.Branch( 'E_p_lv2', AddressOf( struct, 'E_p_lv2' ),    'E_p_lv2[nsignalx_lv2]/D' )
          self.tout.Branch( 'E_n_lv2', AddressOf( struct, 'E_n_lv2' ),    'E_n_lv2[nsignaly_lv2]/D' )
          self.tout.Branch( 'Nstrips_p_lv2', AddressOf( struct, 'Nstrips_p_lv2' ),    'Nstrips_p_lv2[nsignalx_lv2]/I' )
          self.tout.Branch( 'Nstrips_n_lv2', AddressOf( struct, 'Nstrips_n_lv2' ),    'Nstrips_n_lv2[nsignaly_lv2]/I' )

#          self.tout.Branch( 'Poi_x_lv1', AddressOf( struct, 'Poi_x_lv1' ),'Poi_x_lv1[nsignalx_lv1]/D' )
#          self.tout.Branch( 'Poi_y_lv1', AddressOf( struct, 'Poi_y_lv1' ),'Poi_y_lv1[nsignaly_lv1]/D' )
#          self.tout.Branch( 'Poi_x_lv2', AddressOf( struct, 'Poi_x_lv2' ),'Poi_x_lv2[nsignalx_lv2]/D' )
#          self.tout.Branch( 'Poi_y_lv2', AddressOf( struct, 'Poi_y_lv2' ),'Poi_y_lv2[nsignaly_lv2]/D' )
          self.tout.Branch( 'Stripid_x_lv1', AddressOf( struct, 'Stripid_x_lv1' ),'Stripid_x_lv1[nsignalx_lv1]/D' )
          self.tout.Branch( 'Stripid_y_lv1', AddressOf( struct, 'Stripid_y_lv1' ),'Stripid_y_lv1[nsignaly_lv1]/D' )

           # === Cluster ===
#          self.tout.Branch( 'E_p',     AddressOf( struct, 'E_p' ),        'E_p[ncluster]/D' )
#          self.tout.Branch( 'E_n',     AddressOf( struct, 'E_n' ),        'E_n[ncluster]/D' )
#          self.tout.Branch( 'Poi_x',     AddressOf( struct, 'Poi_x' ),    'Poi_x[ncluster]/D' )
#          self.tout.Branch( 'Poi_y',     AddressOf( struct, 'Poi_y' ),    'Poi_y[ncluster]/D' )
#          self.tout.Branch( 'DeltaE',  AddressOf( struct, 'DeltaE' ),     'DeltaE[ncluster]/D' )
#          self.tout.Branch( 'Nstrips_x', AddressOf( struct, 'Nstrips_x' ),'Nstrips_x[ncluster]/D' )
#          self.tout.Branch( 'Nstrips_y', AddressOf( struct, 'Nstrips_y' ),'Nstrips_y[ncluster]/D' )

          # ==================================
          # auxfiles
          # ==================================
          self.coef_R = 1 # random to ADC to avoid quantum phenomenon
          if not enums.IsRandom : self.coef_R = 0
          self.dblist = Getdatabase()
          self.line = getTSpline(self.efile, self.dblist) 
          self.response = getResponse()

          # ==================================
          # Draw hist. & tree
          # ==================================
          self.hist_list.append(self.h2_lv1)
          self.hist_list.append(self.h2_lv2)
#          self.hist_list.append(self.hx)
#          self.hist_list.append(self.hy)
#          self.hist_list.append(self.h2_cutflow_x)
#          self.hist_list.append(self.h2_cutflow_y)
#          self.hist_list.append(self.h1_lv2_x_nstrips)
#          self.hist_list.append(self.h1_lv2_y_nstrips)
#          self.hist_list.append(self.h1_event_cutflow)
          self.tree_list.append(self.tout)

          self.drawables = self.hist_list + self.tree_list

      def tran_adc2e(self,ie):
          # TODO: check processing time by "tti" var.
          tti=time.time()
          hitx_lv2, hity_lv2, cluster, hit_signal = {},{},{},{}
          self.tree.GetEntry(self.event_list.GetEntry(ie))

          tti2=time.time()
#          rawdata_list = GetEventTree(self.tree, self.cut, self.coef_R, self.dtype)
#          hitx_lv1, hity_lv1 = Level1HitArray(rawdata_list, self.line, self.dblist)
          hitx_lv1, hity_lv1 = Level1Hit(self.tree, self.coef_R, self.dblist, self.efile, self.line, self.dtype)#Slow
          self.h2_lv1.Fill(len(hitx_lv1),len(hity_lv1))

          tti3=time.time()
          hitx_lv2, hity_lv2 = Level2Hit(hitx_lv1, hity_lv1) # merge adjacent signal
          self.h2_lv2.Fill(len(hitx_lv2),len(hity_lv2))
#          for _mx in hitx_lv2 : self.h1_lv2_x_nstrips.Fill(hitx_lv2[_mx].nstrips)
#          for _my in hity_lv2 : self.h1_lv2_y_nstrips.Fill(hity_lv2[_my].nstrips)

          tti4=time.time()
          if len(hitx_lv2) != 0 and len(hity_lv2) != 0:   
   #          cluster = findcluster(hitx_lv2, hity_lv2)#Slow
   #          hit_signal = ClusterCategory(cluster)#Slow
             hit_signal = matchLv2(hitx_lv2, hity_lv2, self.deltae, self.response)

          tti5=time.time()
          if len(hitx_lv2)*len(hity_lv2) > 512: return 0 # huge hit channel 
          #if len(hit_signal) == 0: return 0 # skip 0 hit events, need those event to check lv1 hit

          # varaibles of ntuple 
          struct.nsignalx_lv1 = len(hitx_lv1)
          struct.nsignaly_lv1 = len(hity_lv1)
          struct.nsignalx_lv2 = len(hitx_lv2)
          struct.nsignaly_lv2 = len(hity_lv2)
          struct.ncluster = len(hitx_lv2)*len(hity_lv2)
          struct.nhit = len(hit_signal)
          struct.trigger  = self.tree.integral_livetime
          struct.livetime  = self.tree.livetime
          # if struct.trigger > 2147482648: print(struct.trigger)
          struct.unixtime = self.tree.unixtime
          makentuple(hit_signal,cluster,hitx_lv2, hity_lv2,hitx_lv1, hity_lv1)
          tti6=time.time()
          self.tout.Fill()
          ttif=tti6-tti
#          print("time ==> ", "GetEntry : ", (tti2-tti)/ttif, "lv1 : ",(tti3-tti2)/ttif, " lv2 : ",(tti4-tti3)/ttif, " match : ",(tti5-tti4)/ttif, " save : ",(tti6-tti5)/ttif )

