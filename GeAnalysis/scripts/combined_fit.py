import os,ROOT,ctypes
ROOT.gErrorIgnoreLevel = ROOT.kFatal
__location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
ROOT.gROOT.LoadMacro( __location__+'/AtlasStyle/AtlasStyle.C')
ROOT.SetAtlasStyle()

#data_file="/Users/chiu.i-huan/Desktop/new_scientific/GeAnalysis/data/JPARC_2021Apri_Terada/Black/203086_beam.root" #black
#data_file="/Users/chiu.i-huan/Desktop/new_scientific/GeAnalysis/data/JPARC_2021Apri_Terada/DEW12007/203079_beam.root" #dew
#data_file="/Users/chiu.i-huan/Desktop/new_scientific/GeAnalysis/data/JPARC_2021Apri_Terada/DEW12007_bar/203089_beam.root" #dewbar
#data_file="/Users/chiu.i-huan/Desktop/new_scientific/GeAnalysis/data/JPARC_2021Apri_Terada/DEW12007_bar_35MeV/203095_beam.root" #dewbar35
data_file="/Users/chiu.i-huan/Desktop/new_scientific/GeAnalysis/data/JPARC_2021Apri_Terada/White/203084_beam.root" #white


name_list=["Si32", "Al43", "Al42", "Fe54", "Fe43", "Ca43", "Ca32", "Mg32", "Cu43", "Fegamma"]
overall_range_down=[74,22,88,42,90,54,155,55.5,113,125]
overall_range_up=[79,23.5,91,44,93.5,55.6,157.5,57.5,119,127]

#for Fe gamma-rays
#data_file="/Users/chiu.i-huan/Desktop/new_scientific/GeAnalysis/data/JPARC_2021Apri_Terada/Fe/203082_beam.root" #Fe
#name_list=["Fegamma_1", "Fegamma_2", "Fegamma_3"]
#overall_range_down=[125,54,153]
#overall_range_up=[127,56,157]

nbins=int(6800)

def getLatex(ch, x = 0.85, y = 0.85):
    _t = ROOT.TLatex()
    _t.SetNDC()
    _t.SetTextFont( 62 )
    _t.SetTextColor( 36 )
    _t.SetTextSize( 0.08 )
    _t.SetTextAlign( 12 )
    return _t

def fit(_h,outname):
    three_peaks=[] 
    three_sigmas=[] 
    count_list, error_list=[],[]
    par0,par1,par2,par3,par4 = map(ctypes.c_double, (0,0,0,0,0))
   
    for _ip in range(len(overall_range_down)):
       _htemp,_hdraw=_h.Clone(), _h.Clone()
       _htemp.GetXaxis().SetRangeUser(overall_range_down[_ip],overall_range_up[_ip])
       _hdraw.GetXaxis().SetRangeUser(overall_range_down[_ip],overall_range_up[_ip])
       peak = ROOT.TF1("peak","gaus", overall_range_down[_ip], overall_range_up[_ip]);
       bkg = ROOT.TF1("bkg","pol1", overall_range_down[_ip],overall_range_up[_ip]);
       _htemp.Fit(peak,"Q")
       _htemp.Fit(bkg,"Q")
       par0=peak.GetParameter(0)
       par1=peak.GetParameter(1)
       par2=peak.GetParameter(2)
       par3=bkg.GetParameter(0)
       par4=bkg.GetParameter(1)

       total = ROOT.TF1("total","gaus(0)+pol1(3)", overall_range_down[_ip],overall_range_up[_ip] )
       total.SetParameters(par0,par1,par2,1,0)
       _htemp.Fit(total,"Q")
       par0,par1,par2,par3,par4=total.GetParameter(0),total.GetParameter(1),total.GetParameter(2),total.GetParameter(3),total.GetParameter(4)
       peak.SetParameters(par0,par1,par2)
       bkg.SetParameters(par3,par4)
       
       three_peaks.append(par1)#peak
       three_sigmas.append(par2)#sigma
       _bindown, _binup=_htemp.GetXaxis().FindBin(par1-3*par2), _htemp.GetXaxis().FindBin(par1+3*par2)
       _binwidth=_htemp.GetBinWidth(1)
       count_list.append(peak.Integral(par1-3*par2,par1+3*par2)/_binwidth)#gaus fit
       #TODO fix error
       _error_temp=ctypes.c_double(0);_sum_temp=_htemp.IntegralAndError(_bindown,_binup,_error_temp,"error")
       error_list.append(_error_temp.value)
       print("Signal+bkg : ",_htemp.Integral(_bindown,_binup), " Signal : {:.2f}".format(peak.Integral(par1-3*par2,par1+3*par2)/_binwidth), " Chisquare : {:.2f}".format(total.GetChisquare()))

       c=ROOT.TCanvas("c{}".format(_ip),"c{}".format(_ip),1200,800)
       _hdraw.SetLineColor(1)
       peak.SetLineColor(4)
       bkg.SetLineColor(3)
       total.SetLineColor(2)
       _hdraw.SetMinimum(0)
       _hdraw.Draw("ep")
       peak.Draw("same")
       total.Draw("same")
       bkg.Draw("same")
       c.SaveAs("/Users/chiu.i-huan/Desktop/c_fit_peak_{0}_{1}.png".format(name_list[_ip],outname))
       
    return three_peaks, three_sigmas, count_list, error_list

if __name__=="__main__":

  f_data=ROOT.TFile(data_file,"read")

  t_data=f_data.Get("tree")
  t_data.Draw("energy >> h_data({},10,180)".format(nbins),"detID == {}".format(1),"")
  h_data=ROOT.gDirectory.Get("h_data")

  h_data.SetLineColorAlpha(2,0.9)
  
  _peak, _sigma, _cout, _error = fit(h_data,outname="data")
  print("===============================================")
  print("Data:")
  for ip in range(len(_peak)):
     print("{0} | Peak : {1:.2f} | Sigma : {2:.2f} | Intensity : {3:.1f} | Error : {4:.1f}".format(name_list[ip],_peak[ip], _sigma[ip], _cout[ip], _error[ip]))

