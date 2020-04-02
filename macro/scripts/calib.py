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
from ROOT import TFile, TTree, gPad, TGraphAsymmErrors, TSpline3, gStyle, gErrorIgnoreLevel, gROOT
ROOT.gROOT.SetBatch(1)
import argparse
from multiprocessing import Pool, cpu_count
import time
from array import array
#from logger import log
import logging
from random import gauss

def fit(i, f, h_name, Amenergy):
    c0 = ROOT.TCanvas("temp_"+h_name,"",0,0,800,800)
    hist = f.Get(h_name)
    g1 = ROOT.TF1("g1","gaus",90,110)
    g2 = ROOT.TF1("g2","gaus",120,150)
    g3 = ROOT.TF1("g3","gaus",190,230)
    g4 = ROOT.TF1("g4","gaus",500,600)
    if i <= 48 and i >= 43: 
       g1 = ROOT.TF1("g1","gaus",85,110)
       g2 = ROOT.TF1("g2","gaus",115,150)
    elif i <= 126 and i >= 96: 
       g1 = ROOT.TF1("g1","gaus",90,130)
       g2 = ROOT.TF1("g2","gaus",120,170)
       g3 = ROOT.TF1("g3","gaus",190,250)
    elif (i <= 153 and i >= 128) or (i <= 218 and i >= 166) or (i <= 255 and i >= 226): 
       g1 = ROOT.TF1("g1","gaus",100,150)
       g2 = ROOT.TF1("g2","gaus",150,200)
       g3 = ROOT.TF1("g3","gaus",230,300)
    elif (i <= 225 and i >= 219) or (i <= 165 and i >= 154): 
       g1 = ROOT.TF1("g1","gaus",100,250)
       g2 = ROOT.TF1("g2","gaus",100,250)
       g3 = ROOT.TF1("g3","gaus",100,250)
    g1.SetLineColor(ROOT.kRed)
    g2.SetLineColor(ROOT.kRed)
    g3.SetLineColor(ROOT.kRed)
    g4.SetLineColor(ROOT.kRed)
    hist.Fit("g1","QR")
    hist.Fit("g2","QR+")
    hist.Fit("g3","QR+")
    hist.Fit("g4","QR+")

    dic = {Amenergy[0]:g1.GetParameter(1), Amenergy[1]:g2.GetParameter(1), Amenergy[2]:g3.GetParameter(1), Amenergy[3]:g4.GetParameter(1)}
#    dic = { g1.GetParameter(1) : Amenergy[i] for i in range(1,5)} 
    print(h_name," : ", dic)
    return hist, dic 

def makeTGraphAndTSpline(i, name, table, energy):
    _g = ROOT.TGraph()
    _s = ROOT.TSpline3()
    _g.SetName("graph_"+name)
    _g.SetPoint(0, 0, 0)
    for i in range(len(energy)):
        _g.SetPoint(i+1, table[energy[i]], energy[i])
        if energy[i] is energy[i-1]: continue
        slope = (energy[i] - energy[i-1])/(table[energy[i]] - table[energy[i-1]])
        f_x = table[energy[i]]
        f_y = energy[i]
    _g.SetPoint(len(energy) + 1, 1500, (1500-f_x)*slope + f_y) 
    _s = ROOT.TSpline3("spline_"+str(i), _g)
    return _g, _s
    
def plot(name, hist, graph, latex):
    namech = name.replace("hist_cmn","ch : ")
    gROOT.ProcessLine("gErrorIgnoreLevel = kWarning;")
    c1 = ROOT.TCanvas("hist"+name,"",0,0,800,800)
    gPad.SetLogy(1)
    hist.Draw()
    latex.DrawLatex(0.5,0.85,namech)
    c1.SaveAs("../run/figs/"+name+"_fit.pdf")

    c2 = ROOT.TCanvas("gr"+name,"",0,0,800,800)
    graph.SetMarkerColor(4)
    graph.SetMarkerStyle(21)
    graph.Draw("ALP")
    latex.DrawLatex(0.5,0.85,namech)

    c2.Print("../run/figs/"+name+"_gr.pdf")

def getLatex(ch, x = 0.85, y = 0.85):
    _t = ROOT.TLatex()
    _t.SetNDC()
    _t.SetTextFont( 62 )
    _t.SetTextColor( 36 )
    _t.SetTextSize( 0.08 )
    _t.SetTextAlign( 12 )
    return _t
    
def main(args, IsRandom = False):
    __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
    ROOT.gROOT.LoadMacro( __location__+'/AtlasStyle/AtlasStyle.C')
    ROOT.SetAtlasStyle()

#    Amenergy = (13.94, 16.81, 17.75, 59.5)
    Amenergy = (13.94, 17.75, 26.3, 59.5)
    hist_name = [] 
    fout = ROOT.TFile( args.output, 'recreate' )

    f = ROOT.TFile(args.input)  
    fout.cd() 
    for i in range(256):
       if (i <= 225 and i >= 219) or (i <= 165 and i >= 154): Amenergy = (16.81, 16.81, 16.81, 59.5)       
       else: Amenergy = (13.94, 16.81, 26.3, 59.5)

       if i < 10: hist_name = "hist_cmn" + "00" + str(i) 
       elif i < 100:  hist_name = "hist_cmn" + "0" + str(i) 
       else : hist_name = "hist_cmn" + str(i)
       # cannot fitting
       if i is 0 : hist_name = "hist_cmn001"
       if i is 78 : hist_name = "hist_cmn079"
       if i is 127 : hist_name = "hist_cmn128"

       hist, table = fit(i, f, hist_name, Amenergy)
       gr, spline = makeTGraphAndTSpline(i, hist_name, table, Amenergy)
       latex = getLatex(i,400,8000)
       plot(hist_name , hist, gr, latex)
       spline.SetName("spline_"+str(i))
       spline.Write()    
    fout.Write()
    os.system("pdfunite ../run/figs/hist_cmn*.pdf ../run/figs/hist_all_book.pdf")
        
 
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("input", type=str, default="./20151112_00009_001.root", help="Input File Name")
    parser.add_argument("--output", type=str, default="./auxfile/spline_calibration.root", help="Input File Name")
    parser.add_argument("--channel", default=False, action="store_true", help="number of CPU")
    parser.add_argument("--nevent", default=500000, action="store_true", help="number of event")
    args = parser.parse_args()

    main( args , True)

