#include <fstream>
#include <iostream>
#include <TROOT.h>
#include <TFile.h>
#include <TTree.h>
#include <TH1F.h>
#include <TRandom3.h>

//#define DEBUG 1

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
  //calibration, change argv[2] in the bottom a*x^2 + b*x + c
// /*  //2020.12 Ryugu exp.
  Double_t a[6]={0.,0.,0.,0.,0.,0.};
  Double_t b[6]={0.024983, 0.100011, 0.024952, 0.024989, 0.100043, 0.024871};
  Double_t c[6]={0.268035, 1.369860, 0.368891, 0.834436, 1.323832, 0.411497};
  int ignore_CH=-1;// */
 /*  //2021.04 terada exp.
  Double_t a[6]={0.,0.,0.,0.,0.,0.};
  Double_t b[6]={0.025,0.024995,0.024995,0.025053,0.025006,0.024983};
  Double_t c[6]={0.260015,0.372299,0.447283,0.098903,0.297717,0.271931};
  int ignore_CH=-1;// */
/*  //2021.04 Ryugu exp.
  Double_t a[6]={0.,0.,0.,0.,0.,0.};
  Double_t b[6]={0.024981,0.024974,0.024981,0.025024,0.249961,0.024999};
  Double_t c[6]={0.300472,0.035980,0.050147,0.338917,0.338917,0.334527};
  int ignore_CH=2; // */

  int base_CH=1;
  double a_base=a[base_CH-1];//CH1
  double b_base=b[base_CH-1];//CH1
  double c_base=c[base_CH-1];//CH1
  double e_shift;

  struct Event{
    Int_t detID;
    Int_t channel;
    Double_t energy_ori;
    Double_t energy_shift;
    Double_t energy;
    Double_t count;
  };
  Event eve;
  TFile * outputTfile = new TFile (Form("%s.root",(run_number+"_beam"+output_name).c_str()),"RECREATE");
  TTree * tree = new TTree ("tree","Event tree from ascii file");
  tree->Branch("detID",&eve.detID,"detID/I");
  tree->Branch("channel",&eve.channel,"channel/I");
  tree->Branch("energy_ori",&eve.energy_ori,"energy_ori/D");
  tree->Branch("energy_shift",&eve.energy_shift,"energy_shift/D");
  tree->Branch("energy",&eve.energy,"energy/D"); //8192,0.26001500,205.06002
  TH1F * h1 = new TH1F ("Channel","Channel",nch,0,nch);
  TH1F * h2 =  new TH1F ("Energy","Energy",int(200/b_base),0,200);//1keV/20 = 50 eV per bin
  TH1F * h2_l =  new TH1F ("el","el",int(50/b_base),20,70);
  TH1F * h2_m =  new TH1F ("em","em",int(70/b_base),70,140);
  TH1F * h2_h =  new TH1F ("eh","eh",int(60/b_base),140,200);
  TRandom *r3 = new TRandom3();


  for(int idet=0; idet < total_dets; idet++){
     eve.detID=idet+1;
     if(eve.detID == ignore_CH) continue;

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
#ifdef DEBUG
     std::cout << " =================================   number of channels for detector : " << idet+1  << " ================================ "<< std::endl;
     cout << "number of channels : " << nch << endl;
#endif


     //energy shift
     e_shift=0;
     if(c[idet]-c_base > b_base) e_shift = c[idet]-c_base;
    
     while(getline(fin,str))
     { 
         str.erase(str.end()-1, str.end()); //remove "," from string
         eve.count = stod(str);//number of event in each channel   
         eve.channel = init_channel;//find channel
#ifdef DEBUG
         if(idet == 0) cout << eve.channel << "|" << eve.count << " ";
#endif

         eve.energy_ori = a[idet]*pow(eve.channel,2)+b[idet]*eve.channel+c[idet];
         eve.energy_shift = eve.energy_ori-e_shift;
         //energy correction (WRONG way)
         double channel_base=(eve.energy_shift-c_base)/b_base;
         double E_down_find=a_base*pow(floor(channel_base),2)+b_base*floor(channel_base)+c_base;
//         double E_up_find=a_base*pow(ceil(channel_base),2)+b_base*ceil(channel_base)+c_base;
//         double Rcentral=(eve.energy_shift-E_down_find)/(E_up_find-E_down_find);
//         std::cout << "ID : " << idet  << " channel : " << channel_base << " ch up : " << ceil(channel_base) << " ch down : " << floor(channel_base)  << " main : " << eve.energy_shift << " up : " << E_up_find << " down : " << E_down_find << std::endl;

         //energy correction (FIX)
         double E_flag=0;
         double E_ori=0;
         double E_ori_pre=0;
         double E_down = eve.energy_shift;
         double E_up = eve.energy_shift+b[idet];
         std::vector<Float_t> vEList;
         std::vector<Float_t> vRatioList;
         for (int j = 1; j < 8192+1; j++){
           E_flag=a_base*pow(j,2)+b_base*j+c_base;
           if(E_flag > E_down && E_flag < E_up){
             E_ori=a_base*pow(j,2)+b_base*(j)+c_base;
             E_ori_pre=a_base*pow(j-1,2)+b_base*(j-1)+c_base;
             vRatioList.push_back((E_flag-E_down)/(E_up-E_down));
             vEList.push_back(E_ori_pre);
           }
         }
         vRatioList.push_back((E_up-E_down)/(E_up-E_down));// 1, final is E_up
         if (E_ori != 0){  
            vEList.push_back(E_ori);
         }else{// no "E_ori" found in loop => all counts into "E_down_find"
            vEList.push_back(E_down_find);
         }
         double random_seed=-1.;

         for (int ie=0; ie < eve.count; ie++){
            random_seed=r3->Rndm(ie);
            //count distribution (WRONG way)
//            if(idet+1 != base_CH){
//               if (r3->Rndm(ie)>Rcentral){ eve.energy = E_down_find;
//               }else{ eve.energy = E_up_find;}
//            }else{
//               eve.energy = eve.energy_shift;
//            }

            //count distribution (FIX)
            if(idet+1 != base_CH){
//               if(ie < vRatioList[0]*eve.count) { eve.energy = vEList[0];
               if(random_seed < vRatioList[0]) { eve.energy = vEList[0];
               }else if (random_seed < vRatioList[1]){eve.energy = vEList[1];
               }else if (random_seed < vRatioList[2]){eve.energy = vEList[2]; 
               }else if (random_seed < vRatioList[3]){eve.energy = vEList[3]; // set maximum is 3 => find three E_flags in the range of E_down~E_up
               }
            }else{
               eve.energy = eve.energy_shift;
            }

            //make histograms
            h1->Fill(eve.channel);
            h2->Fill(eve.energy);//hist. is for corrected energy
            if(eve.energy < h2_l->GetXaxis()->GetXmax()){ h2_l->Fill(eve.energy);
            }else if(eve.energy < h2_m->GetXaxis()->GetXmax()){ h2_m->Fill(eve.energy);
            }else if(eve.energy < h2_h->GetXaxis()->GetXmax()) {h2_h->Fill(eve.energy);}

            tree->Fill();
         }
         init_channel++;
     }
#ifdef DEBUG
         cout << endl;
#endif
   
#ifndef DEBUG
     std::cout << " =================================   Finished process for CH" << idet+1 <<" detector  " << " ================================ "<< std::endl;
#endif
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
    // change calibration in upper
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

