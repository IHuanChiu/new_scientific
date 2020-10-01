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

def compare(spline):   
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
          spline[i].SetLineColor(1)
          la.SetLineColor(2)
          lb.SetLineColor(3)
          lc.SetLineColor(4)
          spline[i].Draw()
          la.Draw("same")
          lb.Draw("same")
          lc.Draw("same")
   
          leg = ROOT.TLegend(.55,.18,.75,.40)
          leg.SetFillColor(0)
          leg.SetLineColor(0)
          leg.SetBorderSize(0)
          leg.AddEntry(spline[i],  "merge", "l")
          leg.AddEntry(la,  "Am", "l")
          leg.AddEntry(lb,  "Ba", "l")
          leg.AddEntry(lc,  "Co", "l")
          leg.Draw("same")
          del la,lb,lc           
       c0.SaveAs("/Users/chiu.i-huan/Desktop/new_scientific/run/figs/cali_plots/comparison_ch{0}_ch{1}.pdf".format(k*4,(k+1)*4-1))

def merge():
    spline_list=[]
    fout=ROOT.TFile("spline_calibration_2mmtest_merge.root","recreate")
    fout.cd()
    for i in range(256):
       _g = ROOT.TGraph()
       _s = ROOT.TSpline3()
       _g.SetPoint(0, 0, 0)
       graph_name="graph_"+str(i)
       _ga=fa.Get(graph_name)
       _gb=fb.Get(graph_name)
       _gc=fc.Get(graph_name)
       # === check fitting plots & adc range (adc, energy) ===       
       _g.SetPoint(1, _ga.GetPointX(1), _ga.GetPointY(1))#Am 13.94
       _g.SetPoint(2, _gc.GetPointX(1), _gc.GetPointY(1))#Co 14.41
       _g.SetPoint(3, _ga.GetPointX(2), _ga.GetPointY(2))#Am 17.75
       _g.SetPoint(4, _ga.GetPointX(3), _ga.GetPointY(3))#Am 26.3
       _g.SetPoint(5, _gb.GetPointX(1), _gb.GetPointY(1))#Ba 31
       _g.SetPoint(6, _ga.GetPointX(4), _ga.GetPointY(4))#Am 59.5
       _g.SetPoint(7, _gb.GetPointX(3), _gb.GetPointY(3))#Ba 81
       _g.SetPoint(8, _gc.GetPointX(2), _gc.GetPointY(2))#Co 122
       slope = (_gc.GetPointY(2) - _gb.GetPointY(3))/(_gc.GetPointX(2) - _gb.GetPointX(3))
       f_x, f_y = _gc.GetPointX(2), _gc.GetPointY(2)
       _g.SetPoint(9, 1500, (1500-f_x)*slope + f_y)
       if i >= 128:#n-side
          _g.SetPoint(9, _gc.GetPointX(3), _gc.GetPointY(3))#Co 136.5
          slope = (_gc.GetPointY(3) - _gc.GetPointY(2))/(_gc.GetPointX(3) - _gc.GetPointX(2))
          f_x, f_y = _gc.GetPointX(3), _gc.GetPointY(3)
          _g.SetPoint(10, 1500, (1500-f_x)*slope + f_y)       
#       _s = ROOT.TSpline3("spline_"+str(i), _g)
#       _s.SetName("spline_"+str(i))
#       _g.SetName(graph_name)
       _g.SetName("spline_"+str(i))
       _g.Write()
#       _s.Write()
#       spline_list.append(_s)
       spline_list.append(_g)
       del _g,_s    
    fout.Write()
    fout.Close()
    compare(spline_list)

if __name__ == "__main__":
   merge()
