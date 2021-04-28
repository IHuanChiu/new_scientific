/// \file
/// \ingroup tutorial_spectrum
/// \notebook
/// Getting Contours From TH2D.
/// Illustrates how to find peaks in histograms.
///
/// This script generates a random number of gaussian peaks
/// on top of a linear background.
/// The position of the peaks is found via TSpectrum and injected
/// as initial values of parameters to make a global fit.
/// The background is computed and drawn on top of the original histogram.
///
/// This script can fit "peaks' heights" or "peaks' areas" (comment out
/// or uncomment the line which defines `__PEAKS_C_FIT_AREAS__`).
///
/// To execute this example, do (in ROOT 5 or ROOT 6):
///
/// ~~~{.cpp}
///  root > .x peaks.C  (generate 10 peaks by default)
///  root > .x peaks.C++ (use the compiler)
///  root > .x peaks.C++(30) (generates 30 peaks)
/// ~~~
///
/// To execute only the first part of the script (without fitting)
/// specify a negative value for the number of peaks, eg
///
/// ~~~{.cpp}
///  root > .x peaks.C(-20)
/// ~~~
///
/// \macro_output
/// \macro_image
/// \macro_code
///
/// \author Rene Brun

#include "TCanvas.h"
#include "TMath.h"
#include "TH1.h"
#include "TF1.h"
#include "TRandom.h"
#include "TSpectrum.h"
#include "TVirtualFitter.h"

//
// Comment out the line below, if you want "peaks' heights".
// Uncomment the line below, if you want "peaks' areas".
//
//#define __PEAKS_C_FIT_AREAS__ 1 /* fit peaks' areas */

Int_t npeaks = 50;
Double_t fpeaks(Double_t *x, Double_t *par) {
   Double_t result = par[0] + par[1]*x[0];
   for (Int_t p=0;p<npeaks;p++) {
      Double_t norm  = par[3*p+2]; // "height" or "area"
      Double_t mean  = par[3*p+3];
      Double_t sigma = par[3*p+4];
#if defined(__PEAKS_C_FIT_AREAS__)
      norm /= sigma * (TMath::Sqrt(TMath::TwoPi())); // "area"
#endif /* defined(__PEAKS_C_FIT_AREAS__) */
      result += norm*TMath::Gaus(x[0],mean,sigma);
   }
   return result;
}
void peaks(Int_t np=50) {
   npeaks = TMath::Abs(np);

   const char *f_name = "/Users/chiu.i-huan/Desktop/new_scientific/GeAnalysis/data/JPARC_2021Apri/Black/203086_beam.root";
   const char *h_name = "Energy"; // must be a "fix bin size" TH1F
   delete gROOT->FindObject(h_name); // prevent "memory leak"
   TFile *ff = new TFile(f_name,"read");
   TH1F *h = (TH1F*)ff->Get(h_name);

   //generate n peaks at random
   Double_t par[3000];
   par[0] = 5;
   par[1] = -0.6/1000;
   Int_t p;
   for (p=0;p<npeaks;p++) {
      par[3*p+2] = 50; // "height"
      par[3*p+3] = 5+gRandom->Rndm()*195; // "mean", gRandom->Rndm(): 0~1
      par[3*p+4] = 0.1+0.5*gRandom->Rndm(); // "sigma"
#if defined(__PEAKS_C_FIT_AREAS__)
      par[3*p+2] *= par[3*p+4] * (TMath::Sqrt(TMath::TwoPi())); // "area"
#endif /* defined(__PEAKS_C_FIT_AREAS__) */
   }
   TF1 *f = new TF1("f",fpeaks,0,200,2+3*npeaks);//name, fcn, xmin, xmax, npar
   f->SetNpx(10000);
   f->SetParameters(par);
   TCanvas *c1 = new TCanvas("c1","c1",10,10,1000,900);
   c1->Divide(1,2);
   c1->cd(1);
   h->Draw();
   TH1F *h2 = (TH1F*)h->Clone("h2");
   //Use TSpectrum to find the peak candidates
   TSpectrum *s = new TSpectrum(2*npeaks);
   s->SetResolution(1);//determines resolution of the neighbouring peaks default value is 1 correspond to 3 sigma distance between peaks.
   Int_t nfound = s->Search(h,0.162809,"",0.005);
   printf("Found %d candidate peaks to fit\n",nfound);
   
   //Print peak position from TSpectrum
   Double_t *xpeaks_ichiu;
   xpeaks_ichiu = s->GetPositionX();
   for (p=0;p<nfound;p++) std::cout << " Found peak at : " << xpeaks_ichiu[p] << std::endl;

   //Estimate background using TSpectrum::Background
   TH1 *hb = s->Background(h,20,"same");
   if (hb) c1->Update();
   if (np <0) return;

   //estimate linear background using a fitting method
   c1->cd(2);
   TF1 *fline = new TF1("fline","pol1",0,200);
   h->Fit("fline","qn");
   //Loop on all found peaks. Eliminate peaks at the background level
   par[0] = fline->GetParameter(0);
   par[1] = fline->GetParameter(1);
   npeaks = 0;
#if ROOT_VERSION_CODE >= ROOT_VERSION(6,00,00)
   Double_t *xpeaks; // ROOT 6
#else
   Float_t *xpeaks; // ROOT 5
#endif
   xpeaks = s->GetPositionX();
   for (p=0;p<nfound;p++) {
      Double_t xp = xpeaks[p];
      std::cout << " Found peak at : " << xp << std::endl;
      Int_t bin = h->GetXaxis()->FindBin(xp);
      Double_t yp = h->GetBinContent(bin);
      if (yp-TMath::Sqrt(yp) < fline->Eval(xp)) continue;
      par[3*npeaks+2] = yp; // "height"
      par[3*npeaks+3] = xp; // "mean"
      par[3*npeaks+4] = 1; // "sigma"
#if defined(__PEAKS_C_FIT_AREAS__)
      par[3*npeaks+2] *= par[3*npeaks+4] * (TMath::Sqrt(TMath::TwoPi())); // "area"
#endif /* defined(__PEAKS_C_FIT_AREAS__) */
      npeaks++;
   }
   printf("Found %d useful peaks to fit\n",npeaks);
   printf("Now fitting: Be patient\n");
   TF1 *fit = new TF1("fit",fpeaks,0,200,2+3*npeaks);
   //we may have more than the default 25 parameters
   TVirtualFitter::Fitter(h2,10+3*npeaks);
   fit->SetParameters(par);
   for (p=0;p<nfound;p++) { 
     Double_t xp = xpeaks[p];
     fit->FixParameter(3*npeaks+3,xp);
   }
   fit->SetNpx(10000);
   h2->Fit("fit");
   c1->SaveAs("test_findpeak.pdf");
}

#if !defined(__CINT__) && defined(__PEAKS_C_FIT_AREAS__)
#undef __PEAKS_C_FIT_AREAS__
#endif /* !defined(__CINT__) && defined(__PEAKS_C_FIT_AREAS__) */
