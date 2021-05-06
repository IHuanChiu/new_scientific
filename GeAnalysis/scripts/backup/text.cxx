#include <iostream>

void text(const char* inputfilename = "sample5cm.txt"){

  std::ifstream fin;
  fin.open(inputfilename);

  if(!fin.good()){
    std::cerr << "ERROR: Cannot open " << inputfilename << std::endl;
    return;
  }

  struct Event{
    Double_t channel;
    Double_t count;
  };

  Event eve;
  TFile * outputTfile = new TFile ("outputTfile5cm.root","RECREATE");
  TTree * tree = new TTree ("EventTree","Event data from ascii file");
  tree->Branch("Count",&eve.count,"count/D");
  tree->Branch("Channel",&eve.channel,"count/D");
 
  double start = 0;
  while( ! fin.eof())
  { 
	  eve.channel = start;
      fin >> eve.count;
      cout << eve.channel << "  " << eve.count << " " << endl;
      tree->Fill();
	  start++;
  }

  fin.close();
  tree->Print();
  outputTfile->Write();

}
