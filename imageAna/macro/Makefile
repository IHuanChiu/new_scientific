RUN=python main.py

TESTDIR=/Users/chiu.i-huan/Desktop/new_scientific/imageAna/data/testinput
SAMPLEDIR=/Users/chiu.i-huan/Desktop/new_scientific/imageAna/data/20200305/root

LOGDIR=/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/log

DATE=$(shell date +'%b%d'| tr '[:upper:]' '[:lower:]')

.PHONY: all Data15 Data16 ZInc Top DYtautau Zee Zmumu Wtaunu Wmunu Wenu Diboson ggH bbH ZP DijetFF15 DijetFF16 DijetFFMC

all: test


test:
	${RUN} ${TESTDIR} -cpu 2 -n 1000 

test2:
	${RUN} ${TESTDIR} -cpu 2 -n 1000 2>&1  |   tee ${LOGDIR}/log2_$@_${DATE}
