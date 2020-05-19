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
from logger import log, supports_color
from helpers import createRatioCanvas
ROOT.gErrorIgnoreLevel = ROOT.kWarning

gROOT.ProcessLine(
"struct RootHistStruct {\
   TH2D* h2_x[128];\
   TH2D* h2_y[128];\
   TH2D* h2_z[128];\
};"
); 

from ROOT import RootHistStruct
Hist = RootHistStruct()

class MakeSlicePlots():

      def __init__(self, _hist3=None):
          self._hist3 = _hist3

          # member
          self._nplots = 40
          self.MaxZ    = 80.
          self.setlogz = 0

          # function
          self.h_xy_list = self._getslice_z()
          self.h_yz_list = self._getslice_x()
          self.h_xz_list = self._getslice_y()

      def _getslice_z(self):
          h_list=[]
          for i in range(self._nplots):                   
             cv  = createRatioCanvas("cv_%s"%(i), 1600, 1600)
             _h3temp = self._hist3.Clone()
             _u, _d = (16 - (32./self._nplots)*i), (16 - (32./self._nplots)*(i+1))
             _h3temp.GetZaxis().SetRangeUser(_d,_u)
             _h2 = _h3temp.Project3D("xy")
             _h2.SetStats(0)
             _h2.SetTitle("slice z %1f mm"%((_d+_u)/2.)) 
             _h2.GetXaxis().SetTitle("X")
             _h2.GetYaxis().SetTitle("Y")
             _h2.GetZaxis().SetRangeUser(0., self.MaxZ)
             _h2.GetXaxis().SetRangeUser(-16, 16)
             _h2.GetYaxis().SetRangeUser(-16, 16)             
             _h2.RebinX(2)
             _h2.RebinY(2)
             h_list.append(_h2)
             gPad.SetLogz(self.setlogz)
             _h2.Draw("colz")
             cv.Print("/Users/chiu.i-huan/Desktop/new_scientific/run/figs/3Dslices/hist_z_%d.ROOT.pdf"%(i)) 
          return h_list

      def _getslice_x(self):
          h_list=[]
          for i in range(self._nplots):      
             cv  = createRatioCanvas("cv_%s"%(i), 1600, 1600)
             _h3temp = self._hist3.Clone()
             _u, _d = (16 - (32./self._nplots)*i), (16 - (32./self._nplots)*(i+1))
             _h3temp.GetZaxis().SetRangeUser(_d,_u)
             _h2 = _h3temp.Project3D("yz")
             _h2.SetStats(0)
             _h2.SetTitle("slice x %1f mm"%((_d+_u)/2.)) 
             _h2.GetZaxis().SetRangeUser(0., self.MaxZ)
             _h2.SetAxisRange(-16, 16,"X")
             _h2.SetAxisRange(-16, 16,"Y")
             _h2.GetXaxis().SetTitle("Y")
             _h2.GetYaxis().SetTitle("Z")
             _h2.RebinX(2)
             _h2.RebinY(2)
             h_list.append(_h2)
             gPad.SetLogz(self.setlogz)
             _h2.Draw("colz")
             cv.Print("/Users/chiu.i-huan/Desktop/new_scientific/run/figs/3Dslices/hist_x_%d.ROOT.pdf"%(i)) 
          return h_list

      def _getslice_y(self):
          h_list=[]
          for i in range(self._nplots):      
             cv  = createRatioCanvas("cv_%s"%(i), 1600, 1600)
             _h3temp = self._hist3.Clone()
             _u, _d = (16 - (32./self._nplots)*i), (16 - (32./self._nplots)*(i+1))
             _h3temp.GetZaxis().SetRangeUser(_d,_u)
             _h2 = _h3temp.Project3D("xz")
             _h2.SetStats(0)
             _h2.SetTitle("slice y %1f mm"%((_d+_u)/2.)) 
             _h2.GetXaxis().SetTitle("X")
             _h2.GetYaxis().SetTitle("Z")
             _h2.GetZaxis().SetRangeUser(0., self.MaxZ)
             _h2.GetXaxis().SetRangeUser(-16, 16)
             _h2.GetYaxis().SetRangeUser(-16, 16)             
             _h2.RebinX(2)
             _h2.RebinY(2)
             h_list.append(_h2)
             gPad.SetLogz(self.setlogz)
             _h2.Draw("colz")
             cv.Print("/Users/chiu.i-huan/Desktop/new_scientific/run/figs/3Dslices/hist_y_%d.ROOT.pdf"%(i)) 
          return h_list

      def GetSlices(self, _axisname):
          if _axisname is "z" or _axisname is "Z":   return self.h_xy_list
          elif _axisname is "y" or _axisname is "Y": return self.h_xz_list
          elif _axisname is "x" or _axisname is "X": return self.h_yz_list
          else:
             print("Wrong axis !!! ")
             return None
         

