NTUPDIR="/Users/chiu.i-huan/Desktop/new_scientific/data/minami_data"
NCORES=8

parallel --eta -j ${NCORES} python3 stability.py -i ${NTUPDIR} -c {1} -s {2} -tr {3} -o 0915 ::: 300n20 400n20 500n20 ::: Am Ba Co ::: 3

#parallel --eta -j ${NCORES} python3 stability.py -i ${NTUPDIR} -c {1} -s {2} -tr {3} -o 0915 ::: 300n20 ::: 0901Am Am Ba Co ::: 5 2
#parallel --eta -j ${NCORES} python3 stability.py -i ${NTUPDIR} -c {1} -s {2} -tr {3} -o 0915 ::: 400n20 ::: 0803Co Am Ba Co ::: 5 2
#parallel --eta -j ${NCORES} python3 stability.py -i ${NTUPDIR} -c {1} -s {2} -tr {3} -o 0915 ::: 500n20 ::: 0720Am 0720Ba Am Ba Co ::: 5 2

#parallel --eta -j ${NCORES} python3 stability.py -i ${NTUPDIR} -c {1} -s {2} -tr {3} -o 0915 ::: 400n20 500n20 ::: Am Co ::: 3
