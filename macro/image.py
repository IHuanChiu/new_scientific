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
#gROOT.ProcessLine("gErrorIgnoreLevel = kPrint, kInfo, kWarning, kError, kBreak, kSysError, kFatal;")
ROOT.gErrorIgnoreLevel = ROOT.kWarning

import time
from logger import log, supports_color
from utils.helpers import GetTChain, createRatioCanvas
from utils.color import SetMyPalette
from slice3D import MakeSlicePlots, makeTH2D 
from enums import getangle

__location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
ROOT.gROOT.LoadMacro( __location__+'/AtlasStyle/AtlasStyle.C')
#ROOT.SetAtlasStyle()

#from scipy.spatial.transform import Rotation as R
import numpy as np

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
# =============== make image =============
#    addition_cut = TCut("weight * (energy_p>{} && energy_p < {})".format(e_min, e_max))
#    icut += addition_cut
    tree.Draw("x:y >> h2(128,-16,16,128,-16,16)",icut,"colz")
    h2 = gDirectory.Get("h2")
#    h2.SetTitle(icut.GetTitle())
    h2.GetXaxis().SetTitle("n-side [mm]")
    h2.GetYaxis().SetTitle("p-side [mm]")
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
#    h1_p.SetTitle(scut.GetTitle())
    h1_p.GetXaxis().SetTitle("energy [keV]")
    h1_p.GetYaxis().SetTitle("Counts")
    h1_n.GetXaxis().SetTitle("energy [keV]")
    h1_n.GetYaxis().SetTitle("Counts")

    return h1_p, h1_n

class Baseplot():

      def __init__(self,infile=None,outname=None,initUT=None,dtype=None): 
          self.infile = infile
          self.outname = outname
          self.dtype = dtype

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
          if "CdTe" in self.dtype:
             mytree.Draw("trigger >> h_trigger(100,200,300)","","")
          else:
             mytree.Draw("trigger >> h_trigger(300,550,850)","","")
          h_tri = gDirectory.Get("h_trigger")
          h_tri.SetTitle("trigger time")
          h_tri.GetXaxis().SetTitle("trigger")
          h_tri.GetYaxis().SetTitle("count")
          h_tri.Write()         

          cv.cd(2)
          gPad.SetRightMargin(0.15)   
          gPad.SetLogz(1) 
          gStyle.SetPalette(56)
          mytree.Draw("nsignaly_lv2:nsignalx_lv2 >> hn2d(25,0,25,25,0,25)","","colz")
          h_nhit = gDirectory.Get("hn2d")
          h_nhit.SetTitle("nhits of lv2")
          h_nhit.GetXaxis().SetTitle("nhits Xaxis")
          h_nhit.GetYaxis().SetTitle("nhits Yaxis")
          h_nhit.Write()
 
          cv.cd(3)
          if "CdTe" in self.dtype:
             Cut = makecut(basecut="((trigger > 235 && trigger < 240) || (trigger > 247 && trigger < 253))")
          else:
             Cut = makecut(basecut="((trigger > 590 && trigger < 600) || (trigger > 620 && trigger < 630))")
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
          gPad.SetLeftMargin(0.15)
          gPad.SetBottomMargin(0.15)
          if "CdTe" in self.dtype:
             Cut.add("(energy_p > 72 && energy_p < 78)")
          else:
             Cut.add("(energy_p > 12 && energy_p < 16)")
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

def GetRotation(_x,_y,_z,_angle):
    c, s = np.cos(_angle), np.sin(_angle)
    #R = np.matrix([[c, -s, 0], [s, c,0], [0,0,1]]) # around z-axis
    #R = np.matrix([[c,0,s], [0,1,0], [-s,0,c]]) # around y-axis
    R = np.matrix([[1,0,0], [0,c,-s], [0,s,c]]) # around x-axis
    v = np.matrix( [ _x, _y, _z ])
    new_v = R*v.reshape(3,1)
    return new_v[0,0], new_v[1,0], new_v[2,0]    

def getContent(ibinx, ibiny, ibinz, h2, h2name, _h3):
    _angle=getangle(h2name)
    _content = h2.GetBinContent(ibinx,ibiny)
    _x,_y,_z = GetRotation(_h3.GetXaxis().GetBinCenter(ibinx), _h3.GetYaxis().GetBinCenter(ibiny), _h3.GetYaxis().GetBinCenter(ibinz),_angle)
    return _x,_y,_z, _content

def run3Dimage(args):
    log().info("Preparing 3D image...")
    ti = time.time()
    treesum = GetTChain(args.inputFolder,"tree")         
    ihlist = makeTH2D(treesum,args.dtype)

    h3d = ROOT.TH3D("solid","solid",128,-16,16,128,-16,16,128,-16,16)
    h3d_t = ROOT.TH3D("solid_t","solid_t",32,-16,16,32,-16,16,32,-16,16)
    h3d.SetXTitle("x")
    h3d.SetYTitle("y")
    h3d.SetZTitle("z")
    h3d_t.SetXTitle("x")
    h3d_t.SetYTitle("y")
    h3d_t.SetZTitle("z")

    if args.input3Dhist is None: 
       numoff=0 
       for h2 in ihlist:
          numoff+=1
          h2name = h2.GetTitle()
#          rfile   =  ROOT.TFile(ifile)
#          h2   =  rfile.Get("h2")
#          h2name = ifile.split("/")[-1]
#          log().info("Current file : %s , Angle is %.1f\u00b0"%(h2name, math.degrees(getangle(h2name))))
          log().info("Current Angle is %.1f\u00b0"%(math.degrees(getangle(h2name))))
          for ibinx in range(1,h3d.GetXaxis().GetNbins()+1):
             for ibiny in range(1,h3d.GetYaxis().GetNbins()+1):
                for ibinz in range(1,h3d.GetZaxis().GetNbins()+1):
                   x,y,z,content = getContent(ibinx, ibiny, ibinz, h2, h2name, h3d)
                   h3d.Fill(x,y,z,content)
          log().info("Running time : %.1f s , (%s/%s) files "%(time.time() - ti, numoff, len(ihlist)))         
    else:
       r3dfile  =  ROOT.TFile(args.input3Dhist)    
       h3d = r3dfile.Get("solid")

    cv  = createRatioCanvas("cv", 1600, 1600)
    log().info("Making 3D plots")
    _h3d_t = h3d.Clone()
    _h3d_t.Rebin3D(4,4,4)
    cut_cont = 280
    for _ix in range(1,_h3d_t.GetXaxis().GetNbins()+1):
       for _iy in range(1,_h3d_t.GetYaxis().GetNbins()+1):
          for _iz in range(1,_h3d_t.GetZaxis().GetNbins()+1):
             _bin = _h3d_t.GetBin(_ix,_iy,_iz)
             _x,_y,_z=_h3d_t.GetXaxis().GetBinCenter(_ix),_h3d_t.GetYaxis().GetBinCenter(_iy),_h3d_t.GetZaxis().GetBinCenter(_iz)
             if(_h3d_t.GetBinContent(_bin) > cut_cont): h3d_t.Fill(_x,_y,_z,_h3d_t.GetBinContent(_bin))
    SetMyPalette("RB",0.5)
    h3d_t.Draw("BOX2Z")
    cv.Print("/Users/chiu.i-huan/Desktop/new_scientific/run/figs/hist_3D_image.ROOT.pdf")

    # === make slices for xyz-sxis ===
    SetMyPalette("Bird",1)
    _MS = MakeSlicePlots(_hist3=h3d)
    h2_list_x, h2_list_y, h2_list_z = _MS.GetSlices("x"), _MS.GetSlices("y"), _MS.GetSlices("z")

    _out = "/Users/chiu.i-huan/Desktop/new_scientific/run/figs/repro_3Dimage" 
    if args.output is not None: outname = _out + "_" +args.output + ".root"
    else: outname = _out+".root"
    log().info("Output : %s, figs: /Users/chiu.i-huan/Desktop/new_scientific/run/figs/hist_3D_image.ROOT.pdf"%(outname))
    f = ROOT.TFile( outname, 'recreate' )
    f.cd()

    h3d_t.Write()
    h3d.Write()
    f.Write()    
        
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("-i", "--inputFolder", type=str, default="/Users/chiu.i-huan/Desktop/new_scientific/run/root/CdTe_root/", help="Input Ntuple Name")
    parser.add_argument("-o", "--output", type=str, default=None, help="Output file")
    parser.add_argument("-p", "--input3Dhist", type=str, default=None, help="Input 3D file")
    parser.add_argument("-d", "--dtype", dest="dtype", type=str, default = "CdTe", help="Si or CdTe" )
    args = parser.parse_args()
    
    run3Dimage( args )
