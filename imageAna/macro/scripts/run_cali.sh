# === Ryugu CdTeDSD1 ===
#python calib.py -i /Users/chiu.i-huan/Desktop/new_scientific/imageAna/data/machine2_cali --table energy_table/machine2_data -s Am -v 400n5
#python calib.py -i /Users/chiu.i-huan/Desktop/new_scientific/imageAna/data/machine2_cali --table energy_table/machine2_data -s Co -v 400n5
#python calib.py -i /Users/chiu.i-huan/Desktop/new_scientific/imageAna/data/machine2_cali --table energy_table/machine2_data -s Ba -v 400n5

# === Ryugu CdTeDSD2 ===
#python calib.py -i /Users/chiu.i-huan/Desktop/new_scientific/imageAna/data/CdTeDSD2_2mm_Cali -o cdtedsd2 --table energy_table/cdtedsd2_data -s Am -v 500n30
#python calib.py -i /Users/chiu.i-huan/Desktop/new_scientific/imageAna/data/CdTeDSD2_2mm_Cali -o cdtedsd2 --table energy_table/cdtedsd2_data -s Ba -v 500n30
#python calib.py -i /Users/chiu.i-huan/Desktop/new_scientific/imageAna/data/CdTeDSD2_2mm_Cali -o cdtedsd2 --table energy_table/cdtedsd2_data -s Co -v 500n30
#python merge_spline.py -o cdtedsd2 -v 500n30

# === Osaka CdTeDSD7 ===
python calib.py -i /Users/chiu.i-huan/Desktop/new_scientific/imageAna/data/IPMU2021Aug_OsakaNo7 -o osaka7 --table energy_table/osakacdte7_data -v 500n20 -s Am
python calib.py -i /Users/chiu.i-huan/Desktop/new_scientific/imageAna/data/IPMU2021Aug_OsakaNo7 -o osaka7 --table energy_table/osakacdte7_data -v 500n20 -s Ba
python calib.py -i /Users/chiu.i-huan/Desktop/new_scientific/imageAna/data/IPMU2021Aug_OsakaNo7 -o osaka7 --table energy_table/osakacdte7_data -v 500n20 -s Co
python merge_spline.py -o osaka7 -v 500n30
