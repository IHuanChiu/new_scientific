NTUPDIR="../data/CdTedata"
OUTDIR="/Users/chiu.i-huan/Desktop/new_scientific/run/root/ntuple_test"
NCORES=8

if [ ! -d ${OUTDIR} ] 
then
    mkdir ${OUTDIR}
fi

     
# ================== make ntuplke ====================
parallel --eta -j ${NCORES} python3 main.py ${NTUPDIR}/20200307a_000{1}_001.root ::: 70 71

