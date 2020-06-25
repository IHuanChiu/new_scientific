#include <fstream>
#include <iostream>
#include <TROOT.h>
#include <TFile.h>
#include <TTree.h>

int usage(void)
{
    std::string message = "Usage: ./run <input root file> <output>";
    std::cerr << message << std::endl;
    return 0;
}

void tran(std::string input_name, std::string output_name){

  std::ifstream fin;
  fin.open(input_name);

  if(!fin.good()){
    std::cerr << "ERROR: Cannot open " << input_name << std::endl;
    return;
  }

  struct Event{
    Double_t channel;
    Double_t count;
  };

  Event eve;
  TFile * outputTfile = new TFile (Form("../data/%s.root",output_name.c_str()),"RECREATE");
  TTree * tree = new TTree ("EventTree","Event data from ascii file");
  tree->Branch("Count",&eve.count,"count/D");
  tree->Branch("Channel",&eve.channel,"count/D");
 
//  double start = 0;
//  while( ! fin.eof())
//  { 
//	  eve.channel = start;
//      fin >> eve.count;
//      cout << eve.channel << "  " << eve.count << " " << endl;
//      tree->Fill();
//	  start++;
//  }

  fin.close();
  tree->Print();
  outputTfile->Write();

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

