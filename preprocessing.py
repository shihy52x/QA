#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#  Copyright © XYM
# CreateTime: 2018-05-30 20:54:30
import pandas as pd


def split_file(category_list,filename):
    df = pd.read_table(filename,sep='\t',
                        header=None,index_col=False,
                        error_bad_lines=False)

    #1st col: Question, 2nd col: Passage, 4th:Answer
    df = df [[0,1,4]]
    df.columns = ['Question','Passage','Answer']

    #create splited files into ./split-file
    sp_file_path = './split_file' 
    if (os.path.exists(sp_file_path )):
        print (sp_file_path + " exist, removing  ......")
        os.system('rm -r ' + sp_file_path)
        os.system('mkdir ' + sp_file_path)

    for ques_type in category_list:
        df_sub = df[df['Question'].str.contains(ques_type)]
        out_file = sp_file_path + '/' + qt
        df_sub.to_csv(out_file , sep='\t')
        print ("creating " + out_file )


def qtype_expore(category_list,filename):

    print ("Statistics of Questions Type:")
    print '%14s %10s %10s' % ("Question Type","count","ratio")
    df = pd.read_table(filename,sep='\t',
                        header=None,index_col=False,
                        error_bad_lines=False)
    N_sum = 0
    for qt in Qtype:
        df_sub = df[df['Question'].str.contains(qt)]
        count = df_sub.describe()['Question']['count']
        print '%14s %10d %10.3f' % (qt,count,count/N)
        N_sum = N_sum + count
    N_rest = N - N_sum
    print '%14s %10d %10.3f' % ('others',N_rest,N_rest/N)

