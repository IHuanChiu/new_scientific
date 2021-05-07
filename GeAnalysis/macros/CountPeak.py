import sys,os,argparse,random,math,ROOT,yaml,ctypes

def get_yaml_conf(yamlfile):
    if not os.path.isfile(yamlfile):
        raise Exception("File {} not found. Please supply valid yaml input file.".format(yamlfile))
    with open(yamlfile) as f:
       data = yaml.load(f, Loader=yaml.FullLoader)
    return data

def get3sigma(_e):
    _s_e24k=0.152#keV
    _s_e134k=0.268#keV
    return 3*(0.152+((_s_e134k-_s_e24k)/(134-24))*_e)
#    p0=0.0311232
#    p1=0.00459369
#    p2=-1.27339e-05
#    return 3*p2*pow(_e,2)+p1*_e+p0

def dofit(_h,_e,_sig):
    #TODO dofit to find sigma and energy ???
    f1 = ROOT.TF1("f1","gaus",_h.GetXaxis().GetXmin(),_h.GetXaxis())
    return e,sig

def neighbor_exit(_h,_e,_3sigma):
    bin_down6sigma=_h.FindBin(_e-2*_3sigma)
    bin_down3sigma=_h.FindBin(_e-1*_3sigma)
    bin_up3sigma=_h.FindBin(_e+1*_3sigma)
    bin_up6sigma=_h.FindBin(_e+2*_3sigma)
    maxbin_central, maxbin_down, maxbin_up=-1,-1,-1
    for i in range(bin_down3sigma, bin_up3sigma):
       if _h.GetBinContent(i) > maxbin_central: maxbin_central = _h.GetBinContent(i)
    for i in range(bin_down6sigma, bin_down3sigma):
       if _h.GetBinContent(i) > maxbin_down: maxbin_down = _h.GetBinContent(i)
    for i in range(bin_up3sigma, bin_up6sigma):
       if _h.GetBinContent(i) > maxbin_up: maxbin_up = _h.GetBinContent(i)

    if math.fabs(1-(maxbin_up/maxbin_down)) < 0.5: 
       # no neighbor peak
       return "None"
    elif maxbin_up/maxbin_down > 1:
       return "Up"
    else:
       return "Down"

def main(args):
    conf = get_yaml_conf(args.yamlfile)
    file_list=[]
    for prop, propv in conf.items():
       if prop == "Input":
          for _item in conf[prop]:
             for _prop, _propv in _item.items():
                if _prop == "path": _filepath = _item[_prop][0]
                else: file_list.append(_filepath+_item[_prop][0])

    for inputfile in file_list:
       _inf = ROOT.TFile(inputfile,"read")
       _h = _inf.Get("Energy")
       print(" ============================================== ")
       print(" Current file : {}".format(inputfile))
       print(" Total Events: {}".format(int(_h.GetEntries())))
   
   
       for prop, propv in conf.items():
          if prop == "Input": continue
          for _nameconf in conf[prop]:
             print("\033[1m Atom : {0}\033[0m".format(_nameconf))
             for _item in conf[prop][_nameconf]:
                for _prop, _propv in _item.items():
                   _line=_prop
                   e_central=_item[_prop][0]
                   _3sigma=_item[_prop][1]*3
                   Type=neighbor_exit(_h, e_central,_3sigma)
                   error_main, error_up, error_down=ctypes.c_double(0),ctypes.c_double(0),ctypes.c_double(0)
                   #n_signal=_h.Integral(_h.FindBin(e_central-_3sigma),_h.FindBin(e_central+_3sigma))
                   n_signal=_h.IntegralAndError(_h.FindBin(e_central-_3sigma),_h.FindBin(e_central+_3sigma),error_main)
                   if Type == "None":
                      n_bkg_down=_h.IntegralAndError(_h.FindBin(e_central-_3sigma*2),_h.FindBin(e_central-_3sigma),error_down)
                      n_bkg_up=_h.IntegralAndError(_h.FindBin(e_central+_3sigma),_h.FindBin(e_central+_3sigma*2),error_up)
                      final_count = n_signal-n_bkg_down-n_bkg_up
                      error=math.sqrt(math.pow(error_main.value,2)+math.pow(error_down.value,2)+math.pow(error_up.value,2))
                   if Type == "Up":
                      n_bkg_down=_h.IntegralAndError(_h.FindBin(e_central-_3sigma*2),_h.FindBin(e_central-_3sigma),error_down)
                      final_count = n_signal-2*n_bkg_down
                      error=math.sqrt(math.pow(error_main.value,2)+math.pow(error_down.value,2)*math.pow(2,2))
                   if Type == "Down":
                      n_bkg_up=_h.IntegralAndError(_h.FindBin(e_central+_3sigma),_h.FindBin(e_central+_3sigma*2),error_up)
                      final_count = n_signal-2*n_bkg_up
                      error=math.sqrt(math.pow(error_main.value,2)+math.pow(error_up.value,2)*math.pow(2,2))
       
                   if final_count < 0 or final_count < error*2: 
                      print("          {0}, Energy : \033[1;36m {1:.2f} \u00B1 {2:.2f}\033[0m, Count : \033[1;35m {3}\033[0m ".format(_prop,e_central,_item[_prop][1], "No Peak"))
                   else:
                      if Type != "None":
                         print("          {0}, Energy : \033[1;36m {1:.2f} \u00B1 {2:.2f}\033[0m, Count : \033[1;32m {3} \u00B1 {5}\033[0m, Type : \033[1;33m {4} \033[0m".format(_prop,e_central,_item[_prop][1], int(final_count), Type, int(error)))
                      else:
                         print("          {0}, Energy : \033[1;36m {1:.2f} \u00B1 {2:.2f}\033[0m, Count : \033[1;32m {3} \u00B1 {5}\033[0m, Type : {4}".format(_prop,e_central,_item[_prop][1], int(final_count), Type, int(error)))

       print(" ============================================== ")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument( "-y", "--yamlfile", type=str, default="./configs/muonXray_EnergyTable.yaml", help="Yaml File Name")
    args = parser.parse_args()

    main( args)
