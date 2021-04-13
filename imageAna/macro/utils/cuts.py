#!/usr/bin/env python    
#-*- coding:utf-8 -*-   
"""
This module provides definition of cuts.
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
import enums 
from utils.logger import log

def PreEventSelection(ifile, tree, nmax):
    if not nmax: nmax = tree.GetEntries()
    cut = TCut("1")
    if "test_f_" in ifile : cut = TCut("integral_livetime > 500 && integral_livetime < 1500")#JPARC March Si-data
    if "20200307a" in ifile : cut = TCut("integral_livetime > 220 && integral_livetime < 380")#JPARC March CdTe-data
    cut += TCut("Entry$ < {}".format(nmax))
    cv = ROOT.TCanvas("","")
    tree.Draw(">>elist", cut) 
    elist = gROOT.FindObject("elist")
    _cutname=cut.GetTitle()
    return elist,_cutname

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
         
def findadccut(line, dtype, ecut):
    adccut = []
    if ecut is None : applyEcut = enums.EnergyCut
    else : applyEcut = ecut
    if "CdTe" in dtype:
       for ch in range(0, 256): 
          cut_flag = 0
          for iadc in range(20,500):
             if ch < 128: #asic 0~3
                if (line[ch].Eval(iadc) > applyEcut) and (cut_flag == 0): 
                   adccut.append(iadc)
                   cut_flag = 1
             else: #asic 4~7
                if (line[ch].Eval(iadc) > (applyEcut/2.)) and (cut_flag == 0): 
                   adccut.append(iadc)
                   cut_flag = 1
          if cut_flag == 0: adccut.append(enums.ADCUpperBound)# not find a good cut value for adc, drop this channel
    else:
       for ch in range(0, 256): 
          cut_flag = 0
          for iadc in range(10,1000):
             if ch < 128: #asic 0~3
                if (line[ch].Eval(iadc) > (applyEcut)) and (cut_flag == 0): 
                   adccut.append(iadc)
                   cut_flag = 1
             else: #asic 4~7
                if (line[ch].Eval(iadc) > (applyEcut)) and (cut_flag == 0): 
                   adccut.append(iadc)
                   cut_flag = 1
          if cut_flag == 0: adccut.append(enums.ADCUpperBound)# not find a good cut value for adc, drop this channel
    return adccut 

