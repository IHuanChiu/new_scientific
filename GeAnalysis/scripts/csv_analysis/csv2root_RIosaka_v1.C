std::vector<TString> vNameList;
int skiplines = 9;

void GetNameList(){
   std::ifstream list_name("data_list.txt");//command : ls csv/* >> data_list.txt
   TString line;
   while(1)
   {
      if (!list_name.good()) break;
      line.ReadLine(list_name);
      vNameList.push_back(line);
   }
   
}

void csv2root_RIosaka_v1()
{
  GetNameList();
  TFile* calfile = new TFile("./ge_calfunc_1115.root","read");
  TF1* cal_func;

  for (int ifile=0;ifile<vNameList.size()-1;ifile++){
     std::string checkname=vNameList[ifile].Data();
     if(checkname.find("_ch2_")!=string::npos){
        cal_func=(TF1*)calfile->Get("cal_func_ch2");
     }else{
        cal_func=(TF1*)calfile->Get("cal_func_ch3");
     }
     TString outfile = TString(vNameList[ifile]);
     outfile.ReplaceAll(".CSV",".root");
     outfile.ReplaceAll("csv/","root/");
     TFile* outroot = new TFile(outfile, "recreate");
     TTree* tree = new TTree("tree","tree");
     Int_t channel;
     Double_t energy;
     tree->Branch("channel", &channel, "channel/I");
     tree->Branch("energy", &energy, "energy/D");

     std::ifstream fin;
     fin.open(vNameList[ifile]);
     std::string line, value;
     int ch_init=0;int count=0; int lineNo=0;

     while(getline(fin,line)){
        if(lineNo > skiplines-1){
           std::stringstream   linestream(line);
           int index =0; 
           while(getline(linestream,value,','))
           {
                 if(index==0){
                    ch_init=std::stod(value);
                 }else{
                    channel=ch_init+index;
                    for(int i=0;i<std::stod(value);i++){
                       double pha_value = channel+gRandom->Uniform(-0.5,0.5);
                       energy=cal_func->Eval(pha_value);
                       tree->Fill();
                    }//fill tree
                 }//get value
              index++;
           }//getline
        }//skip lines
        lineNo++;
     }//loop lines

     tree->Write();
     outroot->Write();
     cout<<outroot->GetName()<<" is created."<<endl;

  }//loop files
}//class
