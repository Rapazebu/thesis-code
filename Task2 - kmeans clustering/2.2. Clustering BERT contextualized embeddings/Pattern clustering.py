# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 09:54:46 2022

@author: marta
"""

import json 
import pandas as pd 
from codecs import *

#%%

# PART 1. Create a dataframe from my set of features

def OpenFile(filename):
    f = open(filename)
    r = json.load(f)
    data = r['data']
    return data

def CreateDataFrame1(data):
    datapoints = []
    subjects = []
    objects = []
    indobjects = []
    clausals = []
    
    for item in data: #item sono tanti quanti i verbi
        verb = item['query']
        labels = item['labels']
        for d in labels:            
            
            datas = d['data']
            if 'slots' in datas: 
                slots = datas['slots']
                label = d['label']    #label sono tante quante i datapoint, per ogni verbo tante quante i pattern
                datapoints.append(verb + '_' + label)
                
                sbj = 'x'
                obj = 'x'
                iobj = 'x'
                claus = 'x'
                for x in slots:
                    if x['slot'] == 'subject':
                        sbj = (x['semtype'])
                    if x['slot'] == 'object':
                        obj = (x['semtype'])
                    if x['slot'] == 'prep_compl':
                        iobj = (x['semtype'])
                    if x['slot'] == 'clausals':
                        claus = (x['semtype'])
            
                subjects.append(sbj)
                objects.append(obj)
                clausals.append(claus)
                indobjects.append(iobj)
                
    print('subjects: ', len(subjects))
    print('objects', len(objects))
    print("datapoints: ", len(datapoints))
    
    D = {'datapoints': datapoints, 'subjects':subjects, 'objects':objects, 'clausals':clausals, 'prep_compl':indobjects }
    
    return D

data = OpenFile('G:/.shortcut-targets-by-id/1YeL3GRFiK8VcX2qGQ49XTVJekScNZ2CV/COPREDICATION DUESSELDORF C11/Datasets (vari corpora)/database.json')
D = CreateDataFrame1(data)
df = pd.DataFrame(D)


#%%
# PART 2. Create the vector (0/1) given the semantic type of a slot
 
def readjson(filename):
    f = open(filename, "r", "utf-8")
    r = json.load(f)
    data = r["_sub"]
    return data


def search_m(Ls, mytype, vec = [], figliodic = False): # don't forget specify vec = [], otherwise it appends to the last computed values 
    for D in Ls:
        
        # controllo se il tipo è il mio tipo
        if D['_st'] in mytype:
            trovato = True
            figliodic = True
        else:
            trovato = False
        
        # se il tipo è il mio tipo o se è figlio annoto la lieta notizia
        if trovato == True or figliodic == True:
            vec.append(1.) 
            print(1, D['_st'])
        else: 
            vec.append(0.)
    
        # se ci sono figli richiamo la funzione ricordando a figliodic se il padre era il mio tipo
        if D['_sub'] == []:
            pass 
        else:
            search_m(D['_sub'], mytype, vec, figliodic)
            
        # impedisco di segnare positivamente i fratelli del mio tipo
        if trovato == True:
            figliodic = False
            
    return vec


types = readjson("G:/.shortcut-targets-by-id/1YeL3GRFiK8VcX2qGQ49XTVJekScNZ2CV/COPREDICATION DUESSELDORF C11/Datasets (vari corpora)/semantic_types.json")


# concatenate the vectors for each row

def ritornavettorone(types, df):
    vettoroni = []
    for index, row in df.iterrows():
        v1 = search_m(types, row['subjects'], [])
        v2 = search_m(types, row['objects'], [])
        v3 = search_m(types, row['clausals'], [])
        v4 = search_m(types, row['prep_compl'], [])
        vettorone = v1 + v2 + v3 + v4
        vettoroni.append(vettorone)
    return vettoroni


List = ritornavettorone(types, df)
df = df.assign(vectors = List)

#%%

# PART 3. clustering vectors

from sklearn.cluster import KMeans

X = np.array(List)
n_clusters = 40
kmeans = KMeans(n_clusters, random_state=0).fit(X)
labels = kmeans.labels_
centroids = kmeans.cluster_centers_

#visualize the list of verbs that are in each cluster

metadati = df.datapoints

Ls = []
n = len(metadati)
for i in range(n):
    tup = (metadati[i], labels[i])
    Ls.append(tup)

Ls.sort(key = lambda x: x[1])

print(Ls)


#%%


f = open("k-means_40_clusters_M.txt", "a")

for j in range(n_clusters + 1):
    f.write("cluster n° " + str(j) + "\n")
    for x in Ls:
        if x[1] == j:
            f.write(str(x[0]) + ", ")
    f.write("\n")
    f.write("\n")
f.close()







