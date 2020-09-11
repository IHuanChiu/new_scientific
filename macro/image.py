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
#       SBP = SimpleBackProjection(h2list=ihlist)
#       h3d=SBP.h3d
       FBP = Filter(h2list=ihlist)
       h3d=FBP.filtH3

    else:
       r3dfile  =  ROOT.TFile(args.input3Dhist)    
       h3d = r3dfile.Get("solid")

    log().info("Making 3D plots")
    cv  = createRatioCanvas("cv", 1600, 1600)
    _h3d_t = h3d.Clone()
    if (_h3d_t.GetNbinsX() >= 128) : _h3d_t.Rebin3D(2,2,2)
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
       
       log().info("Making 2D Slices")
       SetMyPalette("Bird",1)
       _MS = MakeSlicePlots(_hist3=h3d)
       h2_list_x, h2_list_y, h2_list_z = _MS.GetSlices("x"), _MS.GetSlices("y"), _MS.GetSlices("z")

       log().info("Storing all 2D & 3D plots")
       _out = "/Users/chiu.i-huan/Desktop/new_scientific/run/figs/repro_3Dimage"+"."+args.dtype
       if args.output is not None: outname = _out + "_" +args.output + ".root"
       else: outname = _out+".root"
       log().info("Output : %s, in: /Users/chiu.i-huan/Desktop/new_scientific/run/figs"%(outname))
       f = ROOT.TFile( outname, 'recreate' )
       f.cd()

       for _h2 in ihlist: 
          _h2.Write()
       for _ih2 in range(len(FBP.filth2)): 
          FBP.filth2[_ih2].SetTitle("Filt, angle : %.1f%s"%(360./len(FBP.filth2)*_ih2,enums.DEG))
          FBP.filth2[_ih2].Write()           
       h3d_t.Write()
       h3d.Write()

       if len(ihlist) == 16:
          SetMyPalette("Bird",1)
          cv2  = createRatioCanvas("cv2", 3600, 3600)
          cv2.Divide(4,4)
          for _ih in range(len(ihlist)): 
             cv2.cd(_ih+1).SetRightMargin(0.18)
             if (ihlist[_ih].GetNbinsX() >= 128): ihlist[_ih].Rebin2D(4,4)
             ihlist[_ih].SetStats(0)
             ihlist[_ih].SetXTitle("x")
             ihlist[_ih].SetYTitle("y")
             ihlist[_ih].SetTitle("angle : %.1f%s"%(360./len(ihlist)*_ih,enums.DEG))
             ihlist[_ih].Draw("colz")
          _out2dfig = _outfig.replace("hist_3D_image", "hist_2D_image")
          cv2.Print(_out2dfig)
       else: 
          log.info("Cannot make 2D images, check angle range !")
       cv2.Write()
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
    parser.add_argument("-c", "--cut", type=int, default = 100, help="count cut for 3D image" )
    args = parser.parse_args()
    
    run3Dimage( args )
