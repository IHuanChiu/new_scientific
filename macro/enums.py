# - - - - - - - - - - - enum defs  - - - - - - - - - - - - #
IsRandom = True

#keV
EnergyCut      = 8
ADCUpperBound  = 1000
DeltaEnergy    = 5
ClusterMatch   = 10

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
    nstep = 16 # number of roration steps
    if "20200307a" in hist_name:
       if "00057" in hist_name:   return 0  * 2*(math.pi)/nstep
       elif "00058" in hist_name: return 1  * 2*(math.pi)/nstep
       elif "00059" in hist_name: return 2  * 2*(math.pi)/nstep
       elif "00060" in hist_name: return 3  * 2*(math.pi)/nstep
       elif "00061" in hist_name: return 4  * 2*(math.pi)/nstep
       elif "00062" in hist_name: return 5  * 2*(math.pi)/nstep
       elif "00063" in hist_name: return 6  * 2*(math.pi)/nstep
       elif "00064" in hist_name: return 7  * 2*(math.pi)/nstep
       elif "00065" in hist_name: return 8  * 2*(math.pi)/nstep
       elif "00066" in hist_name: return 9  * 2*(math.pi)/nstep
       elif "00067" in hist_name: return 10 * 2*(math.pi)/nstep
       elif "00068" in hist_name: return 11 * 2*(math.pi)/nstep
       elif "00069" in hist_name: return 12 * 2*(math.pi)/nstep
       elif "00070" in hist_name: return 13 * 2*(math.pi)/nstep
       elif "00071" in hist_name: return 14 * 2*(math.pi)/nstep
       elif "00072" in hist_name: return 15 * 2*(math.pi)/nstep
       elif "00073" in hist_name: return 0 * 2*(math.pi)/nstep
    elif "test_f" in hist_name:
       if   "00001" in hist_name: return 0  * 2*(math.pi)/nstep
       elif "00002" in hist_name: return 1  * 2*(math.pi)/nstep
       elif "00003" in hist_name: return 2  * 2*(math.pi)/nstep
       elif "00004" in hist_name: return 3  * 2*(math.pi)/nstep
       elif "00005" in hist_name: return 4  * 2*(math.pi)/nstep
       elif "00006" in hist_name: return 5  * 2*(math.pi)/nstep
       elif "00007" in hist_name: return 6  * 2*(math.pi)/nstep
       elif "00008" in hist_name: return 7  * 2*(math.pi)/nstep
       elif "00009" in hist_name: return 8  * 2*(math.pi)/nstep
       elif "00010" in hist_name: return 9  * 2*(math.pi)/nstep
       elif "00011" in hist_name: return 10 * 2*(math.pi)/nstep
       elif "00012" in hist_name: return 11 * 2*(math.pi)/nstep
       elif "00013" in hist_name: return 12 * 2*(math.pi)/nstep
       elif "00014" in hist_name: return 13 * 2*(math.pi)/nstep
       elif "00015" in hist_name: return 14 * 2*(math.pi)/nstep
       elif "00016" in hist_name: return 15 * 2*(math.pi)/nstep
       elif "00017" in hist_name: return 0 * 2*(math.pi)/nstep
       elif "00018" in hist_name: return 1  * 2*(math.pi)/nstep
       elif "00019" in hist_name: return 2  * 2*(math.pi)/nstep
       elif "00020" in hist_name: return 3  * 2*(math.pi)/nstep
       elif "00021" in hist_name: return 4  * 2*(math.pi)/nstep
       elif "00022" in hist_name: return 5  * 2*(math.pi)/nstep
       elif "00023" in hist_name: return 6  * 2*(math.pi)/nstep
       elif "00024" in hist_name: return 7  * 2*(math.pi)/nstep
       elif "00025" in hist_name: return 8  * 2*(math.pi)/nstep
       elif "00026" in hist_name: return 9  * 2*(math.pi)/nstep
       elif "00027" in hist_name: return 10 * 2*(math.pi)/nstep
       elif "00028" in hist_name: return 11 * 2*(math.pi)/nstep
       elif "00029" in hist_name: return 12 * 2*(math.pi)/nstep
       elif "00030" in hist_name: return 13 * 2*(math.pi)/nstep
       elif "00031" in hist_name: return 14 * 2*(math.pi)/nstep
       elif "00032" in hist_name: return 15 * 2*(math.pi)/nstep
       elif "00033" in hist_name: return 0 * 2*(math.pi)/nstep
       elif "00034" in hist_name: return 1  * 2*(math.pi)/nstep
       elif "00035" in hist_name: return 2  * 2*(math.pi)/nstep
       elif "00036" in hist_name: return 3  * 2*(math.pi)/nstep
       elif "00037" in hist_name: return 4  * 2*(math.pi)/nstep
       elif "00038" in hist_name: return 5  * 2*(math.pi)/nstep
       elif "00039" in hist_name: return 6  * 2*(math.pi)/nstep
       elif "00040" in hist_name: return 7  * 2*(math.pi)/nstep
       elif "00041" in hist_name: return 8  * 2*(math.pi)/nstep
       elif "00042" in hist_name: return 9  * 2*(math.pi)/nstep
       elif "00043" in hist_name: return 10 * 2*(math.pi)/nstep
       elif "00044" in hist_name: return 11 * 2*(math.pi)/nstep
       elif "00045" in hist_name: return 12 * 2*(math.pi)/nstep
       elif "00046" in hist_name: return 13 * 2*(math.pi)/nstep
       elif "00047" in hist_name: return 14 * 2*(math.pi)/nstep
       elif "00048" in hist_name: return 15 * 2*(math.pi)/nstep
       elif "00049" in hist_name: return 0 * 2*(math.pi)/nstep
       elif "00050" in hist_name: return 1  * 2*(math.pi)/nstep
       elif "00051" in hist_name: return 2  * 2*(math.pi)/nstep
       elif "00052" in hist_name: return 3  * 2*(math.pi)/nstep
       elif "00053" in hist_name: return 4  * 2*(math.pi)/nstep
       elif "00054" in hist_name: return 5  * 2*(math.pi)/nstep
       elif "00055" in hist_name: return 6  * 2*(math.pi)/nstep
       elif "00056" in hist_name: return 7  * 2*(math.pi)/nstep
       elif "00057" in hist_name: return 8  * 2*(math.pi)/nstep
    else:
       print("Check hist name !")

## EOF
