from __future__ import division
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
from ROOT import TFile, TTree, gROOT
ROOT.gROOT.SetBatch(1)
import argparse
import math
from multiprocessing import Pool, cpu_count
from array import array
from random import gauss

def test():
    print(__name__)

def checkTree(tree, ori_tree):
#    print "=========== Checking tree ===========" 
    totalevent  = tree.GetEntries()
    totalxhit, totalyhit, totalhit = 0,0,0
    for e in tree:     
       totalxhit += e.nsignalx_lv1
       totalyhit += e.nsignaly_lv1
       totalhit += e.nhit

    print("=========== Results ===========")
    print("Total passed events : ", totalevent,"/",ori_tree.GetEntries())
    print("Total passed hits (average) =>  ", " X : ", totalxhit, "(", totalxhit/totalevent ,"); "," Y : ", totalyhit, "(", totalyhit/totalevent ,"); "," Point : ", totalhit, "(", totalhit/totalevent ,");")
        
if __name__ == "__main__":
    f = ROOT.TFile("../run/root/tranadc_dsd_temp.root","read") 
    mytree = f.Get("tree")
    checkTree(mytree,mytree)
    
