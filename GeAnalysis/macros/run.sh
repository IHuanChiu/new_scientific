# tran. pha to root
./text2root ../data/JPARC_2021Apri/DEW12007_bar/203089
# count peak
python CountPeak.py 
# make comparison
root mk_Comparison.C 
