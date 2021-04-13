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
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/imageAna/macro/utils/')
#gROOT.ProcessLine("gErrorIgnoreLevel = kPrint, kInfo, kWarning, kError, kBreak, kSysError, kFatal;")
ROOT.gErrorIgnoreLevel = ROOT.kWarning

from logger import log, supports_color
from utils.helpers import GetTChain, createRatioCanvas
from utils.color import SetMyPalette

__location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
ROOT.gROOT.LoadMacro( __location__+'/AtlasStyle/AtlasStyle.C')

def getBIN(h): 
    n = h.GetNbinsX()
    xlow = h.GetBinLowEdge(1)
    xhigh = h.GetBinLowEdge(n)+h.GetBinWidth(n)
    return (n,xlow,xhigh)

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

class makecut():
      def __init__(self,basecut):
          self.base = basecut
      def add(self,cutname):
          self.base += "&&" + cutname
      def get(self):
          return TCut(self.base)

def image(tree, icut, position):
# =============== make image =============
    tree.Draw("y:x >> h2(128,-16,16,128,-16,16)",icut,"colz")
    h2 = gDirectory.Get("h2")
    h2.GetYaxis().SetTitle("Al side [mm]")
    h2.GetXaxis().SetTitle("Pt side [mm]")
    h2.SetDirectory(0)
#    gPad.SetLogz(1)
    return h2


def spectrum(tree, scut):
    h1_s = ROOT.TH1F("Spectrum_allside","Spectrum allside", 300,0,150)
    h1_p = ROOT.TH1F("Spectrum_pside","Spectrum pside", 300,0,150)
    h1_n = ROOT.TH1F("Spectrum_nside","Spectrum nside", 300,0,150)

    tree.Draw("energy >> h1_s(500,0,200)",scut,"")
    tree.Draw("energy_p >> h1_p(500,0,200)",scut,"same")
    tree.Draw("energy_n >> h1_n(500,0,200)",scut,"same")
    h1_s=gDirectory.Get("h1_s")
    h1_p=gDirectory.Get("h1_p")
    h1_n=gDirectory.Get("h1_n")
#    h1_p.SetTitle(scut.GetTitle())
    h1_s.SetStats(0)
    h1_p.SetStats(0)
    h1_n.SetStats(0)
    h1_s.GetXaxis().SetTitle("energy [keV]")
    h1_s.GetYaxis().SetTitle("Counts")
    h1_p.GetXaxis().SetTitle("energy [keV]")
    h1_p.GetYaxis().SetTitle("Counts")
    h1_n.GetXaxis().SetTitle("energy [keV]")
    h1_n.GetYaxis().SetTitle("Counts")

    return h1_s, h1_p, h1_n

class Baseplot():

      def __init__(self,infile=None,outname=None,initUT=None,dtype=None): 
          self.infile = infile
          self.outname = outname
          self.dtype = dtype
#          self.tri_cut1_d, self.tri_cut1_u, self.trig_cut2_d, self.trig_cut2_u = 1625, 1640, 1655, 1670

      def plots(self):
          log().info("Plotting...")
          ROOT.SetAtlasStyle()
          if type(self.infile) == str : filename = self.infile
          else : filename = self.infile.GetName()          
          f = ROOT.TFile(filename)
          mytree   =  f.Get("tree")

          printname = "../run/figs/"+self.outname
          outf = ROOT.TFile( printname+".root", 'recreate' )
          outf.cd()

          cv  = createRatioCanvas("cv", 1600, 1600)
          cv.Divide(2,2)

          cv.cd(1)
          if "Lab" in self.dtype or "lab" in self.dtype:
             mytree.Draw("trigger >> h_trigger","","")
          elif "JPARCDec" in self.dtype:
             mytree.Draw("trigger >> h_trigger(300,1550,1850)","","")
          elif "CdTe" in self.dtype:
             mytree.Draw("trigger >> h_trigger(100,200,300)","","")
          else:
             mytree.Draw("trigger >> h_trigger(300,550,850)","","")
          h_tri = gDirectory.Get("h_trigger")
          h_tri.SetTitle("trigger time")
          h_tri.SetStats(0)
          h_tri.GetXaxis().SetTitle("trigger")
          h_tri.GetYaxis().SetTitle("count")
          h_tri.Write()         
          if "Lab" in self.dtype or "lab" in self.dtype:
             Cut = makecut(basecut="1")
          elif "JPARCDec" in self.dtype:
             Cut = makecut(basecut="((trigger > 1625 && trigger < 1640) || (trigger > 1655 && trigger < 1670))")
          elif "CdTe" in self.dtype:
             Cut = makecut(basecut="((trigger > 235 && trigger < 240) || (trigger > 247 && trigger < 253))")
          else:
             Cut = makecut(basecut="((trigger > 590 && trigger < 600) || (trigger > 620 && trigger < 630))")
          cut = Cut.get()
          line1_d = ROOT.TLine(1625,0,1625,h_tri.GetMaximum())
          line1_u = ROOT.TLine(1640,0,1640,h_tri.GetMaximum())
          line2_d = ROOT.TLine(1655,0,1655,h_tri.GetMaximum())
          line2_u = ROOT.TLine(1670,0,1670,h_tri.GetMaximum())
          line1_d.SetLineColor(ROOT.kAzure); line1_u.SetLineColor(ROOT.kAzure);
          line2_d.SetLineColor(2); line2_u.SetLineColor(2);
          line1_d.Draw("same");line1_u.Draw("same");line2_d.Draw("same");line2_u.Draw("same");          

          cv.cd(2)
          gPad.SetRightMargin(0.15)   
          gPad.SetLogz(1) 
          gStyle.SetPalette(56)
          mytree.Draw("nsignaly_lv2:nsignalx_lv2 >> hn2d(25,0,25,25,0,25)",cut,"colz")
          h_nhit = gDirectory.Get("hn2d")
          h_nhit.SetTitle("nhits of lv2")
          h_nhit.GetXaxis().SetTitle("nhits Xaxis")
          h_nhit.GetYaxis().SetTitle("nhits Yaxis")
          h_nhit.Write()
 
          cv.cd(3)
          hist_spectrum_s, hist_spectrum_p, hist_spectrum_n = spectrum(mytree,cut)
          hist_spectrum_s.Write()
          hist_spectrum_p.Write()
          hist_spectrum_n.Write()
          hist_spectrum_s.SetLineColor(1)
          hist_spectrum_s.SetLineWidth(1)
          #hist_spectrum_p.SetLineColor(ROOT.kPink+9)
          hist_spectrum_p.SetLineColor(2)
          hist_spectrum_p.SetLineWidth(1)
          hist_spectrum_n.SetLineColor(ROOT.kAzure-1)
          hist_spectrum_n.SetLineWidth(1)

          maxbin = hist_spectrum_n.GetMaximum()
          if  hist_spectrum_p.GetMaximum() > maxbin : maxbin = hist_spectrum_p.GetMaximum()
          if  hist_spectrum_s.GetMaximum() > maxbin : maxbin = hist_spectrum_s.GetMaximum()
          hist_spectrum_n.SetMaximum(maxbin*1.15)

          leg = ROOT.TLegend(.55,.78,.90,.90)
          hist_spectrum_n.Draw()
          hist_spectrum_p.Draw("same")
          #hist_spectrum_s.Draw("same")
          #leg.AddEntry(hist_spectrum_s,  "E #gamma", "l")
          leg.AddEntry(hist_spectrum_p,  "Pt side (Cathode)", "l")
          leg.AddEntry(hist_spectrum_n,  "Al side (Anode)", "l")
          leg.Draw("same")
          
 
          cv.cd(4)
          gPad.SetLeftMargin(0.15)
          gPad.SetBottomMargin(0.15)
          if "Lab" in self.dtype or "lab" in self.dtype:
             Cut.add("1")
          elif "JPARCDec" in self.dtype:
             Cut.add("1")
          elif "CdTe" in self.dtype:
             Cut.add("(energy > 72 && energy < 78)")
          else:
             Cut.add("(energy > 12 && energy < 16)")
          cut = Cut.get()
          hist_image = image(mytree,cut,"all")
          hist_image.Write()
          gPad.SetLogz(0) 
          gStyle.SetPalette(56)
          gPad.SetRightMargin(0.15)
          if "Lab" in self.dtype or "JPARC" in self.dtype:
             hist_image.RebinX(1)
             hist_image.RebinY(1)
          else:
             hist_image.RebinX(4)
             hist_image.RebinY(4)
          hist_image.Draw("colz")

          outf.Write()
          cv.Print(printname+".pdf")
          log().info("Show plot : {}".format(printname.replace("../run/", "./")+".pdf"))

