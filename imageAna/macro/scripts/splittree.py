#!/usr/bin/env python    
#-*- coding:utf-8 -*-   
"""
This module splits the tree based on unixtime
"""
__author__    = "I-Huan CHIU"
__email__     = "ichiu@chem.sci.osaka-u.ac.jp"
__created__   = "2020-08-06"
__copyright__ = "Copyright 2019 I-Huan CHIU"
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
#import rotstep
import numpy as np
from root_numpy import hist2array, array2hist, tree2array, array2tree
import linecache

def GetSplitTree(box_step,treesum):
    _name_list, _tree_list = [], []
    startline = 7
    endstep = 4
    for _iz in range(box_step):
       for _iy in range(box_step):
          for _ix in range(box_step):             
             _stepi,_stepf = linecache.getline('rotdatabase.txt', int(startline)), linecache.getline('rotdatabase.txt', int(startline+endstep))
             _stepi,_stepf=_stepi.replace("\n",""),_stepf.replace("\n","")
             timeArray_i, timeArray_f = time.strptime(_stepi, "%Y-%m-%d %H:%M:%S"), time.strptime(_stepf, "%Y-%m-%d %H:%M:%S")
             timestamp_i, timestamp_f = time.mktime(timeArray_i), time.mktime(timeArray_f)
             _cut="(unixtime > {0} && unixtime < {1})".format(timestamp_i, timestamp_f)
             startline+=16 # go to next rotation step
             if _ix==4 and _iy!=4:# i.e.: line167, (4,0,0)-> (0,1,0), x is from 4 to 0 + y is from 0 to 1
                startline+=16
             if _ix==4 and _iy==4 and _iz!=4:# i.e.: line1943, (4,4,0) -> (0,0,1), x is from 4 to 0 + y is from 4 to 0 + z is from 0 to 1
                startline+=32
#             array_list.append(tree2array(treesum,branches=["nhit","x","y","nsignaly_lv2","nsignalx_lv2","energy","energy_p","energy_n","unixtime"],selection=_cut))             
             _tree_list.append(treesum.CopyTree(_cut))
             _name_list.append("pos{}".format(_ix+_iy*5+_iz*25))
    return _name_list, _tree_list

def makeplots(_i,_name,tree):
    tree.Draw("energy >> h1(160,0,80)","","")
    tree.Draw("y:x >> h2(128,-16,16,128,-16,16)","(energy > 55 && energy < 65)","colz")
    h1 = gDirectory.Get("h1")
    h1.SetName("spectrum_"+_name)
    h1.SetTitle(_name)
    h1.GetXaxis().SetTitle("Energy [keV]")
    h1.GetYaxis().SetTitle("Counts")
    h1.SetDirectory(0)
    h1.Write()
    h2 = gDirectory.Get("h2")
    h2.SetName("image_"+_name)
    h2.SetTitle("energy > 55 & energy < 65 & "+_name)
    h2.GetXaxis().SetTitle("X [mm]")
    h2.GetYaxis().SetTitle("Y [mm]")
    h2.SetDirectory(0)
    h2.Write()
    return 0

def makecv(_file, box_step):
    _i = ROOT.TFile(_file,"read")
    for _iz in range(box_step):
       _cv  = createRatioCanvas("cv_{}".format(_iz), 2500, 2500)
       _cv.Divide(box_step,box_step)
       for _iy in range(box_step):
          for _ix in range(box_step):             
             _cv.cd((_ix+1)+_iy*box_step)
             _imagename="image_"+"pos{}".format(_ix+_iy*5+_iz*25)
             _image = _i.Get(_imagename)
             _image.SetStats(0)
             _image.SetTitle("pos{}".format(_ix+_iy*5+_iz*25))
             _image.Draw("colz")
       _pdfname = _file.replace("_split.root","_split_cv{}.pdf".format(_iz))
       _cv.SaveAs(_pdfname)

def SplitTree(args):
    log().info('Processing tree2array...')
    treesum = GetTChain(args.inputFolder,"tree")         

    log().info('Spliting...')
    tree_list,name_list=[],[]
    box_step=5
    name_list, tree_list = GetSplitTree(box_step,treesum)

    log().info('Writing Output...')
    outname = args.inputFolder.replace(".root","_split.root")
    f = ROOT.TFile( outname, 'recreate' )
    f.cd()
    for _ilsit in range(len(tree_list)):
        _name=name_list[_ilsit]
        newtree=tree_list[_ilsit]
        makeplots(_ilsit,_name,newtree)
    for _ilsit in range(len(tree_list)):
        _name=name_list[_ilsit]
#        newtree=array2tree(tree_list[_ilsit])
        newtree=tree_list[_ilsit]
        newtree.SetName("tree_"+_name)
        newtree.Write()
    log().info('Output : %s'%(outname)) 
    f.Write()   

    makecv(outname,box_step)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("-i", "--inputFolder", type=str, default="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/20200406a_5to27_cali_calidata.root", help="Input Ntuple Name")
    parser.add_argument("-o", "--output", type=str, default=None, help="Output file")
    args = parser.parse_args()
    
    SplitTree( args )
