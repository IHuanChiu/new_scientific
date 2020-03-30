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

import sys,os,random,math,ROOT
from ROOT import TFile, TTree
from ROOT import gROOT, AddressOf, gPad
ROOT.gROOT.SetBatch(1)
import argparse
import math
from multiprocessing import Pool, cpu_count
import time
from array import array
import logging
from random import gauss
import numpy as np
from tran import getSpline
from image import createRatioCanvas

__location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
ROOT.gROOT.LoadMacro( __location__+'/AtlasStyle/AtlasStyle.C')
ROOT.SetAtlasStyle()

def plot(args):
    f = ROOT.TFile(args.input)   
    tree = f.Get("eventtree")
    slinename = "../run/auxfile/spline_calibration.root"
    Efile = ROOT.TFile(slinename, 'read') # not always open
    fout = ROOT.TFile( args.output, 'recreate' )
    line = list()
    for i in range(256):
       line.append(getSpline(Efile, i))
    nbin = 500
    cv  = createRatioCanvas("cv", 800, 800) 
    h1_p = ROOT.TH1D("specp","specp",nbin,0,100)
    h1_n = ROOT.TH1D("specn","specn",nbin,0,100)
    h1_all = ROOT.TH1D("specall","specall",nbin,0,100)
    ti = time.time()
    print(" all events : " , tree.GetEntries())
    for ie in range(tree.GetEntries()):
       if ie > 50000: continue
       if ie%10000 is 0 : print("event running : ", ie , " time : ", time.time() - ti)
       tree.GetEntry(ie)
       for ch in range(32):
          if(tree.adc0[ch]-tree.cmn0 > 30) : h1_p.Fill(line[ch + 32*0].Eval(tree.adc0[ch]-tree.cmn0 + random.uniform(-0.5,0.5)))
          if(tree.adc1[ch]-tree.cmn1 > 30) : h1_p.Fill(line[ch + 32*1].Eval(tree.adc1[ch]-tree.cmn1 + random.uniform(-0.5,0.5)))
          if(tree.adc2[ch]-tree.cmn2 > 30) : h1_p.Fill(line[ch + 32*2].Eval(tree.adc2[ch]-tree.cmn2 + random.uniform(-0.5,0.5)))
          if(tree.adc3[ch]-tree.cmn3 > 30) : h1_p.Fill(line[ch + 32*3].Eval(tree.adc3[ch]-tree.cmn3 + random.uniform(-0.5,0.5)))

          if(tree.adc4[ch]-tree.cmn4 > 80) : h1_n.Fill(line[ch + 32*0 + 128].Eval(tree.adc4[ch]-tree.cmn4 + random.uniform(-0.5,0.5)))
          if(tree.adc5[ch]-tree.cmn5 > 80) : h1_n.Fill(line[ch + 32*1 + 128].Eval(tree.adc5[ch]-tree.cmn5 + random.uniform(-0.5,0.5)))
          if(tree.adc6[ch]-tree.cmn6 > 80) : h1_n.Fill(line[ch + 32*2 + 128].Eval(tree.adc6[ch]-tree.cmn6 + random.uniform(-0.5,0.5)))
          if(tree.adc7[ch]-tree.cmn7 > 80) : h1_n.Fill(line[ch + 32*3 + 128].Eval(tree.adc7[ch]-tree.cmn7 + random.uniform(-0.5,0.5)))

          if(tree.adc0[ch]-tree.cmn0 > 30) : h1_all.Fill(line[ch + 32*0].Eval(tree.adc0[ch]-tree.cmn0 + random.uniform(-0.5,0.5)))
          if(tree.adc1[ch]-tree.cmn1 > 30) : h1_all.Fill(line[ch + 32*1].Eval(tree.adc1[ch]-tree.cmn1 + random.uniform(-0.5,0.5)))
          if(tree.adc2[ch]-tree.cmn2 > 30) : h1_all.Fill(line[ch + 32*2].Eval(tree.adc2[ch]-tree.cmn2 + random.uniform(-0.5,0.5)))
          if(tree.adc3[ch]-tree.cmn3 > 30) : h1_all.Fill(line[ch + 32*3].Eval(tree.adc3[ch]-tree.cmn3 + random.uniform(-0.5,0.5)))
          if(tree.adc4[ch]-tree.cmn4 > 80) : h1_all.Fill(line[ch + 32*0 + 128].Eval(tree.adc4[ch]-tree.cmn4 + random.uniform(-0.5,0.5)))
          if(tree.adc5[ch]-tree.cmn5 > 80) : h1_all.Fill(line[ch + 32*1 + 128].Eval(tree.adc5[ch]-tree.cmn5 + random.uniform(-0.5,0.5)))
          if(tree.adc6[ch]-tree.cmn6 > 80) : h1_all.Fill(line[ch + 32*2 + 128].Eval(tree.adc6[ch]-tree.cmn6 + random.uniform(-0.5,0.5)))
          if(tree.adc7[ch]-tree.cmn7 > 80) : h1_all.Fill(line[ch + 32*3 + 128].Eval(tree.adc7[ch]-tree.cmn7 + random.uniform(-0.5,0.5)))
    fout.cd()
    gPad.SetLogy(1)
    h1_p.SetLineColor(ROOT.kPink+9)
    h1_p.SetLineWidth(2)
    h1_p.SetMaximum(h1_p.GetMaximum()*30)
    h1_p.GetXaxis().SetTitle("Energy [keV]")
    h1_p.GetYaxis().SetTitle("Counts/{}keV".format(100./nbin))
    h1_n.SetLineColor(ROOT.kAzure-1)
    h1_n.SetLineWidth(2)
    h1_all.SetLineColor(1)
    h1_all.SetLineWidth(2)
    h1_p.Draw()
    h1_n.Draw("same")
    h1_all.Draw("same")
    leg = ROOT.TLegend(.45,.75,.6,.92)
    leg.AddEntry(h1_p,  "P-side", "l")
    leg.AddEntry(h1_n,  "N-side", "l")
    leg.AddEntry(h1_all,  "All", "l")
    leg.Draw("same")
    cv.SaveAs("../run/figs/quick_spec.pdf")

    h1_p.Write()
    h1_n.Write()
    h1_all.Write()
    cv.Write()
    fout.Close()
    
    

if __name__ == '__main__' : 
  parser = argparse.ArgumentParser(description='Process some integers.')
  parser.add_argument("input", type=str, default="./20151112_00009_001.root", help="Input File Name")
  parser.add_argument("--output", type=str, default="../run/root/quick_spectum.root", help="Input File Name")
  args = parser.parse_args()

  plot( args )

