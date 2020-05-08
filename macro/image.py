#!/usr/bin/env python    
#-*- coding:utf-8 -*-   
"""
This module provides the plots
"""
__author__    = "I-Huan CHIU"
__email__     = "ichiu@chem.sci.osaka-u.ac.jp"
__created__   = "2019-11-08"
__copyright__ = "Copyright 2019 I-Huan CHIU"
__license__   = "GPL http://www.gnu.org/licenses/gpl.html"

# modules
import sys,os,random,math,ROOT
from ROOT import TFile, TTree, gROOT, gStyle, TCut, gPad, gDirectory
ROOT.gROOT.SetBatch(1)
import argparse
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/macro/utils/')

import time
from logger import log, supports_color
from utils.helpers import GetInputList

__location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
ROOT.gROOT.LoadMacro( __location__+'/AtlasStyle/AtlasStyle.C')
#ROOT.SetAtlasStyle()

def getBIN(h): 
    n = h.GetNbinsX()
    xlow = h.GetBinLowEdge(1)
    xhigh = h.GetBinLowEdge(n)+h.GetBinWidth(n)
    return (n,xlow,xhigh)
    
def createRatioCanvas(Name = "cs", w = 1200, h = 800):
    cRatioCanvas = ROOT.TCanvas(Name,"",0,0,int(w),int(h))
    cRatioCanvas.GetFrame().SetBorderMode(0)
    cRatioCanvas.GetFrame().SetBorderSize(0)
    cRatioCanvas.SetBorderMode(0)
    cRatioCanvas.SetBorderSize(0)
    cRatioCanvas.SetFillStyle(0)
    cRatioCanvas.SetFillColor(0)
    cRatioCanvas.SetRightMargin(0.15)
    cRatioCanvas.SetWindowSize( int(w + (w-cRatioCanvas.GetWw())), int(h + (h-cRatioCanvas.GetWh())) )
    return cRatioCanvas

def gettreename(treename):
      
    dTreeNameMap = {
    "pside_1" : "adc0",
    "pside_2" : "adc1",
    "pside_3" : "adc2",
    "pside_4" : "adc3",
    "nside_1" : "adc4",
    "nside_2" : "adc5",
    "nside_3" : "adc6",
    "nside_4" : "adc7"
    }
    return dTreeNameMap[treename]

def definecut(cutname):
#    cut1 = TCut("(trigger > 590 && trigger < 600) || (trigger > 620 && trigger < 630)")
#    cut2 = TCut("(weight > 1./50)")# Mvalue < 5    
#    finalcut = cut1 + cut2
    return TCut(cutname)

class makecut():
      def __init__(self,basecut):
          self.base = basecut
      def add(self,cutname):
          self.base += "&&" + cutname
      def get(self):
          return TCut(self.base)

def image(tree, icut, position):
     
    ROOT.SetAtlasStyle()
    e_min,e_max = 10,100
    if position is "low": e_min,e_max = 10,20
    if position is "high": e_min,e_max = 60,80
# =============== make image =============
#    addition_cut = TCut("weight * (energy_p>{} && energy_p < {})".format(e_min, e_max))
#    icut += addition_cut
    tree.Draw("x:y >> h2(128,-16,16,128,-16,16)",icut,"colz")
    h2 = gDirectory.Get("h2")
    h2.GetXaxis().SetTitle("p-side [mm]")
    h2.GetYaxis().SetTitle("n-side [mm]")
    h2.SetDirectory(0)
#    gPad.SetLogz()
    return h2


def spectrum(tree, scut):
    h1_p = ROOT.TH1F("Spectrum_pside","Spectrum pside", 100,0,100)
    h1_n = ROOT.TH1F("Spectrum_nside","Spectrum nside", 100,0,100)

    tree.Draw("energy_p >> h1_p(100,0,100)",scut,"")
    tree.Draw("energy_n >> h1_n(100,0,100)",scut,"same")
    h1_p=gDirectory.Get("h1_p")
    h1_n=gDirectory.Get("h1_n")
    h1_p.GetXaxis().SetTitle("energy [keV]")
    h1_p.GetYaxis().SetTitle("Counts")
    h1_n.GetXaxis().SetTitle("energy [keV]")
    h1_n.GetYaxis().SetTitle("Counts")

    return h1_p, h1_n

class Baseplot():

      def __init__(self,infile=None,outname=None): 
          self.infile = infile
          self.outname = outname

      def plots(self):
          log().info("Plotting...")
          filename = self.infile.GetName()
          f = ROOT.TFile(filename)
          mytree   =  f.Get("tree")

          printname = "../run/figs/"+self.outname
          outf = ROOT.TFile( printname+".root", 'recreate' )
          outf.cd()

          cv  = createRatioCanvas("cv", 1600, 1600)
          cv.Divide(2,2)

          cv.cd(1)
          mytree.Draw("trigger >> h_trigger(100,200,300)","","")
          h_tri = gDirectory.Get("h_trigger")
          h_tri.GetXaxis().SetTitle("trigger")
          h_tri.GetYaxis().SetTitle("count")
          h_tri.Write()         

          cv.cd(2)
          gPad.SetRightMargin(0.15)   
          gPad.SetLogz(1) 
          gStyle.SetPalette(56)
          mytree.Draw("nsignaly_lv2:nsignalx_lv2 >> hn2d(25,0,25,25,0,25)","","colz")
          h_nhit = gDirectory.Get("hn2d")
          h_nhit.GetXaxis().SetTitle("nhits Xaxis")
          h_nhit.GetYaxis().SetTitle("nhits Yaxis")
          h_nhit.Write()
 
          cv.cd(3)
          Cut = makecut(basecut="((trigger > 235 && trigger < 240) || (trigger > 247 && trigger < 253))")
          cut = Cut.get()
          hist_spectrum_p, hist_spectrum_n = spectrum(mytree,cut)
          hist_spectrum_p.Write()
          hist_spectrum_n.Write()
          hist_spectrum_p.SetLineColor(ROOT.kPink+9)
          hist_spectrum_p.SetLineWidth(2)
          hist_spectrum_p.SetMaximum(hist_spectrum_p.GetMaximum()*1.3);
          hist_spectrum_n.SetLineColor(ROOT.kAzure-1)
          hist_spectrum_n.SetLineWidth(2)
          hist_spectrum_p.Draw()
          hist_spectrum_n.Draw("same")
          leg = ROOT.TLegend(.55,.78,.75,.90)
          leg.AddEntry(hist_spectrum_p,  "P-side", "l")
          leg.AddEntry(hist_spectrum_n,  "N-side", "l")
          leg.Draw("same")
          
 
          cv.cd(4)
          Cut.add("(energy_p > 72 && energy_p < 78)")
          cut = Cut.get()
          hist_image = image(mytree,cut,"all")
          hist_image.Write()
          gPad.SetLogz(0) 
          gStyle.SetPalette(56)
          gPad.SetRightMargin(0.15)
          hist_image.RebinX(4)
          hist_image.RebinY(4)
          hist_image.Draw("colz")

          outf.Write()
          cv.Print(printname+".pdf")
#          log().info("Finished plots!")
   
def rnu3Dimage(args):

#    ilist = GetInputList(args.inputFolder)
#    rfile   =  ROOT.TFile(args.input)
#    mytree   =  rfile.Get("tree")

    cv  = createRatioCanvas("cv", 1600, 1600)
    h3d = ROOT.TH3D("test","test",128,-16,16,128,-16,16,128,-16,16)
    for i in range(10000):
       h3d.Fill(random.uniform(-0.5,0.5), 20*random.uniform(-0.5,0.5), 20*random.uniform(-0.5,0.5))
    h3d.Draw("BOX2Z")
    cv.Print("../run/figs/test_3D_image.ROOT.pdf")

    f = ROOT.TFile( '../run/figs/repro_3Dimage.root', 'recreate' )
    f.cd()
    h3d.Write()
    f.Write()    
        
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("input", type=str, default="../run/figs/20200307a_rootfiles/", help="Input Ntuple Name")
    parser.add_argument("--output", type=str, default="../run/root/tranadc_dsd.root", help="Output file for adctoenergy")
    args = parser.parse_args()
    
    rnu3Dimage( args )
