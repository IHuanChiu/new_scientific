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

class rawdata_eventtree:
      def __init__(self): 
          self.options = list()
          self.declare_option("detid", 0)
          self.declare_option("asicid", 0)
          self.declare_option("stripid", 0)
          self.declare_option("adc", 0)
          self.declare_option("adcm", 0)
          self.declare_option("cmn", 0)
          self.declare_option("adccut", 0)
          self.declare_option("upperbound", 0)
          self.declare_option("coef_R", 0)

      def declare_option(self, optName, defaultVal = None):
           self.options.append(optName)
           if not (type(defaultVal) == type(None)):
               setattr(self, optName, defaultVal)     
 

class hitchannel:
      def __init__(self): 
          self.options = list()
          self.declare_option("index", 0)
          self.declare_option("adc", 0)
          self.declare_option("energy", 0)
          self.declare_option("position", 0)
          self.declare_option("channel", 0)
          self.declare_option("asic", 0)
          self.declare_option("nstrips", 0)

      def declare_option(self, optName, defaultVal = None):
           self.options.append(optName)
           if not (type(defaultVal) == type(None)):
               setattr(self, optName, defaultVal)      


class hitphoton:     
      def __init__(self): 
          self.options = list()
          self.declare_option("index", 0)
          self.declare_option("energy_p")
          self.declare_option("energy_n")
          self.declare_option("adc_p")
          self.declare_option("adc_n")
          self.declare_option("x")
          self.declare_option("y")
          self.declare_option("weight",0)
          self.declare_option("deltaE",0.0)
          self.declare_option("nstrips_x",0)
          self.declare_option("nstrips_y",0)

      def declare_option(self, optName, defaultVal = None):
           self.options.append(optName)
           if not (type(defaultVal) == type(None)):
               setattr(self, optName, defaultVal)      


class database:
      def __init__(self,detid,asicid,channel,posx,posy,widthx,widthy,ecut,calfunc):
          self.detid   = detid
          self.asicid  = asicid
          self.channel = channel
          self.posx    = posx
          self.posy    = posy
          self.widthx  = widthx
          self.widthy  = widthy
          self.ecut    = ecut
          self.calfunc = calfunc
