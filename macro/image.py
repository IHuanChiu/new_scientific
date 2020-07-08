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

from logger import log, supports_color
from utils.helpers import GetTChain, createRatioCanvas
from utils.color import SetMyPalette
from slice3D import MakeSlicePlots, makeTH2D, mergeTH2D 
from utils.filtbp import Filter, SimpleBackProjection 
import enums

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

def run3Dimage(args):
    h3d_t = ROOT.TH3D("solid_t_{}".format(args.cut),"solid_t_{}".format(args.cut),32,-16,16,32,-16,16,32,-16,16)
    h3d_t.SetXTitle("x")
    h3d_t.SetYTitle("y")
    h3d_t.SetZTitle("z")

    if args.input3Dhist is None: 
       log().info("Preparing 2D image...")
       treesum = GetTChain(args.inputFolder,"tree")         
       _ihlist = makeTH2D(treesum,args.dtype)
       ihlist  = mergeTH2D(_ihlist)

       log().info("Processing Back Projection...")
       SBP = SimpleBackProjection(h2list=ihlist)
       h3d=SBP.h3d

#       FBP = Filter(h2list=ihlist)
#       h3d=FBP.filtH3

    else:
       r3dfile  =  ROOT.TFile(args.input3Dhist)    
       h3d = r3dfile.Get("solid")

    log().info("Making 3D plots")
    cv  = createRatioCanvas("cv", 1600, 1600)
    _h3d_t = h3d.Clone()
    _h3d_t.Rebin3D(4,4,4)
    for _ix in range(1,_h3d_t.GetXaxis().GetNbins()+1):
       for _iy in range(1,_h3d_t.GetYaxis().GetNbins()+1):
          for _iz in range(1,_h3d_t.GetZaxis().GetNbins()+1):
             _bin = _h3d_t.GetBin(_ix,_iy,_iz)
             _x,_y,_z=_h3d_t.GetXaxis().GetBinCenter(_ix),_h3d_t.GetYaxis().GetBinCenter(_iy),_h3d_t.GetZaxis().GetBinCenter(_iz)
             if(_h3d_t.GetBinContent(_bin) > args.cut): h3d_t.Fill(_x,_y,_z,_h3d_t.GetBinContent(_bin))
    SetMyPalette("RB",0.5)
    h3d_t.Draw("BOX2Z")
    if args.output is not None: _outfig = "/Users/chiu.i-huan/Desktop/new_scientific/run/figs/hist_3D_image."+args.dtype+"."+args.output+"_cut{}.ROOT.pdf".format(args.cut) 
    else: _outfig = "/Users/chiu.i-huan/Desktop/new_scientific/run/figs/hist_3D_image."+args.dtype+"_cut{}.ROOT.pdf".format(args.cut)
    cv.Print(_outfig)

    # === make slices for xyz-sxis & projection ===
    if args.input3Dhist is None: 

       if len(ihlist) is 16:
          SetMyPalette("Bird",1)
          cv2  = createRatioCanvas("cv2", 3600, 3600)
          cv2.Divide(4,4) 
          for _ih in range(len(ihlist)): 
             cv2.cd(_ih+1).SetRightMargin(0.18)
             _tempih = ihlist[_ih].Clone()
             _tempih.Rebin2D(4,4)
             _tempih.SetStats(0)
             _tempih.SetXTitle("x")
             _tempih.SetYTitle("y")
             _tempih.SetTitle("angle : %.1f%s"%(360./len(ihlist)*_ih,enums.DEG))
             _tempih.Draw("colz")
          _out2dfig = _outfig.replace("hist_3D_image", "hist_2D_image")
          cv2.Print(_out2dfig)
       else: 
          log.info("Cannot make 2D images, check angle range !")
       
       log().info("Making 2D Slices")
       SetMyPalette("Bird",1)
       _MS = MakeSlicePlots(_hist3=h3d)
       h2_list_x, h2_list_y, h2_list_z = _MS.GetSlices("x"), _MS.GetSlices("y"), _MS.GetSlices("z")

       log().info("Storing all 2D & 3D plots")
       _out = "/Users/chiu.i-huan/Desktop/new_scientific/run/figs/repro_3Dimage"+"."+args.dtype
       if args.output is not None: outname = _out + "_" +args.output + ".root"
       else: outname = _out+".root"
       log().info("Output : %s, figs: /Users/chiu.i-huan/Desktop/new_scientific/run/figs/hist_3D_image.ROOT.pdf"%(outname))
       f = ROOT.TFile( outname, 'recreate' )
       f.cd()

       for _h2 in ihlist: 
          _h2.Write()
       cv2.Write()
       h3d_t.Write()
       h3d.Write()
       f.Write()    

    else: 
       _out = "/Users/chiu.i-huan/Desktop/new_scientific/run/figs/repro_3Dimage"+"."+args.dtype
       if args.output is not None: outname = _out + "_" +args.output + ".root"
       else: outname = _out+".root"
       f = ROOT.TFile( outname, 'update' )
       f.cd()
       h3d_t.Write()
        
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("-i", "--inputFolder", type=str, default="/Users/chiu.i-huan/Desktop/new_scientific/run/root/CdTe_root/", help="Input Ntuple Name")
    parser.add_argument("-o", "--output", type=str, default=None, help="Output file")
    parser.add_argument("-p", "--input3Dhist", type=str, default=None, help="Input 3D file")
    parser.add_argument("-d", "--dtype", dest="dtype", type=str, default = "CdTe", help="Si or CdTe" )
    parser.add_argument("-c", "--cut", type=int, default = 50, help="count cut for 3D image" )
    args = parser.parse_args()
    
    run3Dimage( args )
