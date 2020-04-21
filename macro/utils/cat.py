#!/usr/bin/env python    
#-*- coding:utf-8 -*-   
"""
This module provides definition of categories.
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
import enums 
from logger import log

class Category():
      def __init__(self, point=None):
          # category for single point
          self.point = point
          self.case1 = self.get1and1(self.point)
          self.case2 = self.get1and2(self.point)
          self.case3 = self.get2and1(self.point)
          self.case4 = self.get2and2(self.point)
          self.case5 = self.getother(self.point)
          self.hit = self.gethit()

      def get1and1(self,_p):
          _d={}
          _n=0
          if _p.nstrips_x is 1 and _p.nstrips_y is 1:
             _n+=1
             _d.update({_n:_p})
             return _d
          else: return None

      def get1and2(self,_p):
          _d={}
          _n=0
          if _p.nstrips_x is 1 and _p.nstrips_y is 2:
             Ex0 = _p.Lv1hit_x[_p.Lv1index_x[0]].energy
             Ey0 = _p.Lv1hit_y[_p.Lv1index_y[0]].energy
             Ey1 = _p.Lv1hit_y[_p.Lv1index_y[1]].energy
             _n+=1
             _d.update({_n:_p})
#             return _d
          else: return None

      def get2and1(self,_p):
          _d={}
          _n=0
          if _p.nstrips_x is 2 and _p.nstrips_y is 1:
             Ex0 = _p.Lv1hit_x[_p.Lv1index_x[0]].energy
             Ex1 = _p.Lv1hit_x[_p.Lv1index_x[1]].energy
             Ey0 = _p.Lv1hit_y[_p.Lv1index_y[0]].energy
             _n+=1
             _d.update({_n:_p})
#             return _d
          else: return None

      def get2and2(self,_p):
          _d={}
          _n=0
          if _p.nstrips_x is 2 and _p.nstrips_y is 2:
             Ex0 = _p.Lv1hit_x[_p.Lv1index_x[0]].energy
             Ex1 = _p.Lv1hit_x[_p.Lv1index_x[1]].energy
             Ey0 = _p.Lv1hit_y[_p.Lv1index_y[0]].energy
             Ey1 = _p.Lv1hit_y[_p.Lv1index_y[1]].energy
             _n+=1
             _d.update({_n:_p})
#             return _d
          else: return None

      def getother(self,_p):
          _d={}
          _n=0
          if _p.nstrips_x > 2 or _p.nstrips_y > 2:
             maxpoint=min(_p.nstrips_x,_p.nstrips_y)
             _n+=1
             _d.update({_n:_p})
#             return _d
          else: return None

      def gethit(self):
          _dic = {}
          _n = 0
          if self.case1:
             for _i in self.case1:
                _n += 1
                _dic.update({_n:self.case1[_i]})
          elif self.case2:
             for _i in self.case2:
                _n += 1
                _dic.update({_n:self.case2[_i]})
          elif self.case3:
             for _i in self.case3:
                _n += 1
                _dic.update({_n:self.case3[_i]})
          elif self.case4:
             for _i in self.case4:
                _n += 1
                _dic.update({_n:self.case4[_i]})
          elif self.case5:
             for _i in self.case5:
                _n += 1
                _dic.update({_n:self.case5[_i]})

          return _dic
          
