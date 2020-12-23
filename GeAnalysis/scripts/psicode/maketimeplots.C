#include <iostream>
#include <fstream>
#include <sstream>

std::vector<TString> vRootFileNames;
std::vector<TString> vRootFileComments;
int num_det=3;
double energy_up=140;
double energy_down=130;

void ReadRootFileList();

//=================================================================
void maketimeplots()
{
    ReadRootFileList();

    //    gROOT->Reset();
    //gROOT->SetStyle("Plain");
    gStyle->SetPaperSize(26, 20);
    // gStyle->SetOptStat(0);
    gStyle->SetTitleXOffset(1.15);
    gStyle->SetTitleYOffset(1.15);
    gStyle->SetTitleBorderSize(0);
    gStyle->SetLegendBorderSize(0);
    gStyle->SetPadBottomMargin(0.12);
    gStyle->SetPadLeftMargin(0.12);
    gStyle->SetPadTopMargin(0.12);
    //gStyle->SetPadRightMargin(0.05);
    gStyle->SetCanvasColor(10);
    gStyle->SetPadColor(0);
    gStyle->SetTitleFillColor(0);
    gStyle->SetCanvasColor(0);
    gStyle->SetPalette(1, 0);
    //gStyle->SetOptTitle(kFALSE);
    gStyle->SetLabelSize(0.045, "XYZ");
    gStyle->SetTitleSize(0.05, "XYZ");
    //gROOT->LoadMacro("RootFit.C");

    // vectors for resulting parameters from fit including errors for all decay channels
    std::vector<Float_t> vContent;
    std::vector<Float_t> verr_Content;
    std::vector<Float_t> vEnergy;
    std::vector<Float_t> verr_Energy;

    //--------------------------------------------------------------------------
    for (Int_t fileID = 0; fileID < vRootFileNames.size(); fileID++)
    //for (Int_t fileID = 0; fileID < 1; fileID++)
    {
        TFile *f1 = new TFile(vRootFileNames[fileID]);

        TH3F *hGermaniumEnergyVsTimeFine1 = (TH3F *)(f1->FindObjectAny("hGermaniumEnergyVsTimeUltraFine"));
        //TH3F *hGermaniumEnergyVsTimeFine1 = (TH3F *)(f1->FindObjectAny("hGermaniumEnergyVsTimeFine"));
        TH1F *hMuonEventStats1 = (TH1F *)(f1->FindObjectAny("hMuonStats"));
        TH2F *hMuonEnergy1 = (TH2F *)(f1->FindObjectAny("hMuonEnergy"));
        TH1F *hGeEnergykeV = (TH1F *)(f1->FindObjectAny("hGeEnergykeV"));

        // projection histograms vector
        std::vector<TH1F *> hMergedSpectrum;

        // transfer time cuts
        Int_t energyBinMin = hGermaniumEnergyVsTimeFine1->GetZaxis()->FindBin(energy_down);
        Int_t energyBinMax = hGermaniumEnergyVsTimeFine1->GetZaxis()->FindBin(energy_up);
        Double_t energyCutRangeMin = hGermaniumEnergyVsTimeFine1->GetZaxis()->GetBinLowEdge(energyBinMin);
        Double_t energyCutRangeMax = hGermaniumEnergyVsTimeFine1->GetZaxis()->GetBinLowEdge(energyBinMax) + hGermaniumEnergyVsTimeFine1->GetZaxis()->GetBinWidth(energyBinMax);

        // hMergedSpectrum[0] is with cuts for prompt peaks
		for(int idet = 1 ; idet < num_det+1; idet++){
           hMergedSpectrum.push_back((TH1F *)(hGermaniumEnergyVsTimeFine1->ProjectionX(Form("proj01_%d",idet), idet, idet, energyBinMin, energyBinMax)));   // MB14C for now has bad timing 1~8
		}

        // hMergedSpectrumVsTime[0]
        std::vector<TH2F *> hMergedSpectrumVsTime;
        hGermaniumEnergyVsTimeFine1->GetYaxis()->SetRange(1, 8);
        hMergedSpectrumVsTime.push_back((TH2F *)(hGermaniumEnergyVsTimeFine1->Project3D("xz")));
        hMergedSpectrumVsTime[0]->SetName("projxz01");

        hGermaniumEnergyVsTimeFine1->GetYaxis()->SetRange(11, 11);
        hMergedSpectrumVsTime.push_back((TH2F *)(hGermaniumEnergyVsTimeFine1->Project3D("xz")));
        hMergedSpectrumVsTime[1]->SetName("projxz11");

        hGermaniumEnergyVsTimeFine1->GetYaxis()->SetRange(13, 14);
        hMergedSpectrumVsTime.push_back((TH2F *)(hGermaniumEnergyVsTimeFine1->Project3D("xz")));
        hMergedSpectrumVsTime[2]->SetName("projxz21");

        hGermaniumEnergyVsTimeFine1->GetYaxis()->SetRange(16, 18);
        hMergedSpectrumVsTime.push_back((TH2F *)(hGermaniumEnergyVsTimeFine1->Project3D("xz")));
        hMergedSpectrumVsTime[3]->SetName("projxz31");

        hGermaniumEnergyVsTimeFine1->GetYaxis()->SetRange(20, 22);
        hMergedSpectrumVsTime.push_back((TH2F *)(hGermaniumEnergyVsTimeFine1->Project3D("xz")));
        hMergedSpectrumVsTime[4]->SetName("projxz41");

        hGermaniumEnergyVsTimeFine1->GetYaxis()->SetRange(24, 27);
        hMergedSpectrumVsTime.push_back((TH2F *)(hGermaniumEnergyVsTimeFine1->Project3D("xz")));
        hMergedSpectrumVsTime[5]->SetName("projxz51");

        hMergedSpectrumVsTime[0]->Add(hMergedSpectrumVsTime[1], 1);
        hMergedSpectrumVsTime[0]->Add(hMergedSpectrumVsTime[2], 1);
        hMergedSpectrumVsTime[0]->Add(hMergedSpectrumVsTime[3], 1);
        hMergedSpectrumVsTime[0]->Add(hMergedSpectrumVsTime[4], 1);
        hMergedSpectrumVsTime[0]->Add(hMergedSpectrumVsTime[5], 1);

        // muon
        auto hisMuonEnt1 = (TH1F *)(hMuonEnergy1->ProjectionX("ppp", 1, 1));

#define MAKE_PHADATA 1
#ifdef MAKE_PHADATA
        //----------------------------------------------------
        // make pha text data file
        //----------------------------------------------------
		for (int ih = 0; ih < hMergedSpectrum.size(); ih++){
           TString phaDataName(vRootFileNames[fileID].Data());
           phaDataName.ReplaceAll(".root", Form("_pha_time_Det%s.dat",hGermaniumEnergyVsTimeFine1->GetYaxis()->GetBinLabel(ih+1)));
           phaDataName.ReplaceAll("data", "pha");
           ofstream phaDataFile(phaDataName.Data());
           cout << "pha data: " << phaDataName.Data() << endl;
           TDatime now;
           phaDataFile << "# PHA DATA for PSI muX-2019-Nov created by Akira Sato" << endl;
           phaDataFile << "# Date: " << now.AsSQLString() << endl;
           phaDataFile << "# Root file: " << vRootFileNames[fileID].Data() << endl;
   //        phaDataFile << "# Number of muons: " << Form("%.0f", muon_num_cut1) << endl;
           phaDataFile << "# Energy cut range (ns): " << Form("%.1f - %.1f", energyCutRangeMin, energyCutRangeMax) << endl;
           phaDataFile << "# PHA data format: binID, energy(keV) at the bin center, content" << endl;
           Int_t nbin = hMergedSpectrum[ih]->GetNbinsX();
           for (Int_t i = 1; i < nbin + 1; i++)
           {
               Double_t binCenter = hMergedSpectrum[ih]->GetBinCenter(i);
               Double_t binContent = hMergedSpectrum[ih]->GetBinContent(i);
               phaDataFile << i << ", " << binCenter << ", " << binContent << endl;
           }
           phaDataFile.close();
		}
#endif

#ifdef MAKE_HISTOROOT
        //----------------------------------------------------
        // make pha text data file
        //----------------------------------------------------
        TString histoRootName(vRootFileNames[fileID].Data());
        histoRootName.ReplaceAll(".root", "_histo.root");
        TFile histoRootFile(histoRootName.Data(), "recreate");
        cout << "root file for histo: " << histoRootName.Data() << endl;
        hMergedSpectrum[0]->Write();
        hMergedSpectrumVsTime[0]->Write();
        hisMuonEnt1->Write();
        histoRootFile.Close();
#endif

#ifdef PLOT_HISTO
        TCanvas *c000 = new TCanvas("c000", "c000", 200, 0, 2000, 1200);
        hMergedSpectrum[0]->SetLineWidth(2);
        hMergedSpectrum[0]->DrawCopy();

        TCanvas *c001 = new TCanvas("c001", "c001", 200, 0, 2000, 1200);
        c001->SetLogz();
        hMergedSpectrumVsTime[0]->DrawCopy("colz");

        TCanvas *cMu = new TCanvas("cMu", "cMu");
        hisMuonEnt1->GetXaxis()->SetRangeUser(0, 700);
        hisMuonEnt1->Draw();
//        cout << "Number of muons (from integral) 1 = " << muon_num_cut1 << endl;
#endif
    }
}

//=================================================================
void ReadRootFileList()
{
    std::ifstream runListFile("data_list.txt");
    if (!runListFile)
    {
        return 1;
    }

    TString line;
    while (1)
    {
        line.ReadLine(runListFile);
        if (!runListFile.good())
            break;
        TObjArray *list_by_dquate = line.Tokenize("\"");
        TString rootFileName(((TObjString *)list_by_dquate->At(0))->String());
        TString comment(((TObjString *)list_by_dquate->At(2))->String());
        vRootFileNames.push_back(rootFileName);
        vRootFileComments.push_back(comment);
    }

#ifdef DEBUG
    for (Int_t i = 0; i < vRootFileNames.size(); i++)
    {
        cout << "rootFile" << i << ": " << vRootFileNames[i] << endl;
    }
#endif
}
