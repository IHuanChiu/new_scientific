#!/usr/bin/env python    
#-*- coding:utf-8 -*-   
"""
This module provides the slice plots
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
from logger import log, supports_color

class MakeSlicePlots():

      def __init__(self, _hist3=None):
          self._hist3 = _hist3
          self._nplots = 100
          self.h_xy_list = self._getslice_z()
          self.h_yz_list = self._getslice_x()
          self.h_xz_list = self._getslice_y()

      def _getslice_z(self):
          h_list=[]
          for i in range(self._nplots):      
             _h3temp = self._hist3.Clone()
             _u, _d = (16 - (32./self._nplots)*i), (16 - (32./self._nplots)*(i+1))
             _h3temp.GetZaxis().SetRangeUser(_d,_u)
             _h2 = _h3temp.Project3D("xy")
             _h2.SetStats(0)
             _h2.SetTitle("slice_z_%s"%(i)) 
             _h2.GetXaxis().SetTitle("X")
             _h2.GetYaxis().SetTitle("Y")
             _h2.GetZaxis().SetRangeUser(0., 30.)
             _h2.GetXaxis().SetRangeUser(-16, 16)
             _h2.GetYaxis().SetRangeUser(-16, 16)             
             #_h2.Rebin2D(4,4)
             h_list.append(_h2)
          return h_list

      def _getslice_x(self):
          h_list=[]
          for i in range(self._nplots):      
             _h3temp = self._hist3.Clone()
             _u, _d = (16 - (32./self._nplots)*i), (16 - (32./self._nplots)*(i+1))
             _h3temp.GetZaxis().SetRangeUser(_d,_u)
             _h2 = _h3temp.Project3D("yz")
             _h2.SetStats(0)
             _h2.SetTitle("slice_x_%s"%(i)) 
             _h2.GetXaxis().SetTitle("Y")
             _h2.GetYaxis().SetTitle("Z")
             _h2.GetZaxis().SetRangeUser(0., 30.)
             _h2.GetXaxis().SetRangeUser(-16, 16)
             _h2.GetYaxis().SetRangeUser(-16, 16)             
             #_h2.Rebin2D(4,4)
             h_list.append(_h2)
          return h_list

      def _getslice_y(self):
          h_list=[]
          for i in range(self._nplots):      
             _h3temp = self._hist3.Clone()
             _u, _d = (16 - (32./self._nplots)*i), (16 - (32./self._nplots)*(i+1))
             _h3temp.GetZaxis().SetRangeUser(_d,_u)
             _h2 = _h3temp.Project3D("xz")
             _h2.SetStats(0)
             _h2.SetTitle("slice_y_%s"%(i)) 
             _h2.GetXaxis().SetTitle("X")
             _h2.GetYaxis().SetTitle("Z")
             _h2.GetZaxis().SetRangeUser(0., 30.)
             _h2.GetXaxis().SetRangeUser(-16, 16)
             _h2.GetYaxis().SetRangeUser(-16, 16)             
             #_h2.Rebin2D(4,4)
             h_list.append(_h2)
          return h_list

      def GetSlices(self, _axisname):
          if _axisname is "z" or _axisname is "Z":   return self.h_xy_list
          elif _axisname is "y" or _axisname is "Y": return self.h_xz_list
          elif _axisname is "x" or _axisname is "X": return self.h_yz_list
          else:
             print("Wrong axis !!! ")
             return None
         

