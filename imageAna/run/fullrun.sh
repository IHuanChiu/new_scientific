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
# ================== simple test run ====================
# =====
#python3 main.py /Users/chiu.i-huan/Desktop/new_scientific/imageAna/data/JPARC2021Apri/STD27MeV/ -d CdTe_Lab -e ${MACRODIR}/auxfile/cdtedsd_2020a_cal_3_m5c400v.root -o STD27MeV

#python3 main.py /Users/chiu.i-huan/Desktop/new_scientific/imageAna/data/watanabe_sample/cdtedsd_inseki2_tmp1.root -d CdTe_Lab -e ${MACRODIR}/auxfile/cdtedsd_2020a_cal_3_m5c400v.root -o STD27MeV_fix
#parallel --eta -j ${NCORES} python3 main.py /Users/chiu.i-huan/Desktop/new_scientific/imageAna/data/JPARC2021Apri/Co57/cdtedsd_0402a_0000{1}_001.root -d CdTe_Lab -o Co57_{1} -e ${MACRODIR}/auxfile/cdtedsd_2020a_cal_3_m5c400v.root ::: 5 6 7 8 9 
#parallel --eta -j ${NCORES} python3 main.py /Users/chiu.i-huan/Desktop/new_scientific/imageAna/data/JPARC2021Apri/Co57/cdtedsd_0403a_0000{1}_001.root -d CdTe_Lab -o Co57_{1} -e ${MACRODIR}/auxfile/cdtedsd_2020a_cal_3_m5c400v.root ::: 3 4 5 6 7 8 9
#python3 sum_plots.py ../../../2020.12.09/sumrootblank2.root -d CdTe_JPARCDec -o blank2
#python3 main.py ../data/IPMU2021Aug_OsakaNo7/500n20/Image/20210806a_00003_001.root -d FEC2 -o 500n20_image_newPOI -e ${MACRODIR}/auxfile/spline_calibration_osaka7_500n20_merge.root -n 50000

# =====
# ================== 2mm CdTe OsakaNo7 (2021.08) ====================
# =====
#python3 main.py ../data/IPMU2021Aug_OsakaNo7/500n20/Image/20210806a_00003_001.root -d FEC2 -o 500n20_image_newPOI -e ${MACRODIR}/auxfile/spline_calibration_osaka7_500n20_merge.root  
#python3 main.py ../data/IPMU2021Aug_OsakaNo7/500n20/Am/20210804a_00006_001.root -d FEC2 -o 500n20_Am_test -e ${MACRODIR}/auxfile/spline_calibration_osaka7_500n20_merge.root  
#python3 main.py ../data/IPMU2021Aug_OsakaNo7/500n20/Ba/20210804a_00009_001.root -d FEC2 -o 500n20_Ba_test -e ${MACRODIR}/auxfile/spline_calibration_osaka7_500n20_merge.root  
#python3 main.py ../data/IPMU2021Aug_OsakaNo7/500n20/Co/20210804a_00016_001.root -d FEC2 -o 500n20_Co_Ecorr2 -e ${MACRODIR}/auxfile/spline_calibration_osaka7_500n20_merge.root  
 # *** calibration sample ***
#parallel --eta -j ${NCORES} python3 main.py ../data/IPMU2021Aug_OsakaNo7/500n20/{1}/20210806a_0000{2}_001.root -d FEC2 -o 500n20_{1}_newPOI -e ${MACRODIR}/auxfile/spline_calibration_osaka7_500n20_merge.root ::: Image ::: 3 4 5 6 7 8 
#parallel --eta -j ${NCORES} python3 main.py ../data/IPMU2021Aug_OsakaNo7/500n20/{1}/20210804a_000{2}_001.root -d FEC2 -o 500n20_{1} -e ${MACRODIR}/auxfile/spline_calibration_osaka7_500n20_merge.root ::: Ba ::: 09 10 11
#parallel --eta -j ${NCORES} python3 main.py ../data/IPMU2021Aug_OsakaNo7/500n20/{1}/20210804a_000{2}_001.root -d FEC2 -o 500n20_{1} -e ${MACRODIR}/auxfile/spline_calibration_osaka7_500n20_merge.root ::: Co ::: 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 


# =====
# ================== 2mm CdTe old (2020.07) ====================
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
# ================== CdTeDSD2 2mm J-PARC (2021.06) ====================
# =====
#python3 main.py ../data/CdTeDSD2_2mm_Cali/500n30/Am/cdtedsd2_0602b_am_500v.root -d CdTe_Lab -o 500n30_Am -e ${MACRODIR}/auxfile/spline_calibration_cdtedsd2_500n30_merge.root  
#python3 main.py ../data/CdTeDSD2_2mm_Cali/500n30/Ba/cdtedsd2_0602b_ba_500v.root -d CdTe_Lab -o 500n30_Ba -e ${MACRODIR}/auxfile/spline_calibration_cdtedsd2_500n30_merge.root  
#python3 main.py ../data/CdTeDSD2_2mm_Cali/500n30/Co/cdtedsd2_0602b_co_500v.root -d CdTe_Lab -o 500n30_Co -e ${MACRODIR}/auxfile/spline_calibration_cdtedsd2_500n30_merge.root  
 # *** calibration sample ***
#parallel --eta -j ${NCORES} python3 main.py ../data/CdTeDSD2_2mm_Cali/500n30/{1}/cdtedsd2_0607a_000{2}_001.root -d CdTe_Lab -o 500n30_{1} -e ${MACRODIR}/auxfile/spline_calibration_cdtedsd2_500n30_merge.root ::: Am ::: 25 26 27 28 29 
#parallel --eta -j ${NCORES} python3 main.py ../data/CdTeDSD2_2mm_Cali/500n30/{1}/cdtedsd2_0609a_000{2}_001.root -d CdTe_Lab -o 500n30_{1} -e ${MACRODIR}/auxfile/spline_calibration_cdtedsd2_500n30_merge.root ::: Am ::: 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 
#parallel --eta -j ${NCORES} python3 main.py ../data/CdTeDSD2_2mm_Cali/500n30/{1}/cdtedsd2_0607a_000{2}_001.root -d CdTe_Lab -o 500n30_{1} -e ${MACRODIR}/auxfile/spline_calibration_cdtedsd2_500n30_merge.root ::: Ba ::: 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 
#parallel --eta -j ${NCORES} python3 main.py ../data/CdTeDSD2_2mm_Cali/500n30/{1}/cdtedsd2_0607a_000{2}_001.root -d CdTe_Lab -o 500n30_{1} -e ${MACRODIR}/auxfile/spline_calibration_cdtedsd2_500n30_merge.root ::: Co ::: 04 05 06 07 08 09
#parallel --eta -j ${NCORES} python3 main.py ../data/CdTeDSD2_2mm_Cali/500n30/{1}/cdtedsd2_0609a_000{2}_001.root -d CdTe_Lab -o 500n30_{1} -e ${MACRODIR}/auxfile/spline_calibration_cdtedsd2_500n30_merge.root ::: Co ::: 06 07 08 09 10 18 19 20 21 22 23 24 25


# =====
# ================== make ntuplke & plots J-PARC (2020.03) ====================
# =====
#parallel --eta -j ${NCORES} python3 main.py ${NTUPDIRCDTE}_merge/20200307a_{1}.root -o merge ::: 55to73 77to95 95to111
   # *** Si ***
#parallel --eta -j ${NCORES} python3 main.py ${NTUPDIRSI}/test_f_000{1}_001.root -d Si -e ${MACRODIR}/auxfile/spline_calibration.root ::: 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 
#parallel --eta -j ${NCORES} python3 main.py /Users/chiu.i-huan/Desktop/new_scientific/imageAna/data/Sidata_calibration/20200225a_000{1}_001.root -d Si -e ${MACRODIR}/auxfile/spline_calibration.root ::: 02 03 04 05 06 07 08 09 10
#python3 main.py /Users/chiu.i-huan/Desktop/new_scientific/imageAna/data/Sidata_calibration/20200225a_image.root -d Si -e ${MACRODIR}/auxfile/spline_calibration.root 
   # *** Scan cut ***
#parallel --eta -j ${NCORES} python3 main.py ${NTUPDIRCDTE}/20200307a_00057_001.root -o cut{1}_delta{2} -cut {1} -m {2} ::: 5 10 20 40 ::: 10 5 3 2
#parallel --eta -j ${NCORES} python3 main.py ${NTUPDIRSI}/test_f_00007_001.root -d Si -e ${MACRODIR}/auxfile/spline_calibration.root -o cut{1}_delta{2} -cut {1} -m {2} ::: 2 3 8 12 ::: 10 5 3 2



# =====
# ================== run rotation 2D plots and FBP image ====================
# =====
#python3 image.py -i ${OUTDIR}/CdTe_root_fix -d CdTe_30MeV -o forpaper
#python3 image.py -i ${OUTDIR}/CdTe_root_fix -d CdTe_30MeV -o no14keV
#python3 image.py -i ${OUTDIR}/Si_root_fix -d Si -o 1120
#python3 image.py -i ${OUTDIR}/JPARC2020March_Si_sum.root -o forSipaper_yx -d Si_30MeV -c 0 -s 1
#python3 image.py -i ${OUTDIR}/JPARC2020March_Si_sum.root -o forSipaper -d Si_35MeV


# =====
# ================== run MLEM ====================
# =====
   # plots is x:y -> check movemeasurement & updateImage 
#python3 mksr.py --imageinput /Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/figs/repro_3Dimage.CdTe_30MeV.root -o 30MeV -l 1 
#python3 mksr.py --imageinput /Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/figs/repro_3Dimage.CdTe_30MeV_no14keV.root -o 30MeV_no14keV -l 15
#python3 mksr.py --imageinput /Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/figs/repro_3Dimage.CdTe_30MeV_no14keV.root -o 30MeV_osem_no14keV -l 15 -t osem
#python3 mksr.py --imageinput /Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/figs/repro_3Dimage.CdTe_30MeV_forpaper.root -o 30MeV_ImageCut_w_rot12_noX_osem_forpaper -l 10 -t osem
#python3 mksr.py --imageinput /Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/figs/repro_3Dimage.CdTe_30MeV_forpaper.root -o 30MeV_cutR_forpaper -l 15
#python3 mksr.py --imageinput /Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/figs/repro_3Dimage.CdTe_30MeV_forpaper.root -o 30MeV_mlem_forpaper -l 15
#python3 mksr.py --imageinput /Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/figs/repro_3Dimage.CdTe_30MeV_forpaper.root -o 30MeV_cutT10_10per_Lyaxis_mlem_forpaper -l 80
#python3 mksr.py --imageinput /Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/figs/repro_3Dimage.CdTe_30MeV_forpaper.root -o 30MeV_cutT10_10per_Lyaxis_Yshift_zero_osem_forpaper -l 20 -t osem -testcut 0
#python3 mksr.py --imageinput /Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/figs/repro_3Dimage.CdTe_30MeV_forpaper.root -o 30MeV_cutT10_10per_Lyaxis_Yshift_0p5_osem_forpaper -l 20 -t osem -testcut 0.5
#python3 mksr.py --imageinput /Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/figs/repro_3Dimage.CdTe_30MeV_forpaper.root -o 30MeV_cutT10_10per_Lyaxis_Yshift_0p75_osem_forpaper -l 20 -t osem -testcut 0.75
#python3 mksr.py --imageinput /Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/figs/repro_3Dimage.CdTe_30MeV_forpaper.root -o 30MeV_cutT10_10per_Lyaxis_Yshift_1_osem_forpaper -l 20 -t osem -testcut 1
#python3 mksr.py --imageinput /Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/figs/repro_3Dimage.CdTe_30MeV_forpaper.root -o 30MeV_cutT10_10per_Lyaxis_Yshift_1p25_osem_forpaper -l 20 -t osem -testcut 1.25
#python3 mksr.py --imageinput /Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/figs/repro_3Dimage.CdTe_30MeV_forpaper.root -o 30MeV_cutT10_10per_Lyaxis_Yshift_1p5_osem_forpaper -l 20 -t osem -testcut 1.5

#final 
#python3 mksr.py --imageinput /Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/figs/repro_3Dimage.CdTe_30MeV_forpaper.root -o 30MeV_cutT10_10per_Lyaxis_Yshift_1p25_mlem_forpaper -l 100 -t mlem
#python3 mksr.py --imageinput /Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/figs/repro_3Dimage.CdTe_30MeV_forpaper.root -o 30MeV_mlem_forpaper -l 100 -t mlem

#mc
python3 mksr.py --imageinput /Users/chiu.i-huan/Desktop/geant4WS/geant4-xrayimage/macro/root/repro_MC.root -o mc_test -l 10 -t mlem
