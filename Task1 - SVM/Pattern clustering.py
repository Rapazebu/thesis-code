# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 09:54:46 2022

@author: marta
"""
# this part is to create a dataframe


import json 
import pandas as pd 

def OpenFile(filename):
    f = open(filename)
    r = json.load(f)
    data = r['data']
    return data

def CreateDataFrameFeatures(data):
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
    



#%%


data = OpenFile('G:/.shortcut-targets-by-id/1YeL3GRFiK8VcX2qGQ49XTVJekScNZ2CV/COPREDICATION DUESSELDORF C11/Datasets (vari corpora)/database.json')
   
D = CreateDataFrame1(data)
df = pd.DataFrame(D)
    
#%%

