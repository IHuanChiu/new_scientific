// ==================================================
// ================ NOT =============================
// ================== FINISHED ======================
// ==================== YEY =========================
// ==================================================

#include <fstream>
#include <iostream>
#include <TROOT.h>
#include <TFile.h>
#include <TTree.h>
#include <TH1F.h>

using namespace std;

int usage(void)
{
    std::string message = "Usage: ./run <input root file> <output>";
    std::cerr << message << std::endl;
    return 0;
}

void tran(std::string input_name, std::string output_name){
  int skiplines = 18;//skip haed lines
  int nch=8192;
  int inti_channel = 1;
  string str, str_temp;
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
  
  struct Event{
    Int_t channel;
    Double_t energy;
    Double_t count;
  };
  Event eve;
  TFile * outputTfile = new TFile (Form("%s.root",(input_name+output_name).c_str()),"RECREATE");
  TTree * tree = new TTree ("tree","Event tree from ascii file");
  tree->Branch("channel",&eve.channel,"channel/I");
  tree->Branch("energy",&eve.energy,"energy/D");
  TH1F * h1 = new TH1F ("ADCspectrum","ADCspectrum",nch,0,nch);
  TH1F * h2 =  new TH1F ("energy","energy",nch,0,415);;
 
  while(getline(fin,str))
  { 
      str.erase(str.end()-1, str.end()); //remove "," from string
      eve.count = stod(str);//number of event in each channel

      eve.channel = inti_channel;//find channel
      if(input_name.find("CH3") != string::npos) eve.energy = (inti_channel+13.467)/19.833;
      if(input_name.find("CH5") != string::npos) eve.energy = (inti_channel);
      if(input_name.find("CH7") != string::npos) eve.energy = (inti_channel+11.467)/19.833;

      cout << eve.channel << "|" << eve.count << " ";
      for (int ie=0; ie < eve.count; ie++){
         tree->Fill();
         h1->Fill(eve.channel);
         h2->Fill(eve.energy);
      }
      inti_channel++;
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
  tree->Print();
  h1->Write();
  h2->Write();
  outputTfile->Write();
  cout << "output : " <<Form("%s.root",(input_name+output_name).c_str()) << endl;

}

int main(int argc, char *argv[]){
  
  if(argc < 3){
    argv[2] = "";
  }
  if(argc < 2){
    usage();
    exit(1);
  }

  printf("%s <input file>=%s <output file>=%s\n",argv[0],argv[1],argv[2]);
  tran(argv[1], argv[2]);
 
  return 0;
}

