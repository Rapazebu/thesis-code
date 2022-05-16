# -*- coding: utf-8 -*-
"""
Created on Sun Feb 27 15:07:00 2022

@author: marta
"""
import numpy as np
from numpy import array
from scipy.cluster.vq import vq, kmeans, whiten, kmeans2


""" questo serve a ottenere la matrice"""

def ritornamatrice(vettori):
    Ls = []
    for x in vettori: 
        rigasplit = x.split("\t")
        raw = rigasplit[1:]
        Ms = []
        for y in raw:
            Float = float(y)
            Ms.append(Float)
        Ls.append(Ms)
    return Ls

features = array(ritornamatrice(vettori))

#whitened normalizza features
whitened = whiten(features) 

#kmeans(obs, k_or_guess) RITORNA I CENTROIDI 
k_or_guess = 40
ks, distortion = kmeans(whitened,k_or_guess)

#kmeans2()
#
centroids, labels = kmeans2(whitened, k_or_guess)

Ls = []

n = len(metadati)
for i in range(n):
    tup = (metadati[i], labels[i])
    Ls.append(tup)
    

Ls.sort(key = lambda x: x[1])

#%%


 #f = open("risultati_clustering_01/03.txt", "a", "utf-8")
f = open("k-means_40_clusters.txt", "a")
for j in range(k_or_guess + 1):
    f.write("cluster n° " + str(j) + "\n")
    for x in Ls:
        if x[1] == j:
            f.write(str(x[0]) + ", ")
    f.write("\n")
    f.write("\n")
f.close()
    

    
    

    
