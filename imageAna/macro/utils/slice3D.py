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
from utils.logger import log, supports_color
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
          name = "/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/figs/3Dslices/hist_z_all.ROOT.pdf"
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
          name = "/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/figs/3Dslices/hist_x_all.ROOT.pdf"
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
          name = "/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/figs/3Dslices/hist_y_all.ROOT.pdf"
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
          if _axisname == "z" or _axisname == "Z":   return self.h_xy_list
          elif _axisname == "y" or _axisname == "Y": return self.h_xz_list
          elif _axisname == "x" or _axisname == "X": return self.h_yz_list
          else:
             print("Wrong axis !!! ")
             return None

def _getUTcut(_iplot):
    _nsteps = 31
    _timerange = 1800
    _timerange2 = 4500
    _group1 = "((unixtime > 1583670785 && unixtime < 1583727074) && (int(((unixtime-1583670785)/{0})%{1})=={2}))".format(_timerange,_nsteps,_iplot)
    _group2 = "((unixtime > 1583736900 && unixtime < 1583758670) && (int(((unixtime-1583736900)/{0})%{1})=={2}))".format(_timerange,_nsteps,_iplot)
    _group3 = "((unixtime > 1583758670 && unixtime < 1583793160) && (int(((unixtime-1583758670)/{0})%{1})=={2}) && ({3}>=10))".format(_timerange,_nsteps,(_iplot-10),_iplot)#from 225
    _group4 = "((unixtime > 1583797637 && unixtime < 1583798147) && ({0}==0))".format(_iplot)
    _group5 = "((unixtime > 1583798147 && unixtime < 1583802651) && ({0}==1))".format(_iplot)
    _group6 = "((unixtime > 1583802651) && (int(((unixtime-1583802651)/{0})%{1})=={2}) && ({3}%2==1) && ({3}>=3))".format(_timerange2,(_nsteps-1)/2,(_iplot-1)/2,_iplot)#from 67.5
    _utcut_name = "("+_group1+"||"+_group2+"||"+_group3+"||"+_group4+"||"+_group5+"||"+_group6+")"
    return _utcut_name

def makeTH2D(_chain,dtype):
    _nsteps = 31
    _timerange = 1800
    _it = enums.UTOfRotation
    h2list=[]
    if "CdTe" in dtype:
       cutname = "((trigger > 235 && trigger < 240) || (trigger > 247 && trigger < 253)) && (energy_p > 72 && energy_p < 78)" 
    else: 
       cutname = "((trigger > 590 && trigger < 600) || (trigger > 620 && trigger < 630)) && (energy_p > 12 && energy_p < 16)" 
    UTcut = "((unixtime-{0}) > 0)".format(_it)# all momentum
#    UTcut = "((unixtime > 1583663336 && unixtime < 1583663640) || (unixtime > 1583665785 && unixtime < 1583668072) || (unixtime > 1583670126 && unixtime < 1583728926) || (unixtime > 1583797615 && unixtime < 1583807420) || (unixtime > 1583808902 && unixtime < 1583823904) || (unixtime > 1583825103 && unixtime < 1583837643) || (unixtime > 1583838416 && unixtime < 1583846500) || (unixtime > 1583847476 && unixtime < 1583872201))"# momentum 30MeV
#    UTcut = "((unixtime > 1583663750 && unixtime < 1583664003) || (unixtime > 1583668150 && unixtime < 1583669991) || (unixtime > 1583736792 && unixtime < 1583795103))".format(_it)# momentum 35MeV
    for _i in range(_nsteps):
#       icut = TCut(cutname+"&&"+UTcut+"&&"+"(int(((unixtime-{0})/{1})%{2})=={3})".format(_it,_timerange,_nsteps,_i)) 
       icut = TCut(cutname+"&&"+UTcut+"&&"+_getUTcut(_i))
       _chain.Draw('x:y >> h{}(128,-16,16,128,-16,16)'.format(_i),icut,"colz")
#       realsize = 113./78
#       _chain.Draw("x*{0}:y*{0} >> h{1}(128,-25,25,128,-25,25)".format(realsize,_i),icut,"colz")
       h2list.append(gDirectory.Get("h{}".format(_i)))
    for _ih in range(len(h2list)): 
       h2list[_ih].SetTitle("h{}_2d".format(_ih))
    return h2list

def mergeTH2D(_h2list):
    # merge hist. at same angle
    _n_angle_step, _n_step=16, 31
    h2list=[]
    h2list.append(_h2list[0])
    for _i in range(1,_n_angle_step):
       _h2list[_i].Add(_h2list[_n_step-_i])
       h2list.append(_h2list[_i])
    return h2list
    
