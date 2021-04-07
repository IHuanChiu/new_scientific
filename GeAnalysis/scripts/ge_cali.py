import os,time
_unit=input("ch/keV : ")
_es=input("small energy : ")
_el=input("large energy : ")
_ideal=float(_unit)*(float(_el)-float(_es))
print("ideal value={}".format(_ideal))
while 1:
   _p1=input("1st peak : ")
   _p2=input("2nd peak : ")
   print("Precision : {}".format((int(_p2)-int(_p1))/_ideal))
   _gain=input(" gain : ")
   print("next gain={}".format(float(_gain)*_ideal/(int(_p2)-int(_p1))))
