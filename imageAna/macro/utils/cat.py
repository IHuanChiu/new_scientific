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
          if (_clu.nstrips_x == 1 and _clu.nstrips_y == 1) or Re:
             _p = setphoton((_clu.energy_p+_clu.energy_n)*0.5,_clu.energy_p,_clu.energy_n,_clu.adc_p,_clu.adc_n,_clu.x,_clu.y,1)
             _n+=1
             _d.update({_n:_p})
          return _d

      def get1and2(self,_clu,Re):
          _d={}
          _n=0
          if (_clu.nstrips_x == 1 and _clu.nstrips_y == 2) or Re:
             Ex0 = _clu.Lv1hit_x[_clu.Lv1index_x[0]].energy # same with _clu.energy_p
             Ey0 = _clu.Lv1hit_y[_clu.Lv1index_y[0]].energy
             Ey1 = _clu.Lv1hit_y[_clu.Lv1index_y[1]].energy
             if( math.fabs(Ex0 - (Ey0+Ey1)) < enums.DeltaEnergy): # Two photons
                _p = setphoton(Ey0, Ex0*Ey0/(Ey0+Ey1), Ey0, _clu.adc_p*Ey0/(Ey0+Ey1), _clu.Lv1hit_y[_clu.Lv1index_y[0]].adc, _clu.x, _clu.Lv1hit_y[_clu.Lv1index_y[0]].position, 2)
                _n+=1
                _d.update({_n:_p})

                _p = setphoton(Ey1, Ex0*Ey1/(Ey0+Ey1), Ey1, _clu.adc_p*Ey1/(Ey0+Ey1), _clu.Lv1hit_y[_clu.Lv1index_y[1]].adc, _clu.x, _clu.Lv1hit_y[_clu.Lv1index_y[1]].position, 2)
                _n+=1
                _d.update({_n:_p})               
             else: # One noise
                if(math.fabs(Ex0 - Ey0) < math.fabs(Ex0 - Ey1)) and (math.fabs(Ex0 - Ey0) < enums.DeltaEnergy):
                   _p = setphoton((_clu.energy_p+_clu.Lv1hit_y[_clu.Lv1index_y[0]].energy)*0.5,_clu.energy_p, _clu.Lv1hit_y[_clu.Lv1index_y[0]].energy, _clu.adc_p, _clu.Lv1hit_y[_clu.Lv1index_y[0]].adc, _clu.x, _clu.Lv1hit_y[_clu.Lv1index_y[0]].position, 2)
                   _n+=1
                   _d.update({_n:_p})
                if (math.fabs(Ex0 - Ey1) < math.fabs(Ex0 - Ey1)) and (math.fabs(Ex0 - Ey1) < enums.DeltaEnergy):
                   _p = setphoton((_clu.energy_p+_clu.Lv1hit_y[_clu.Lv1index_y[1]].energy)*0.5,_clu.energy_p, _clu.Lv1hit_y[_clu.Lv1index_y[1]].energy, _clu.adc_p, _clu.Lv1hit_y[_clu.Lv1index_y[1]].adc, _clu.x, _clu.Lv1hit_y[_clu.Lv1index_y[1]].position, 2)
                   _n+=1
                   _d.update({_n:_p})
          return _d

      def get2and1(self,_clu,Re):
          _d={}
          _n=0
          if (_clu.nstrips_x == 2 and _clu.nstrips_y == 1) or Re:
             Ex0 = _clu.Lv1hit_x[_clu.Lv1index_x[0]].energy
             Ex1 = _clu.Lv1hit_x[_clu.Lv1index_x[1]].energy
             Ey0 = _clu.Lv1hit_y[_clu.Lv1index_y[0]].energy
             if( math.fabs(Ey0 - (Ex0+Ex1)) < enums.DeltaEnergy):
                _p = setphoton(Ex0, Ex0, Ey0*Ex0/(Ex0+Ex1), _clu.Lv1hit_x[_clu.Lv1index_x[0]].adc, _clu.adc_n*Ex0/(Ex0+Ex1), _clu.Lv1hit_x[_clu.Lv1index_x[0]].position, _clu.y, 3) 
                _n+=1
                _d.update({_n:_p})

                _p = setphoton(Ex1, Ex1, Ey0*Ex1/(Ex0+Ex1), _clu.Lv1hit_x[_clu.Lv1index_x[1]].adc, _clu.adc_n*Ex1/(Ex0+Ex1), _clu.Lv1hit_x[_clu.Lv1index_x[1]].position, _clu.y, 3) 
                _n+=1
                _d.update({_n:_p})               
             else: 
                if(math.fabs(Ey0 - Ex0) < math.fabs(Ey0 - Ex1)) and (math.fabs(Ey0 - Ex0) < enums.DeltaEnergy):
                   _p = setphoton((_clu.Lv1hit_x[_clu.Lv1index_x[0]].energy+Ey0)*0.5, _clu.Lv1hit_x[_clu.Lv1index_x[0]].energy, Ey0, _clu.Lv1hit_x[_clu.Lv1index_x[0]].adc, _clu.adc_n, _clu.Lv1hit_x[_clu.Lv1index_x[0]].position, _clu.y, 3)
                   _n+=1
                   _d.update({_n:_p})
                if (math.fabs(Ey0 - Ex1) < math.fabs(Ey0 - Ex1)) and (math.fabs(Ey0 - Ex1) < enums.DeltaEnergy):
                   _p = setphoton((_clu.Lv1hit_x[_clu.Lv1index_x[1]].energy+Ey0)*0.5, _clu.Lv1hit_x[_clu.Lv1index_x[1]].energy, Ey0, _clu.Lv1hit_x[_clu.Lv1index_x[1]].adc, _clu.adc_n, _clu.Lv1hit_x[_clu.Lv1index_x[1]].position, _clu.y, 3)
                   _n+=1
                   _d.update({_n:_p})
          return _d

      def get2and2(self,_clu):
          _d={}
          _n=0
          if _clu.nstrips_x == 2 and _clu.nstrips_y == 2:
             Ex0 = _clu.Lv1hit_x[_clu.Lv1index_x[0]].energy
             Ex1 = _clu.Lv1hit_x[_clu.Lv1index_x[1]].energy
             Ey0 = _clu.Lv1hit_y[_clu.Lv1index_y[0]].energy
             Ey1 = _clu.Lv1hit_y[_clu.Lv1index_y[1]].energy
             if(math.fabs(Ex0+Ex1-Ey0-Ey1)  < enums.DeltaEnergy ):#four photons
                if(math.fabs(Ex0-Ey0) < enums.DeltaEnergy) and (math.fabs(Ex1-Ey1) < enums.DeltaEnergy):
                   _p = setphoton(_clu.Lv1hit_x[_clu.Lv1index_x[0]].energy ,_clu.Lv1hit_x[_clu.Lv1index_x[0]].energy, _clu.Lv1hit_y[_clu.Lv1index_y[0]].energy, _clu.Lv1hit_x[_clu.Lv1index_x[0]].adc, _clu.Lv1hit_y[_clu.Lv1index_y[0]].adc, _clu.Lv1hit_x[_clu.Lv1index_x[0]].position, _clu.Lv1hit_y[_clu.Lv1index_y[0]].position, 4)
                   _n+=1
                   _d.update({_n:_p})
                   _p = setphoton(_clu.Lv1hit_x[_clu.Lv1index_x[1]].energy, _clu.Lv1hit_x[_clu.Lv1index_x[1]].energy, _clu.Lv1hit_y[_clu.Lv1index_y[1]].energy, _clu.Lv1hit_x[_clu.Lv1index_x[1]].adc, _clu.Lv1hit_y[_clu.Lv1index_y[1]].adc, _clu.Lv1hit_x[_clu.Lv1index_x[1]].position, _clu.Lv1hit_y[_clu.Lv1index_y[1]].position, 4)
                   _n+=1
                   _d.update({_n:_p})
                elif (math.fabs(Ex0-Ey1) < enums.DeltaEnergy) and (math.fabs(Ex1-Ey0) < enums.DeltaEnergy):
                   _p = setphoton(_clu.Lv1hit_x[_clu.Lv1index_x[0]].energy, _clu.Lv1hit_x[_clu.Lv1index_x[0]].energy, _clu.Lv1hit_y[_clu.Lv1index_y[1]].energy, _clu.Lv1hit_x[_clu.Lv1index_x[0]].adc, _clu.Lv1hit_y[_clu.Lv1index_y[1]].adc, _clu.Lv1hit_x[_clu.Lv1index_x[0]].position, _clu.Lv1hit_y[_clu.Lv1index_y[1]].position, 4)
                   _n+=1
                   _d.update({_n:_p})
                   _p = setphoton(_clu.Lv1hit_x[_clu.Lv1index_x[1]].energy, _clu.Lv1hit_x[_clu.Lv1index_x[1]].energy, _clu.Lv1hit_y[_clu.Lv1index_y[0]].energy, _clu.Lv1hit_x[_clu.Lv1index_x[1]].adc, _clu.Lv1hit_y[_clu.Lv1index_y[0]].adc, _clu.Lv1hit_x[_clu.Lv1index_x[1]].position, _clu.Lv1hit_y[_clu.Lv1index_y[0]].position, 4)
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
                      _p = setphoton((_clu.Lv1hit_x[_clu.Lv1index_x[i]].energy+_clu.Lv1hit_y[_clu.Lv1index_y[j]].energy)*0.5,_clu.Lv1hit_x[_clu.Lv1index_x[i]].energy, _clu.Lv1hit_y[_clu.Lv1index_y[j]].energy, _clu.Lv1hit_x[_clu.Lv1index_x[i]].adc, _clu.Lv1hit_y[_clu.Lv1index_y[j]].adc, _clu.Lv1hit_x[_clu.Lv1index_x[i]].position, _clu.Lv1hit_y[_clu.Lv1index_y[j]].position, 5)
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


class EventCategory():
      def __init__(self, hitx=None, hity=None, deltae=None, response=None):
          # category for single cluster
          self.hitx = hitx 
          self.hity = hity
          self.DeltaEnergy = enums.DeltaEnergy
          if deltae is not None: self.DeltaEnergy = deltae
          self.response_dic = response # check tran.py for the order of list 
          self.case1, self.case2, self.case3, self.case4, self.case5 = None, None, None, None, None

          self.GetCategory(self.hitx, self.hity)
          self.photon_list = self.SumCategories()

      def GetCategory(self, _xlist, _ylist):         
          if len(_xlist) == 1 and len(_ylist) == 1:
             self.case1 = self.get1and1(_xlist[1], _ylist[1])
          elif len(_xlist) == 1 and len(_ylist) == 2:
             self.case2 = self.get1and2(_xlist[1], _ylist[1], _ylist[2])
          elif len(_xlist) == 2 and len(_ylist) == 1:
             self.case3 = self.get2and1(_xlist[1], _xlist[2], _ylist[1])
          elif len(_xlist) == 2 and len(_ylist) == 2:
             self.case4 = self.get2and2(_xlist[1], _xlist[2], _ylist[1], _ylist[2])
          elif len(_xlist) > 2 or len(_ylist) > 2:
             self.case5 = self.getother(_xlist,_ylist)

      def SumCategories(self):
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

      def energy_correction_1d(self, _hitp, _hitn):
          bin_range=0.2
          epi1=(_hitp.energy+_hitn.energy)/2
          epi2=(_hitp.energy-_hitn.energy)/2
          if epi2 < -30: epi2 = -30
          if epi2 > 5: epi2 = 4.9
          _response=self.response_dic[int((epi2+30)*(1/bin_range))]
          _e_corr=_response.Eval(epi1)
          return _e_corr          
 
      def energy_correction(self, _hitp, _hitn):
#          if _hitp.nstrips > 4: _hitp.nstrips = 4
#          if _hitn.nstrips > 4: _hitn.nstrips = 4
          #TODO need to be fixed
          _hitp.nstrips, _hitn.nstrips =1,1
          _name="p"+str(_hitp.nstrips)+"n"+str(_hitn.nstrips)
          if not self.response_dic.get(_name): _name="p"+str(4)+"n"+str(3)
          _response=self.response_dic[_name]
          epi1=(_hitp.energy+_hitn.energy)/2 # === epi1 is (e_pt+e_al)/2 ===
          epi2=(_hitp.energy-_hitn.energy)/2 # === epi2 is (e_pt-e_al)/2 ===
          #TODO need to be fixed
          _e_corr=_response.Interpolate(epi1,epi2) #watanabe method
#          if _e_corr == 0:
#             _e_corr = (_hitp.energy+_hitn.energy)*0.5
#             print("epi1 : ", epi1 , " epi2 : ", epi2 , " n,p = ", _hitp.nstrips," ", _hitn.nstrips)
#             print("p : ", _hitp.energy)
#             print("n : ", _hitn.energy)

#          _ratio=epi2/_e_corr
          return _e_corr

      def get1and1(self, _x0, _y0, _type=None):
          if _type is None: _t = 1
          else: _t = _type
          _d, _n={}, 0
          #_e_corr=self.energy_correction(_x0,_y0)
          _e_corr=self.energy_correction_1d(_x0,_y0)
          _p = setphoton(_e_corr, _x0.energy,_y0.energy,_x0.adc,_y0.adc,_x0.position,_y0.position,_t)
          #_p = setphoton((_x0.energy+_y0.energy)*0.5, _x0.energy,_y0.energy,_x0.adc,_y0.adc,_x0.position,_y0.position,_t)
          _n+=1
          _d.update({_n:_p})
          return _d

      def get1and2(self, _x0, _y0, _y1, _type=None):
          if _type is None: _t = 2
          else: _t = _type
          _d, _n={}, 0
          Ex0, Ey0, Ey1 = _x0.energy, _y0.energy, _y1.energy
          if( math.fabs(Ex0 - (Ey0+Ey1)) <= self.DeltaEnergy): # Two photons
             _p = setphoton(Ey0, Ex0*Ey0/(Ey0+Ey1), Ey0, _x0.adc*Ey0/(Ey0+Ey1), _y0.adc, _x0.position, _y0.position, _t)
             _n+=1
             _d.update({_n:_p})
             _p = setphoton(Ey1, Ex0*Ey1/(Ey0+Ey1), Ey1, _x0.adc*Ey1/(Ey0+Ey1), _y1.adc, _x0.position, _y1.position, _t)
             _n+=1
             _d.update({_n:_p})               
          else: # One noise
             if(math.fabs(Ex0 - Ey0) < math.fabs(Ex0 - Ey1)) and (math.fabs(Ex0 - Ey0) <= self.DeltaEnergy):
                _d = self.get1and1(_x0, _y0, 2)
             if (math.fabs(Ex0 - Ey0) > math.fabs(Ex0 - Ey1)) and (math.fabs(Ex0 - Ey1) <= self.DeltaEnergy):
                _d = self.get1and1(_x0, _y1, 2)
          return _d
                        
      def get2and1(self, _x0, _x1, _y0, _type=None):
          if _type is None: _t = 3
          else: _t = _type
          _d, _n={}, 0
          Ex0, Ex1, Ey0 = _x0.energy, _x1.energy, _y0.energy
          if( math.fabs(Ey0 - (Ex0+Ex1)) <= self.DeltaEnergy):
             _p = setphoton(Ex0, Ex0, Ey0*Ex0/(Ex0+Ex1), _x0.adc, _y0.adc*Ex0/(Ex0+Ex1), _x0.position, _y0.position, _t) 
             _n+=1
             _d.update({_n:_p})

             _p = setphoton(Ex1, Ex1, Ey0*Ex1/(Ex0+Ex1), _x1.adc, _y0.adc*Ex1/(Ex0+Ex1), _x1.position, _y0.position, _t) 
             _n+=1
             _d.update({_n:_p})               
          else: 
             if(math.fabs(Ey0 - Ex0) < math.fabs(Ey0 - Ex1)) and (math.fabs(Ey0 - Ex0) <= self.DeltaEnergy):
                _d = self.get1and1(_x0, _y0, 3)
             if (math.fabs(Ey0 - Ex0) > math.fabs(Ey0 - Ex1)) and (math.fabs(Ey0 - Ex1) <= self.DeltaEnergy):
                _d = self.get1and1(_x1, _y0, 3)
          return _d

      def get2and2(self, _x0, _x1, _y0, _y1, _type=None):
          if _type is None: _t = 4
          else: _t = _type
          _d, _n={}, 0
          Ex0, Ex1, Ey0, Ey1 = _x0.energy, _x1.energy, _y0.energy, _y1.energy
          if(math.fabs(Ex0+Ex1-Ey0-Ey1)  <= self.DeltaEnergy ):#two photons
             if(math.fabs(Ex0-Ey0) <= self.DeltaEnergy) and (math.fabs(Ex1-Ey1) <= self.DeltaEnergy):
                _p = setphoton(_x0.energy, _x0.energy, _y0.energy, _x0.adc, _y0.adc, _x0.position, _y0.position, _t)
                _n+=1
                _d.update({_n:_p})
                _p = setphoton(_x1.energy, _x1.energy, _y1.energy, _x1.adc, _y1.adc, _x1.position, _y1.position, _t)
                _n+=1
                _d.update({_n:_p})
             elif (math.fabs(Ex0-Ey1) <= self.DeltaEnergy) and (math.fabs(Ex1-Ey0) <= self.DeltaEnergy):
                _p = setphoton(_x0.energy, _x0.energy, _y1.energy, _x0.adc, _y1.adc, _x0.position, _y1.position, _t)
                _n+=1
                _d.update({_n:_p})
                _p = setphoton(_x1.energy, _x1.energy, _y0.energy, _x1.adc, _y0.adc, _x1.position, _y0.position, _t)
                _n+=1
                _d.update({_n:_p})
          elif ((Ey0+Ey1) > (Ex0+Ex1)):# one noise in y-side -> return case3 (2*1)
             if  (((Ex0+Ex1) - Ey0) <= self.DeltaEnergy):                   
                _d = self.get2and1(_x0,_x1,_y0, 4)
             elif (((Ex0+Ex1) - Ey1) <= self.DeltaEnergy):
                _d = self.get2and1(_x0,_x1,_y1, 4)
          else:# one noise in x-side -> return case2 (1*2)
             if  (((Ey0+Ey1) - Ex0) <= self.DeltaEnergy):
                _d = self.get1and2(_x0,_y0,_y1, 4)
             elif (((Ey0+Ey1) - Ex1) <= self.DeltaEnergy):
                _d = self.get1and2(_x1,_y0,_y1, 4)
          return _d

      def getother(self, _xlist, _ylist, _type=None):
          if _type is None: _t = 5
          else: _t = _type
          _d, _n, point={}, 0, 0
          maxpoint=min(len(_xlist),len(_ylist))
          xElist, yElist = setEnergyindex(_xlist), setEnergyindex(_ylist)
          for i in range(maxpoint):
             xi, Ex = xElist[i]
             yi, Ey = yElist[i]
             xhit, yhit = _xlist[xi], _ylist[yi]
             if math.fabs(Ex-Ey) <= self.DeltaEnergy:
                _p = setphoton((xhit.energy+yhit.energy)*0.5, xhit.energy, yhit.energy, xhit.adc, yhit.adc, xhit.position, yhit.position, _t)
                _n+=1
                _d.update({_n:_p})
          return _d

def setEnergyindex(hitlv2):
    lv2Elist={}
    for _hit in hitlv2:
       lv2Elist.update({_hit:hitlv2[_hit].energy})
    return sorted(lv2Elist.items(), key=lambda d: d[1], reverse=True)

def setphoton(_e,ep,en,adcp,adcn,x,y,case):
    _p = hitphoton()
    _p.energy  = _e
    _p.energy_p  = ep
    _p.energy_n  = en
    _p.adc_p     = adcp
    _p.adc_n     = adcn
    _p.x         = x
    _p.y         = y
    _p.type      = case
    return _p
          
