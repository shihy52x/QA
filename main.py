from __future__ import division
import pandas as pd
import pdb
import nltk
import os
from nltk.stem.porter import PorterStemmer as stem
from nltk.corpus import wordnet


def get_ent(sent):
    ps = nltk.sent_tokenize(sent)
    for ps_i in ps:
        pt = nltk.word_tokenize(ps_i)
        tag = nltk.pos_tag(pt)
        nameEnt = nltk.ne_chunk(tag)
    return nameEnt

def get_ent_who(sent,grammar=None):
    ps = nltk.sent_tokenize(sent)
    for ps_i in ps:
        pt = nltk.word_tokenize(ps_i)
        tag = nltk.pos_tag(pt)
        if grammar!=None:
            cp = nltk.RegexpParser(grammar)
            nameEnt = cp.parse(tag)
        else:
            nameEnt = nltk.ne_chunk(tag)
    return nameEnt

def find_first(tl,s):
    for tli in tl:
        if s in tli[1]:
            return tli[0]

def find_similarity(word,sent_token):
    word1_synset = wordnet.synsets(word)[0]
    score_old = 0
    for word2 in sent_token:
        word2_synset = wordnet.synsets(word2)[0]
        score_new = word1_synset.wup_similarity(word2_synset)
        if score_new >= score_old:
            score_old = score_new
            word_best = word2
    return word_best

def who_find_ans(row):
    [ques,pas,ans] = [row['Question'],row['Passage'],row['Answer']]
    grammar = "NP: {<DT>?<JJ>*<NN>}"
    ques_ent = get_ent_who(ques)
    pas_ent = get_ent_who(pas,grammar)
    anchor_que = find_first(ques_ent.leaves(),'VB')
    anchor_que_stem = stem().stem(anchor_que)
    pas_vb=[]
    anchor_pas = None
    for pas_i in pas_ent.leaves():
        if 'VB' in pas_i[1]:
            if anchor_que_stem == stem().stem(pas_i[0]):
                anchor_pas = pas_i[0]
                break
            pas_vb.append(pas_i[0])
    pdb.set_trace()
    if anchor_pas ==None:
        anchor_pas = find_similarity(anchor_que_stem,pas_vb)

def how_many_find_ans(row):    
    [ques,pas,ans] = [row['Question'],row['Passage'],row['Answer']]
    ques_ent = get_ent(ques)
    ans_ent = get_ent(ans)
    anchor = find_first(ques_ent.leaves(),'NN')
    ans_find = find_first(ans_ent.leaves(),'CD')
    return ans_find


from preprocessing import split_file,qtype_explore
Qtype = ['what','where','when','who','why','how many','how much']
#df = pd.read_csv('split/who',sep ='\t',nrows=10)
df = pd.read_csv('data/train_serial.tsv',sep ='\t',nrows=1000)
N = len(df)
N_hm = 0
i = 0
print "Total Number of sample is :", N
for index, row in df.iterrows():
    if i%100 ==0:
        print "i=",i
    i=i+1
    [ques,pas,ans] = [row['Question'],row['Passage'],row['Answer']]
    ans_find = who_find_ans(row)
    if ans_find and ans_find in ans:
        N_hm = N_hm +1

print N_hm,N,N_hm/N
