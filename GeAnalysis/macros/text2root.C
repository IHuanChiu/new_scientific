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
    Double_t channel;
    Double_t count;
  };
  Event eve;
  TFile * outputTfile = new TFile (Form("../data/%s.root",output_name.c_str()),"RECREATE");
  TTree * tree = new TTree ("tree","Event data from ascii file");
  tree->Branch("Count",&eve.count,"count/D");
  tree->Branch("Channel",&eve.channel,"count/D");
  TH1F * h1 = new TH1F ("spectrum","spectrum",nch,0,nch);
 
  while(getline(fin,str))
  { 
      eve.channel = inti_channel;
      str.erase(str.end()-1, str.end()); //remove "," from string
      eve.count = stod(str);

      cout << eve.channel << "|" << eve.count << " ";
      tree->Fill();
      h1->Fill(eve.channel,eve.count);
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
  outputTfile->Write();
  cout << "output : " <<Form("../data/%s.root",output_name.c_str()) << endl;

}

int main(int argc, char *argv[]){
  if(argc != 3){ 
    usage();
    exit(1);
  }

  printf("%s <input file>=%s <output file>=%s\n",argv[0],argv[1],argv[2]);
  tran(argv[1], argv[2]);
 
  return 0;
}

