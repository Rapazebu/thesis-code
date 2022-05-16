import json 
import pandas as pd 
import numpy as np 
import simplemma
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel
import nltk 
from nltk.stem import SnowballStemmer


def ReturnDatabase(filename):
    f = open(filename)
    r = json.load(f)
    data = r['data']
    dataClean = []
    for x in data: 
        if x[1] != 'x' and x[1] != 'u' and '.' not in x[1] and '_' not in x[0]:
            dataClean.append(x)
    return dataClean

def count(dataClean):
  patterns = {}
  for x in dataClean:
    pattern = (x[0], x[1])
    if pattern not in patterns: 
       patterns[pattern] = 1
    else: 
       patterns[pattern]  = patterns[pattern] + 1  
  return patterns #(abbaiare,1): 3, (abbaiare,2): 5

def getsentences(data, patterns):
  Ls = []
  for x in data: 
    tup = (x[0], x[1])
    if patterns[tup] > 30:
      trip = (x[0], x[1], x[2])
      Ls.append(trip)
  return Ls

def gettokens_SIMPLEMMA(Ls):
  Ms = []
  langdata = simplemma.load_data('it')
  for x in Ls: 
    sentence = x[2].split(" ")
    for tok in sentence:
      lemmatized = simplemma.lemmatize(tok, langdata)
      if lemmatized == x[0]:
        tup = (x[0], x[1], tok, x[2])
        Ms.append(tup)
        break
  return Ms

def gettokens_SNOWBALL(Ls):
  Ms = []
  stemmer_snowball = SnowballStemmer('italian')
  for x in Ls: 
    sentence = x[2].split(" ")
    verb_stem = stemmer_snowball.stem(x[0])
    for tok in sentence:
      tok_stem = stemmer_snowball.stem(tok)
      #print(tok, tok_stem)
      if tok_stem == verb_stem:
        tup = (x[0], x[1], tok, x[2])
        Ms.append(tup)
        break
  return Ms

  # get embeddings 
 
def get_word_idx(sent: str, word: str):
     return sent.split(" ").index(word)

def get_hidden_states(encoded, token_ids_word, model, layers):
     """Push input IDs through model. Stack and sum `layers` (last four by default).
        Select only those subword token outputs that belong to our word of interest
        and average them."""
     with torch.no_grad():
         output = model(**encoded)
 
     # Get all hidden states
     states = output.hidden_states
     # Stack and sum all requested layers
     output = torch.stack([states[i] for i in layers]).sum(0).squeeze()
     # Only select the tokens that constitute the requested word
     word_tokens_output = output[token_ids_word]
 
     return word_tokens_output.mean(dim=0)
 
def get_word_vector(sent, idx, tokenizer, model, layers):
     """Get a word vector by first tokenizing the input sentence, getting all token idxs
        that make up the word of interest, and then `get_hidden_states`."""
     encoded = tokenizer.encode_plus(sent, return_tensors="pt")
     # get all token idxs that belong to the word of interest
     token_ids_word = np.where(np.array(encoded.word_ids()) == idx)
 
     return get_hidden_states(encoded, token_ids_word, model, layers)
 
def main(sent, tok, layers=None):
     # Use last four layers by default
     layers = [-4, -3, -2, -1] if layers is None else layers

     tokenizer = AutoTokenizer.from_pretrained("dbmdz/bert-base-italian-xxl-cased")
     model = AutoModel.from_pretrained("dbmdz/bert-base-italian-xxl-cased", output_hidden_states=True) 
     idx = get_word_idx(sent, tok)

     word_embedding = get_word_vector(sent, idx, tokenizer, model, layers)
     return word_embedding 

     # appends the vector to the list, i. e. returns a list label, sentence, vector

def getvectors(Ms):
  Ns = []
  for x in Ms: 
    try:
        embedding = main(x[3], x[2])
        label = x[0] + "_" + x[1]
        tup = (label, x[3], embedding)
        Ns.append(tup)
    except: 
        print ("non riesco a trovarti l'embedding")
        pass
  return Ns

  # takes the list label-sentence-vector and creates a dictionary label:average of vectors for label

def getaverage(Ns):
  d = {}
  for x in Ns:
    if x[0] not in d:
      d[x[0]] = [x[2]]
    else: 
      d[x[0]] = d[x[0]] + [x[2]]
  avgs = {}
  for key in d:
    avgs[key] = [x.numpy() for x in d[key]]
    avg = np.mean(avgs[key], axis = 0)
    avgs[key] = avg
  return avgs

def getmetadata(Ns):
  d = {}
  # counts how many embeddings we have for each pattern
  for x in Ns:
    if x[0] not in d:
      d[x[0]] = 1
    else: 
      d[x[0]] = d[x[0]] + 1
  fh = open('G:/My Drive/TESI codici/metadata.csv', "w", "utf-8")
  for x in d:
    fh.write(x)
    fh.write("\t")
    fh.write(str(d[x]))
    fh.write("\n")  
  fh.close()

if __name__ == "__main__":
  data = ReturnDatabase("G:/My Drive/TESI codici/TPAS corpus.json")
  patterns = count(data)
  Ls = getsentences(data, patterns)
  #Ms = gettokens_SIMPLEMMA(Ls)
  Ns = getvectors(Ms[3])   # sarà una lista [ (label , sentence, vector), (..., ..., ...), ...]
  avgs = getaverage(Ns)        # sarà un dizionario {label_1: average vector, label_2:average vector, etc}

from codecs import *
fh = open('G:/My Drive/TESI codici/vectors_to_cluster_addentrare.csv', "w", "utf-8")
meta = [str(i) for i in range(769)]
fh.write("label")
for x in meta:
  tabbed = "\t" + str(x) 
  fh.write(tabbed)
fh.write("\n")

for x in avgs:
  print(x)
  fh.write(x)
  lista = [str(x +1) for x in avgs[x]]
  print(len(avgs[x]))
  for x in lista:
    n = "\t" + x 
    fh.write(n)
  fh.write("\n")
fh.close()

getmetadata(Ns)