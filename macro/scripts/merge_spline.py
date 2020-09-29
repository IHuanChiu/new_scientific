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
from ROOT import TFile, TTree, gPad, TGraphAsymmErrors, TSpline3, gStyle, gErrorIgnoreLevel, gROOT
ROOT.gROOT.SetBatch(1)

fa=ROOT.TFile("spline_calibration_2mmtest_Am.root","read")
fb=ROOT.TFile("spline_calibration_2mmtest_Ba.root","read")
fc=ROOT.TFile("spline_calibration_2mmtest_Co.root","read")

def compare():   
    for k in range(64):
       c0 = ROOT.TCanvas("temp_"+str(k),"temp_"+str(k),800,800)
       c0.Divide(2,2)
       for j in range(4):
          c0.cd(j+1)
          i=k*4+j 
          linename = "spline_"+str(i) 
          la=fa.Get(linename)
          lb=fb.Get(linename)
          lc=fc.Get(linename)
          la.SetLineColor(1)
          lb.SetLineColor(2)
          lc.SetLineColor(4)
          la.Draw()
          lb.Draw("same")
          lc.Draw("same")
   
          leg = ROOT.TLegend(.55,.28,.75,.40)
          leg.SetFillColor(0)
          leg.SetLineColor(0)
          leg.SetBorderSize(0)
          leg.AddEntry(la,  "Am", "l")
          leg.AddEntry(lb,  "Ba", "l")
          leg.AddEntry(lc,  "Co", "l")
          leg.Draw("same")
          del la,lb,lc           
       c0.SaveAs("/Users/chiu.i-huan/Desktop/new_scientific/run/figs/cali_plots/comparison_ch{0}_ch{1}.pdf".format(k*4,(k+1)*4)-1)
    return 1

def merge():
    return 1

if __name__ == "__main__":
   compare()
