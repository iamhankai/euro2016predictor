# -*- coding: utf-8 -*-
"""
Created on Wed Jun 08 15:56:54 2016

@author: hankai
"""

def nation_record_count(path):
    nation_record_dict = {}
    rf = open(path,'rb')
    for line in rf.readlines():
        str_list = line.split('\t')
        nation1 = str_list[0].lower()
        nation2 = str_list[1].lower()
        goal1 = float(str_list[2])
        goal2 = float(str_list[3])
        year = int(str_list[6])
        # count
        record_dict1 = {'win':0.0,'draw':0.0,'lose':0.0,'goal':0.0,'match':0.0}
        nation_record_dict.setdefault(nation1,record_dict1)
        record_dict2 = {'win':0.0,'draw':0.0,'lose':0.0,'goal':0.0,'match':0.0}
        nation_record_dict.setdefault(nation2,record_dict2)
        # win draw lose
        if(goal1>goal2):
            nation_record_dict[nation1]['win']+=1
            nation_record_dict[nation2]['lose']+=1
        elif(goal1<goal2):
            nation_record_dict[nation1]['lose']+=1
            nation_record_dict[nation2]['win']+=1
        else:
            nation_record_dict[nation1]['draw']+=1
            nation_record_dict[nation2]['draw']+=1
        # goal
        nation_record_dict[nation1]['goal']+=goal1
        nation_record_dict[nation2]['goal']+=goal2
        # match
        nation_record_dict[nation1]['match']+=1
        nation_record_dict[nation2]['match']+=1
    return nation_record_dict

def get_nation1_record(nation_record_dict,nation1):
    win1 = nation_record_dict[nation1]['win']/nation_record_dict[nation1]['match']
    draw1 = nation_record_dict[nation1]['draw']/nation_record_dict[nation1]['match']
    lose1 = nation_record_dict[nation1]['lose']/nation_record_dict[nation1]['match']
    goal1 = nation_record_dict[nation1]['goal']/nation_record_dict[nation1]['match']
    return [win1,draw1,lose1,goal1]
    
def read_train(history_path,is_knockout):
    nation_record_dict=nation_record_count(history_path)
    X = []
    y = []
    rf = open(history_path,'rb')
    for line in rf.readlines():
        str_list = line.split('\t')
        nation1 = str_list[0].lower()
        nation2 = str_list[1].lower()
        # history record
        nation1_record = get_nation1_record(nation_record_dict,nation1)
        nation2_record = get_nation1_record(nation_record_dict,nation2)
        elo1 = float(str_list[4])/2000
        elo2 = float(str_list[5])/2000
        # gather together
        vec = [elo1,elo2]
        vec.extend(nation1_record)
        vec.extend(nation2_record)
        # save to X,y
        yi = int(str_list[2])-int(str_list[3])
        if is_knockout and yi==0:
            continue
        X.append(vec)
        y.append(yi)
    return X,y



#history_path = './data/rawdata_elo.txt'
#nation_record_dict=nation_record_count(history_path)
 