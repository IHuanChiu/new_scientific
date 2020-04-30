REGIONS_BTAG_BVETO="STT_SS_SR_BVETO_tree_SS STT_SS_SR_BTAG_tree_SS"
REGIONS_BINC="STT_SS_SR_tree_SS"

CAT_ID_ALL="LooseNotMed MedNotTight Tight"
CAT_ID_INC="INC"
DIST="leadtaupt subleadtaupt metmet mttot subleadtauptdijet"

NTUPDIR="../data/CdTedata"

OUTDIR="/Users/chiu.i-huan/Desktop/new_scientific/run/root/ntuple_test"
NCORES=8

if [ ! -d ${OUTDIR} ] 
then
    mkdir ${OUTDIR}
fi

     
# ================== test plots ====================
parallel --eta -j 5 python main.py ${NTUPDIR}/20200307a_000{1}_001.root ::: 70 71

