#include <fstream>
#include <iostream>
#include <TROOT.h>
#include <TFile.h>
#include <TTree.h>
#include <TH1F.h>
#include <TRandom3.h>

using namespace std;

int usage(void)
{
    std::string message = "Usage: ./text2root <path + run number>";
    std::cerr << message << std::endl;
    message = "Usage: check configs";
    std::cerr << message << std::endl;
    return 0;
}

string ReadInputFiles(void){
    std::ifstream runListFile("configs/data_list.txt");
    if (!runListFile)
    {
        return "None";
    }
    // TODO not finished yet
    return "None";
//    TString line;
//    while (1)
//    {
//        line.ReadLine(runListFile);
//        if (!runListFile.good())
//            break;
//        TObjArray *list_by_dquate = line.Tokenize("\"");
//        TString rootFileName(((TObjString *)list_by_dquate->At(0))->String());
//        TString comment(((TObjString *)list_by_dquate->At(2))->String());
//        vRootFileNames.push_back(rootFileName);
//        vRootFileComments.push_back(comment);
//    }
}

void tran(std::string run_number, std::string nDets, std::string output_name){
  int skiplines = 18;//skip haed lines
  int nch=8192;
  string str, str_temp;
  static const int total_dets=std::stoi( nDets );
  //calibration
  Double_t a[6]={0.,0.,0.,0.,0.,0.};
  Double_t b[6]={0.025,0.024995,0.024995,0.025053,0.025006,0.024983};
  Double_t c[6]={0.260015,0.372299,0.447283,0.098903,0.297717,0.271931};
  double a_base=a[0];//CH1
  double b_base=b[0];//CH1
  double c_base=c[0];//CH1
  double e_shift;

  struct Event{
    Int_t detID;
    Int_t channel;
    Double_t energy_ori;
    Double_t energy;
    Double_t count;
  };
  Event eve;
  TFile * outputTfile = new TFile (Form("%s.root",(run_number+"_beam"+output_name).c_str()),"RECREATE");
  TTree * tree = new TTree ("tree","Event tree from ascii file");
  tree->Branch("detID",&eve.detID,"detID/I");
  tree->Branch("channel",&eve.channel,"channel/I");
  tree->Branch("energy_ori",&eve.energy_ori,"energy_ori/D");
  tree->Branch("energy",&eve.energy,"energy/D"); //8192,0.26001500,205.06002
  TH1F * h1 = new TH1F ("Channel","Channel",nch,0,nch);
  TH1F * h2 =  new TH1F ("Energy","Energy",int(200/b_base),0,200);//1keV/20 = 50 eV per bin
  TH1F * h2_l =  new TH1F ("el","el",int(50/b_base),20,70);
  TH1F * h2_m =  new TH1F ("em","em",int(70/b_base),70,140);
  TH1F * h2_h =  new TH1F ("eh","eh",int(60/b_base),140,200);
  TRandom *r3 = new TRandom3();


  for(int idet=0; idet < total_dets; idet++){
     std::cout << " =================================   Current detector : " << idet+1  << " ================================ "<< std::endl;
     eve.detID=idet+1;

     int init_channel = 1;
     std::string input_name=run_number+"_beam_CH"+std::to_string(idet+1)+".pha";
     std::ifstream fin;
     fin.open(input_name);
   
     if(!fin.good()){
       std::cerr << "ERROR: Cannot open " << input_name << std::endl;
       return;
     }
     for(int i = 0; i < skiplines-1; i++) fin.ignore(1000,'\n');
   
     //get real nch for data
     getline(fin,str_temp);
     str_temp.erase(str_temp.begin(), str_temp.begin()+2); 
     nch = stod(str_temp); 
     cout << "number of channels : " << nch << endl;

     //energy shift
     e_shift=0;
     if(c[idet]-c_base > b_base) e_shift = c[idet]-c_base;
    
     while(getline(fin,str))
     { 
         str.erase(str.end()-1, str.end()); //remove "," from string
         eve.count = stod(str);//number of event in each channel   
         eve.channel = init_channel;//find channel
         eve.energy_ori = a[idet]*pow(eve.channel,2)+b[idet]*eve.channel+c[idet];
         eve.energy = eve.energy_ori-e_shift;
         //energy correction
         double channel_base=(eve.energy-c_base)/b_base;
         double E_down=a_base*pow(floor(channel_base),2)+b_base*floor(channel_base)+c_base;
         double E_up=a_base*pow(ceil(channel_base),2)+b_base*ceil(channel_base)+c_base;
         double Rcentral=(eve.energy-E_down)/(E_up-E_down);
         if(eve.energy > 160 && idet != 0)std::cout << "ID : " << idet  << " channel : " << channel_base << " ch up : " << ceil(channel_base) << " ch down : " << floor(channel_base)  << " main : " << eve.energy << " up : " << E_up << " down : " << E_down << " ratio down : " << Rcentral << std::endl;

         if(idet == 0){
         cout << eve.channel << "|" << eve.count << " ";}
         for (int ie=0; ie < eve.count; ie++){
            //count distribution
            if(idet != 0){
               if (r3->Rndm(ie)<Rcentral){ eve.energy = E_down;
               }else{ eve.energy = E_up;}
            }

            //make histograms
            h1->Fill(eve.channel);
            h2->Fill(eve.energy);//hist. is for corrected energy
            if(eve.energy < 70){ h2_l->Fill(eve.energy);
            }else if(eve.energy < 140){ h2_m->Fill(eve.energy);
            }else if(eve.energy < 210) {h2_h->Fill(eve.energy);}

            tree->Fill();
         }
         init_channel++;
     }
         cout << endl;
   
     fin.close();
  }//loop all detector

  tree->Print();
  h1->Write();
  h2->Write();
  outputTfile->Write();
  cout << "output : " <<Form("%s.root",(run_number+"_beam"+output_name).c_str()) << endl;

  //----------------------------------------------------
  // make pha text data file from merged hist.
  //----------------------------------------------------
  TString phaDataName(run_number+"_beam"+output_name+"_Sum.pha");
  ofstream phaDataFile(phaDataName.Data());
  TDatime now;
  phaDataFile << "# Merged PHA DATA for J-PARC created by I-Huan CHIU" << std::endl;
  phaDataFile << "# Date: " << now.AsSQLString() << std::endl;
  phaDataFile << "# PHA data format: binID, energy(keV) at the bin center, content" << endl;
  Int_t nbin = h2->GetNbinsX();
  for (Int_t i = 1; i < nbin + 1; i++)
  {
      Double_t binCenter = h2->GetBinCenter(i);
      Double_t binContent = h2->GetBinContent(i);
      phaDataFile << i << ", " << binCenter << ", " << binContent << endl;
  }
  phaDataFile.close();
  cout << "output pha : " << phaDataName << endl;

}

int main(int argc, char const *argv[]){
    
  if(argc < 4){
    argv[3] = "";
  }
  if(argc < 3){
    argv[2] = "6";//you should not chagne constant char
  }
  TString inputlist;
  if(argc < 2){
    inputlist=ReadInputFiles();
  }
  if(inputlist == "None"){
    usage();
    exit(1);
  }
  
  printf("%s <run number>=%s <nDets>=%s <output file>=%s\n",argv[0],argv[1],argv[2],argv[3]);
  tran(argv[1], argv[2], argv[3]);
 
  return 0;
}

