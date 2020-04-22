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
          self.case1 = self.get1and1(self.point,False)
          self.case2 = self.get1and2(self.point,False)
          self.case3 = self.get2and1(self.point,False)
          self.case4 = self.get2and2(self.point)
          self.case5 = self.getother(self.point)
          self.hit = self.gethit()

      def get1and1(self,_p,Re):
          _d={}
          _n=0
          if (_p.nstrips_x is 1 and _p.nstrips_y is 1) or Re:
             _n+=1
             _d.update({_n:_p})
          return _d

      def get1and2(self,_p,Re):
          _d={}
          _n=1 # only one photon
          if (_p.nstrips_x is 1 and _p.nstrips_y is 2) or Re:
             Ex0 = _p.Lv1hit_x[_p.Lv1index_x[0]].energy
             Ey0 = _p.Lv1hit_y[_p.Lv1index_y[0]].energy
             Ey1 = _p.Lv1hit_y[_p.Lv1index_y[1]].energy
             if( math.fabs(Ex0 - (Ey0+Ey1)) < enums.DeltaEnergy):
                _p.adc_n = _p.Lv1hit_y[_p.Lv1index_y[0]].adc
                _p.energy_n = Ey0
                _p.energy_p = Ex0*Ey0/(Ey0+Ey1)
                _p.y = _p.Lv1hit_y[_p.Lv1index_y[0]].position                
                _d.update({_n:_p})

                _n+=1
                _p.adc_n = _p.Lv1hit_y[_p.Lv1index_y[1]].adc
                _p.energy_n = Ey1
                _p.energy_p = Ex0*Ey1/(Ey0+Ey1)
                _p.y = _p.Lv1hit_y[_p.Lv1index_y[1]].position                
                _d.update({_n:_p})               
             else: 
                if(math.fabs(Ex0 - Ey0) < math.fabs(Ex0 - Ey1)) and (math.fabs(Ex0 - Ey0) < enums.DeltaEnergy):
                   _p.adc_n = _p.Lv1hit_y[_p.Lv1index_y[0]].adc
                   _p.energy_n = _p.Lv1hit_y[_p.Lv1index_y[0]].energy
                   _p.y = _p.Lv1hit_y[_p.Lv1index_y[0]].position
                   _d.update({_n:_p})
                if (math.fabs(Ex0 - Ey1) < math.fabs(Ex0 - Ey1)) and (math.fabs(Ex0 - Ey1) < enums.DeltaEnergy):
                   _p.adc_n = _p.Lv1hit_y[_p.Lv1index_y[1]].adc
                   _p.energy_n = _p.Lv1hit_y[_p.Lv1index_y[1]].energy
                   _p.y = _p.Lv1hit_y[_p.Lv1index_y[1]].position
                   _d.update({_n:_p})
          return _d

      def get2and1(self,_p,Re):
          _d={}
          _n=1 # only one photon
          if (_p.nstrips_x is 2 and _p.nstrips_y is 1) or Re:
             Ex0 = _p.Lv1hit_x[_p.Lv1index_x[0]].energy
             Ex1 = _p.Lv1hit_x[_p.Lv1index_x[1]].energy
             Ey0 = _p.Lv1hit_y[_p.Lv1index_y[0]].energy
             if( math.fabs(Ey0 - (Ex0+Ex1)) < enums.DeltaEnergy):
                _p.adc_n = _p.Lv1hit_x[_p.Lv1index_x[0]].adc
                _p.energy_n = Ex0
                _p.energy_p = Ey0*Ex0/(Ex0+Ex1)
                _p.y = _p.Lv1hit_x[_p.Lv1index_x[0]].position                
                _d.update({_n:_p})
                _n+=1
                _p.adc_n = _p.Lv1hit_x[_p.Lv1index_x[1]].adc
                _p.energy_n = Ex1
                _p.energy_p = Ey0*Ex1/(Ex0+Ex1)
                _p.y = _p.Lv1hit_x[_p.Lv1index_x[1]].position                
                _d.update({_n:_p})               
             else: 
                if(math.fabs(Ey0 - Ex0) < math.fabs(Ey0 - Ex1)) and (math.fabs(Ey0 - Ex0) < enums.DeltaEnergy):
                   _p.adc_p = _p.Lv1hit_x[_p.Lv1index_x[0]].adc
                   _p.energy_p = _p.Lv1hit_x[_p.Lv1index_x[0]].energy
                   _p.x = _p.Lv1hit_x[_p.Lv1index_x[0]].position
                   _d.update({_n:_p})
                if (math.fabs(Ey0 - Ex1) < math.fabs(Ey0 - Ex1)) and (math.fabs(Ey0 - Ex1) < enums.DeltaEnergy):
                   _p.adc_p = _p.Lv1hit_x[_p.Lv1index_x[1]].adc
                   _p.energy_p = _p.Lv1hit_x[_p.Lv1index_x[1]].energy
                   _p.x = _p.Lv1hit_x[_p.Lv1index_x[1]].position
                   _d.update({_n:_p})
          return _d

      def get2and2(self,_p):
          _d={}
          _n=0
          if _p.nstrips_x is 2 and _p.nstrips_y is 2:
             Ex0 = _p.Lv1hit_x[_p.Lv1index_x[0]].energy
             Ex1 = _p.Lv1hit_x[_p.Lv1index_x[1]].energy
             Ey0 = _p.Lv1hit_y[_p.Lv1index_y[0]].energy
             Ey1 = _p.Lv1hit_y[_p.Lv1index_y[1]].energy
             if(math.fabs(Ex0+Ex1-Ey0-Ey1)  < enums.DeltaEnergy ):#four photons
                if(math.fabs(Ex0-Ey0) < enums.DeltaEnergy) and (math.fabs(Ex1-Ey1) < enums.DeltaEnergy):
                   _n+=1
                   _p.adc_p = _p.Lv1hit_x[_p.Lv1index_x[0]].adc
                   _p.adc_n = _p.Lv1hit_y[_p.Lv1index_y[0]].adc
                   _p.energy_p = _p.Lv1hit_x[_p.Lv1index_x[0]].energy
                   _p.energy_n = _p.Lv1hit_y[_p.Lv1index_y[0]].energy
                   _p.x = _p.Lv1hit_x[_p.Lv1index_x[0]].position
                   _p.y = _p.Lv1hit_y[_p.Lv1index_y[0]].position
                   _d.update({_n:_p})
                   _n+=1
                   _p.adc_p = _p.Lv1hit_x[_p.Lv1index_x[1]].adc
                   _p.adc_n = _p.Lv1hit_y[_p.Lv1index_y[1]].adc
                   _p.energy_p = _p.Lv1hit_x[_p.Lv1index_x[1]].energy
                   _p.energy_n = _p.Lv1hit_y[_p.Lv1index_y[1]].energy
                   _p.x = _p.Lv1hit_x[_p.Lv1index_x[1]].position
                   _p.y = _p.Lv1hit_y[_p.Lv1index_y[1]].position
                   _d.update({_n:_p})
                elif (math.fabs(Ex0-Ey1) < enums.DeltaEnergy) and (math.fabs(Ex1-Ey0) < enums.DeltaEnergy):
                   _n+=1
                   _p.adc_p = _p.Lv1hit_x[_p.Lv1index_x[0]].adc
                   _p.adc_n = _p.Lv1hit_y[_p.Lv1index_y[1]].adc
                   _p.energy_p = _p.Lv1hit_x[_p.Lv1index_x[0]].energy
                   _p.energy_n = _p.Lv1hit_y[_p.Lv1index_y[1]].energy
                   _p.x = _p.Lv1hit_x[_p.Lv1index_x[0]].position
                   _p.y = _p.Lv1hit_y[_p.Lv1index_y[1]].position
                   _d.update({_n:_p})
                   _n+=1
                   _p.adc_p = _p.Lv1hit_x[_p.Lv1index_x[1]].adc
                   _p.adc_n = _p.Lv1hit_y[_p.Lv1index_y[0]].adc
                   _p.energy_p = _p.Lv1hit_x[_p.Lv1index_x[1]].energy
                   _p.energy_n = _p.Lv1hit_y[_p.Lv1index_y[0]].energy
                   _p.x = _p.Lv1hit_x[_p.Lv1index_x[1]].position
                   _p.y = _p.Lv1hit_y[_p.Lv1index_y[0]].position
                   _d.update({_n:_p})
             elif ((Ey0+Ey1) > (Ex0+Ex1)):# n-side share photon case3
                if  (((Ey0+Ey1) - Ex0) < enums.DeltaEnergy):                   
                   _d = self.get1and2(_p,True)
                elif (((Ey0+Ey1) - Ex1) < enums.DeltaEnergy):
                   _p.Lv1hit_x[_p.Lv1index_x[0]] = _p.Lv1hit_x[_p.Lv1index_x[1]]
                   _d = self.get1and2(_p,True)                
             else:# p-side share photon case2
                if  (((Ex0+Ex1) - Ey0) < enums.DeltaEnergy):
                   _d = self.get2and1(_p,True)
                elif (((Ex0+Ex1) - Ey1) < enums.DeltaEnergy):
                   _p.Lv1hit_y[_p.Lv1index_y[0]] = _p.Lv1hit_y[_p.Lv1index_y[1]]
                   _d = self.get2and1(_p,True)
          return _d

      def getother(self,_p):
          _d={}
          _n=0
          if _p.nstrips_x > 2 or _p.nstrips_y > 2:
             maxpoint=min(_p.nstrips_x,_p.nstrips_y)
             for i in range(maxpoint):
                for j in range(maxpoint):
                   Ex = _p.Lv1hit_x[_p.Lv1index_x[i]].energy
                   Ey = _p.Lv1hit_y[_p.Lv1index_y[j]].energy
                   if(math.fabs(Ex-Ey) < enums.DeltaEnergy):        
                      _n+=1
                      _p.adc_p = _p.Lv1hit_x[_p.Lv1index_x[i]].adc
                      _p.adc_n = _p.Lv1hit_y[_p.Lv1index_y[j]].adc
                      _p.energy_p = _p.Lv1hit_x[_p.Lv1index_x[i]].energy
                      _p.energy_n = _p.Lv1hit_y[_p.Lv1index_y[j]].energy
                      _p.x = _p.Lv1hit_x[_p.Lv1index_x[i]].position
                      _p.y = _p.Lv1hit_y[_p.Lv1index_y[j]].position
                      _d.update({_n:_p})
          return _d

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
          
