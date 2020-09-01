#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
This module makes the system response
"""
__author__    = "I-Huan CHIU"
__email__     = "ichiu@chem.sci.osaka-u.ac.jp"
__created__   = "2020-07-07"
__copyright__ = "Copyright 2019 I-Huan CHIU"
__license__   = "GPL http://www.gnu.org/licenses/gpl.html"

# modules
import sys,os,random,math,time,ROOT,argparse
from ROOT import TFile, TTree, gROOT, TCut, gDirectory, TMinuit, Long, Double, TMath, AddressOf
gROOT.SetBatch(1)
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/macro/utils/')
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/macro/')
ROOT.gErrorIgnoreLevel = ROOT.kWarning
from logger import log, supports_color
import enums
from root_numpy import hist2array, array2hist, tree2array
import numpy as np
import ctypes
from array import array;

gROOT.ProcessLine(
"struct MLEMStruct {\
   Double_t  mlemx[128];\
   Double_t  mlemy[128];\
};"
);

from ROOT import MLEMStruct
mlstruct = MLEMStruct()

# ======================= find paramater for fitting ===================
class PrepareParameters():
      def __init__(self,filename=None,npoints=None,stepsize=None,npixels=None,nbins=None):
          self.filename=filename
          self.npoints=npoints
          self.stepsize=stepsize
          self.npixels=npixels
          self.nbins=nbins
          self.imagearray, self.XYZaxis = self.getimages()

      def getimages(self):
          imagearray, XYZaxis=[], []
          f=ROOT.TFile(self.filename,"read")
          for ix in range(self.npoints):
             for iy in range(self.npoints):
                for iz in range(self.npoints):
                   index=ix+iy*5+iz*25
                   XYZaxis.append([(ix-2)*self.stepsize, (iy-2)*self.stepsize, (iz-2)*self.stepsize])
                   _name = "image_pos"+str(index)
                   imagearray.append(hist2array(f.Get(_name)))
          return imagearray, XYZaxis

      def getfunc(self, name, _down, _up):
          myfunction = "gaus"
          return ROOT.TF1(name,myfunction,_down,_up)

      def fitting_para(self):
          _paramater_list=[]
          fit_range,fit_step=3,7.5
          index, xup, xdown, yup, ydown=0,0,0,0,0
          for ix in range(self.npoints):
             for iy in range(self.npoints):
                for iz in range(self.npoints):               
                   _h2name="_image_"+str(index)
                   h2=ROOT.TH2F(_h2name,_h2name,128,-16,16,128,-16,16) 
                   array2hist(self.imagearray[index],h2)
                   xup=16-fit_step*ix+fit_range
                   xdown=16-fit_step*ix-fit_range
                   yup=16-fit_step*iy+fit_range
                   ydown=16-fit_step*iy-fit_range
                   gx=self.getfunc("gx",xdown,xup)
                   gy=self.getfunc("gy",ydown,yup)                
                   _hx=h2.ProjectionX()
                   _hy=h2.ProjectionY()
                   _hx.Fit("gx","QR")
                   _hy.Fit("gy","QR")                 
                   mean_x, mean_y, sigma_x, sigma_y = gx.GetParameter(1), gy.GetParameter(1), gx.GetParameter(2), gy.GetParameter(2)
                   intensity= _hx.GetEntries()
                   _paramater_list.append([mean_x, mean_y, sigma_x, sigma_y, intensity])                   
                   index+=1
          return _paramater_list

PP=PrepareParameters(filename="/Users/chiu.i-huan/Desktop/new_scientific/run/root/20200406a_5to27_cali_caldatat_0828_split.root",npoints=5,stepsize=10,npixels=125,nbins=128)
paramater_list=PP.fitting_para()
pixel_axis=PP.XYZaxis

# ======================= varaible fitting for function ===================
def deffunc(_x,_y,_z,par):         
    func=par[0]+par[1]*_x+par[2]*_y+par[3]*_z
    return func
def fcn_x(npar, gin, f, par, iflag):
    chisq, nbins = 0., 5
    for _index in range(pow(nbins,3)):
       chisq += pow((paramater_list[_index][0] - deffunc(pixel_axis[_index][0],pixel_axis[_index][1],pixel_axis[_index][2],par)),2)
    f[0] = chisq
def fcn_y(npar, gin, f, par, iflag):
    chisq, nbins = 0., 5
    for _index in range(pow(nbins,3)):
       chisq += pow((paramater_list[_index][1] - deffunc(pixel_axis[_index][0],pixel_axis[_index][1],pixel_axis[_index][2],par)),2)
    f[0] = chisq
def fcn_xsig(npar, gin, f, par, iflag):
    chisq, nbins = 0., 5
    for _index in range(pow(nbins,3)):
       chisq += pow((paramater_list[_index][2] - deffunc(pixel_axis[_index][0],pixel_axis[_index][1],pixel_axis[_index][2],par)),2)
    f[0] = chisq
def fcn_ysig(npar, gin, f, par, iflag):
    chisq, nbins = 0., 5
    for _index in range(pow(nbins,3)):
       chisq += pow((paramater_list[_index][3] - deffunc(pixel_axis[_index][0],pixel_axis[_index][1],pixel_axis[_index][2],par)),2)
    f[0] = chisq
def fcn_inten(npar, gin, f, par, iflag):
    chisq, nbins = 0., 5
    for _index in range(pow(nbins,3)):
       chisq += pow((paramater_list[_index][4] - deffunc(pixel_axis[_index][0],pixel_axis[_index][1],pixel_axis[_index][2],par)),2)
    f[0] = chisq

class SystemResponse():
      def __init__(self):
          self.par_x_y_xs_ys_inten = self.GetSRpar()

      def dofit(self, parname):
          if parname == "x": fcn = fcn_x
          if parname == "y": fcn = fcn_y
          if parname == "xsig": fcn = fcn_xsig
          if parname == "ysig": fcn = fcn_ysig
          if parname == "inten": fcn = fcn_inten
          gMinuit = TMinuit(4)
          gMinuit.SetPrintLevel(-1) # -1  quiet, 0  normal, 1  verbose
          gMinuit.SetFCN( fcn )
          arglist = array( 'd', 10*[0.] )
          ierflg = ctypes.c_int(1982)
      
          arglist[0] = 1
          gMinuit.mnexcm( "SET ERR", arglist, 1, ierflg )
      
          # Set starting values and step sizes for parameters
          vstart = array( 'd', ( 3,  1,  0.1,  0.01  ) )
          step   = array( 'd', ( 0.1, 0.1, 0.01, 0.001 ) )
          gMinuit.mnparm( 0, "par0", vstart[0], step[0], 0, 0, ierflg )
          gMinuit.mnparm( 1, "parx", vstart[1], step[1], 0, 0, ierflg )
          gMinuit.mnparm( 2, "pary", vstart[2], step[2], 0, 0, ierflg )
          gMinuit.mnparm( 3, "parz", vstart[3], step[3], 0, 0, ierflg )
      
          # Now ready for minimization step
          arglist[0] = 500
          arglist[1] = 1.
          gMinuit.mnexcm( "MIGRAD", arglist, 2, ierflg )
      
          # Print results
          par0,par1,par2,par3 = map(ctypes.c_double, (0,0,0,0))
          par0_err,par1_err,par2_err,par3_err = map(ctypes.c_double, (0,0,0,0))
          amin, edm, errdef = map(ctypes.c_double, (0.18, 0.19, 0.20))
          nvpar, nparx, icstat = map(ctypes.c_int, (1983, 1984, 1985))
          gMinuit.mnstat( amin, edm, errdef, nvpar, nparx, icstat )
          gMinuit.GetParameter(0,par0,par0_err)
          gMinuit.GetParameter(1,par1,par0_err)
          gMinuit.GetParameter(2,par2,par0_err)
          gMinuit.GetParameter(3,par3,par0_err)
          return [par0,par1,par2,par3]

      def GetSRpar(self):
          _par_x_y_xs_ys_inten={}
          _par_x_y_xs_ys_inten.update({"x":self.dofit("x")})
          _par_x_y_xs_ys_inten.update({"y":self.dofit("y")})
          _par_x_y_xs_ys_inten.update({"xsig":self.dofit("xsig")})
          _par_x_y_xs_ys_inten.update({"ysig":self.dofit("ysig")})
          _par_x_y_xs_ys_inten.update({"intensity":self.dofit("inten")})
          return _par_x_y_xs_ys_inten


# ======================= Maximum Likelihood Expectation Maximization ===================
class MLEM():
      def __init__(self,para_dic=None,nbins=None):
          self.nbins=nbins
          self.para_dic=para_dic
          self.image_var=self.srf(0,0,0)
          self.mlemh2,self.mlemhx,self.mlemhy=self.mkimage()
          self.mlemtree=self.mktree()

      def srf(self,_x,_y,_z):
          # system response function: 
          # input : object(x,y,z)
          # output : image(x,y,xsig,ysig,intensity)
          par_x, par_y, par_xsig, par_ysig, par_inten = self.para_dic["x"], self.para_dic["y"], self.para_dic["xsig"], self.para_dic["ysig"], self.para_dic["intensity"]
          image_x = par_x[0].value+par_x[1].value*_x+par_x[2].value*_y+par_x[3].value*_z
          image_y = par_y[0].value+par_y[1].value*_x+par_y[2].value*_y+par_y[3].value*_z
          image_xsig = par_xsig[0].value+par_xsig[1].value*_x+par_xsig[2].value*_y+par_xsig[3].value*_z
          image_ysig = par_ysig[0].value+par_ysig[1].value*_x+par_ysig[2].value*_y+par_ysig[3].value*_z
          image_intensity = par_inten[0].value+par_inten[1].value*_x+par_inten[2].value*_y+par_inten[3].value*_z
          return [image_x,image_y,image_xsig,image_ysig,image_intensity]

      def mktree(self):
          _tree=TTree('tree','tree')          
          _tree.SetDirectory(0)
          _tree.Branch( 'mlemx', AddressOf( mlstruct, 'mlemx' ),  'mlemx/D' )
          _tree.Branch( 'mlemy', AddressOf( mlstruct, 'mlemy' ),  'mlemy/D' )
          for ie in range(int(self.image_var[4])):
             _tree.Fill()
          return _tree

      def mkimage(self):
          hx=ROOT.TH1D("hx","hx",self.nbins,-16,16)
          hy=ROOT.TH1D("hy","hy",self.nbins,-16,16)
          h2=ROOT.TH2D("image","image",self.nbins,-16,16,self.nbins,-16,16)
          hx_gaus = ROOT.TF1("hx_gaus","TMath::Gaus(x,{0},{1})".format(self.image_var[0],self.image_var[2]),-16,16)
          hy_gaus = ROOT.TF1("hy_gaus","TMath::Gaus(x,{0},{1})".format(self.image_var[1],self.image_var[3]),-16,16)
          hx.FillRandom("hx_gaus",int(self.image_var[4]))
          hy.FillRandom("hy_gaus",int(self.image_var[4]))
          for ix in range(128):
             for iy in range(128):
                xvalue=hx.GetBinContent(ix+1)
                yvalue=hy.GetBinContent(iy+1)
                _bin=h2.GetBin(ix,iy)
                if(xvalue!=0 and yvalue!=0): h2.SetBinContent(_bin,(xvalue+yvalue)/2)
          return h2,hx,hy

      def iterate(self):
          return 0

# ======================= test part ===================
def GetImageSpace(filename,npixels,npoints,nbins,mypoint):
    # Object spcae to image spcae (by weighting image)
    mypixel_axis=[]
    index,stepsize=0,10
    for ix in range(npoints):
       for iy in range(npoints):
          for iz in range(npoints):
             mypixel_axis.append([(ix-2)*stepsize, (iy-2)*stepsize, (iz-2)*stepsize])

    weight, sumw = 0,0
    imagearray_list, weight_list=[],[]
    myimageA = np.zeros((nbins,nbins),dtype=float)
    f=ROOT.TFile(filename,"read")
    for i in range(pow(npoints,3)):
      # get cal. images
      _name = "image_pos"+str(i)
      imagearray_list.append(hist2array(f.Get(_name)))
    for i in range(pow(npoints,3)):
       # get weight from each imges
       if (np.sum(((mypoint-mypixel_axis[i])**2)) == 0): mypoint=mypoint+0.00000000001 #skip divide by zero
       weight=1/np.sum(((mypoint-mypixel_axis[i])**2))#Inverse square distance
       sumw+=weight
       weight_list.append(weight)# use this weight_list to find image for mypoint
    for i in range(pow(npoints,3)):
       # find corresponding image from the giving object space
       myimageA+=imagearray_list[i]*(weight_list[i]/sumw)
    return myimageA

def mkSystemResponse(filename,_np):
    n_images=pow(_np,3)
    am241_intensity = 363.1*1000 #Bq
    _time=600 #second
    image_list=[]
    f=ROOT.TFile(filename,"read")
    for i in range(n_images):    
       _name = "image_pos"+str(i)
       image_list.append(f.Get(_name))
    _sr=np.zeros((len(image_list),image_list[0].GetNbinsX(),image_list[0].GetNbinsY()),dtype=float)
    for i in range(len(image_list)):
       _sr[i]=hist2array(image_list[i])
    _sr = _sr/(am241_intensity*_time)
    return _sr

# ======================= run ===================
def testrun(args):
    log().info("Test run...")
    _sr=mkSystemResponse(args.inputFolder, args.npoints)
    testpoint=np.array([0,0,0])
    testimage = GetImageSpace(args.inputFolder,128,5,128,testpoint)

    log().info("System response...")
    SR=SystemResponse()# fitting and print result
    ML=MLEM(para_dic=SR.par_x_y_xs_ys_inten,nbins=128)

    #no need
    fout=ROOT.TFile("/Users/chiu.i-huan/Desktop/mytesth3output.root", 'recreate' )
    h3=ROOT.TH3D("h3","h3",_sr.shape[0], 0, 125,_sr.shape[1], -16, 16,_sr.shape[2],-16,16)
    array2hist(_sr,h3)
    fout.cd()
#    h3.Write()

    log().info("Making MLEM plots...")
    ML.mlemtree.Write()
    ML.mlemhx.Write()
    ML.mlemhy.Write()
    ML.mlemh2.Write()

    h2=ROOT.TH2D("h2","h2",testimage.shape[0], -16, 16,testimage.shape[1], -16, 16)
    array2hist(testimage,h2)
    _h1x=h2.ProjectionX()
    _h1y=h2.ProjectionY()
    _h1x.Write()
    _h1y.Write()
    h2.Write()

    log().info("Output : %s"%("/Users/chiu.i-huan/Desktop/mytesth3output.root"))
    exit(0)

if __name__=="__main__":

   parser = argparse.ArgumentParser(description='Process some integers.')
   parser.add_argument("-i","--inputFolder", type=str, default="/Users/chiu.i-huan/Desktop/new_scientific/run/root/20200406a_5to27_cali_caldatat_0828_split.root", help="Input File Name")
   parser.add_argument("-n","--npoints",dest="npoints",type=int, default=5, help="Number of images")
   parser.add_argument("-p","--npixels",dest="npixels",type=int, default=50, help="Number of images")
   args = parser.parse_args()

   testrun(args)
