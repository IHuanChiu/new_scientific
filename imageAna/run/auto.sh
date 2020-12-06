ANADIR="/Users/ninomiya/Desktop/new_scientific/imageAna/"
MACRODIR="/Users/ninomiya/Desktop/new_scientific/imageAna/macro/"
DATAPATH="/Users/ninomiya/Desktop/data_ASIC/20201124"
CALIFILES=${MACRODIR}/auxfile/spline_calibration_machine2_400n5_merge.root
wait_min=1
OUTNAME=test
sumfile_name=sumroot.root
while : 
do
    LASTFILE=`ls $DATAPATH/ | grep -i jparcdata | grep -v .root | tail -1`
    LASTROOTFILE=`ls $ANADIR/run/root/ | grep -i jparcdata | tail -1`

    $DATAPATH/rawdata2root_v10_vata450.sh $DATAPATH/${LASTFILE}

				echo " ============================== ANALYSIS ============================== "
    python3 main.py $DATAPATH/${LASTFILE}.root -d CdTe_Lab -e $CALIFILES -o ${OUTNAME} 

				if [ -e $ANADIR/run/root/$sumfile_name ]; then
				   rm $ANADIR/run/root/$sumfile_name
				fi
				hadd $ANADIR/run/root/$sumfile_name $ANADIR/run/root/*.root
				python sum_plots.py $ANADIR/run/root/$sumfile_name -d CdTe_Lab -o ${OUTNAME}

				echo " ============================== OUTPUTs ============================== "
				echo " NTUPLE: $ANADIR/run/root/${LASTFILE}_${OUTNAME}.root"
				echo " FIGs: $ANADIR/run/figs/${LASTFILE}_${OUTNAME}.pdf"
				open -a Preview $ANADIR/run/figs/${LASTFILE}_${OUTNAME}.pdf
				open -a Preview $ANADIR/run/figs/sumplots_${OUTNAME}.pdf

				echo " ============================== Wait $wait_min mins ============================== "
				sleep $(($wait_min*60))
				killall Preview
done
