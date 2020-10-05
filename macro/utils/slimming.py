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
from array import array
from random import gauss

def DisableBranch(tree):
    tree.SetBranchStatus("*",0)
    tree.SetBranchStatus("adc0",1) 
    tree.SetBranchStatus("adc1",1) 
    tree.SetBranchStatus("adc2",1) 
    tree.SetBranchStatus("adc3",1) 
    tree.SetBranchStatus("adc4",1) 
    tree.SetBranchStatus("adc5",1) 
    tree.SetBranchStatus("adc6",1) 
    tree.SetBranchStatus("adc7",1) 
    tree.SetBranchStatus("cmn0",1) 
    tree.SetBranchStatus("cmn1",1) 
    tree.SetBranchStatus("cmn2",1) 
    tree.SetBranchStatus("cmn3",1) 
    tree.SetBranchStatus("cmn4",1) 
    tree.SetBranchStatus("cmn5",1) 
    tree.SetBranchStatus("cmn6",1) 
    tree.SetBranchStatus("cmn7",1) 
    tree.SetBranchStatus("index0",1) 
    tree.SetBranchStatus("index1",1) 
    tree.SetBranchStatus("index2",1) 
    tree.SetBranchStatus("index3",1) 
    tree.SetBranchStatus("index4",1) 
    tree.SetBranchStatus("index5",1) 
    tree.SetBranchStatus("index6",1) 
    tree.SetBranchStatus("index7",1) 
    tree.SetBranchStatus("hitnum0",1) 
    tree.SetBranchStatus("hitnum1",1) 
    tree.SetBranchStatus("hitnum2",1) 
    tree.SetBranchStatus("hitnum3",1) 
    tree.SetBranchStatus("hitnum4",1) 
    tree.SetBranchStatus("hitnum5",1) 
    tree.SetBranchStatus("hitnum6",1) 
    tree.SetBranchStatus("hitnum7",1) 
    tree.SetBranchStatus("integral_livetime",1) 
    tree.SetBranchStatus("unixtime",1) 
    return tree

    
