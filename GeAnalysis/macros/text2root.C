#include <fstream>
#include <iostream>
#include <TROOT.h>
#include <TFile.h>
#include <TTree.h>
#include <TH1F.h>

using namespace std;

int usage(void)
{
    std::string message = "Usage: ./run <run number> <Total detector>";
    std::cerr << message << std::endl;
    return 0;
}

void tran(std::string run_number, std::string nDets, std::string output_name){
  int skiplines = 18;//skip haed lines
  int nch=8192;
  string str, str_temp;
  static const int total_dets=std::stoi( nDets );
  //calibration TODO: why I cannot use Double_t a[total_dets]?
  Double_t a[6]={0.,0.,0.,0.,0.,0.};
  Double_t b[6]={0.025,0.024995,0.024995,0.025053,0.025006,0.024983};
  Double_t c[6]={0.260015,0.372299,0.447283,0.098903,0.297717,0.271931};

  struct Event{
    Int_t detID;
    Int_t channel;
    Double_t energy;
    Double_t count;
  };
  Event eve;
  TFile * outputTfile = new TFile (Form("%s.root",(run_number+"_beam"+output_name).c_str()),"RECREATE");
  TTree * tree = new TTree ("tree","Event tree from ascii file");
  tree->Branch("detID",&eve.detID,"detID/I");
  tree->Branch("channel",&eve.channel,"channel/I");
  tree->Branch("energy",&eve.energy,"energy/D");
  TH1F * h1 = new TH1F ("Channel","Channel",nch,0,nch);
  TH1F * h2 =  new TH1F ("Energy","Energy",220*20,0,220);//1keV/20 = 50 eV per bin
  TH1F * h2_l =  new TH1F ("el","el",50*20,20,70);
  TH1F * h2_m =  new TH1F ("em","em",70*20,70,140);
  TH1F * h2_h =  new TH1F ("eh","eh",60*20,140,200);


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
     
    
     while(getline(fin,str))
     { 
         str.erase(str.end()-1, str.end()); //remove "," from string
         eve.count = stod(str);//number of event in each channel
   
         eve.channel = init_channel;//find channel
         eve.energy = a[idet]*pow(eve.channel,2)+b[idet]*eve.channel+c[idet];
         if(idet == 0){
         cout << eve.channel << "|" << eve.count << " ";}
         for (int ie=0; ie < eve.count; ie++){
            h1->Fill(eve.channel);
            h2->Fill(eve.energy);
            if(eve.energy < 70){ h2_l->Fill(eve.energy);
            }else if(eve.energy < 140){ h2_m->Fill(eve.energy);
            }else if(eve.energy < 210) {h2_h->Fill(eve.energy);}
            tree->Fill();
         }
         init_channel++;
     }
         cout << endl;
   
   //  while(!fin.eof())
   //  { 
   //      eve.channel = inti_channel;
   //      fin >> eve.count;
   //      cout << "  " << eve.count << " ";
   //      tree->Fill();
   //      inti_channel++;
   //  }
   
     fin.close();
  }//loop all detector

  tree->Print();
  h1->Write();
  h2->Write();
  outputTfile->Write();
  cout << "output : " <<Form("%s.root",(run_number+"_beam"+output_name).c_str()) << endl;

}

int main(int argc, char *argv[]){
  
  if(argc < 4){
    argv[3] = "";
  }
  if(argc < 3){
    argv[2] = "6";
  }
  if(argc < 2){
    usage();
    exit(1);
  }

  printf("%s <run number>=%s <nDets>=%s <output file>=%s\n",argv[0],argv[1],argv[2],argv[3]);
  tran(argv[1], argv[2], argv[3]);
 
  return 0;
}

