# - - - - - - - - - - - enum defs  - - - - - - - - - - - - #
IsRandom = True

#keV
EnergyCut      = 10
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

def reset(cut, deltaE):
    EnergyCut = cut
    DeltaEnergy = deltaE
## EOF
