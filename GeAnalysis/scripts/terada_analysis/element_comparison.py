import os,ROOT,ctypes
ROOT.gErrorIgnoreLevel = ROOT.kFatal
__location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
ROOT.gROOT.LoadMacro( __location__+'/AtlasStyle/AtlasStyle.C')
ROOT.SetAtlasStyle()

input_file="./intensity_files/intensity_sum.root" #black

name_list=["Si32", "Al43", "Al42", "Fe54", "Fe43", "Ca43", "Ca32", "Mg32", "Cu43", "Fe#gamma"]

nbins=int(6800)

def getLatex(ch, x = 0.85, y = 0.85):
    _t = ROOT.TLatex()
    _t.SetNDC()
    _t.SetTextFont( 62 )
    _t.SetTextColor( 36 )
    _t.SetTextSize( 0.08 )
    _t.SetTextAlign( 12 )
    return _t

if __name__=="__main__":

  f_data=ROOT.TFile(input_file,"read")
  h1_white, h1_black, h1_dew, h1_dewbar, h1_dew35 = f_data.Get("white_CH1"), f_data.Get("black_CH1"), f_data.Get("dew_CH1"), f_data.Get("dewbar_CH1"), f_data.Get("dew_35_CH1")
  for i in range(2,7):
     h1_white.Add(f_data.Get("white_CH{}".format(i)),1)
     h1_black.Add(f_data.Get("black_CH{}".format(i)),1)
     h1_dew.Add(f_data.Get("dew_CH{}".format(i)),1)
     h1_dewbar.Add(f_data.Get("dewbar_CH{}".format(i)),1)
     h1_dew35.Add(f_data.Get("dew_35_CH{}".format(i)),1)

  h0 = ROOT.TH1F("sum", "sum",len(name_list),0,len(name_list))  
  h1 = ROOT.TH1F("w", "w",len(name_list),0,len(name_list))  
  h2 = ROOT.TH1F("b", "b",len(name_list),0,len(name_list))  
  h3 = ROOT.TH1F("d", "d",len(name_list),0,len(name_list))  
  h4 = ROOT.TH1F("db", "db",len(name_list),0,len(name_list))  
  h5 = ROOT.TH1F("d35", "d35",len(name_list),0,len(name_list))
  h0.SetTitle(";;X/Si(3-2)")
  h0.GetYaxis().CenterTitle()
  h0.SetMaximum(1.6); h0.SetMinimum(0); 
  for i in range(len(name_list)):
     h0.GetXaxis().SetBinLabel(i+1, name_list[i])
     h1.Fill(i,h1_white.GetBinContent(i+1)/h1_white.GetBinContent(1))
     h2.Fill(i,h1_black.GetBinContent(i+1)/h1_black.GetBinContent(1))
     h3.Fill(i,h1_dew.GetBinContent(i+1)/h1_dew.GetBinContent(1))
     h4.Fill(i,h1_dewbar.GetBinContent(i+1)/h1_dewbar.GetBinContent(1))
     h5.Fill(i,h1_dew35.GetBinContent(i+1)/h1_dew35.GetBinContent(1))
  h1.SetMarkerColor(4);h1.SetLineColor(4);
  h2.SetMarkerColor(2);h2.SetLineColor(2);
  h3.SetMarkerColor(3);h3.SetLineColor(3);
  h4.SetMarkerColor(8);h4.SetLineColor(8);
  h5.SetMarkerColor(5);h5.SetLineColor(5);
  c=ROOT.TCanvas("c","c",1200,800)
  h0.Draw("     hist lp")
  h1.Draw("same hist lp")
  h2.Draw("same hist lp")
  h3.Draw("same hist lp")
  h4.Draw("same hist lp")
  h5.Draw("same hist lp")
  leg = ROOT.TLegend(.60,.7,.9,.90)
  leg.SetFillColor(0)
  leg.SetLineColor(0)
  leg.SetBorderSize(0)
  leg.AddEntry(h1,"White","p")
  leg.AddEntry(h2,"Black","p")
  leg.AddEntry(h3,"DEW","p")
  leg.AddEntry(h4,"DEWbar","p")
  leg.AddEntry(h5,"DEWbar35","p")
  leg.Draw("same")
  c.SaveAs("/Users/chiu.i-huan/Desktop/c_com_ele.pdf")

