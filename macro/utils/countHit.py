#!/usr/bin/env python    
#-*- coding:utf-8 -*-   
"""
This module provides the hit selection.
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
import math
from multiprocessing import Pool, cpu_count
from array import array
from random import gauss
import numpy as np
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/macro/utils/')
from hits import hitchannel, hitphoton
from cat import Category 
import heapq 
import enums
import time

def SetWeight(adcx, adcy, a, b):
    # ============ find hit point of photon (2D) ===========
#    if(math.fabs(adcy - (adcx*a + b))) > 5 : return False
#    return True
    return math.fabs(adcy - (adcx*a + b))

def SelectEnergy(_ex, _ey):
    if math.fabs(_ex-_ey) > 10: return False
    return True

def isAdjacent(i, _hit):
    if (i-1) is 0 : return False # first
#    if(_hit[i].energy + _hit[i-1].energy) > enums.MaxSumRange : return False # over Si max range
#    if _hit[i].energy > enums.SiEnergyRange and math.fabs(_hit[i].energy - _hit[i-1].energy) < enums.DeltaNoise : return False # same noise
    if _hit[i].channel - _hit[i-1].channel is 1 : return True
    else: return False

def reset(index, _lv1hit, nad, _mhit):
    energy, adc = 0., 0.
    for i in range(nad+1):
       energy += _lv1hit[index-i].energy
       adc += _lv1hit[index-i].adc
    _mhit.energy, _mhit.adc = energy, adc

    if nad is 1:  
       if _lv1hit[index].energy > _lv1hit[index -1].energy: _mhit.channel, _mhit.position = _lv1hit[index].channel, _lv1hit[index].position
       else: _mhit.channel, _mhit.position = _lv1hit[index].channel, _lv1hit[index].position
    else:
       dic = {}
       for i in range(nad+1):
           new_index = index-i 
           dic.update({new_index:_lv1hit[new_index].energy})
       _index = heapq.nlargest(1,dic)
       _mhit.channel, _mhit.position = _lv1hit[_index[0]].channel, _lv1hit[_index[0]].position

    _mhit.Lv1hit = _lv1hit 
    _mhit.Lv1index = [index - _n for _n in range(nad+1)]
    _mhit.nstrips = nad+1
    return _mhit
          
def Level2Hit(_hitx, _hity):  
    merge_xhit, merge_yhit = {}, {}
    merge_nx, merge_ny = {}, {}
    m_nx, m_ny = 0, 0  #id 
    n_adx, n_ady = 0, 0 #nstrips

    for ix in range(1, 1+len(_hitx)):
       if(isAdjacent(ix, _hitx)):
          #update hit info. due to adjacent channels
          n_adx += 1
          _newmergehit = hitchannel()
          _newmergehit = reset(ix, _hitx, n_adx, _newmergehit)
          merge_xhit.update({m_nx:_newmergehit})
       else:
          n_adx = 0
          m_nx += 1
          _hitx[ix].Lv1hit = _hitx
          _hitx[ix].Lv1index = [ix]
          _hitx[ix].nstrips = n_adx+1
          merge_xhit.update({m_nx:_hitx[ix]})   
    for iy in range(1, 1+len(_hity)):
       if(isAdjacent(iy, _hity)):
          n_ady += 1
          _newmergehit = hitchannel()
          _newmergehit = reset(iy, _hity, n_ady, _newmergehit)
          merge_yhit.update({m_ny:_newmergehit})
       else:
          n_ady = 0
          m_ny += 1
          _hity[iy].Lv1hit = _hity
          _hity[iy].Lv1index = [iy]
          _hity[iy].nstrips = n_ady+1
          merge_yhit.update({m_ny:_hity[iy]})
    
    return merge_xhit, merge_yhit

def findpoint(_hitx_lv2, _hity_lv2):
    point_list = {}
    _nhit = 0
    for ix in range(1, 1+len(_hitx_lv2)):
       for iy in range(1, 1+len(_hity_lv2)):
          _nhit += 1
          delta_energy = math.fabs(_hitx_lv2[ix].energy - _hity_lv2[iy].energy)
          point_list.update({_nhit:SetphotonInfo(_nhit, _hitx_lv2[ix], _hity_lv2[iy], delta_energy)})
    return point_list                          

def matchhit(_nx, _ny, _p):   
    list_signal = {}
    dic = {}
    _nhit = 0#number of real photons

    for _ip in range(1,len(_p)+1):
       c = Category(point=_p[_ip]) # category for one cluster
       single_dic = c.hit
       for _s in single_dic:#one cluster might has several reco. photon
          _nhit += 1
          list_signal.update({_nhit:single_dic[_s]})

     # === simple Delta E selection ===
#    for ip in range(1, 1+len(_p)):
#       dic.update({ip:_p[ip].deltaE})
#    maxpoint = min(_nx, _ny)
#    _id = heapq.nsmallest(maxpoint,dic)
#    for _ip in _id:
#       if _p[_ip].deltaE > 10: continue#drop photon with large deltaE
#       _nhit += 1
#       list_signal.update({_nhit:_p[_ip]})

    return list_signal

def SetphotonInfo(index, _x, _y, _delta):
    _signal = hitphoton()     
    _signal.index = index
    _signal.energy_p = _x.energy
    _signal.energy_n = _y.energy
    _signal.adc_p = _x.adc
    _signal.adc_n = _y.adc
    _signal.x = _x.position
    _signal.y = _y.position
    _signal.nstrips_x = _x.nstrips
    _signal.nstrips_y = _y.nstrips
    _signal.deltaE = _delta
    _signal.Lv1index_x = _x.Lv1index
    _signal.Lv1index_y = _y.Lv1index
    _signal.Lv1hit_x = _x.Lv1hit
    _signal.Lv1hit_y = _y.Lv1hit
    return _signal 

def SetHitInfo(index, adc, energy, poi, ch, asic):
    _hit = hitchannel()
    _hit.index = index
    _hit.adc = adc
    _hit.energy = energy
    _hit.position = poi
    _hit.channel = ch
    _hit.asic = asic
    return _hit    

def Level1Hit(rawdata_list, Eline, dblist):
    # TODO merge GetEventTree in here 
    n_hit_x = 0
    n_hit_y = 0
    signalx, signaly = {}, {}
    # ========= find signal region (p-side and n-side) ============
    for i_data in rawdata_list:
       if i_data.adcm < i_data.adccut: continue
       if i_data.adc > i_data.upperbound: continue

       if i_data.detid is 0: 
          n_hit_x += 1
          energy = Eline[i_data.stripid].Eval(i_data.adcm)
          poi = dblist[i_data.stripid].posx
          signalx.update({n_hit_x:SetHitInfo(n_hit_x, i_data.adcm, energy, poi, i_data.stripid, i_data.asicid)})
       else:
          n_hit_y += 1
          energy = Eline[i_data.stripid].Eval(i_data.adcm)
          poi = dblist[i_data.stripid].posy
          signaly.update({n_hit_y:SetHitInfo(n_hit_y, i_data.adcm, energy, poi, i_data.stripid, i_data.asicid)})
    return signalx, signaly
        
def Level1Hit_Shima1(tree, adccut, coef_R, dblist, eline):
    adc_hitcut = 1000
    n_hit_x = 0
    n_hit_y = 0
    signalx, signaly = {}, {}

    # ========= find signal region (p-side and n-side) ============
    for iasic in range(8): 
       for ch in range(32):
          if iasic is 0:
             if ((tree.adc0[ch*2] - tree.cmn0) > adccut[ch+iasic*32]) and (tree.adc0[ch*2] < adc_hitcut):
                n_hit_x += 1 #hit !
                adc = tree.adc0[ch*2]-tree.cmn0 + coef_R * random.uniform(-0.5,0.5)
                energy = eline[ch+iasic*32].Eval(adc)
#                energy = dblist[ch+iasic*32].calfunc.Eval(adc)
                poi = dblist[ch+iasic*32].posx
                signal_hitx = SetHitInfo(n_hit_x, adc, energy, poi, ch + iasic*32, iasic)
                signalx.update({n_hit_x:signal_hitx})               
          elif iasic is 1: 
             if ((tree.adc1[ch*2] - tree.cmn1) > adccut[ch+iasic*32]) and (tree.adc1[ch*2] < adc_hitcut):
                n_hit_x += 1
                adc = tree.adc1[ch*2]-tree.cmn1 + coef_R * random.uniform(-0.5,0.5) 
                energy = eline[ch+iasic*32].Eval(adc)
#                energy = dblist[ch+iasic*32].calfunc.Eval(adc)
                poi = dblist[ch+iasic*32].posx
                signal_hitx = SetHitInfo(n_hit_x, adc, energy, poi, ch + 32*iasic, iasic)
                signalx.update({n_hit_x:signal_hitx})               
          elif iasic is 2: 
             if ((tree.adc2[ch*2] - tree.cmn2) > adccut[ch+iasic*32]) and (tree.adc2[ch*2] < adc_hitcut): 
                n_hit_x += 1
                adc = tree.adc2[ch*2]-tree.cmn2 + coef_R * random.uniform(-0.5,0.5) 
                energy = eline[ch+iasic*32].Eval(adc)
#                energy = dblist[ch+iasic*32].calfunc.Eval(adc)
                poi = dblist[ch+iasic*32].posx
                signal_hitx = SetHitInfo(n_hit_x, adc, energy, poi, ch + 32*iasic, iasic)
                signalx.update({n_hit_x:signal_hitx})               
          elif iasic is 3: 
             if ((tree.adc3[ch*2] - tree.cmn3) > adccut[ch+iasic*32]) and (tree.adc3[ch*2] < adc_hitcut):
                n_hit_x += 1
                adc = tree.adc3[ch*2]-tree.cmn3 + coef_R * random.uniform(-0.5,0.5) 
                energy = eline[ch+iasic*32].Eval(adc)
#                energy = dblist[ch+iasic*32].calfunc.Eval(adc)
                poi = dblist[ch+iasic*32].posx
                signal_hitx = SetHitInfo(n_hit_x, adc, energy, poi, ch + 32*iasic, iasic)
                signalx.update({n_hit_x:signal_hitx})               
          elif iasic is 4: 
             if ((tree.adc4[ch*2] - tree.cmn4) > adccut[ch+iasic*32]) and (tree.adc4[ch*2] < adc_hitcut):
                n_hit_y += 1
                adc = tree.adc4[ch*2]-tree.cmn4 + coef_R * random.uniform(-0.5,0.5) 
                energy = eline[ch+iasic*32].Eval(adc)
#                energy = dblist[ch+iasic*32].calfunc.Eval(adc)
                poi = dblist[ch+iasic*32].posy
                signal_hity = SetHitInfo(n_hit_y, adc, energy, poi, (ch + 32*iasic), iasic)
                signaly.update({n_hit_y:signal_hity})               
          elif iasic is 5: 
             if ((tree.adc5[ch*2] - tree.cmn5) > adccut[ch+iasic*32]) and (tree.adc5[ch*2] < adc_hitcut): 
                n_hit_y += 1
                adc = tree.adc5[ch*2]-tree.cmn5 + coef_R * random.uniform(-0.5,0.5) # save adc
#                energy = dblist[ch+iasic*32].calfunc.Eval(adc)
                energy = eline[ch+iasic*32].Eval(adc)
                poi = dblist[ch+iasic*32].posy
                signal_hity = SetHitInfo(n_hit_y, adc, energy, poi, (ch + 32*iasic), iasic)
                signaly.update({n_hit_y:signal_hity})               
          elif iasic is 6: 
             if ((tree.adc6[ch*2] - tree.cmn6) > adccut[ch+iasic*32]) and (tree.adc6[ch*2] < adc_hitcut): 
                n_hit_y += 1
                adc = tree.adc6[ch*2]-tree.cmn6 + coef_R * random.uniform(-0.5,0.5) # save adc
#                energy = dblist[ch+iasic*32].calfunc.Eval(adc)
                energy = eline[ch+iasic*32].Eval(adc)
                poi = dblist[ch+iasic*32].posy
                signal_hity = SetHitInfo(n_hit_y, adc, energy, poi, (ch + 32*iasic), iasic)
                signaly.update({n_hit_y:signal_hity})               
          elif iasic is 7: 
             if ((tree.adc7[ch*2] - tree.cmn7) > adccut[ch+iasic*32]) and (tree.adc7[ch*2] < adc_hitcut): 
                n_hit_y += 1
                adc = tree.adc7[ch*2]-tree.cmn7 + coef_R * random.uniform(-0.5,0.5) # save adc
#                energy = dblist[ch+iasic*32].calfunc.Eval(adc)
                energy = eline[ch+iasic*32].Eval(adc)
                poi = dblist[ch+iasic*32].posy
                signal_hity = SetHitInfo(n_hit_y, adc, energy, poi, (ch + 32*iasic), iasic)
                signaly.update({n_hit_y:signal_hity})               
      
    return signalx, signaly
        
