#!/usr/bin/env python    
#-*- coding:utf-8 -*-   
"""
This module shows the main functions.
"""
__author__    = "I-Huan CHIU"
__email__     = "ichiu@chem.sci.osaka-u.ac.jp"
__created__   = "2019-11-08"
__copyright__ = "Copyright 2019 I-Huan CHIU"
__license__   = "GPL http://www.gnu.org/licenses/gpl.html"

# modules
import sys,os,random,math,ROOT
from ROOT import TFile, TTree, TCut, TChain, TSelector
from ROOT import gROOT, AddressOf
ROOT.gROOT.SetBatch(1)
import argparse
import math
from multiprocessing import Pool, cpu_count
import time
from time import localtime, asctime
from array import array
import logging
from utils.helpers import GetInputList 
from process import Processor

def main(args):
    
    ilist = GetInputList(args.inputFolder) 
    p = Processor(ifilelist = ilist, ofile=args.output, ncores = args.ncores, nevents = args.nevents, efile = args.efile)
    p.mainprocess() 
    exit(0)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("inputFolder", type=str, default="/Users/chiu.i-huan/Desktop/new_scientific/data/testinput/", help="Input File Name")
    parser.add_argument( "-o", "--output", type=str, default="../run/root/tranadc_dsd_", help="Output File Name")
    parser.add_argument( "-e", "--efile", type=str, default="../run/auxfile/spline_calibration.root", help="Calibration file Name")
    parser.add_argument( "-cpu", "--ncores", dest="ncores", type=int, default = 4, help="number of CPU")
    parser.add_argument( "-n", "--nevents", dest="nevents", type=int, default = None, help="Number of processing events." )
    args = parser.parse_args()

    main( args)

