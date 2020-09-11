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
import sys,os,random,math,time,ROOT,argparse, ctypes
from ROOT import TFile, TTree, gROOT, TCut, gDirectory, TMinuit, Long, Double, TMath, AddressOf
gROOT.SetBatch(1)
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/macro/utils/')
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/macro/')
ROOT.gErrorIgnoreLevel = ROOT.kWarning
from logger import log, supports_color
from helpers import GetTChain, createRatioCanvas, ProgressBar
import enums
from root_numpy import hist2array, array2hist, tree2array
import numpy as np
from array import array

gROOT.ProcessLine(
"struct MLEMStruct {\
   Double_t  mlemx;\
   Double_t  mlemy;\
};"
);

from ROOT import MLEMStruct
mlstruct = MLEMStruct()
paramater_list,point_axis=[],[]

# ======================= find the paramaters by fitting ===================
class PrepareParameters():
      def __init__(self,filename=None,npoints=None,stepsize=None,npixels=None,nbins=None):
          self.filename=filename
          self.npoints=npoints
          self.stepsize=stepsize
          self.npixels=npixels
          self.nbins=nbins
          self.imagearray = self.getimages()
          self.par_list, self.hist_fitx, self.hist_fity = self.fitting_para()

      def getimages(self):
          global point_axis
          imagearray,point_axis=[],[]
          f=ROOT.TFile(self.filename,"read")
          index=0
          for iz in range(self.npoints):
             for iy in range(self.npoints):
                for ix in range(self.npoints):
                   point_axis.append([(ix-2)*self.stepsize, (iy-2)*self.stepsize, (iz-2)*self.stepsize])
                   _name = "image_pos"+str(index)
                   imagearray.append(hist2array(f.Get(_name)))
                   index+=1
          return imagearray

      def getfunc(self, name, _down, _up):
          myfunction = "gaus"
          return ROOT.TF1(name,myfunction,_down,_up)

      def fitting_para(self):
          global paramater_list
          paramater_list, hist_fitxlist, hist_fitylist=[], [], []
          fit_range,fit_step=5,7.5
          fitz_range=1
          index, xup, xdown, yup, ydown=0,0,0,0,0
          for iz in range(self.npoints):
             for iy in range(self.npoints):
                for ix in range(self.npoints):               
                   _h2name="_image_"+str(index)
                   h2=ROOT.TH2F(_h2name,_h2name,128,-16,16,128,-16,16) 
                   array2hist(self.imagearray[index],h2)
                   xup=16-fit_step*ix+fit_range+iz*fitz_range
                   xdown=16-fit_step*ix-fit_range-iz*fitz_range
                   yup=16-fit_step*iy+fit_range+iz*fitz_range
                   ydown=16-fit_step*iy-fit_range-iz*fitz_range
                   gx=self.getfunc("gx"+str(index),xdown,xup)
                   gy=self.getfunc("gy"+str(index),ydown,yup)                
#                   gx=self.getfunc("gx"+str(index),-16,16)
#                   gy=self.getfunc("gy"+str(index),-16,16)                
                   _hx=h2.ProjectionX()
                   _hy=h2.ProjectionY()
                   _hx.Fit("gx"+str(index),"QR")
                   _hy.Fit("gy"+str(index),"QR")                 
                   mean_x, mean_y, sigma_x, sigma_y = gx.GetParameter(1), gy.GetParameter(1), gx.GetParameter(2), gy.GetParameter(2)
                   intensity= _hx.GetEntries()
#                   intensity= gx.Integral(gx.GetXmin(),gx.GetXmax()) # intensity from fitting
                   paramater_list.append([mean_x, mean_y, sigma_x, sigma_y, intensity])                  
                   hist_fitxlist.append(_hx)
                   hist_fitylist.append(_hy)
                   index+=1
                   del _hx, _hy, gx, gy
          return paramater_list, hist_fitxlist, hist_fitylist

# ======================= fit with TMinuit for the varaibles of function ===================
def deffunc(_x,_y,_z,par):         
    func=par[0]+par[1]*_x+par[2]*_y+par[3]*_z
    return func
def fcn_x(npar, gin, f, par, iflag):
    chisq, nbins = 0., 5
    for _index in range(pow(nbins,3)):
       chisq += pow((paramater_list[_index][0] - deffunc(point_axis[_index][0],point_axis[_index][1],point_axis[_index][2],par)),2)
    f[0] = chisq
def fcn_y(npar, gin, f, par, iflag):
    chisq, nbins = 0., 5
    for _index in range(pow(nbins,3)):
       chisq += pow((paramater_list[_index][1] - deffunc(point_axis[_index][0],point_axis[_index][1],point_axis[_index][2],par)),2)
    f[0] = chisq
def fcn_xsig(npar, gin, f, par, iflag):
    chisq, nbins = 0., 5
    for _index in range(pow(nbins,3)):
       chisq += pow((paramater_list[_index][2] - deffunc(point_axis[_index][0],point_axis[_index][1],point_axis[_index][2],par)),2)
    f[0] = chisq
def fcn_ysig(npar, gin, f, par, iflag):
    chisq, nbins = 0., 5
    for _index in range(pow(nbins,3)):
       chisq += pow((paramater_list[_index][3] - deffunc(point_axis[_index][0],point_axis[_index][1],point_axis[_index][2],par)),2)
    f[0] = chisq
def fcn_inten(npar, gin, f, par, iflag):
    chisq, nbins = 0., 5
    for _index in range(pow(nbins,3)):
       chisq += pow((paramater_list[_index][4] - deffunc(point_axis[_index][0],point_axis[_index][1],point_axis[_index][2],par)),2)
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
      def __init__(self,PPclass=None,SRclass=None,npoints=None,nbins=None,npixels=None):
          # class members
          self.PP=PPclass
          self.SR=SRclass
          # setup varaibles
          self.nbins=nbins
          self.npoints=npoints
          self.npixels=npixels
          self.object_range=20 #mm
          # parametor members
          self.hist_fitx=self.PP.hist_fitx
          self.hist_fity=self.PP.hist_fity
          self.para_dic=self.SR.par_x_y_xs_ys_inten
          self.ori_image_list=self.PP.imagearray
          self.image_hx_hy_list_ori, self.image_hx_hy_list_sr=self.mkimage()
          self.mlemtree=self.mktree()
          self.image_init=self.mkInitImage()

          # test part
          self.test_ratio=None
          self.ff=ROOT.TFile("/Users/chiu.i-huan/Desktop/new_scientific/run/figs/repro_3Dimage.CdTe_LP_0909.root","read")
          self.h_measurement_list=[]
          for i in range(16):
             _name = "h"+str(i)
             self.h_measurement_list.append(hist2array(self.ff.Get(_name)))
          self.test_object_ratio=self.findratio(hist2array(self.image_init),self.h_measurement_list[1])

      def srf(self,_x,_y,_z,_type=None):
          """
          system response function: 
          input : object(pixel_of_x,pixel_of_y,pixel_of_z)
          output : image(x,y,xsig,ysig,intensity)
          """          
          if _type == "bintype": 
             _x= -1*self.object_range+_x*((2.*self.object_range)/self.npixels)
             _y= -1*self.object_range+_y*((2.*self.object_range)/self.npixels)
             _z= -1*self.object_range+_z*((2.*self.object_range)/self.npixels)
          par_x, par_y, par_xsig, par_ysig, par_inten = self.para_dic["x"], self.para_dic["y"], self.para_dic["xsig"], self.para_dic["ysig"], self.para_dic["intensity"]
          image_x = par_x[0].value+par_x[1].value*_x+par_x[2].value*_y+par_x[3].value*_z
          image_y = par_y[0].value+par_y[1].value*_x+par_y[2].value*_y+par_y[3].value*_z
          image_xsig = par_xsig[0].value+par_xsig[1].value*_x+par_xsig[2].value*_y+par_xsig[3].value*_z
          image_ysig = par_ysig[0].value+par_ysig[1].value*_x+par_ysig[2].value*_y+par_ysig[3].value*_z
          image_intensity = par_inten[0].value+par_inten[1].value*_x+par_inten[2].value*_y+par_inten[3].value*_z
          return [image_x,image_y,image_xsig,image_ysig,image_intensity]

      def mktree(self):
          mypoint=[7,7,7]
          image_var = self.srf(mypoint[0],mypoint[1],mypoint[2])
          _tree=TTree('tree','tree')          
          _tree.SetDirectory(0)
          _tree.Branch( 'mlemx', AddressOf( mlstruct, 'mlemx' ),  'mlemx/D' )
          _tree.Branch( 'mlemy', AddressOf( mlstruct, 'mlemy' ),  'mlemy/D' )
          hx_gaus = ROOT.TF1("hx_gaus","TMath::Gaus(x,{0},{1})".format(image_var[0],image_var[2]),-16,16)
          hy_gaus = ROOT.TF1("hy_gaus","TMath::Gaus(x,{0},{1})".format(image_var[1],image_var[3]),-16,16)
          for ie in range(int(image_var[4])):
             mlstruct.mlemx=hx_gaus.GetRandom(-16,16)
             mlstruct.mlemy=hy_gaus.GetRandom(-16,16)
             _tree.Fill()
          return _tree

      def mkimage(self):
          # make original vs. system response comparison plots
          image_hx_hy_list_sr, image_hx_hy_list_ori=[],[]
          _ip=0
          for _iz in range(self.npoints):
             _cvx  = createRatioCanvas("cvx_{}".format(_iz), 2500, 2500)
             _cvy  = createRatioCanvas("cvy_{}".format(_iz), 2500, 2500)
             _cvx.Divide(self.npoints,self.npoints)
             _cvy.Divide(self.npoints,self.npoints)
             _cvfitx  = createRatioCanvas("cvfitx_{}".format(_iz), 2500, 2500)
             _cvfity  = createRatioCanvas("cvfity_{}".format(_iz), 2500, 2500)
             _cvfitx.Divide(self.npoints,self.npoints)
             _cvfity.Divide(self.npoints,self.npoints)
             for _iy in range(self.npoints):
                for _ix in range(self.npoints):              
                   # original plots
                   _h2name="image_ori_"+str(_ip)             
                   _h2=ROOT.TH2F(_h2name,_h2name,self.nbins,-16,16,self.nbins,-16,16) 
                   array2hist(self.ori_image_list[_ip],_h2)
                   image_hx_hy_list_ori.append(_h2)
                   image_hx_hy_list_ori.append(_h2.ProjectionX())
                   image_hx_hy_list_ori.append(_h2.ProjectionY())

                   # system response plots
                   image_var = self.srf(point_axis[_ip][0], point_axis[_ip][1], point_axis[_ip][2])
                   _h2name="image_sr_"+str(_ip)
                   h2=ROOT.TH2D(_h2name,_h2name,self.nbins,-16,16,self.nbins,-16,16)
                   hx=ROOT.TH1D(_h2name+"hx",_h2name+"hx",self.nbins,-16,16)
                   hy=ROOT.TH1D(_h2name+"hy",_h2name+"hy",self.nbins,-16,16)
                   hx_gaus = ROOT.TF1("hx_gaus","TMath::Gaus(x,{0},{1})".format(image_var[0],image_var[2]),-20,20)
                   hy_gaus = ROOT.TF1("hy_gaus","TMath::Gaus(x,{0},{1})".format(image_var[1],image_var[3]),-20,20)
                   array2hist(random_sample(hx_gaus,int(image_var[4])),hx)
                   array2hist(random_sample(hy_gaus,int(image_var[4])),hy)
                   #hx.FillRandom("hx_gaus",int(image_var[4]))
                   #hy.FillRandom("hy_gaus",int(image_var[4]))
                   for ie in range(int(image_var[4])):
                      h2.Fill(hx_gaus.GetRandom(-16,16), hy_gaus.GetRandom(-16,16))
                   image_hx_hy_list_sr.append(h2)
                   image_hx_hy_list_sr.append(hx)
                   image_hx_hy_list_sr.append(hy)            

                   # comparison canvas fitting result
                   _cvfitx.cd((_ix+1)+_iy*self.npoints)
                   self.hist_fitx[_ip].SetMaximum(350)
                   self.hist_fitx[_ip].Draw()
                   _cvfity.cd((_iy+1)+_ix*self.npoints)
                   self.hist_fity[_ip].SetMaximum(350)
                   self.hist_fity[_ip].Draw()
                   # comparison canvas MLEM result
                   hx_ori=_h2.ProjectionX()
                   hy_ori=_h2.ProjectionY()
                   hx_ori.SetStats(0)
                   hy_ori.SetStats(0)
                   hx_ori.SetLineColor(1)
                   hy_ori.SetLineColor(1)
                   hx.SetStats(0)
                   hy.SetStats(0)
                   hx.SetLineColor(2)
                   hy.SetLineColor(2)
#                   hx_ori.SetMaximum(hx_ori.GetMaximum()*1.5)
#                   hy_ori.SetMaximum(hy_ori.GetMaximum()*1.5)
                   hx_ori.SetMaximum(350)
                   hy_ori.SetMaximum(350)
                   _cvx.cd((_ix+1)+_iy*self.npoints) 
                   hx_ori.Draw()
                   hx.Draw("same")
                   _cvy.cd((_iy+1)+_ix*self.npoints) 
                   hy_ori.Draw()
                   hy.Draw("same")
                   del _h2, h2, hx, hy
                   _ip+=1 

             _pdfname = "/Users/chiu.i-huan/Desktop/new_scientific/run/figs/MLEM_comparison_x_z{}.pdf".format(_iz)
             _cvx.SaveAs(_pdfname)
             _pdfname = _pdfname.replace("_x_","_y_")
             _cvy.SaveAs(_pdfname)
             _pdffit = "/Users/chiu.i-huan/Desktop/new_scientific/run/figs/MLEM_comparison_fitx_z{}.pdf".format(_iz)
             _cvfitx.SaveAs(_pdffit)
             _pdffit = _pdffit.replace("_fitx_","_fity_")
             _cvfity.SaveAs(_pdffit)
          return image_hx_hy_list_ori, image_hx_hy_list_sr

      def mkInitImage(self):
          # return initial image from object
          prog = ProgressBar(ntotal=pow(self.npixels,3),text="Processing image",init_t=time.time())
          _image_init=ROOT.TH2D("image_init","image_init",self.nbins,-16,16,self.nbins,-16,16)
          _image_init_array=np.zeros((self.nbins,self.nbins),dtype=float)
          nevents=1
          nevproc=0
          for ie in range(int(nevents)):
             for _iz in range(self.npixels):
                for _iy in range(self.npixels):
                   for _ix in range(self.npixels):
                      nevproc+=1
                      if prog: prog.update(nevproc)
                      imagespace_vars = self.srf(_ix, _iy, _iz, "bintype")
                      fx = ROOT.TF1("fx","TMath::Gaus(x,{0},{1})".format(imagespace_vars[0],imagespace_vars[2]),-16,16)
                      fy = ROOT.TF1("fy","TMath::Gaus(x,{0},{1})".format(imagespace_vars[1],imagespace_vars[3]),-16,16)
                      _image_init.Fill(fx.GetRandom(-16,16), fy.GetRandom(-16,16))
                      del fx, fy
          if prog: prog.finalize()
          return _image_init

      def updateImage(self,_object):
          #TODO nevents is not good
          _image_update=ROOT.TH2D("image_update","image_update",self.nbins,-16,16,self.nbins,-16,16)
          for _iz in range(_object.shape[2]):
             for _iy in range(_object.shape[1]):
                for _ix in range(_object.shape[0]):
                   _xaxis = -20+_ix*(40./self.npixels)
                   _yaxis = -20+_iy*(40./self.npixels)
                   _zaxis = -20+_iz*(40./self.npixels)
                   imagespace_vars = self.srf(_xaxis, _yaxis, _zaxis)
                   fx = ROOT.TF1("fx","TMath::Gaus(x,{0},{1})".format(imagespace_vars[0],imagespace_vars[2]),-16,16)
                   fy = ROOT.TF1("fy","TMath::Gaus(x,{0},{1})".format(imagespace_vars[1],imagespace_vars[3]),-16,16)
                   for ie in range(int(nevents)):
                      _image_update.Fill(fx.GetRandom(-16,16), fy.GetRandom(-16,16))
          return _image_update

      def findratio(self,measurement_image_array,reproduction_image_array):
          # input/output type: numpy.array
          _where_0 = np.where(reproduction_image_array == 0)
          reproduction_image_array[_where_0]=1
          image_ratio=measurement_image_array/reproduction_image_array

          hist_image_ratio=ROOT.TH2D("image_ratio","image_ratio",self.nbins,-16,16,self.nbins,-16,16)
          array2hist(image_ratio,hist_image_ratio) # image_ratio is image ratio
          self.test_ratio=hist_image_ratio
          # TODO next : find object ratio by system response
          object_ratio=np.ones((self.npixels,self.npixels,self.npixels),dtype=float)
          return object_ratio

      def updateObject(self,object_pre,object_ratio):
          # update object based on object ratio
          object_update=object_pre*object_ratio
          return object_update

      def iterate(self,n_iteration):                   
          hist_final_object=ROOT.TH3D("MLEM_3Dimage","MLEM_3Dimage",self.npixels,-20,20,self.npixels,-20,20,self.npixels,-20,20)
          final_object=np.zeros((self.npixels,self.npixels,self.npixels),dtype=float)
          for h_measurement_array in self.h_measurement_list:
             _object_pre=np.ones((self.npixels,self.npixels,self.npixels),dtype=float)# training object space
             for i in range(n_iteration):
                if i == 0: 
                   _image = self.image_init
                   _object_update=_object_pre
                else: 
                   _image = self.updateImage(_object_update)
                _object_ratio=self.findratio(h_measurement_array, hist2array(_image)) 
                _object_update=self.updateObject(_object_update, _object_ratio)
                final_object+=_object_update# projeaction of all images
          array2hist(final_object,hist_final_object)
          return hist_final_object

      def printoutput(self,RootType_list, _outname, savetype):
          if savetype == "re" or savetype == "RE" or savetype == "Re": _savetype = "recreate"
          if savetype == "up" or savetype == "UP" or savetype == "Up": _savetype = "update"
          fout=ROOT.TFile(_outname, _savetype)
          fout.cd()    
          if isinstance(RootType_list, list):
             for _iR in RootType_list:
                _iR.Write()
          else:
             RootType_list.Write()
          fout.Close()

# ======================= test part (old) ===================
def GetImageSpace(filename,npixels,npoints,nbins,mypoint):
    # Object spcae to image spcae (by weighting image)
    my_axis=[]
    index,stepsize=0,10
    for ix in range(npoints):
       for iy in range(npoints):
          for iz in range(npoints):
             my_axis.append([(ix-2)*stepsize, (iy-2)*stepsize, (iz-2)*stepsize])

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
       if (np.sum(((mypoint-my_axis[i])**2)) == 0): mypoint=mypoint+0.00000000001 #skip divide by zero
       weight=1/np.sum(((mypoint-my_axis[i])**2))#Inverse square distance
       sumw+=weight
       weight_list.append(weight)# use this weight_list to find image for mypoint
    for i in range(pow(npoints,3)):
       # find corresponding image from the giving object space
       myimageA+=imagearray_list[i]*(weight_list[i]/sumw)
    return myimageA

def mkWeightFunc(filename,_np):
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
    outfilename = "/Users/chiu.i-huan/Desktop/mytesth3output.root"
    log().info("Test run...")
    image_nbins=128
    _sr=mkWeightFunc(args.inputFolder, args.npoints)
    testpoint=np.array([0,0,0])
    testimage = GetImageSpace(args.inputFolder,image_nbins,5,image_nbins,testpoint)

    log().info("Progressing System response and making MLEM plots...")
    PP=PrepareParameters(filename=args.inputFolder,npoints=args.npoints,stepsize=args.stepsize,npixels=args.npixels,nbins=image_nbins) # get cali. image list
    SR=SystemResponse()# get system response by TMinuit fitting
    ML=MLEM(PPclass=PP,SRclass=SR,npoints=args.npoints,nbins=image_nbins,npixels=args.npixels) # do iterate and get final plots

    #no need
    log().info("Print outputs...")
    ML.printoutput(ML.mlemtree,outfilename,"re")
    ML.printoutput(ML.image_hx_hy_list_ori,outfilename,"up")
    ML.printoutput(ML.image_hx_hy_list_sr,outfilename,"up")
    ML.printoutput(ML.image_init,outfilename,"up")
    ML.printoutput(ML.test_ratio,outfilename,"up")

    # save fitting plots
#    ML.printoutput(PP.hist_fitx,outfilename,"up")
#    ML.printoutput(PP.hist_fity,outfilename,"up")

    log().info("Output : %s"%(outfilename))
    exit(0)

if __name__=="__main__":

   parser = argparse.ArgumentParser(description='Process some integers.')
   parser.add_argument("-i","--inputFolder", type=str, default="/Users/chiu.i-huan/Desktop/new_scientific/run/root/20200406a_5to27_cali_caldatat_0828_split.root", help="Input File Name")
   parser.add_argument("-n","--npoints",dest="npoints",type=int, default=5, help="Number of images")
   parser.add_argument("-s","--stepsize",dest="stepsize",type=int, default=10, help="Number of images")
   parser.add_argument("-p","--npixels",dest="npixels",type=int, default=30, help="Number of images")
   args = parser.parse_args()

   testrun(args)
