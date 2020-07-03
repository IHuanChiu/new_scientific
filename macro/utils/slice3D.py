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
import enums

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
          self.MaxZ    = 250.
          self.MinZ    = 50.
          self.setlogz = 0

          # function
          self.h_xy_list = self._getslice_z()
          self.h_yz_list = self._getslice_x()
          self.h_xz_list = self._getslice_y()

      def _getslice_z(self):
          h_list=[]
          name = "/Users/chiu.i-huan/Desktop/new_scientific/run/figs/3Dslices/hist_z_all.ROOT.pdf"
          cv  = createRatioCanvas("cv_z", 1600, 1600)
          cv.Print(name + "[", "pdf");
          for i in range(self._nplots):                   
             _h3temp = self._hist3.Clone()
             _u, _d = (16 - (32./self._nplots)*i), (16 - (32./self._nplots)*(i+1))
             _h3temp.GetZaxis().SetRangeUser(_d,_u)
             _h2 = _h3temp.Project3D("xy")
             _h2.SetStats(0)
             _h2.SetTitle("slice z %.1f mm"%((_d+_u)/2.)) 
             _h2.GetXaxis().SetTitle("X [mm]")
             _h2.GetYaxis().SetTitle("Y [mm]")
             _h2.GetZaxis().SetRangeUser(self.MinZ, self.MaxZ)
             _h2.GetXaxis().SetRangeUser(-16, 16)
             _h2.GetYaxis().SetRangeUser(-16, 16)             
             _h2.RebinX(4)
             _h2.RebinY(4)
             h_list.append(_h2)
             gPad.SetLogz(self.setlogz)
             _h2.Draw("colz")
             cv.Print(name, "pdf") 
          cv.Print(name + "]", "pdf");
          return h_list

      def _getslice_x(self):
          h_list=[]
          name = "/Users/chiu.i-huan/Desktop/new_scientific/run/figs/3Dslices/hist_x_all.ROOT.pdf"
          cv  = createRatioCanvas("cv_x", 1600, 1600)
          cv.Print(name + "[", "pdf");
          for i in range(self._nplots):      
             _h3temp = self._hist3.Clone()
             _u, _d = (16 - (32./self._nplots)*i), (16 - (32./self._nplots)*(i+1))
             _h3temp.GetXaxis().SetRangeUser(_d,_u)
             _h2 = _h3temp.Project3D("yz")
             _h2.SetStats(0)
             _h2.SetTitle("slice x %.1f mm"%((_d+_u)/2.)) 
             _h2.GetZaxis().SetRangeUser(self.MinZ, self.MaxZ)
             _h2.SetAxisRange(-16, 16,"X")
             _h2.SetAxisRange(-16, 16,"Y")
             _h2.GetXaxis().SetTitle("Y [mm]")
             _h2.GetYaxis().SetTitle("Z [mm]")
             _h2.RebinX(4)
             _h2.RebinY(4)
             h_list.append(_h2)
             gPad.SetLogz(self.setlogz)
             _h2.Draw("colz")
             cv.Print(name, "pdf") 
          cv.Print(name + "]", "pdf");
          return h_list

      def _getslice_y(self):
          h_list=[]
          name = "/Users/chiu.i-huan/Desktop/new_scientific/run/figs/3Dslices/hist_y_all.ROOT.pdf"
          cv  = createRatioCanvas("cv_y", 1600, 1600)
          cv.Print(name + "[", "pdf");
          for i in range(self._nplots):      
             _h3temp = self._hist3.Clone()
             _u, _d = (16 - (32./self._nplots)*i), (16 - (32./self._nplots)*(i+1))
             _h3temp.GetYaxis().SetRangeUser(_d,_u)
             _h2 = _h3temp.Project3D("xz")
             _h2.SetStats(0)
             _h2.SetTitle("slice y %.1f mm"%((_d+_u)/2.)) 
             _h2.GetXaxis().SetTitle("X [mm]")
             _h2.GetYaxis().SetTitle("Z [mm]")
             _h2.GetZaxis().SetRangeUser(self.MinZ, self.MaxZ)
             _h2.GetXaxis().SetRangeUser(-16, 16)
             _h2.GetYaxis().SetRangeUser(-16, 16)             
             _h2.RebinX(4)
             _h2.RebinY(4)
             h_list.append(_h2)
             gPad.SetLogz(self.setlogz)
             _h2.Draw("colz")
             cv.Print(name, "pdf") 
          cv.Print(name + "]", "pdf");
          return h_list

      def GetSlices(self, _axisname):
          if _axisname is "z" or _axisname is "Z":   return self.h_xy_list
          elif _axisname is "y" or _axisname is "Y": return self.h_xz_list
          elif _axisname is "x" or _axisname is "X": return self.h_yz_list
          else:
             print("Wrong axis !!! ")
             return None
         
def makeTH2D(_chain,dtype):
    _nsteps = 31
    _timerange = 1800
    _it = enums.UTOfRotation
    h2list=[]
    if "CdTe" in dtype:
       cutname = "((trigger > 235 && trigger < 240) || (trigger > 247 && trigger < 253)) && (energy_p > 72 && energy_p < 78)" 
    else: 
       cutname = "((trigger > 590 && trigger < 600) || (trigger > 620 && trigger < 630)) && (energy_p > 12 && energy_p < 16)" 
    UTcut = "((unixtime-{0}) > 0)".format(_it)
    for _i in range(_nsteps):
       icut = TCut(cutname+"&&"+UTcut+"&&"+"(int(((unixtime-{0})/{1})%{2})=={3})".format(_it,_timerange,_nsteps,_i)) 
#       _chain.Draw("x:y >> h{}(128,-16,16,128,-16,16)".format(_i),icut,"colz")
       realsize = 113./78
       _chain.Draw("x*{0}:y*{0} >> h{1}(128,-25,25,128,-25,25)".format(realsize,_i),icut,"colz")
       h2list.append(gDirectory.Get("h{}".format(_i)))
    return h2list

def mergeTH2D(_h2list):
    # merge hist. with same angle
    _n_angle_step, _n_step=16, 31
    h2list=[]
    h2list.append(_h2list[0])
    for _i in range(1,_n_angle_step):
       _h2list[_i].Add(_h2list[_n_step-_i])
       h2list.append(_h2list[_i])
    return h2list
    
