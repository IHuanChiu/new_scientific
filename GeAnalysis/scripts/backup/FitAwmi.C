#include "TCanvas.h"
#include "TMath.h"
#include "TH1.h"
#include "TF1.h"
#include "TRandom.h"
#include "TSpectrum.h"
#include "TVirtualFitter.h"

void FitAwmi() {
   Double_t a;
   Int_t i,nfound=0,bin;
   Int_t nbins = 256;
   Int_t xmin = 0;
   Int_t xmax = nbins;
   Double_t * source = new Double_t[nbins];
   Double_t * dest = new Double_t[nbins];
   TH1F *h = new TH1F("h","Fitting using AWMI algorithm",nbins,xmin,xmax);
   TH1F *d = new TH1F("d","",nbins,xmin,xmax);
   TFile *f = new TFile("TSpectrum.root");
   h=(TH1F*) f->Get("fit;1");
   for (i = 0; i < nbins; i++) source[i]=h->GetBinContent(i + 1);
   TCanvas *Fit1 = gROOT->GetListOfCanvases()->FindObject("Fit1");
   if (!Fit1) Fit1 = new TCanvas("Fit1","Fit1",10,10,1000,700);
   h->Draw("L");
   TSpectrum *s = new TSpectrum();
   //searching for candidate peaks positions
   nfound = s->SearchHighRes(source, dest, nbins, 2, 0.1, kFALSE, 10000, kFALSE, 0);
   Bool_t *FixPos =new Bool_t[nfound];
   Bool_t *FixAmp = new Bool_t[nfound];
   for(i = 0; i< nfound ; i++){
      FixPos[i] = kFALSE;
      FixAmp[i] = kFALSE;
   }
   //filling in the
   initial estimates of the input parameters
   Double_t *PosX = new Double_t[nfound];
   Double_t *PosY = new Double_t[nfound];
   PosX = s->GetPositionX();
   for (i = 0; i < nfound; i++) {
      a=PosX[i];
      bin = 1 + Int_t(a + 0.5);
      PosY[i] = h->GetBinContent(bin);
   }
   TSpectrumFit *pfit=new TSpectrumFit(nfound);
   pfit->SetFitParameters(xmin, xmax-1, 1000, 0.1, pfit->kFitOptimChiCounts,
   pfit->kFitAlphaHalving, pfit->kFitPower2,
   pfit->kFitTaylorOrderFirst);
   pfit->SetPeakParameters(2, kFALSE, PosX, (Bool_t *) FixPos, PosY, (Bool_t *) FixAmp);
   pfit->FitAwmi(source);
   Double_t *CalcPositions = new Double_t[nfound];
   Double_t *CalcAmplitudes = new Double_t[nfound];
   CalcPositions=pfit->GetPositions();
   CalcAmplitudes=pfit->GetAmplitudes();
   for (i = 0; i < nbins; i++) d->SetBinContent(i + 1,source[i]);
   d->SetLineColor(kRed);
   d->Draw("SAME L");
   for (i = 0; i < nfound; i++) {
      a=CalcPositions[i];
      bin = 1 + Int_t(a + 0.5);
      PosX[i] = d->GetBinCenter(bin);
      PosY[i] = d->GetBinContent(bin);
   }
   TPolyMarker * pm = (TPolyMarker*)h->GetListOfFunctions()->FindObject("TPolyMarker");
   if (pm) {
      h->GetListOfFunctions()->Remove(pm);
      delete pm;
   }
   pm = new TPolyMarker(nfound, PosX, PosY);
   h->GetListOfFunctions()->Add(pm);
   pm->SetMarkerStyle(23);
   pm->SetMarkerColor(kRed);
   pm->SetMarkerSize(1);
}
