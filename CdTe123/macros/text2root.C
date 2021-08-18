#include <fstream>
#include <iostream>
#include <TROOT.h>
#include <TFile.h>
#include <TTree.h>
#include <TH1F.h>

using namespace std;

int usage(void)
{
    std::string message = "Usage: ./run <input file> <output name>";
    std::cerr << message << std::endl;
    return 0;
}

void tran(std::string input_name, std::string output_name){
  int skiplines = 10;//skip haed lines
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
//  nch = stod(str_temp); 
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
  TH1F * h1 = new TH1F ("ADC","ADC",nch,0,nch);
  TH1F * h2 =  new TH1F ("energy","energy",nch,0,500);;

  bool find_data_line=false;
  while(getline(fin,str)) // get each line in fin
  { 
      //Get region => Data->End
      if(!find_data_line){
        if(str.find("<<DATA>>") != string::npos) find_data_line=true;
        continue; // <<DATA>> is continue
      }
      if(!find_data_line) continue;
      if(str.find("<<END>>") != string::npos) break;

      str.erase(str.end()-1, str.end()); //remove "," from string
      eve.count = stod(str);//number of count in each channel

      eve.channel = inti_channel;//find channel
      eve.energy = -0.264337+eve.channel*0.0447607;
      cout << eve.channel << "|" << eve.count << " ";
      if(inti_channel%10 == 0) cout << " \n";
      for (int ie=0; ie < eve.count; ie++){
         tree->Fill();
         h1->Fill(eve.channel);
         h2->Fill(eve.energy);
      }
      inti_channel++;
  }
      cout << endl;

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
 
