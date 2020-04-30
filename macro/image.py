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
from ROOT import TFile, TTree, gROOT, gStyle, TCut, gPad, gDirectory
ROOT.gROOT.SetBatch(1)
import argparse
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/macro/utils/')

import time
from tran import tran

__location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
ROOT.gROOT.LoadMacro( __location__+'/AtlasStyle/AtlasStyle.C')
ROOT.SetAtlasStyle()

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

def definecut():
    cut1 = TCut("(trigger > 590 && trigger < 600) || (trigger > 620 && trigger < 630)")
    cut2 = TCut("(weight > 1./50)")# Mvalue < 5
    finalcut = cut1 + cut2
    return finalcut

def image(tree, icut, position):
     
    e_min,e_max = 10,100
    if position is "low": e_min,e_max = 10,20
    if position is "high": e_min,e_max = 60,80
# =============== make image =============
    addition_cut = TCut("weight * (energy_p>{} && energy_p < {})".format(e_min, e_max))
    icut += addition_cut
    print("cut for image : ",)
    icut.Print()
    tree.Draw("x:y >> h2(128,0,128,128,0,128)",icut,"colz")
    h2 = gDirectory.Get("h2")
    h2.GetXaxis().SetTitle("p-side [ch]")
    h2.GetYaxis().SetTitle("n-side [ch]")
    h2.SetDirectory(0)
    gPad.SetLogz()
    return h2


def spectrum(tree, scut):
    h1_p = ROOT.TH1F("Spectrum_pside","Spectrum pside", 100,0,100)
    h1_n = ROOT.TH1F("Spectrum_nside","Spectrum nside", 100,0,100)

    print("cut for spectum : ",)
    scut.Print()
    tree.Draw("energy_p >> h1_p(100,0,100)",scut,"")
    tree.Draw("energy_n >> h1_n(100,0,100)",scut,"same")
    h1_p=gDirectory.Get("h1_p")
    h1_n=gDirectory.Get("h1_n")
    h1_p.GetXaxis().SetTitle("energy [keV]")
    h1_p.GetYaxis().SetTitle("Counts")
    h1_n.GetXaxis().SetTitle("energy [keV]")
    h1_n.GetYaxis().SetTitle("Counts")

    return h1_p, h1_n

class Baseplots():

      def __init__(self,infile=None,outname=None): 
          self.infile = infile
          self.outname = outname

      def plots(self,):
   

def main(args):

#    f = ROOT.TFile( '../run/root/repro_image.root', 'recreate' )
    rfile   =  ROOT.TFile(args.input)
    mytree   =  rfile.Get("tree")

    cut = definecut()
    hist_spectrum_p, hist_spectrum_n = spectrum(mytree,cut)
    cut = definecut()
    hist_image = image(mytree,cut,"all")
    cut = definecut()
    hist_image_low = image(mytree,cut,"low")
    cut = definecut()
    hist_image_high = image(mytree,cut,"high")

    cv  = createRatioCanvas("cv", 1600, 1200)
    cv.Divide(2,3)

    cv.cd(1)
    mytree.Draw("trigger >> h_trigger(200,550,750)","","")
    h_tri = gDirectory.Get("h_trigger")
    h_tri.GetXaxis().SetTitle("trigger")
    h_tri.GetYaxis().SetTitle("count")

    cv.cd(2)
    gPad.SetRightMargin(0.15)   
    gPad.SetLogz(1) 
    mytree.Draw("nhity:nhitx >> hn2d(25,0,25,25,0,25)","","colz")
    h_nhit = gDirectory.Get("hn2d")
    h_nhit.GetXaxis().SetTitle("nhits Xaxis")
    h_nhit.GetYaxis().SetTitle("nhits Yaxis")

    cv.cd(3)
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
    gPad.SetLogz(1) 
    gStyle.SetPalette(53)
    gPad.SetRightMargin(0.15)
    hist_image.Draw("colz")
    cv.cd(5)
    gStyle.SetPalette(53)
    gPad.SetRightMargin(0.15)
    hist_image_low.Draw("colz")
    cv.cd(6)
    gStyle.SetPalette(53)
    gPad.SetRightMargin(0.15)
    hist_image_high.Draw("colz")

#    cv.Update()
    printname = "../run/figs/"+
    cv.Print("../run/figs/test_e_image.ROOT.pdf")

#    f.cd()
#    hist_image.Write()
#    hist_image_low.Write()
#    hist_image_high.Write()
#    hist_spectrum_p.Write()
#    hist_spectrum_n.Write()
#    h_tri.Write()
#    h_nhit.Write()
#    cv.Write()
#    f.Write()    
#    f.Close()    
        
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("input", type=str, default="../run/root/20200307a_00070_001_tranadc_dsd.root", help="Input Ntuple Name")
    parser.add_argument("--output", type=str, default="../run/root/tranadc_dsd.root", help="Output file for adctoenergy")
    args = parser.parse_args()
    
    main( args )
