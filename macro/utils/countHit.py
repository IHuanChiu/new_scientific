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
#import numpy as np
from HitChannel import prehitchannel, hitphoton
import heapq 

def SetWeight(adcx, adcy, a, b):
    # ============ find hit point of photon (2D) ===========
#    if(math.fabs(adcy - (adcx*a + b))) > 5 : return False
#    return True
    return math.fabs(adcy - (adcx*a + b))

def isAdjacent(i, _hit):
    if (i-1) is 0 : return False # first
    if _hit[i].position - _hit[i-1].position is 1 : return True
    else: return False

def mergehit(_nx, _ny, _hitx, _hity):   
    pre_signal_list = {}
    merge_xhit, merge_yhit = {}, {}
    m_nx, m_ny = 0, 0    
    _nhit = 0
    _weight = 1.0
    
    for ix in range(1, 1+_nx):
       if(isAdjacent(ix, _hitx)): 
          _hitx[ix].energy += _hitx[ix -1].energy
          _hitx[ix].adc += _hitx[ix -1].adc 
          merge_xhit.update({m_nx:_hitx[ix]})
       else:
          m_nx += 1
          merge_xhit.update({m_nx:_hitx[ix]})
   
    for iy in range(1, 1+_ny):
       if(isAdjacent(iy, _hity)): 
          _hity[iy].energy += _hity[iy -1].energy
          _hity[iy].adc += _hity[iy -1].adc
          merge_yhit.update({m_ny:_hity[iy]})
       else:
          m_ny += 1
          merge_yhit.update({m_ny:_hity[iy]})

    for ix in range(1, 1+m_nx):
       for iy in range(1, 1+m_ny):
          _nhit += 1
          delta_energy = math.fabs(merge_xhit[ix].energy - merge_yhit[iy].energy)
          pre_signal_list.update({_nhit:SetphotonInfo(_nhit, merge_xhit[ix].energy, merge_yhit[iy].energy, merge_xhit[ix].adc, merge_yhit[iy].adc, merge_xhit[ix].position, merge_yhit[iy].position, _weight, delta_energy)})
    return m_nx, m_ny, _nhit, pre_signal_list                          

def matchhit(_nx, _ny, _npoint, _s):   
    list_signal = {}
    dic = {}

    for ip in range(1, 1+_npoint):
       dic.update({ip:_s[ip].deltaE})

    maxpoint = min(_nx, _ny)
    _id = heapq.nlargest(maxpoint,dic)
    _nhit = 0#should be same with maxpoint
    for _ip in _id:
       _nhit += 1
       list_signal.update({_nhit:_s[_ip]})
    return _nhit, list_signal

def SetphotonInfo(index, _ep, _en, _ap, _an, _x, _y, _weight, _delta):
    _signal = hitphoton()     
    _signal.index = index
    _signal.energy_p = _ep
    _signal.energy_n = _en
    _signal.adc_p = _ap
    _signal.adc_n = _an
    _signal.x = _x
    _signal.y = _y
    _signal.weight = _weight
    _signal.deltaE = _delta
    return _signal 

def SetHitInfo(index, adc, energy, poi, ch, asic):
    _hit = prehitchannel()
    _hit.index = index
    _hit.adc = adc
    _hit.energy = energy
    _hit.position = poi
    _hit.channel = ch
    _hit.asic = asic
    return _hit    

def defineHit(tree, Eline, adccut_p, adccut_n, coef_a, coef_b, coef_R):
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

      
    return n_hit_x, n_hit_y, signalx, signaly
        
