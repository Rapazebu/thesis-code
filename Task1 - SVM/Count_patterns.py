# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 12:05:20 2022

@author: marta
"""

import json

def ReturnDatabase(filename):
    f = open(filename)
    r = json.load(f)
    data = r['data']
    dataClean = []
    for x in data: 
        if x[1] != 'x' and x[1] != 'u' and '.' not in x[1] and '_' not in x[0]:
            dataClean.append(x)
            
    
    return dataClean

#ritorna verbi con almeno tre pattern con più di tre frasi 
#non funziona sigh 

def ReturnVerbs(data):
    verbs = []
    for x in data: 
        if x[0] not in verbs:
            verbs.append(x[0])
    return verbs

    
def ReturnVerbsMoreThanThree(verbs, patterns):
    count = 0
    Ls2 = []
    Ls3 = []
    for pattern in patterns:
        for verb in verbs:
            if verb in pattern:
                print(verb)
                count = count + 1
                tup = (pattern, patterns[pattern])
                if count > 2:
                    Ls2.append(tup)
                if count > 3:
                    Ls3.append(tup)
    set(Ls2)
    set(Ls3)
    return Ls2, Ls3
                

    


if __name__ == "__main__":
    data = ReturnDatabase('G:/.shortcut-targets-by-id/1YeL3GRFiK8VcX2qGQ49XTVJekScNZ2CV/COPREDICATION DUESSELDORF C11/Datasets (vari corpora)/TPAS corpus.json')
    
    patterns = {}
    for x in data:
        if x[1] != 'x' and x[1] != 'u' and '.' not in x[1] and '_' not in x[0]:
            pattern = x[0] + " " + x[1]
            if pattern not in patterns: 
                patterns[pattern] = 1
            else: 
                patterns[pattern]  = patterns[pattern] + 1
    
    MoreThan30 = {}
    for key in patterns: 
        if patterns[key] > 30:
            MoreThan30[key] = patterns[key]
    
    verbs = ReturnVerbs(data)
    Ls2, Ls3 = ReturnVerbsMoreThanThree(verbs, MoreThan30)

#%%
    
from codecs import *
fh = open("GoodVerbss.txt", "w", "utf-8")
for x in MoreThan30:
    fh.write(x + " :" + str(MoreThan30[x]) + "\n")
fh.close()


#%%
from codecs import *
fh = open("Counts_TPAS_databases.txt", "w", "utf-8")
fh.write("TPAS patterns are 5683 (x, u, .m, .a, .f not included), of which:\n")
fh.write("\t 1422 patterns have more than 30 instances\n")
fh.write("\t 1852 patterns have more than 20 instances\n\n")
fh.write("Patterns with less then 20 instances are 3687, and they are listed below in the format 'pattern: n° instances': \n\n")
for x in MoreThan30:
    fh.write(x + " :" + str(MoreThan30[x]) + "\n")
fh.close()

#%% 
count = 0
for x in data:
    if x[0] == 'rientrare':s
        count = count + 1
   print(count)

