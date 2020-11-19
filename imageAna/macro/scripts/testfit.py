#   Example of a fitting program
#   ============================
#
#   The fitting function fcn is a simple chisquare function
#   The data consists of 5 data points (arrays x,y,z) + the errors in errorsz
#   More details on the various functions or parameters for these functions
#   can be obtained in an interactive ROOT session with:
#    Root > TMinuit *minuit = new TMinuit(10);
#    Root > minuit->mnhelp("*",0)  to see the list of possible keywords
#    Root > minuit->mnhelp("SET",0) explains most parameters


from ROOT import TMinuit
from array import array;
import ctypes

Error = 0;
z = array( 'f', ( 1., 0.96, 0.89, 0.85, 0.78 ) )
errorz = array( 'f', 5*[0.01] )

x = array( 'f', ( 1.5751, 1.5825,  1.6069,  1.6339,   1.6706  ) )
y = array( 'f', ( 1.0642, 0.97685, 1.13168, 1.128654, 1.44016 ) )

ncount = 0

##______________________________________________________________________________
def testfit():

   gMinuit = TMinuit(5)
   gMinuit.SetFCN( fcn )

   arglist = array( 'd', 10*[0.] )
   ierflg = ctypes.c_int(1982)

   arglist[0] = 1
   gMinuit.mnexcm( "SET ERR", arglist, 1, ierflg )

 # Set starting values and step sizes for parameters
   vstart = array( 'd', ( 3,  1,  0.1,  0.01  ) )
   step   = array( 'd', ( 0.1, 0.1, 0.01, 0.001 ) )
   gMinuit.mnparm( 0, "a1", vstart[0], step[0], 0, 0, ierflg )
   gMinuit.mnparm( 1, "a2", vstart[1], step[1], 0, 0, ierflg )
   gMinuit.mnparm( 2, "a3", vstart[2], step[2], 0, 0, ierflg )
   gMinuit.mnparm( 3, "a4", vstart[3], step[3], 0, 0, ierflg )

 # Now ready for minimization step
   arglist[0] = 500
   arglist[1] = 1.
   gMinuit.mnexcm( "MIGRAD", arglist, 2, ierflg )

 # Print results
   amin, edm, errdef = map(ctypes.c_double, (0.18, 0.19, 0.20))
   nvpar, nparx, icstat = map(ctypes.c_int, (1983, 1984, 1985))
   gMinuit.mnstat( amin, edm, errdef, nvpar, nparx, icstat )
   gMinuit.mnprin( 3, amin.value )


##______________________________________________________________________________
def fcn( npar, gin, f, par, iflag ):
   global ncount
   nbins = 5

 # calculate chisquare
   chisq, delta = 0., 0.
   for i in range(nbins):
      delta  = (z[i]-func(x[i],y[i],par))/errorz[i]
      chisq += delta*delta

   f[0] = chisq
   ncount += 1

def func( x, y, par ):
   value = ( (par[0]*par[0])/(x*x)-1)/ ( par[1]+par[2]*y-par[3]*y*y)
   return value


##______________________________________________________________________________
if __name__ == '__main__':
   testfit()

