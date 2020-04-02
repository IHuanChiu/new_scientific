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

def PreEventSelection(args, tree):
    cut = TCut("1")
    if "test" in args.input : cut = TCut("integral_livetime > 500 && integral_livetime < 1500")
    cv = ROOT.TCanvas("","")
    tree.Draw(">>elist", cut) 
    elist = gROOT.FindObject("elist")
    return elist

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
    for ch in range(0, 128): 
       cut_flag = 0
       for iadc in range(20,500):
          if (line[ch].Eval(iadc) > enums.EnergyCut) and (cut_flag is 0): 
             adccut_p.append(iadc)
             cut_flag = 1
       if cut_flag is 0: adccut_p.append(100)# not find a good cut value for adc
    for ch in range(0, 128): 
       cut_flag = 0
       for iadc in range(20,500):
          if (line[ch+128].Eval(iadc) > enums.EnergyCut) and (cut_flag is 0): 
             adccut_n.append(iadc)
             cut_flag = 1
       if cut_flag is 0: adccut_n.append(100)# not find a good cut value for adc
    return adccut_p, adccut_n   

