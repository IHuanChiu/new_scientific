#!/usr/bin/env python3
###################################
# Written by Miho Katsuragawa (Jun 26th, 2020)
# 
# Search All DB
# > python3 search_muX.py
#
# Search for energy (default energy range is 5 keV)
#   python3 search_muX.py -e (Energy)
#   python3 search_muX.py -e (Energy) -r (Energy range)
#
# Search for atom
#   python3 search_muX.py -a (Atom)
#
# Search for mass number
#   python3 search_muX.py -m (Mass number)
#
# e.g., if you search muonic X-ray of carbon (C) in 70 keV to 90, tap 
#   python3 search_muX.py -e 80 -r 10 -a C
###################################

import sys, os
import argparse
import sqlite3

def interface():
    parser = argparse.ArgumentParser(description = 'Serch mu-X or atm.')
    parser.add_argument('-e', '--energy', type=float, default=0.0, help=' Energy (keV) ')
    parser.add_argument('-r', '--rng', type=int, default=5, help='Range of energy (keV).')
    parser.add_argument('-a', '--atomname', type=str, default='None', help='e.g., C')
    parser.add_argument('-m', '--maxatom', type=int, default=50, help='Maximum atmic number')
    parser.add_argument('-n', '--maxn', type=int, default=5, help='Maximum n_top')
    args = parser.parse_args()
    return args

def SearchDB(dbname, e, w, a, m, n):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    selection = ' DB'
    
    if (e == 0.0):selection = selection + ' where energy > ' + str(e)
    else: selection = selection + ' where energy > ' + str(e-w) + ' and energy < ' + str(e+w)
    
    if (a == 'None'):pass
    else: selection = selection + ' and atom = \'' + a +'\''
    
    selection = selection + ' and mass <= ' + str(m)
    selection = selection + ' and n_top <= ' + str(n)
        
    c.execute('SELECT * FROM' + selection)
    results = c.fetchall()
    
    print('**************************************************************')
    print('     Search with : ')
    print('          ', selection)
    print('**************************************************************')
    print('   Atom         Mass     Energy     n_top     n_down')
    print(' --------    ---------  --------  --------  --------')
    
    moji = 10
    for result in results: 
       print(result[0].center(moji) + str(result[1]).rjust(moji)  + str(result[4]).rjust(moji)+ str(result[2]).rjust(moji)+ str(result[3]).rjust(moji))

    return 0

def main():
    args = interface()
    energy = args.energy
    rng = args.rng
    atomname = args.atomname
    maxatom = args.maxatom
    maxn = args.maxn
    
    dbname = 'XmuDB.db'
    
    SearchDB(dbname, energy, rng, atomname, maxatom, maxn)
   
    return 0

if __name__ == '__main__':
    main()
