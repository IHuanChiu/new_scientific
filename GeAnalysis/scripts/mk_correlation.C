/* """
This module provides the correlation plots
   """
__author__    = "I-Huan CHIU"
__email__     = "ichiu@chem.sci.osaka-u.ac.jp"
__created__   = "2021-05-18"
__copyright__ = "Copyright 2021 I-Huan CHIU"
__license__   = "GPL http://www.gnu.org/licenses/gpl.html"
// */

void mk_correlation(){

   // si32 : 76keV
   // al43 : 23keV
   // al42 : 89keV
   // fe54 : 43keV
   // fe43 : 92keV

   double black_si32 =
   double white_si32 =
   double dew_si32 =
   double dewbar_si32 =
   double dewbar35_si32 =

   TGraph* gr1 = new TGraph(1,x,y);//white
   TGraph* gr2 = new TGraph(1,x,y);//black
   TGraph* gr3 = new TGraph(3,x,y);//dew


} 
