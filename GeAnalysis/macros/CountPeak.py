import sys,os,argparse,random,math,ROOT,yaml

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
       print(" ============================================== ")
       print(" Current file : {}".format(inputfile))
       _inf = ROOT.TFile(inputfile,"read")
       _h = _inf.Get("Energy")
   
   
       for prop, propv in conf.items():
          if prop == "Input": continue
          for _item in conf[prop]:
             for _prop, _propv in _item.items():
                _atom=_prop
                for _ienergy in _item[_prop]:
                   e_central=_ienergy
                   _3sigma=get3sigma(e_central)
                   Type=neighbor_exit(_h, e_central,_3sigma)
                   n_signal=_h.Integral(_h.FindBin(e_central-_3sigma),_h.FindBin(e_central+_3sigma))
                   if Type == "None":
                      n_bkg_down=_h.Integral(_h.FindBin(e_central-_3sigma*2),_h.FindBin(e_central-_3sigma))
                      n_bkg_up=_h.Integral(_h.FindBin(e_central+_3sigma),_h.FindBin(e_central+_3sigma*2))
                      final_count = n_signal-n_bkg_down-n_bkg_up
                      error=math.sqrt(math.pow(math.sqrt(n_signal),2)+math.pow(math.sqrt(n_bkg_down+n_bkg_up),2))
                   if Type == "Up":
                      n_bkg_down=_h.Integral(_h.FindBin(e_central-_3sigma*2),_h.FindBin(e_central-_3sigma))
                      final_count = n_signal-2*n_bkg_down
                      error=math.sqrt(math.pow(math.sqrt(n_signal),2)+math.pow(math.sqrt(2*n_bkg_down),2))
                   if Type == "Down":
                      n_bkg_up=_h.Integral(_h.FindBin(e_central+_3sigma),_h.FindBin(e_central+_3sigma*2))
                      final_count = n_signal-2*n_bkg_up
                      error=math.sqrt(math.pow(math.sqrt(n_signal),2)+math.pow(math.sqrt(2*n_bkg_up),2))

                   if final_count < 0 or final_count < error*2: 
                      print(" Atom : {0},  Energy : \033[1;36m {1:.2f} \033[0m, Count : \033[1;35m {2} \033[0m ".format(_atom,e_central, "No Peak"))
                   else:
                      if Type != "None":
                         print(" Atom : {0},  Energy : \033[1;36m {1:.2f} \033[0m, Count : \033[1;32m {2} \033[0m ({4}) , Type : \033[1;33m {3} \033[0m".format(_atom,e_central, int(final_count), Type, int(error)))
                      else:
                         print(" Atom : {0},  Energy : \033[1;36m {1:.2f} \033[0m, Count : \033[1;32m {2} \033[0m ({4}), Type : {3}".format(_atom,e_central, int(final_count), Type, int(error)))

       print(" ============================================== ")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument( "-y", "--yamlfile", type=str, default="./configs/muonXray_EnergyTable.yaml", help="Yaml File Name")
    args = parser.parse_args()

    main( args)
