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
from hits import level1hitchannel, hitphoton
import heapq 
import enums

def SetWeight(adcx, adcy, a, b):
    # ============ find hit point of photon (2D) ===========
#    if(math.fabs(adcy - (adcx*a + b))) > 5 : return False
#    return True
    return math.fabs(adcy - (adcx*a + b))

def isAdjacent(i, _hit):
    if (i-1) is 0 : return False # first
    if(_hit[i].energy + _hit[i-1].energy) > enums.MaxSumRange : return False # over Si max range
    if _hit[i].energy > enums.SiEnergyRange and math.fabs(_hit[i].energy - _hit[i-1].energy) < enums.DeltaNoise : return False # same noise
    if _hit[i].channel - _hit[i-1].channel is 1 : return True
    else: return False

def resetPosition(index ,_lv1hit, flag):
    if flag is 1:  
       if _lv1hit[index].energy > _lv1hit[index -1].energy: return _lv1hit[index].channel, _lv1hit[index].position
       else: return _lv1hit[index-1].channel, _lv1hit[index-1].position      
    else:
       dic = {}
       for i in range(flag+1):
           new_index = index-i 
           dic.update({new_index:_lv1hit[new_index].energy})
       _index = heapq.nlargest(1,dic)
       return _lv1hit[_index[0]].channel, _lv1hit[_index[0]].position

def resetEnergyADC(index ,_lv1hit, nad):
    energy = 0
    adc = 0
    for i in range(nad+1):
       energy += _lv1hit[index-i].energy
       adc += _lv1hit[index-i].adc
    return energy, adc
          
def Level2Hit(_hitx, _hity):  
    # merge 
    merge_xhit, merge_yhit = {}, {}
    merge_nx, merge_ny = {}, {}
    m_nx, m_ny = 0, 0   
    n_adx, n_ady = 0, 0
    
    for ix in range(1, 1+len(_hitx)):
       if(isAdjacent(ix, _hitx)):
          n_adx += 1
          _newmergehit = level1hitchannel()
          _newmergehit.energy, _newmergehit.adc = resetEnergyADC(ix, _hitx, n_adx)
          _newmergehit.channel, _newmergehit.position = resetPosition(ix, _hitx, n_adx)
          merge_xhit.update({m_nx:_newmergehit})
          merge_nx.update({m_nx:n_adx})
       else:
          n_adx = 0
          m_nx += 1
          merge_xhit.update({m_nx:_hitx[ix]})   
          merge_nx.update({m_nx:n_adx})
    for iy in range(1, 1+len(_hity)):
       if(isAdjacent(iy, _hity)):
          n_ady += 1
          _newmergehit = level1hitchannel()
          _newmergehit.channel, _newmergehit.position = resetPosition(iy, _hity, n_ady)
          _newmergehit.energy, _newmergehit.adc = resetEnergyADC(iy, _hity, n_ady)
          merge_yhit.update({m_ny:_newmergehit})
          merge_ny.update({m_ny:n_ady})
       else:
          n_ady = 0
          m_ny += 1
          merge_yhit.update({m_ny:_hity[iy]})
          merge_ny.update({m_ny:n_ady})
    
    return merge_xhit, merge_yhit, merge_nx, merge_ny

def findpoint(_hitx_lv2, _hity_lv2, _mhitx, _mhity):
    point_list = {}
    _nhit = 0
    for ix in range(1, 1+len(_hitx_lv2)):
       for iy in range(1, 1+len(_hity_lv2)):
          _nhit += 1
          delta_energy = math.fabs(_hitx_lv2[ix].energy - _hity_lv2[iy].energy)
          point_list.update({_nhit:SetphotonInfo(_nhit, _hitx_lv2[ix].energy, _hity_lv2[iy].energy, _hitx_lv2[ix].adc, _hity_lv2[iy].adc, _hitx_lv2[ix].position, _hity_lv2[iy].position, delta_energy, _mhitx[ix], _mhity[iy])})
    return point_list                          

def matchhit(_nx, _ny, _p):   
    list_signal = {}
    dic = {}

    for ip in range(1, 1+len(_p)):
       dic.update({ip:_p[ip].deltaE})

    maxpoint = min(_nx, _ny)
    _id = heapq.nlargest(maxpoint,dic)
    _nhit = 0#number of real photons

    for _ip in _id:
       if _p[_ip].deltaE > 10: continue#drop photon with large deltaE
       _nhit += 1
       list_signal.update({_nhit:_p[_ip]})

    return list_signal

def SetphotonInfo(index, _ep, _en, _ap, _an, _x, _y, _delta, _nx, _ny):
    _signal = hitphoton()     
    _signal.index = index
    _signal.energy_p = _ep
    _signal.energy_n = _en
    _signal.adc_p = _ap
    _signal.adc_n = _an
    _signal.x = _x
    _signal.y = _y
    _signal.mergehit_x = _nx
    _signal.mergehit_y = _ny
    _signal.deltaE = _delta
    return _signal 

def SetHitInfo(index, adc, energy, poi, ch, asic):
    _hit = level1hitchannel()
    _hit.index = index
    _hit.adc = adc
    _hit.energy = energy
    _hit.position = poi
    _hit.channel = ch
    _hit.asic = asic
    return _hit    

def Level1Hit(tree, Eline, adccut_p, adccut_n, coef_R):
    adc_hitcut = 1000
    n_hit_x = 0
    n_hit_y = 0
    signalx, signaly = {}, {}
    # ========= find signal region (p-side and n-side) ============
    for iasic in range(4): 
       for ch in range(32):
          if iasic is 0 and ((tree.adc0[ch] - tree.cmn0) > adccut_p[ch+iasic*32]) and (tree.adc0[ch] < adc_hitcut): 
             n_hit_x += 1 #hit !
             adc_p = tree.adc0[ch]-tree.cmn0 + coef_R * random.uniform(-0.5,0.5)
             energy_p = Eline[ch + 32*iasic].Eval(adc_p)
             poi_p = (ch+iasic*32)
             signal_hitx = SetHitInfo(n_hit_x, adc_p, energy_p, poi_p, ch + 32*iasic, iasic)
             signalx.update({n_hit_x:signal_hitx})               
          if iasic is 1 and ((tree.adc1[ch] - tree.cmn1) > adccut_p[ch+iasic*32]) and (tree.adc1[ch] < adc_hitcut): 
             n_hit_x += 1
             adc_p = tree.adc1[ch]-tree.cmn1 + coef_R * random.uniform(-0.5,0.5) 
             energy_p = Eline[ch + 32*iasic].Eval(adc_p)
             poi_p = (ch+iasic*32)
             signal_hitx = SetHitInfo(n_hit_x, adc_p, energy_p, poi_p, ch + 32*iasic, iasic)
             signalx.update({n_hit_x:signal_hitx})               
          if iasic is 2 and ((tree.adc2[ch] - tree.cmn2) > adccut_p[ch+iasic*32]) and (tree.adc2[ch] < adc_hitcut): 
             n_hit_x += 1
             adc_p = tree.adc2[ch]-tree.cmn2 + coef_R * random.uniform(-0.5,0.5) 
             energy_p = Eline[ch + 32*iasic].Eval(adc_p)
             poi_p = (ch+iasic*32)
             signal_hitx = SetHitInfo(n_hit_x, adc_p, energy_p, poi_p, ch + 32*iasic, iasic)
             signalx.update({n_hit_x:signal_hitx})               
          if iasic is 3 and ((tree.adc3[ch] - tree.cmn3) > adccut_p[ch+iasic*32]) and (tree.adc3[ch] < adc_hitcut): 
             n_hit_x += 1
             adc_p = tree.adc3[ch]-tree.cmn3 + coef_R * random.uniform(-0.5,0.5) 
             energy_p = Eline[ch + 32*iasic].Eval(adc_p)
             poi_p = (ch+iasic*32)
             signal_hitx = SetHitInfo(n_hit_x, adc_p, energy_p, poi_p, ch + 32*iasic, iasic)
             signalx.update({n_hit_x:signal_hitx})               

          if iasic is 0 and ((tree.adc4[ch] - tree.cmn4) > adccut_n[ch+iasic*32]) and (tree.adc4[ch] < adc_hitcut): 
             n_hit_y += 1
             adc_n = tree.adc4[ch]-tree.cmn4 + coef_R * random.uniform(-0.5,0.5) 
             energy_n = Eline[ch + 32*iasic+128].Eval(adc_n)
             poi_n = 128-((32-ch)+iasic*32)
             signal_hity = SetHitInfo(n_hit_y, adc_n, energy_n, poi_n, (ch + 32*iasic+128), iasic)
             signaly.update({n_hit_y:signal_hity})               
          if iasic is 1 and ((tree.adc5[ch] - tree.cmn5) > adccut_n[ch+iasic*32]) and (tree.adc5[ch] < adc_hitcut): 
             n_hit_y += 1
             adc_n = tree.adc5[ch]-tree.cmn5 + coef_R * random.uniform(-0.5,0.5) # save adc
             energy_n = Eline[ch + 32*iasic+128].Eval(adc_n)
             poi_n = 128-((32-ch)+iasic*32)
             signal_hity = SetHitInfo(n_hit_y, adc_n, energy_n, poi_n, (ch + 32*iasic+128), iasic)
             signaly.update({n_hit_y:signal_hity})               
          if iasic is 2 and ((tree.adc6[ch] - tree.cmn6) > adccut_n[ch+iasic*32]) and (tree.adc6[ch] < adc_hitcut): 
             n_hit_y += 1
             adc_n = tree.adc6[ch]-tree.cmn6 + coef_R * random.uniform(-0.5,0.5) # save adc
             energy_n = Eline[ch + 32*iasic+128].Eval(adc_n)
             poi_n = 128-((32-ch)+iasic*32)
             signal_hity = SetHitInfo(n_hit_y, adc_n, energy_n, poi_n, (ch + 32*iasic+128), iasic)
             signaly.update({n_hit_y:signal_hity})               
          if iasic is 3 and ((tree.adc7[ch] - tree.cmn7) > adccut_n[ch+iasic*32]) and (tree.adc7[ch] < adc_hitcut): 
             n_hit_y += 1
             adc_n = tree.adc7[ch]-tree.cmn7 + coef_R * random.uniform(-0.5,0.5) # save adc
             energy_n = Eline[ch + 32*iasic+128].Eval(adc_n)
             poi_n = 128-((32-ch)+iasic*32)
             signal_hity = SetHitInfo(n_hit_y, adc_n, energy_n, poi_n, (ch + 32*iasic+128), iasic)
             signaly.update({n_hit_y:signal_hity})               

      
    return signalx, signaly
        
def Level1Hit_Shima1(tree, Eline, adccut_p, adccut_n, coef_R, dblist):
    adc_hitcut = 1000
    n_hit_x = 0
    n_hit_y = 0
    signalx, signaly = {}, {}

    # ========= find signal region (p-side and n-side) ============
    for iasic in range(4): 
       for ch in range(32):
          if iasic is 0 and ((tree.adc0[ch*2] - tree.cmn0) > adccut_p[ch+iasic*32]) and (tree.adc0[ch*2] < adc_hitcut): 
             n_hit_x += 1 #hit !
             adc_p = tree.adc0[ch*2]-tree.cmn0 + coef_R * random.uniform(-0.5,0.5)
             energy_p = Eline[ch + 32*iasic].Eval(adc_p)
             poi_p = dblist[ch+iasic*32].posx
             signal_hitx = SetHitInfo(n_hit_x, adc_p, energy_p, poi_p, ch + 32*iasic, iasic)
             signalx.update({n_hit_x:signal_hitx})               
          if iasic is 1 and ((tree.adc1[ch*2] - tree.cmn1) > adccut_p[ch+iasic*32]) and (tree.adc1[ch*2] < adc_hitcut): 
             n_hit_x += 1
             adc_p = tree.adc1[ch*2]-tree.cmn1 + coef_R * random.uniform(-0.5,0.5) 
             energy_p = Eline[ch + 32*iasic].Eval(adc_p)
             poi_p = dblist[ch+iasic*32].posx
             signal_hitx = SetHitInfo(n_hit_x, adc_p, energy_p, poi_p, ch + 32*iasic, iasic)
             signalx.update({n_hit_x:signal_hitx})               
          if iasic is 2 and ((tree.adc2[ch*2] - tree.cmn2) > adccut_p[ch+iasic*32]) and (tree.adc2[ch*2] < adc_hitcut): 
             n_hit_x += 1
             adc_p = tree.adc2[ch*2]-tree.cmn2 + coef_R * random.uniform(-0.5,0.5) 
             energy_p = Eline[ch + 32*iasic].Eval(adc_p)
             poi_p = dblist[ch+iasic*32].posx
             signal_hitx = SetHitInfo(n_hit_x, adc_p, energy_p, poi_p, ch + 32*iasic, iasic)
             signalx.update({n_hit_x:signal_hitx})               
          if iasic is 3 and ((tree.adc3[ch*2] - tree.cmn3) > adccut_p[ch+iasic*32]) and (tree.adc3[ch*2] < adc_hitcut): 
             n_hit_x += 1
             adc_p = tree.adc3[ch*2]-tree.cmn3 + coef_R * random.uniform(-0.5,0.5) 
             energy_p = Eline[ch + 32*iasic].Eval(adc_p)
             poi_p = dblist[ch+iasic*32].posx
             signal_hitx = SetHitInfo(n_hit_x, adc_p, energy_p, poi_p, ch + 32*iasic, iasic)
             signalx.update({n_hit_x:signal_hitx})               

          if iasic is 0 and ((tree.adc4[ch*2] - tree.cmn4) > adccut_n[ch+iasic*32]) and (tree.adc4[ch*2] < adc_hitcut): 
             n_hit_y += 1
             adc_n = tree.adc4[ch*2]-tree.cmn4 + coef_R * random.uniform(-0.5,0.5) 
             energy_n = Eline[ch + 32*iasic+128].Eval(adc_n)
             poi_n = dblist[ch+iasic*32+128].posy
             signal_hity = SetHitInfo(n_hit_y, adc_n, energy_n, poi_n, (ch + 32*iasic+128), iasic)
             signaly.update({n_hit_y:signal_hity})               
          if iasic is 1 and ((tree.adc5[ch*2] - tree.cmn5) > adccut_n[ch+iasic*32]) and (tree.adc5[ch*2] < adc_hitcut): 
             n_hit_y += 1
             adc_n = tree.adc5[ch*2]-tree.cmn5 + coef_R * random.uniform(-0.5,0.5) # save adc
             energy_n = Eline[ch + 32*iasic+128].Eval(adc_n)
             poi_n = dblist[ch+iasic*32+128].posy
             signal_hity = SetHitInfo(n_hit_y, adc_n, energy_n, poi_n, (ch + 32*iasic+128), iasic)
             signaly.update({n_hit_y:signal_hity})               
          if iasic is 2 and ((tree.adc6[ch*2] - tree.cmn6) > adccut_n[ch+iasic*32]) and (tree.adc6[ch*2] < adc_hitcut): 
             n_hit_y += 1
             adc_n = tree.adc6[ch*2]-tree.cmn6 + coef_R * random.uniform(-0.5,0.5) # save adc
             energy_n = Eline[ch + 32*iasic+128].Eval(adc_n)
             poi_n = dblist[ch+iasic*32+128].posy
             signal_hity = SetHitInfo(n_hit_y, adc_n, energy_n, poi_n, (ch + 32*iasic+128), iasic)
             signaly.update({n_hit_y:signal_hity})               
          if iasic is 3 and ((tree.adc7[ch*2] - tree.cmn7) > adccut_n[ch+iasic*32]) and (tree.adc7[ch*2] < adc_hitcut): 
             n_hit_y += 1
             adc_n = tree.adc7[ch*2]-tree.cmn7 + coef_R * random.uniform(-0.5,0.5) # save adc
             energy_n = Eline[ch + 32*iasic+128].Eval(adc_n)
             poi_n = dblist[ch+iasic*32+128].posy
             signal_hity = SetHitInfo(n_hit_y, adc_n, energy_n, poi_n, (ch + 32*iasic+128), iasic)
             signaly.update({n_hit_y:signal_hity})               

      
    return signalx, signaly
        
