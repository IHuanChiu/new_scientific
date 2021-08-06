#!/usr/bin/env python    
#-*- coding:utf-8 -*-   
"""
This module make projection with 2mm CdTe image using Xray test chart
"""
__author__    = "I-Huan CHIU"
__email__     = "ichiu@rirc.osaka-u.ac.jp"
__created__   = "2021-08-06"
__copyright__ = "Copyright 2021 I-Huan CHIU"
__license__   = "GPL http://www.gnu.org/licenses/gpl.html"

# modules
import sys,os,random,math,ROOT,time
from ROOT import TFile, TTree, gROOT, gStyle, TCut, gPad, gDirectory
ROOT.gROOT.SetBatch(1)
import argparse
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/imageAna/macro/utils/')
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/imageAna/macro/')
ROOT.gErrorIgnoreLevel = ROOT.kWarning

from utils.helpers import GetTChain, createRatioCanvas
from logger import log, supports_color
import numpy as np
from root_numpy import hist2array, array2hist, tree2array, array2tree
import linecache
from scipy import ndimage, misc

def GetProjection(treesum):
    treesum.Draw("y:x >> h2(192,-24,24,192,-24,24)","(energy > 30 && energy < 40)","colz")
    h2=gDirectory.Get("h2")
    h2.SetDirectory(0)
    h2_array=hist2array(h2)
    h2_array_rot=ndimage.rotate(h2_array,26.46310428088216,reshape=False)
    h2new=ROOT.TH2F("test","test",192,-24,24,192,-24,24)
    array2hist(h2_array_rot,h2new)
    h2new.GetYaxis().SetRangeUser(-5,16)
    h2new.GetXaxis().SetRangeUser(-16,16)
    hx=h2new.ProjectionX()
    hy=h2new.ProjectionY()
    return hx, hy, h2new

def makecv(_h2, _h2_rot, _hx,_hy):
    _cv  = createRatioCanvas("cv_test_projection", 3600, 3400)
    _cv.Divide(2,2)
    _cv.cd(1)
    _h2.SetTitle("Original Image;X [mm]; Y [mm]")
    _h2.SetStats(0)
    gStyle.SetPalette(56)
    _h2.Draw("colz")

    _cv.cd(2)
    _h2_rot.SetTitle("Rotated Image;X' [mm]; Y' [mm]")
    _h2_rot.SetStats(0)
    gStyle.SetPalette(56)
    _h2_rot.Draw("colz")

    _cv.cd(3)
    _hx.SetTitle("Projection Xprime;X' [mm]; Counts")
    _hx.SetStats(0)
    _hx.SetLineColor(1)
    _hx.Draw("hist")

    _cv.cd(4)
    _hy.SetTitle("Projection Yprime;Y' [mm]; Counts")
    _hy.SetStats(0)
    _hy.SetLineColor(1)
    _hy.Draw("hist")
    _cv.SaveAs("/Users/chiu.i-huan/Desktop/XChart_projection.pdf")

def main(args):
    log().info('Reading tree...')
    treesum = GetTChain(args.input,"tree")         

    log().info('Plotting...')
    treesum.Draw("y:x >> h2(128,-16,16,128,-16,16)","(energy > 20 && energy < 40)","colz")
    h2=gDirectory.Get("h2")
    h2.SetDirectory(0)

    log().info('Projection...')
    h2x, h2y, h2rot = GetProjection(treesum)

    log().info('Drawing...')
    makecv(h2, h2rot, h2x, h2y)

    log().info('Writing Output...')
    outname = args.input.replace(".root","_projection.root")
    f = ROOT.TFile( outname, 'recreate' )
    f.cd()
    h2.Write()
    h2x.Write()
    h2y.Write()
    h2rot.Write()
    log().info('Output : %s'%(outname)) 
    f.Write()   

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("-i", "--input", type=str, default="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/20210806a_00003_001_500n20_image.root", help="Input Ntuple Name")
    args = parser.parse_args()
    
    main( args )
