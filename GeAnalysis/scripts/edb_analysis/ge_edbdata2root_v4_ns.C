

void ge_edbdata2root_v4_ns()
{
  char edbfilename[256] = "./edb/MUSE203307_01_001_000.edb";
//  char edbfilename[256] = "./edb/MUSE203303_01_001_000.edb";// 2, 3, 5
  TString funcfile = "ge_calfunc_linear_0627.root";

  TFile* calfile = new TFile(funcfile);
  TF1* cal_func[6];
  for(int ch_index=0; ch_index<6; ch_index++) cal_func[ch_index] = (TF1*)calfile->Get(Form("cal_func_ch%d", ch_index+1));
  cout<<"Calfile ...  "<<funcfile<<endl;
  calfile->Close();


  TString outrootfilename = TString(edbfilename);
  outrootfilename.ReplaceAll(".edb","_ene.root");
  outrootfilename.ReplaceAll("./edb","./root");
  cout<<"Open ...  "<<edbfilename<<endl;
  ifstream inputfile(edbfilename, ios::in|ios::binary);

  TFile* outrootfile = new TFile(outrootfilename, "recreate");

  TTree* edbtree = new TTree("edbtree","edbtree");
  unsigned char timepacket[8]={0x5c, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};
  unsigned short packetID;
  unsigned char moduleID;
  unsigned char detectorID;
  unsigned int tdc_value;
  Double_t tdc_value_corr;
  unsigned int adc_value;
  unsigned int time_sec= 0;
  unsigned int time_32k= 0;
  unsigned int time_40M= 0;
  Double_t time_edb;
  Double_t time_edb_timepacket;
  Double_t epi_value;
  Double_t pha_value;
  Double_t time_edb_last[16]={0.0};
  unsigned int adc_value_last[16]={0};
  Double_t delta_t_det;
  unsigned int last_adc_value;

  Double_t energy;
  Int_t tdc;
  Int_t ch;
  Int_t pha;
  Int_t adc;
  Int_t nevent=0;

//  edbtree->Branch("timepacket", timepacket, "timepacket[8]/b");
//  edbtree->Branch("time_sec", &time_sec, "time_sec/i");
//  edbtree->Branch("time_32k", &time_32k, "time_32k/i");
//  edbtree->Branch("time_40M", &time_40M, "time_40M/i");
//  edbtree->Branch("time_edb", &time_edb, "time_edb/D");
//  edbtree->Branch("packetID", &packetID, "packetID/s");
//  edbtree->Branch("moduleID", &moduleID, "moduleID/b");
//  edbtree->Branch("detectorID", &detectorID, "detectorID/b");
//  edbtree->Branch("tdc_value", &tdc_value, "tdc_value/i");
//  edbtree->Branch("tdc_value_corr", &tdc_value_corr, "tdc_value_corr/D");
//  edbtree->Branch("adc_value", &adc_value, "adc_value/i");
//  edbtree->Branch("pha_value", &pha_value, "pha_value/D");
//  edbtree->Branch("epi_value", &epi_value, "epi_value/D");
  edbtree->Branch("delta_t_det", &delta_t_det, "delta_t_det/D");
//  edbtree->Branch("last_adc_value", &last_adc_value, "last_adc_value/i");
//
  edbtree->Branch("ch", &ch, "ch/i");
//  edbtree->Branch("pha", &pha, "pha/i");
//  edbtree->Branch("tdc", &tdc, "tdc/i");
//  edbtree->Branch("adc", &adc, "adc/i");
//  edbtree->Branch("nevent", &nevent, "nevent/i");
  edbtree->Branch("energy", &energy, "energy/D");

  unsigned char readdata[8];

  unsigned int time_tmp_int;
  unsigned int time_tmp2_int;

  while(!inputfile.eof())
  {
    inputfile.read((char*)readdata, 8);

    if(readdata[0]==0x5c)
    {
      timepacket[0]=readdata[0];
      timepacket[1]=readdata[1];
      timepacket[2]=readdata[2];
      timepacket[3]=readdata[3];
      timepacket[4]=readdata[4];
      timepacket[5]=readdata[5];
      timepacket[6]=readdata[6];
      timepacket[7]=readdata[7];
      time_tmp_int = 0x1000000 * timepacket[1] + 0x10000 * timepacket[2] + 0x100 * timepacket[3] + 0x1 * timepacket[4];
      time_tmp2_int = timepacket[7] + 0x100*timepacket[6] + 0x10000 * timepacket[5]+0x1000000*timepacket[4];

      time_32k = (time_tmp2_int >> 11) & 0x7fff;
      time_40M = time_tmp2_int & 0x7ff;

      time_sec = (time_tmp_int >> 2);
      time_edb_timepacket = (Double_t)time_sec + (Double_t)time_32k/3.2e+4 + (Double_t) time_40M /4.0e+7;
      time_edb = time_edb_timepacket;

      tdc_value_corr = tdc_value;

      packetID = 0x5c00;
      detectorID = 0x00;
      adc_value = 0;
      tdc_value = 0;
      moduleID = 0x0;
      pha_value = 0.0;
      epi_value = 0.0;

      adc = 0;
      tdc = 0;
      energy = 0.0;
      ch = 0;

      edbtree->Fill();

    }
    else if(readdata[0]==0x46)
    {
      packetID = readdata[0]*0x0100 + readdata[1];
      moduleID = (readdata[2] & 0xf0) >> 4;
      detectorID = (readdata[2] & 0x0f);
      tdc_value = 0x00010000 * readdata[3] + 0x000000100 * readdata[4] + 0x00000001 * readdata[5];
      adc_value = 0x000000100 * readdata[6] + 0x00000001 * readdata[7];
      time_edb = time_edb_timepacket + (Double_t)tdc_value * 5.0e-9;

      tdc_value_corr = tdc_value;
      pha_value = (Double_t)adc_value + gRandom->Uniform(-0.5,0.5);
      if(detectorID<7 && detectorID>0) epi_value = cal_func[detectorID-1]->Eval(pha_value);
      else epi_value=0.0;

      delta_t_det = time_edb - time_edb_last[detectorID];
      last_adc_value = adc_value_last[detectorID];

      adc = adc_value;
      tdc = tdc_value;
      energy = epi_value;
      ch = detectorID;

      edbtree->Fill();

      time_edb_last[detectorID] = time_edb;
      adc_value_last[detectorID] = adc_value;
    }

  }


  outrootfile->Write();
  cout<<outrootfilename<<" is created."<<endl;

}
