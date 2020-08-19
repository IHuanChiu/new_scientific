# - - - - - - - - - - - enum defs  - - - - - - - - - - - - #
IsRandom = True

#keV
EnergyCut      = 10
ADCUpperBound  = 1000
DeltaEnergy    = 5
ClusterMatch   = 10
UTOfRotation   = 1583670785
DEG = u"\xb0"

DEFAULT  = u'\x1b[39;49m'
BLUE     = u'\x1b[34m'
BLUEBOLD = u'\x1b[1;34m'
RED      = u'\x1b[31m'
REDBOLD  = u'\x1b[1;31m'
REDBKG   = u'\x1b[1;41;37m'
YELLOW   = u'\x1b[33m'
UNSET    = u'\x1b[0m'

import math
def getangle(hist_name):
    n_angle_step = 16 # number of roration steps
    initposition = 0 # if the rotation is not start from 0 angle
    if "20200307a" in hist_name:
       if "00057" in hist_name:   return 0  * 2*(math.pi)/n_angle_step
       elif "00058" in hist_name: return 1  * 2*(math.pi)/n_angle_step
       elif "00059" in hist_name: return 2  * 2*(math.pi)/n_angle_step
       elif "00060" in hist_name: return 3  * 2*(math.pi)/n_angle_step
       elif "00061" in hist_name: return 4  * 2*(math.pi)/n_angle_step
       elif "00062" in hist_name: return 5  * 2*(math.pi)/n_angle_step
       elif "00063" in hist_name: return 6  * 2*(math.pi)/n_angle_step
       elif "00064" in hist_name: return 7  * 2*(math.pi)/n_angle_step
       elif "00065" in hist_name: return 8  * 2*(math.pi)/n_angle_step
       elif "00066" in hist_name: return 9  * 2*(math.pi)/n_angle_step
       elif "00067" in hist_name: return 10 * 2*(math.pi)/n_angle_step
       elif "00068" in hist_name: return 11 * 2*(math.pi)/n_angle_step
       elif "00069" in hist_name: return 12 * 2*(math.pi)/n_angle_step
       elif "00070" in hist_name: return 13 * 2*(math.pi)/n_angle_step
       elif "00071" in hist_name: return 14 * 2*(math.pi)/n_angle_step
       elif "00072" in hist_name: return 15 * 2*(math.pi)/n_angle_step
       elif "00073" in hist_name: return 0 * 2*(math.pi)/n_angle_step
    elif "test_f" in hist_name:
       if   "00001" in hist_name: return 0  * 2*(math.pi)/n_angle_step
       elif "00002" in hist_name: return 1  * 2*(math.pi)/n_angle_step
       elif "00003" in hist_name: return 2  * 2*(math.pi)/n_angle_step
       elif "00004" in hist_name: return 3  * 2*(math.pi)/n_angle_step
       elif "00005" in hist_name: return 4  * 2*(math.pi)/n_angle_step
       elif "00006" in hist_name: return 5  * 2*(math.pi)/n_angle_step
       elif "00007" in hist_name: return 6  * 2*(math.pi)/n_angle_step
       elif "00008" in hist_name: return 7  * 2*(math.pi)/n_angle_step
       elif "00009" in hist_name: return 8  * 2*(math.pi)/n_angle_step
       elif "00010" in hist_name: return 9  * 2*(math.pi)/n_angle_step
       elif "00011" in hist_name: return 10 * 2*(math.pi)/n_angle_step
       elif "00012" in hist_name: return 11 * 2*(math.pi)/n_angle_step
       elif "00013" in hist_name: return 12 * 2*(math.pi)/n_angle_step
       elif "00014" in hist_name: return 13 * 2*(math.pi)/n_angle_step
       elif "00015" in hist_name: return 14 * 2*(math.pi)/n_angle_step
       elif "00016" in hist_name: return 15 * 2*(math.pi)/n_angle_step
       elif "00017" in hist_name: return 0  * 2*(math.pi)/n_angle_step
       elif "00018" in hist_name: return 1  * 2*(math.pi)/n_angle_step
       elif "00019" in hist_name: return 2  * 2*(math.pi)/n_angle_step
       elif "00020" in hist_name: return 3  * 2*(math.pi)/n_angle_step
       elif "00021" in hist_name: return 4  * 2*(math.pi)/n_angle_step
       elif "00022" in hist_name: return 5  * 2*(math.pi)/n_angle_step
       elif "00023" in hist_name: return 6  * 2*(math.pi)/n_angle_step
       elif "00024" in hist_name: return 7  * 2*(math.pi)/n_angle_step
       elif "00025" in hist_name: return 8  * 2*(math.pi)/n_angle_step
       elif "00026" in hist_name: return 9  * 2*(math.pi)/n_angle_step
       elif "00027" in hist_name: return 10 * 2*(math.pi)/n_angle_step
       elif "00028" in hist_name: return 11 * 2*(math.pi)/n_angle_step
       elif "00029" in hist_name: return 12 * 2*(math.pi)/n_angle_step
       elif "00030" in hist_name: return 13 * 2*(math.pi)/n_angle_step
       elif "00031" in hist_name: return 14 * 2*(math.pi)/n_angle_step
       elif "00032" in hist_name: return 15 * 2*(math.pi)/n_angle_step
       elif "00033" in hist_name: return  0 * 2*(math.pi)/n_angle_step
       elif "00034" in hist_name: return 1  * 2*(math.pi)/n_angle_step
       elif "00035" in hist_name: return 2  * 2*(math.pi)/n_angle_step
       elif "00036" in hist_name: return 3  * 2*(math.pi)/n_angle_step
       elif "00037" in hist_name: return 4  * 2*(math.pi)/n_angle_step
       elif "00038" in hist_name: return 5  * 2*(math.pi)/n_angle_step
       elif "00039" in hist_name: return 6  * 2*(math.pi)/n_angle_step
       elif "00040" in hist_name: return 7  * 2*(math.pi)/n_angle_step
       elif "00041" in hist_name: return 8  * 2*(math.pi)/n_angle_step
       elif "00042" in hist_name: return 9  * 2*(math.pi)/n_angle_step
       elif "00043" in hist_name: return 10 * 2*(math.pi)/n_angle_step
       elif "00044" in hist_name: return 11 * 2*(math.pi)/n_angle_step
       elif "00045" in hist_name: return 12 * 2*(math.pi)/n_angle_step
       elif "00046" in hist_name: return 13 * 2*(math.pi)/n_angle_step
       elif "00047" in hist_name: return 14 * 2*(math.pi)/n_angle_step
       elif "00048" in hist_name: return 15 * 2*(math.pi)/n_angle_step
       elif "00049" in hist_name: return  0 * 2*(math.pi)/n_angle_step
       elif "00050" in hist_name: return 1  * 2*(math.pi)/n_angle_step
       elif "00051" in hist_name: return 2  * 2*(math.pi)/n_angle_step
       elif "00052" in hist_name: return 3  * 2*(math.pi)/n_angle_step
       elif "00053" in hist_name: return 4  * 2*(math.pi)/n_angle_step
       elif "00054" in hist_name: return 5  * 2*(math.pi)/n_angle_step
       elif "00055" in hist_name: return 6  * 2*(math.pi)/n_angle_step
       elif "00056" in hist_name: return 7  * 2*(math.pi)/n_angle_step
       elif "00057" in hist_name: return 8  * 2*(math.pi)/n_angle_step
    else:
       if   "h0_2d"  in hist_name: return (initposition + 0 )  * 2*(math.pi)/n_angle_step
       elif "h1_2d"  in hist_name: return (initposition + 1 )  * 2*(math.pi)/n_angle_step
       elif "h2_2d"  in hist_name: return (initposition + 2 )  * 2*(math.pi)/n_angle_step
       elif "h3_2d"  in hist_name: return (initposition + 3 )  * 2*(math.pi)/n_angle_step
       elif "h4_2d"  in hist_name: return (initposition + 4 )  * 2*(math.pi)/n_angle_step
       elif "h5_2d"  in hist_name: return (initposition + 5 )  * 2*(math.pi)/n_angle_step
       elif "h6_2d"  in hist_name: return (initposition + 6 )  * 2*(math.pi)/n_angle_step
       elif "h7_2d"  in hist_name: return (initposition + 7 )  * 2*(math.pi)/n_angle_step
       elif "h8_2d"  in hist_name: return (initposition + 8 )  * 2*(math.pi)/n_angle_step
       elif "h9_2d"  in hist_name: return (initposition + 9 )  * 2*(math.pi)/n_angle_step
       elif "h10_2d" in hist_name: return (initposition + 10)  * 2*(math.pi)/n_angle_step
       elif "h11_2d" in hist_name: return (initposition + 11)  * 2*(math.pi)/n_angle_step
       elif "h12_2d" in hist_name: return (initposition + 12)  * 2*(math.pi)/n_angle_step
       elif "h13_2d" in hist_name: return (initposition + 13)  * 2*(math.pi)/n_angle_step
       elif "h14_2d" in hist_name: return (initposition + 14)  * 2*(math.pi)/n_angle_step
       elif "h15_2d" in hist_name: return (initposition + 15)  * 2*(math.pi)/n_angle_step
       elif "h16_2d" in hist_name: return (initposition + 15)  * 2*(math.pi)/n_angle_step
       elif "h17_2d" in hist_name: return (initposition + 14)  * 2*(math.pi)/n_angle_step
       elif "h18_2d" in hist_name: return (initposition + 13)  * 2*(math.pi)/n_angle_step
       elif "h19_2d" in hist_name: return (initposition + 12)  * 2*(math.pi)/n_angle_step
       elif "h20_2d" in hist_name: return (initposition + 11)  * 2*(math.pi)/n_angle_step
       elif "h21_2d" in hist_name: return (initposition + 10)  * 2*(math.pi)/n_angle_step
       elif "h22_2d" in hist_name: return (initposition + 9 )  * 2*(math.pi)/n_angle_step
       elif "h23_2d" in hist_name: return (initposition + 8 )  * 2*(math.pi)/n_angle_step
       elif "h24_2d" in hist_name: return (initposition + 7 )  * 2*(math.pi)/n_angle_step
       elif "h25_2d" in hist_name: return (initposition + 6 )  * 2*(math.pi)/n_angle_step
       elif "h26_2d" in hist_name: return (initposition + 5 )  * 2*(math.pi)/n_angle_step
       elif "h27_2d" in hist_name: return (initposition + 4 )  * 2*(math.pi)/n_angle_step
       elif "h28_2d" in hist_name: return (initposition + 3 )  * 2*(math.pi)/n_angle_step
       elif "h29_2d" in hist_name: return (initposition + 2 )  * 2*(math.pi)/n_angle_step
       elif "h30_2d" in hist_name: return (initposition + 1 )  * 2*(math.pi)/n_angle_step
       else:
          print("Check hist name !")

def findangle(UTtime):
    _nstep=16 
    _RT=1800 # rotation time 1800 s
    return (int(UTtime/_RT)%_nstep) * 2*(math.pi)/_nstep

## EOF
