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
from hits import hitphoton

class Category():
      def __init__(self, cluster=None):
          # category for single cluster
          self.cluster = cluster
          self.case1 = self.get1and1(self.cluster,False)
          self.case2 = self.get1and2(self.cluster,False)
          self.case3 = self.get2and1(self.cluster,False)
          self.case4 = self.get2and2(self.cluster)
          self.case5 = self.getother(self.cluster)
          self.hit = self.gethit()

      def get1and1(self,_clu,Re):
          _d={}
          _n=0
          if (_clu.nstrips_x is 1 and _clu.nstrips_y is 1) or Re:
             _p = setphoton(_clu.energy_p,_clu.energy_n,_clu.adc_p,_clu.adc_n,_clu.x,_clu.y,1)
             _n+=1
             _d.update({_n:_p})
          return _d

      def get1and2(self,_clu,Re):
          _d={}
          _n=0
          if (_clu.nstrips_x is 1 and _clu.nstrips_y is 2) or Re:
             Ex0 = _clu.Lv1hit_x[_clu.Lv1index_x[0]].energy # same with _clu.energy_p
             Ey0 = _clu.Lv1hit_y[_clu.Lv1index_y[0]].energy
             Ey1 = _clu.Lv1hit_y[_clu.Lv1index_y[1]].energy
             if( math.fabs(Ex0 - (Ey0+Ey1)) < enums.DeltaEnergy): # Two photons
#                _clu.adc_n = _clu.Lv1hit_y[_clu.Lv1index_y[0]].adc
#                _clu.energy_n = Ey0
#                _clu.energy_p = Ex0*Ey0/(Ey0+Ey1)
#                _clu.y = _clu.Lv1hit_y[_clu.Lv1index_y[0]].position                
                _p = setphoton(Ex0*Ey0/(Ey0+Ey1), Ey0, _clu.adc_p*Ey0/(Ey0+Ey1), _clu.Lv1hit_y[_clu.Lv1index_y[0]].adc, _clu.x, _clu.Lv1hit_y[_clu.Lv1index_y[0]].position, 2)
                _n+=1
                _d.update({_n:_p})

#                _clu.adc_n = _clu.Lv1hit_y[_clu.Lv1index_y[1]].adc
#                _clu.energy_n = Ey1
#                _clu.energy_p = Ex0*Ey1/(Ey0+Ey1)
#                _clu.y = _clu.Lv1hit_y[_clu.Lv1index_y[1]].position                
                _p = setphoton(Ex0*Ey1/(Ey0+Ey1), Ey1, _clu.adc_p*Ey1/(Ey0+Ey1), _clu.Lv1hit_y[_clu.Lv1index_y[1]].adc, _clu.x, _clu.Lv1hit_y[_clu.Lv1index_y[1]].position, 2)
                _n+=1
                _d.update({_n:_p})               
             else: # One noise
                if(math.fabs(Ex0 - Ey0) < math.fabs(Ex0 - Ey1)) and (math.fabs(Ex0 - Ey0) < enums.DeltaEnergy):
#                   _clu.adc_n = _clu.Lv1hit_y[_clu.Lv1index_y[0]].adc
#                   _clu.energy_n = _clu.Lv1hit_y[_clu.Lv1index_y[0]].energy
#                   _clu.y = _clu.Lv1hit_y[_clu.Lv1index_y[0]].position
                   _p = setphoton(_clu.energy_p, _clu.Lv1hit_y[_clu.Lv1index_y[0]].energy, _clu.adc_p, _clu.Lv1hit_y[_clu.Lv1index_y[0]].adc, _clu.x, _clu.Lv1hit_y[_clu.Lv1index_y[0]].position, 2)
                   _n+=1
                   _d.update({_n:_p})
                if (math.fabs(Ex0 - Ey1) < math.fabs(Ex0 - Ey1)) and (math.fabs(Ex0 - Ey1) < enums.DeltaEnergy):
#                   _clu.adc_n = _clu.Lv1hit_y[_clu.Lv1index_y[1]].adc
#                   _clu.energy_n = _clu.Lv1hit_y[_clu.Lv1index_y[1]].energy
#                   _clu.y = _clu.Lv1hit_y[_clu.Lv1index_y[1]].position
                   _p = setphoton(_clu.energy_p, _clu.Lv1hit_y[_clu.Lv1index_y[1]].energy, _clu.adc_p, _clu.Lv1hit_y[_clu.Lv1index_y[1]].adc, _clu.x, _clu.Lv1hit_y[_clu.Lv1index_y[1]].position, 2)
                   _n+=1
                   _d.update({_n:_p})
          return _d

      def get2and1(self,_clu,Re):
          _d={}
          _n=0
          if (_clu.nstrips_x is 2 and _clu.nstrips_y is 1) or Re:
             Ex0 = _clu.Lv1hit_x[_clu.Lv1index_x[0]].energy
             Ex1 = _clu.Lv1hit_x[_clu.Lv1index_x[1]].energy
             Ey0 = _clu.Lv1hit_y[_clu.Lv1index_y[0]].energy
             if( math.fabs(Ey0 - (Ex0+Ex1)) < enums.DeltaEnergy):
#                _clu.adc_n = _clu.Lv1hit_x[_clu.Lv1index_x[0]].adc
#                _clu.energy_n = Ex0
#                _clu.energy_p = Ey0*Ex0/(Ex0+Ex1)
#                _clu.y = _clu.Lv1hit_x[_clu.Lv1index_x[0]].position               
                _p = setphoton(Ex0, Ey0*Ex0/(Ex0+Ex1), _clu.Lv1hit_x[_clu.Lv1index_x[0]].adc, _clu.adc_n*Ex0/(Ex0+Ex1), _clu.Lv1hit_x[_clu.Lv1index_x[0]].position, _clu.y, 3) 
                _n+=1
                _d.update({_n:_p})
#                _clu.adc_n = _clu.Lv1hit_x[_clu.Lv1index_x[1]].adc
#                _clu.energy_n = Ex1
#                _clu.energy_p = Ey0*Ex1/(Ex0+Ex1)
#                _clu.y = _clu.Lv1hit_x[_clu.Lv1index_x[1]].position                
                _p = setphoton(Ex1, Ey0*Ex1/(Ex0+Ex1), _clu.Lv1hit_x[_clu.Lv1index_x[1]].adc, _clu.adc_n*Ex1/(Ex0+Ex1), _clu.Lv1hit_x[_clu.Lv1index_x[1]].position, _clu.y, 3) 
                _n+=1
                _d.update({_n:_p})               
             else: 
                if(math.fabs(Ey0 - Ex0) < math.fabs(Ey0 - Ex1)) and (math.fabs(Ey0 - Ex0) < enums.DeltaEnergy):
#                   _clu.adc_p = _clu.Lv1hit_x[_clu.Lv1index_x[0]].adc
#                   _clu.energy_p = _clu.Lv1hit_x[_clu.Lv1index_x[0]].energy
#                   _clu.x = _clu.Lv1hit_x[_clu.Lv1index_x[0]].position
                   _p = setphoton(_clu.Lv1hit_x[_clu.Lv1index_x[0]].energy, Ey0, _clu.Lv1hit_x[_clu.Lv1index_x[0]].adc, _clu.adc_n, _clu.Lv1hit_x[_clu.Lv1index_x[0]].position, _clu.y, 3)
                   _n+=1
                   _d.update({_n:_p})
                if (math.fabs(Ey0 - Ex1) < math.fabs(Ey0 - Ex1)) and (math.fabs(Ey0 - Ex1) < enums.DeltaEnergy):
#                   _clu.adc_p = _clu.Lv1hit_x[_clu.Lv1index_x[1]].adc
#                   _clu.energy_p = _clu.Lv1hit_x[_clu.Lv1index_x[1]].energy
#                   _clu.x = _clu.Lv1hit_x[_clu.Lv1index_x[1]].position
                   _p = setphoton(_clu.Lv1hit_x[_clu.Lv1index_x[1]].energy, Ey0, _clu.Lv1hit_x[_clu.Lv1index_x[1]].adc, _clu.adc_n, _clu.Lv1hit_x[_clu.Lv1index_x[1]].position, _clu.y, 3)
                   _n+=1
                   _d.update({_n:_p})
          return _d

      def get2and2(self,_clu):
          _d={}
          _n=0
          if _clu.nstrips_x is 2 and _clu.nstrips_y is 2:
             Ex0 = _clu.Lv1hit_x[_clu.Lv1index_x[0]].energy
             Ex1 = _clu.Lv1hit_x[_clu.Lv1index_x[1]].energy
             Ey0 = _clu.Lv1hit_y[_clu.Lv1index_y[0]].energy
             Ey1 = _clu.Lv1hit_y[_clu.Lv1index_y[1]].energy
             if(math.fabs(Ex0+Ex1-Ey0-Ey1)  < enums.DeltaEnergy ):#four photons
                if(math.fabs(Ex0-Ey0) < enums.DeltaEnergy) and (math.fabs(Ex1-Ey1) < enums.DeltaEnergy):
#                   _clu.adc_p = _clu.Lv1hit_x[_clu.Lv1index_x[0]].adc
#                   _clu.adc_n = _clu.Lv1hit_y[_clu.Lv1index_y[0]].adc
#                   _clu.energy_p = _clu.Lv1hit_x[_clu.Lv1index_x[0]].energy
#                   _clu.energy_n = _clu.Lv1hit_y[_clu.Lv1index_y[0]].energy
#                   _clu.x = _clu.Lv1hit_x[_clu.Lv1index_x[0]].position
#                   _clu.y = _clu.Lv1hit_y[_clu.Lv1index_y[0]].position
                   _p = setphoton(_clu.Lv1hit_x[_clu.Lv1index_x[0]].energy, _clu.Lv1hit_y[_clu.Lv1index_y[0]].energy, _clu.Lv1hit_x[_clu.Lv1index_x[0]].adc, _clu.Lv1hit_y[_clu.Lv1index_y[0]].adc, _clu.Lv1hit_x[_clu.Lv1index_x[0]].position, _clu.Lv1hit_y[_clu.Lv1index_y[0]].position, 4)
                   _n+=1
                   _d.update({_n:_p})
#                   _clu.adc_p = _clu.Lv1hit_x[_clu.Lv1index_x[1]].adc
#                   _clu.adc_n = _clu.Lv1hit_y[_clu.Lv1index_y[1]].adc
#                   _clu.energy_p = _clu.Lv1hit_x[_clu.Lv1index_x[1]].energy
#                   _clu.energy_n = _clu.Lv1hit_y[_clu.Lv1index_y[1]].energy
#                   _clu.x = _clu.Lv1hit_x[_clu.Lv1index_x[1]].position
#                   _clu.y = _clu.Lv1hit_y[_clu.Lv1index_y[1]].position
                   _p = setphoton(_clu.Lv1hit_x[_clu.Lv1index_x[1]].energy, _clu.Lv1hit_y[_clu.Lv1index_y[1]].energy, _clu.Lv1hit_x[_clu.Lv1index_x[1]].adc, _clu.Lv1hit_y[_clu.Lv1index_y[1]].adc, _clu.Lv1hit_x[_clu.Lv1index_x[1]].position, _clu.Lv1hit_y[_clu.Lv1index_y[1]].position, 4)
                   _n+=1
                   _d.update({_n:_p})
                elif (math.fabs(Ex0-Ey1) < enums.DeltaEnergy) and (math.fabs(Ex1-Ey0) < enums.DeltaEnergy):
#                   _clu.adc_p = _clu.Lv1hit_x[_clu.Lv1index_x[0]].adc
#                   _clu.adc_n = _clu.Lv1hit_y[_clu.Lv1index_y[1]].adc
#                   _clu.energy_p = _clu.Lv1hit_x[_clu.Lv1index_x[0]].energy
#                   _clu.energy_n = _clu.Lv1hit_y[_clu.Lv1index_y[1]].energy
#                   _clu.x = _clu.Lv1hit_x[_clu.Lv1index_x[0]].position
#                   _clu.y = _clu.Lv1hit_y[_clu.Lv1index_y[1]].position
                   _p = setphoton(_clu.Lv1hit_x[_clu.Lv1index_x[0]].energy, _clu.Lv1hit_y[_clu.Lv1index_y[1]].energy, _clu.Lv1hit_x[_clu.Lv1index_x[0]].adc, _clu.Lv1hit_y[_clu.Lv1index_y[1]].adc, _clu.Lv1hit_x[_clu.Lv1index_x[0]].position, _clu.Lv1hit_y[_clu.Lv1index_y[1]].position, 4)
                   _n+=1
                   _d.update({_n:_p})
#                   _clu.adc_p = _clu.Lv1hit_x[_clu.Lv1index_x[1]].adc
#                   _clu.adc_n = _clu.Lv1hit_y[_clu.Lv1index_y[0]].adc
#                   _clu.energy_p = _clu.Lv1hit_x[_clu.Lv1index_x[1]].energy
#                   _clu.energy_n = _clu.Lv1hit_y[_clu.Lv1index_y[0]].energy
#                   _clu.x = _clu.Lv1hit_x[_clu.Lv1index_x[1]].position
#                   _clu.y = _clu.Lv1hit_y[_clu.Lv1index_y[0]].position
                   _p = setphoton(_clu.Lv1hit_x[_clu.Lv1index_x[1]].energy, _clu.Lv1hit_y[_clu.Lv1index_y[0]].energy, _clu.Lv1hit_x[_clu.Lv1index_x[1]].adc, _clu.Lv1hit_y[_clu.Lv1index_y[0]].adc, _clu.Lv1hit_x[_clu.Lv1index_x[1]].position, _clu.Lv1hit_y[_clu.Lv1index_y[0]].position, 4)
                   _n+=1
                   _d.update({_n:_p})
             elif ((Ey0+Ey1) > (Ex0+Ex1)):# one noise in y-side -> return case3 (2*1)
                if  (((Ex0+Ex1) - Ey0) < enums.DeltaEnergy):                   
                   _d = self.get2and1(_clu,True)
                elif (((Ex0+Ex1) - Ey1) < enums.DeltaEnergy):
                   _clu.Lv1hit_y[_clu.Lv1index_y[0]] = _clu.Lv1hit_y[_clu.Lv1index_y[1]]
                   _d = self.get2and1(_clu,True)                
             else:# one noise in x-side -> return case2 (1*2)
                if  (((Ey0+Ey1) - Ex0) < enums.DeltaEnergy):
                   _d = self.get1and2(_clu,True)
                elif (((Ey0+Ey1) - Ex1) < enums.DeltaEnergy):
                   _clu.Lv1hit_x[_clu.Lv1index_x[0]] = _clu.Lv1hit_x[_clu.Lv1index_x[1]]
                   _d = self.get1and2(_clu,True)
          return _d

      def getother(self,_clu):
          _d={}
          _n=0
          if _clu.nstrips_x > 2 or _clu.nstrips_y > 2:
             maxpoint=min(_clu.nstrips_x,_clu.nstrips_y)
             for i in range(maxpoint):
                for j in range(maxpoint):
                   Ex = _clu.Lv1hit_x[_clu.Lv1index_x[i]].energy
                   Ey = _clu.Lv1hit_y[_clu.Lv1index_y[j]].energy
                   if(math.fabs(Ex-Ey) < enums.DeltaEnergy):        
#                      _clu.adc_p = _clu.Lv1hit_x[_clu.Lv1index_x[i]].adc
#                      _clu.adc_n = _clu.Lv1hit_y[_clu.Lv1index_y[j]].adc
#                      _clu.energy_p = _clu.Lv1hit_x[_clu.Lv1index_x[i]].energy
#                      _clu.energy_n = _clu.Lv1hit_y[_clu.Lv1index_y[j]].energy
#                      _clu.x = _clu.Lv1hit_x[_clu.Lv1index_x[i]].position
#                      _clu.y = _clu.Lv1hit_y[_clu.Lv1index_y[j]].position
                      _p = setphoton(_clu.Lv1hit_x[_clu.Lv1index_x[i]].energy, _clu.Lv1hit_y[_clu.Lv1index_y[j]].energy, _clu.Lv1hit_x[_clu.Lv1index_x[i]].adc, _clu.Lv1hit_y[_clu.Lv1index_y[j]].adc, _clu.Lv1hit_x[_clu.Lv1index_x[i]].position, _clu.Lv1hit_y[_clu.Lv1index_y[j]].position, 5)
                      _n+=1
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


def setphoton(ep,en,adcp,adcn,x,y,case):
    _p = hitphoton()
    _p.energy_p  = ep
    _p.energy_n  = en
    _p.adc_p     = adcp
    _p.adc_n     = adcn
    _p.x         = x
    _p.y         = y
    _p.type      = case
    return _p
          
