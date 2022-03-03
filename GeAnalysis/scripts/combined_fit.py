"""
Fit peaks and do the correlation based on MC
"""
import os,ROOT,ctypes
ROOT.gErrorIgnoreLevel = ROOT.kFatal
__location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
ROOT.gROOT.LoadMacro( __location__+'/AtlasStyle/AtlasStyle.C')
ROOT.SetAtlasStyle()

correction_file="./output_eff_plots.root"
Correction=True

Sample_name="white" #black, dew, dewbar, dew_35, white

#data_file="/Users/chiu.i-huan/Desktop/new_scientific/GeAnalysis/data/JPARC_2021Apri_Terada/Black/203086_beam.root" #black
#data_file="/Users/chiu.i-huan/Desktop/new_scientific/GeAnalysis/data/JPARC_2021Apri_Terada/DEW12007/203079_beam.root" #dew
#data_file="/Users/chiu.i-huan/Desktop/new_scientific/GeAnalysis/data/JPARC_2021Apri_Terada/DEW12007_bar/203089_beam.root" #dewbar
#data_file="/Users/chiu.i-huan/Desktop/new_scientific/GeAnalysis/data/JPARC_2021Apri_Terada/DEW12007_bar_35MeV/203095_beam.root" #dew_35
data_file="/Users/chiu.i-huan/Desktop/new_scientific/GeAnalysis/data/JPARC_2021Apri_Terada/White/203084_beam.root" #white

name_list=["Si32", "Al43", "Al42", "Fe54", "Fe43", "Ca43", "Ca32", "Mg32", "Cu43", "Fegamma"]# bin index
overall_range_down=[74,22,88,42,92,54,155,55.5,113,125]
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

def correction(peak,count,_idet):
    corr_count_list=[]
    f_temp=ROOT.TFile(correction_file,"read")
    if Sample_name == "dewbar": _Sample_name = "dew"
    else: _Sample_name = Sample_name
    _name="h1_eff_{}_{}".format(_Sample_name,_idet)
    h1=f_temp.Get(_name)
    print("===============================================")
    for ip in range(len(peak)):
       _ratio=h1.GetBinContent(h1.GetXaxis().FindBin(peak[ip]))
       print("peak : {:.2f}, ratio : {:.2f}".format(peak[ip], _ratio))
       if(_ratio < 0.1): _ratio = 0.1#TODO set limit
       corr_count_list.append(count[ip]/_ratio)
    return corr_count_list

def fit(_h,outname):
    three_peaks=[] 
    three_sigmas=[] 
    count_list, error_list=[],[]
    par0,par1,par2,par3,par4 = map(ctypes.c_double, (0,0,0,0,0))
   
    print("================= NEW RUN {} ===================".format(outname))
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
       print("Signal+bkg : ",_htemp.Integral(_bindown,_binup), " Signal : {:.2f}".format(peak.Integral(par1-3*par2,par1+3*par2)/_binwidth), " Chisquare : {:.2f}".format(total.GetChisquare()))
       if ((peak.Integral(par1-3*par2,par1+3*par2)/_binwidth) > _htemp.Integral(_bindown,_binup)):
          count_list.append(0)# bad fitting due to low stat.
       else:
          count_list.append(peak.Integral(par1-3*par2,par1+3*par2)/_binwidth)#gaus fit
       #TODO error is not used
       #error_list.append(peak.IntegralError(par1-3*par2,par1+3*par2)/_binwidth)
       _error_temp=ctypes.c_double(0)
       _sum_temp=_htemp.IntegralAndError(_bindown,_binup,_error_temp,"error")
       error_list.append(_error_temp.value)

       c=ROOT.TCanvas("c{}".format(_ip),"c{}".format(_ip),1200,800)
       _hdraw.SetLineColor(1)
       peak.SetLineColor(4)
       bkg.SetLineColor(3)
       total.SetLineColor(2)
       _hdraw.SetMinimum(0)
       _hdraw.SetTitle(";Energy [keV];Counts/25 eV")
       _hdraw.GetXaxis().CenterTitle(); _hdraw.GetYaxis().CenterTitle();
       _hdraw.Draw("ep")
       peak.Draw("same")
       total.Draw("same")
       bkg.Draw("same")
       c.SaveAs("/Users/chiu.i-huan/Desktop/temp_output/c_fit_peak_{0}_{1}.png".format(name_list[_ip],outname))
       
    return three_peaks, three_sigmas, count_list, error_list

if __name__=="__main__":
  if not os.path.exists("/Users/chiu.i-huan/Desktop/temp_output/"):
     print ("make folder for ouput fig.")
     os.mkdir("/Users/chiu.i-huan/Desktop/temp_output/")
  f_out=ROOT.TFile("./terada_analysis/intensity_files/intensity_{}.root".format(Sample_name),"recreate")

  f_data=ROOT.TFile(data_file,"read")
  t_data=f_data.Get("tree")

  for idet in range(1,6+1):
     hout=ROOT.TH1F("{}_CH{}".format(Sample_name,idet),"{}_CH{}".format(Sample_name,idet),15,0,15)#15 peaks
     t_data.Draw("energy >> h_data({},10,180)".format(nbins),"detID == {}".format(idet),"")
     h_data=ROOT.gDirectory.Get("h_data")
     h_data.SetLineColorAlpha(2,0.9)
  
     _peak, _sigma, _cout, _error = fit(h_data,outname="{}_CH{}".format(Sample_name,idet))
     if Correction: _cout_corr=correction(_peak, _cout, idet)

     print("===============================================")
     print("Data:")
     for ip in range(len(_peak)):
        if Correction:
           print("{0} | Peak : {1:.2f} | Sigma : {2:.2f} | Intensity : {3:.1f} | Corr. Inten. : {4:.1f} | Error : {5:.1f}".format(name_list[ip],_peak[ip], _sigma[ip], _cout[ip], _cout_corr[ip], _error[ip]))
           hout.SetBinContent(ip+1,_cout_corr[ip])
           hout.SetBinError(ip+1,_error[ip])
        else:
           print("{0} | Peak : {1:.2f} | Sigma : {2:.2f} | Intensity : {3:.1f} | Error : {4:.1f}".format(name_list[ip],_peak[ip], _sigma[ip], _cout[ip], _error[ip]))
           hout.SetBinContent(ip+1,_cout[ip])
           hout.SetBinError(ip+1,_error[ip])

     f_out.cd()
     hout.Write()
