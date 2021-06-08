#python calib.py -i /Users/chiu.i-huan/Desktop/new_scientific/imageAna/data/machine2_cali --table energy_table/machine2_data -s Am -v 400n5
#python calib.py -i /Users/chiu.i-huan/Desktop/new_scientific/imageAna/data/machine2_cali --table energy_table/machine2_data -s Co -v 400n5
#python calib.py -i /Users/chiu.i-huan/Desktop/new_scientific/imageAna/data/machine2_cali --table energy_table/machine2_data -s Ba -v 400n5

python calib.py -i /Users/chiu.i-huan/Desktop/new_scientific/imageAna/data/CdTeDSD2_2mm_Cali -o cdtedsd2 --table energy_table/cdtedsd2_data -s Am -v 500n30
python calib.py -i /Users/chiu.i-huan/Desktop/new_scientific/imageAna/data/CdTeDSD2_2mm_Cali -o cdtedsd2 --table energy_table/cdtedsd2_data -s Co -v 500n30
python calib.py -i /Users/chiu.i-huan/Desktop/new_scientific/imageAna/data/CdTeDSD2_2mm_Cali -o cdtedsd2 --table energy_table/cdtedsd2_data -s Ba -v 500n30
python merge_spline.py -o cdtedsd2 -v 500n30
