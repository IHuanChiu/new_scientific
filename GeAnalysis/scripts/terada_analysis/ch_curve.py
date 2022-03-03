import os, ROOT

ROOT.gErrorIgnoreLevel = ROOT.kFatal
__location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
ROOT.gROOT.LoadMacro( __location__+'/AtlasStyle/AtlasStyle.C')
ROOT.SetAtlasStyle()

ref_name="_ref" # none or _ref

def getfile(_fname, hist_index):
    _glist, _flist, _clist = [],[],[]
    _f = ROOT.TFile(_fname,"read")
    for j in range(7):
       _name, _name2 = "_"+str(hist_index)+"_"+str(j), "_"+str(hist_index+1)+"_"+str(j)
       _glist.append(_f.Get("gr"+_name))
       _flist.append(_f.Get("fline"+_name2))
    return _glist, _flist

def plot(_hlist):
    leg = ROOT.TLegend(.75,.2,.9,.50)
    leg.SetFillColor(0)
    leg.SetLineColor(0)
    leg.SetBorderSize(0)
    c1 = ROOT.TCanvas("cc","cc",1000,800)
    c1.cd()
    for _i in range(len(_hlist)):
       _hlist[_i].SetLineColor(_i+1)
       _hlist[_i].SetMarkerColor(_i+1)
       if _i == 0:
          _hlist[_i].Draw()
          leg.AddEntry(_hlist[_i],  "All", "l")
       else:
          _hlist[_i].Draw("same")
          leg.AddEntry(_hlist[_i],  "Ch{}".format(_i), "l")
    return c1, leg

if __name__=="__main__":

   for fig_index in range(5):
      gr_list, fline_list = getfile("comparison_output{}.root".format(ref_name),fig_index) 
   
      _c1,_leg=plot(gr_list) 
      _c1.cd(); _leg.Draw("same")
      _c1.SaveAs("/Users/chiu.i-huan/Desktop/temp_output/ch_com_gr_plot{0}{1}.pdf".format(fig_index,ref_name))
   
      _c2,_leg2=plot(fline_list) 
      _c2.cd(); _leg2.Draw("same")
      _c2.SaveAs("/Users/chiu.i-huan/Desktop/temp_output/ch_com_fline_plot{0}{1}.pdf".format(fig_index,ref_name))
