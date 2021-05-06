//
// The "SpectrumFit" macro fits 1D spectra using either the AWMI method
// (an algorithm without matrix inversion) or the Stiefel-Hestens method
// (a conjugate gradient algorithm) from the "TSpectrumFit" class.
// The "TSpectrum" class is used to find peaks.
//
// To try this macro, in a ROOT (5 or 6) prompt, do ...
// ... for the "AWMI" method ...
// .x SpectrumFit.cxx ... or ... .x SpectrumFit.cxx++
// SpectrumFit(); // another random set of peaks (integer areas)
// SpectrumFit(0, kFALSE); // another random set of peaks (integer heights)
// ... for the "Stiefel-Hestens" method ...
// .x SpectrumFit.cxx(1) ... or ... .x SpectrumFit.cxx++(1)
// SpectrumFit(1); // another random set of peaks (integer areas)
// SpectrumFit(1, kFALSE); // another random set of peaks (integer heights)
//
// Last update: Wed Mar  7 20:04:00 UTC 2018
//
// Changes:
// 2018.03.07 - (initial version)
//
// Modified:
// Ajay Y. Deo
// IIT Roorkee, India
// June 17, 2020
// ajay.deo@ph.iitr.ac.in
//

#include "TROOT.h"
#include "TMath.h"
#include "TRandom.h"
#include "TFile.h"
#include "TH1.h"
#include "TF1.h"
#include "TCanvas.h"
#include "TSpectrum.h"
#include "TSpectrumFit.h"
#include "TPolyMarker.h"
#include "TList.h"

#include <iostream>

TH1F *SpectrumFit_Create_Spectrum(const Bool_t norm = kTRUE) {
  Int_t nbins = 1000;
  Double_t xmin = -10., xmax = 10.;
  delete gROOT->FindObject("h"); // prevent "memory leak"
  TH1F *h = new TH1F("h", "simulated spectrum", nbins, xmin, xmax);
  h->SetStats(kFALSE);
  TF1 f("f", "TMath::Gaus(x, [0], [1], 0)", xmin, xmax);
  // f.SetParNames("mean", "sigma");
  gRandom->SetSeed(0); // make it really random
  // create well separated peaks with exactly known means, heights and areas
  // note: TSpectrumFit assumes that all peaks have the same sigma
  Double_t sigma =
    (xmax - xmin) / Double_t(nbins) * (2. + gRandom->Integer(2));
  Int_t npeaks = 0;
  while (xmax > (xmin + 8. * sigma)) {
    npeaks++;
    xmin += 4. * sigma; // "mean"
    f.SetParameters(xmin, sigma);
    Double_t height = 1. * (1. + gRandom->Integer(10));
    if (norm) height /= sigma * TMath::Sqrt(TMath::TwoPi());
    h->Add(&f, height, "I"); // "" ... or ... "I"
    std::cout << "created "
              << xmin << " "
              << height << " "
              << (height * sigma * TMath::Sqrt(TMath::TwoPi())) << std::endl;
    xmin += 4. * sigma;
  }
  std::cout << "the total number of created peaks = " << npeaks
            << " with sigma = " << sigma << std::endl;
  return h;
}

void SpectrumFit_v2(const Int_t method = 0,
                 const Bool_t norm = kTRUE) {
#if 0 /* 0 or 1 */
  TH1F *h = SpectrumFit_Create_Spectrum(norm);
#else /* 0 or 1 */
//  const char *f_name = "/Users/chiu.i-huan/Desktop/hist.root";
//  const char *h_name = "AB01"; // must be a "fix bin size" TH1F
  const char *f_name = "/Users/chiu.i-huan/Desktop/new_scientific/GeAnalysis/data/JPARC_2021Apri/Black/203086_beam.root";
  const char *h_name = "Energy"; // must be a "fix bin size" TH1F
  delete gROOT->FindObject(h_name); // prevent "memory leak"
  TFile *f = TFile::Open(f_name);
  if ((!f) || f->IsZombie()) { delete f; return; } // just a precaution
  TH1F *h; f->GetObject(h_name, h);
  if (!h)  { delete f; return; } // just a precaution
  h->SetDirectory(gROOT);
  delete f; // no longer needed
#endif /* 0 or 1 */
  TCanvas *cFit =
    ((TCanvas *)(gROOT->GetListOfCanvases()->FindObject("cFit")));
  if (!cFit) cFit = new TCanvas("cFit", "cFit", 10, 10, 1000, 700);
  else cFit->Clear();
  h->Draw();
  //h->Draw("L");
  Int_t i, nfound, bin;
  Int_t nbins = h->GetNbinsX();
#if ROOT_VERSION_CODE >= ROOT_VERSION(6,00,00)
  // ROOT 6
  Double_t *source = new Double_t[nbins];
  Double_t *dest = new Double_t[nbins];
  Double_t *sourceb = new Double_t[nbins];
  Double_t *destb = new Double_t[nbins];
#else
  // ROOT 5
  Float_t *source = new Float_t[nbins];
  Float_t *dest = new Float_t[nbins];
  Float_t *sourceb = new Float_t[nbins];
  Float_t *destb = new Float_t[nbins];
#endif

  TH1F *d2 = (TH1F*)h->Clone("d2");
  TH1F *h2 = (TH1F*)h->Clone("h2");

#if 0 /* 0 or 1 */	//Estimate and subtract background

  TSpectrum *sb = new TSpectrum(); // note: default maxpositions = 100
  for (i = 0; i < nbins; i++) sourceb[i] = h->GetBinContent(i + 1);

   sb->Background(sourceb,nbins,16,TSpectrum::kBackDecreasingWindow,
                 TSpectrum::kBackOrder2,kTRUE,
                 TSpectrum::kBackSmoothing3,kFALSE);
   for (i = 0; i < nbins; i++) d2->SetBinContent(i + 1,sourceb[i]);
   d2->SetLineColor(kGreen);
   d2->Draw("SAME");
   //d2->Draw();
   h2->Add(d2,-1);
#endif /* 0 or 1 */
   h2->SetLineColor(kMagenta);
   h2->Draw("same");

  TSpectrum *s = new TSpectrum(); // note: default maxpositions = 100
  for (i = 0; i < nbins; i++) source[i] = 0;
  for (i = 0; i < nbins; i++) source[i] = h2->GetBinContent(i + 1);
  // searching for candidate peaks positions (very sensitive to sigma)
  Double_t sigma = 3.; // in "bin numbers"
  Double_t sigmaErr = 10.; // in "SearchHighRes" below used as the "threshold"
  nfound =
    s->SearchHighRes(source, dest, nbins, sigma, sigmaErr, kFALSE, 10000, kFALSE, 0);
  // filling in the initial estimates of the input parameters
  Bool_t *FixPos = new Bool_t[nfound];
  Bool_t *FixAmp = new Bool_t[nfound];
  for(i = 0; i < nfound; i++) FixAmp[i] = FixPos[i] = kFALSE;
#if ROOT_VERSION_CODE >= ROOT_VERSION(6,00,00)
  Double_t *Pos, *Amp = new Double_t[nfound]; // ROOT 6
#else
  Float_t *Pos, *Amp = new Float_t[nfound]; // ROOT 5
#endif
  Pos = s->GetPositionX(); // 0 ... (nbins - 1)
  for (i = 0; i < nfound; i++) {
    bin = 1 + Int_t(Pos[i] + 0.5); // the "nearest" bin
    Amp[i] = h2->GetBinContent(bin);
  }
  TSpectrumFit *pfit = new TSpectrumFit(nfound);
  pfit->SetFitParameters(0, (nbins - 1), 1000, 0.1,
                         TSpectrumFit::kFitOptimChiCounts,
                         TSpectrumFit::kFitAlphaHalving,
                         TSpectrumFit::kFitPower2,
                         TSpectrumFit::kFitTaylorOrderFirst);
  pfit->SetPeakParameters(sigma, kFALSE, Pos, FixPos, Amp, FixAmp);
  //pfit->SetBackgroundParameters(source[0], kFALSE, 0., kFALSE, 0., kFALSE);
  if (method == 0) pfit->FitAwmi(source); else pfit->FitStiefel(source);
  Double_t *Positions = pfit->GetPositions();
  Double_t *PositionsErrors = pfit->GetPositionsErrors();
  Double_t *Amplitudes = pfit->GetAmplitudes();
  Double_t *AmplitudesErrors = pfit->GetAmplitudesErrors();
  Double_t *Areas = pfit->GetAreas();
  Double_t *AreasErrors = pfit->GetAreasErrors();

  delete gROOT->FindObject("d"); // prevent "memory leak"

  TH1F *d = new TH1F(*h2); d->SetNameTitle("d", ""); d->Reset("M");
  for (i = 0; i < nbins; i++) d->SetBinContent(i + 1, source[i]);

  Double_t x1 = d->GetBinCenter(1), dx = d->GetBinWidth(1);
  pfit->GetSigma(sigma, sigmaErr);

#if 1 /* 0 or 1 */
  // current TSpectrumFit needs a sqrt(2) correction factor for sigma
  sigma /= TMath::Sqrt2(); sigmaErr /= TMath::Sqrt2();
  // convert "bin numbers" into "x-axis values"
  sigma *= dx; sigmaErr *= dx;
#endif /* 0 or 1 */

  std::cout << "the total number of found peaks = " << nfound
            << " with sigma = " << sigma << " (+-" << sigmaErr << ")"
            << std::endl;
  std::cout << "fit chi^2 = " << pfit->GetChi() << std::endl;

  for (i = 0; i < nfound; i++) {
    bin = 1 + Int_t(Positions[i] + 0.5); // the "nearest" bin
    Pos[i] = d->GetBinCenter(bin);
    Amp[i] = d->GetBinContent(bin);
#if 1 /* 0 or 1 */
    // convert "bin numbers" into "x-axis values"
    Positions[i] = x1 + Positions[i] * dx;
    PositionsErrors[i] *= dx;
    Areas[i] *= dx;
    AreasErrors[i] *= dx;
#endif /* 0 or 1 */
    std::cout << "found "
              << Positions[i] << " (+-" << PositionsErrors[i] << ") "
              << Amplitudes[i] << " (+-" << AmplitudesErrors[i] << ") "
              << Areas[i] << " (+-" << AreasErrors[i] << ")"
              << std::endl;
  }

  d->SetLineColor(kRed); d->SetLineWidth(1);
  d->Draw("SAME L");

  TPolyMarker *pm =
    ((TPolyMarker*)(h2->GetListOfFunctions()->FindObject("TPolyMarker")));
  if (pm) {
    h2->GetListOfFunctions()->Remove(pm);
    delete pm;
  }
  pm = new TPolyMarker(nfound, Pos, Amp);
  h2->GetListOfFunctions()->Add(pm);
  pm->SetMarkerStyle(23);
  pm->SetMarkerColor(kRed);
  pm->SetMarkerSize(1);
  // cleanup
  delete pfit;
  delete [] Amp;
  delete [] FixAmp;
  delete [] FixPos;
  delete s;
  delete [] dest;
  delete [] source;
  return;
}

// end of file SpectrumFit.cxx by Silesius Anonymus
