NTUPDIRCDTE="../data/CdTedata"
NTUPDIRSI="../data/20200305/root/"
MACRODIR="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/macro/"
OUTDIR="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root"
NCORES=8
OUTNAME="test1020"

#if [ ! -d ${OUTDIR} ] 
#then
#    mkdir ${OUTDIR}
#fi

     
# =====
# ================== Simple test run ====================
# =====
#python3 main.py ${NTUPDIRCDTE}/20200307a_00072_001.root -o oldtest_20201005
#python3 main.py /Users/chiu.i-huan/Desktop/new_scientific/imageAna/data/JPARC2021Apri/STD27MeV/ -d CdTe_Lab -e ${MACRODIR}/auxfile/cdtedsd_2020a_cal_3_m5c400v.root -o STD27MeV
python3 main.py /Users/chiu.i-huan/Desktop/new_scientific/imageAna/data/watanabe_sample/cdtedsd_inseki2_tmp1.root -d CdTe_Lab -e ${MACRODIR}/auxfile/cdtedsd_2020a_cal_3_m5c400v.root -o STD27MeV_corr
#python3 sum_plots.py ../../../2020.12.09/sumrootblank2.root -d CdTe_JPARCDec -o blank2



# =====
# ================== 2mm CdTe run ====================
# =====
 # *** battery image sample ***
#parallel --eta -j ${NCORES} python3 main.py /Users/chiu.i-huan/Desktop/new_scientific/imageAna/data/battery_data/{1}/cdtedsd_2020b_0917a_000{2}_001.root -d CdTe_Lab -o battery_{1} -e ${MACRODIR}/auxfile/spline_calibration_2mmtest_merge_1008.root ::: Ba ::: 05 06 07 08 09 10 11 12 13 14 15 16 17
#parallel --eta -j ${NCORES} python3 main.py /Users/chiu.i-huan/Desktop/new_scientific/imageAna/data/battery_data/{1}/cdtedsd_2020b_0917a_000{2}_001.root -d CdTe_Lab -o battery_{1} -e ${MACRODIR}/auxfile/spline_calibration_2mmtest_merge_1008.root ::: Co ::: 19 20 21 22 23

 # *** calibration sample ***
#parallel --eta -j ${NCORES} python3 main.py ../data/minami_data/300n20/{1}/cdtedsd_2020b_0820a_000{2}_001.root -d CdTe_Lab -o 300n20_{1}source_cali_{3} -e ${MACRODIR}/auxfile/spline_calibration_2mmtest_300n20_{3}.root -n 2000000 ::: Am ::: 05 06 07 08 09 ::: merge_1008
#parallel --eta -j ${NCORES} python3 main.py ../data/minami_data/300n20/{1}/cdtedsd_2020b_0901a_000{2}_001.root -d CdTe_Lab -o 300n20_{1}source_cali_{3} -e ${MACRODIR}/auxfile/spline_calibration_2mmtest_300n20_{3}.root -n 2000000 ::: Ba ::: 15 16 17 18 19 ::: merge_1008
#parallel --eta -j ${NCORES} python3 main.py ../data/minami_data/300n20/{1}/cdtedsd_2020b_0820a_000{2}_001.root -d CdTe_Lab -o 300n20_{1}source_cali_{3} -e ${MACRODIR}/auxfile/spline_calibration_2mmtest_300n20_{3}.root -n 2000000 ::: Co ::: 23 24 25 26 27 ::: merge_1008
#
#parallel --eta -j ${NCORES} python3 main.py ../data/minami_data/400n20/{1}/cdtedsd_2020b_0805a_000{2}_001.root -d CdTe_Lab -o 400n20_{1}source_cali_{3} -e ${MACRODIR}/auxfile/spline_calibration_2mmtest_400n20_{3}.root -n 2000000 ::: Am ::: 25 26 27 28 29 ::: merge_1008
#parallel --eta -j ${NCORES} python3 main.py ../data/minami_data/400n20/{1}/cdtedsd_2020b_0803a_000{2}_001.root -d CdTe_Lab -o 400n20_{1}source_cali_{3} -e ${MACRODIR}/auxfile/spline_calibration_2mmtest_400n20_{3}.root -n 2000000 ::: Ba ::: 12 13 14 15 16 ::: merge_1008
#parallel --eta -j ${NCORES} python3 main.py ../data/minami_data/400n20/{1}/cdtedsd_2020b_0805a_000{2}_001.root -d CdTe_Lab -o 400n20_{1}source_cali_{3} -e ${MACRODIR}/auxfile/spline_calibration_2mmtest_400n20_{3}.root -n 2000000 ::: Co ::: 08 09 10 11 12 ::: merge_1008
#
#parallel --eta -j ${NCORES} python3 main.py ../data/minami_data/500n20/{1}/cdtedsd_2020b_0720a_000{2}_001.root -d CdTe_Lab -o 500n20_{1}source_cali_{3} -e ${MACRODIR}/auxfile/spline_calibration_2mmtest_{3}.root -n 2000000 ::: Am ::: 32 33 34 35 36 ::: merge_1008
#parallel --eta -j ${NCORES} python3 main.py ../data/minami_data/500n20/{1}/cdtedsd_2020b_0727a_000{2}_001.root -d CdTe_Lab -o 500n20_{1}source_cali_{3} -e ${MACRODIR}/auxfile/spline_calibration_2mmtest_{3}.root -n 2000000 ::: Ba ::: 08 09 10 11 12 ::: merge_1008
#parallel --eta -j ${NCORES} python3 main.py ../data/minami_data/500n20/{1}/cdtedsd_2020b_0720a_000{2}_001.root -d CdTe_Lab -o 500n20_{1}source_cali_{3} -e ${MACRODIR}/auxfile/spline_calibration_2mmtest_{3}.root -n 2000000 ::: Co ::: 14 15 16 17 18 ::: merge_1008



# =====
# ================== make ntuplke & plots J-PARC 2020March ====================
# =====
#parallel --eta -j ${NCORES} python3 main.py ${NTUPDIRCDTE}_merge/20200307a_{1}.root -o merge ::: 55to73 77to95 95to111
   # *** Si ***
#parallel --eta -j ${NCORES} python3 main.py ${NTUPDIRSI}/test_f_000{1}_001.root -d Si -e ${MACRODIR}/auxfile/spline_calibration.root ::: 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 
   # *** Scan cut ***
#parallel --eta -j ${NCORES} python3 main.py ${NTUPDIRCDTE}/20200307a_00057_001.root -o cut{1}_delta{2} -cut {1} -m {2} ::: 5 10 20 40 ::: 10 5 3 2
#parallel --eta -j ${NCORES} python3 main.py ${NTUPDIRSI}/test_f_00007_001.root -d Si -e ${MACRODIR}/auxfile/spline_calibration.root -o cut{1}_delta{2} -cut {1} -m {2} ::: 2 3 8 12 ::: 10 5 3 2



# =====
# ================== run rotation 2D plots and FBP image ====================
# =====
#python3 image.py -i ${OUTDIR}/CdTe_root_fix -d CdTe -o LP_0909 
#python3 image.py -i ${OUTDIR}/CdTe_root_fix -d CdTe -o 35MeV
#python3 image.py -i ${OUTDIR}/Si_root_fix -d Si -o 1120




# =====
# ================== run MLEM ====================
# =====
#python3 mksr.py --imageinput /Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/figs/repro_3Dimage.CdTe_LP_0909.root 
#python3 mksr.py --imageinput /Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/figs/repro_3Dimage.CdTe_30MeV.root -o 30MeV -l 1
