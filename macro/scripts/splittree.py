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
import sys,os,random,math,ROOT
from ROOT import TFile, TTree, gROOT, gStyle, TCut, gPad, gDirectory
ROOT.gROOT.SetBatch(1)
import argparse
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/macro/utils/')
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/macro/')
ROOT.gErrorIgnoreLevel = ROOT.kWarning

from utils.helpers import GetTChain, createRatioCanvas
from logger import log, supports_color
import enums
import numpy as np
from root_numpy import hist2array, array2hist, tree2array, array2tree

def getUTcut(_x,_y_z):


def SplitTree(args):
    treesum = GetTChain(args.inputFolder,"tree")         
    Tarray = tree2array(treesum)

    cv1  = createRatioCanvas("cv1", 2500, 2500)
    cv2  = createRatioCanvas("cv2", 2500, 2500)
    cv3  = createRatioCanvas("cv3", 2500, 2500)
    cv4  = createRatioCanvas("cv4", 2500, 2500)
    cv5  = createRatioCanvas("cv5", 2500, 2500)

    array_list=[]
    box_size=5
    for iz in range(box_size):
       for iy in range(box_size):
          for ix in range(box_size):
             myUTselection=getUTcut(ix,iy,iz)
             array_list.append(tree2array(treesum,branches=["x","y","nsignaly_lv2","nsignalx_lv2","energy","energy_p","energy_n","unixtime"],selection=myUTselection))


    outname = args.inputFolder.replace(".root","_split.root")
    f = ROOT.TFile( outname, 'recreate' )
    f.cd()
    for _ilsit in range(len(array_list)):
        newtree=array2tree(array_list[_ilsit])
        cv  = createRatioCanvas("cv%d".format(_ilsit), 2500, 2500)
        newtree.Write()
        cv.Write()
    f.Write()    

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("-i", "--inputFolder", type=str, default="/Users/chiu.i-huan/Desktop/new_scientific/run/root/20200406a_5to27_cali_calidata.root", help="Input Ntuple Name")
    parser.add_argument("-o", "--output", type=str, default=None, help="Output file")
    args = parser.parse_args()
    
    SplitTree( args )
