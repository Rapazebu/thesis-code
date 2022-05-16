
import json
import pandas as pd
#from sentence_transformers import SentenceTransformer

#%%

# returns a dictionary of sentence:labelID. For this trial only sentences of the patterns 1 and 2 are considered 

def AccogliereCONT(filename):
    f = open(filename)
    r = json.load(f)
    data = r['data'] 
    sent_lab= []
    sent_lab_tok = []

    for x in data: 
        if x[0] == "accogliere":
            if x[1] == "1":
                tup = (0, x[2])
            if x[1] == "2":
                tup = (1, x[2])
            sent_lab.append(tup)

    
    for x in sent_lab:
        sen = x[1]
        sent_tokenized = sen.split(" ")
        for tok in sent_tokenized:
            if "accog" in tok or "accol" in tok or "ACCOL" in tok or "ACCOG" in tok:
                trip = (x[0], x[1], tok)
                sent_lab_tok.append(trip)
        
                break
    print('era lunga : ', len(sent_lab_tok))
    sent_lab_tok = list(set(sent_lab_tok))
    print("ora lunga ", len(sent_lab_tok))
    sentences = []
    labels = []
    tokens = []
    for x in sent_lab_tok:
        labels.append(x[0])
        sentences.append(x[1])
        tokens.append(x[2])

    
    D = {'labels : ': labels, 'tokens : ': tokens, 'sentences : ': sentences}
    df = pd.DataFrame(D)
    return df




D = Accogliere('G:/.shortcut-targets-by-id/1YeL3GRFiK8VcX2qGQ49XTVJekScNZ2CV/COPREDICATION DUESSELDORF C11/Datasets (vari corpora)/TPAS corpus.json') 


#%%
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

#Our sentences we like to encode
sentences = ['This framework generates embeddings for each input sentence',
    'Sentences are passed as a list of string.',
    'The quick brown fox jumps over the lazy dog.']

Sentences = Ds["sentences"]

#Sentences are encoded by calling model.encode()
embeddings = model.encode(sentences)

#Print the embeddings
for sentence, embedding in zip(sentences, embeddings):
    print("Sentence:", sentence)
    print("Embedding:", embedding)
    print("")




#%%
if __name__ == "__main__":
    Ds = Accogliere('G:/.shortcut-targets-by-id/1YeL3GRFiK8VcX2qGQ49XTVJekScNZ2CV/COPREDICATION DUESSELDORF C11/Datasets (vari corpora)/TPAS corpus.json')
    df = pd.DataFrame(Ds)
    