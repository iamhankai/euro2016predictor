# -*- coding: utf-8 -*-
"""
Created on Mon Jun 06 12:29:59 2016

@author: hankai
"""
import numpy as np
from sklearn import preprocessing

def read_euro2016(path):
    group_list = ['a','b','c','d','e','f']
    group_nation_dict = {'a':[],'b':[],'c':[],'d':[],'e':[],'f':[]}
    nation_group_dict = {}
    nation_elo_dict = {}
    rf = open(path,'rb')
    rf.readline()
    for line in rf.readlines():
        str_list = line.split(',')
        group_nation_dict.setdefault(str_list[0],[]).append(str_list[2])
        nation_group_dict.setdefault(str_list[2],str_list[0])
        nation_elo_dict.setdefault(str_list[2],float(str_list[3]))
    return group_nation_dict,nation_group_dict,nation_elo_dict
        
def read_history(path):
    X = []
    y = []
    rf = open(path,'rb')
    for line in rf.readlines():
        str_list = line.split('\t')
        vec = [float(str_list[4]),float(str_list[5])]
        X.append(vec)
        y.append(int(str_list[2])-int(str_list[3]))
    return X,y


from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import cross_val_score
    
train_path = './data/rawdata_elo.txt'
train_X,train_y = read_history(train_path)  
train_X_normalized = preprocessing.normalize(train_X, norm='l2')
score_gbdt = RandomForestClassifier(n_estimators=30, max_depth=None,
min_samples_split=1, random_state=0)
scores = cross_val_score(score_gbdt, train_X_normalized, train_y)
scores.mean()     
# The mean square error
score_gbdt.fit(train_X_normalized, train_y)
print("mean square error: %.2f" % np.mean((score_gbdt.predict(train_X_normalized[1:100]) - train_y[1:100]) ** 2))

# predict    
euro2016_path = './data/euro2016.csv'
group_nation_dict,nation_group_dict,nation_elo_dict = read_euro2016(euro2016_path)
test_X = []
group_list = ['a','b','c','d','e','f']
vs_list = []
for g in group_list:
    for i in range(4):
        for j in range(i+1,4):
            nation1 = group_nation_dict[g][i]
            nation2 = group_nation_dict[g][j]
            vs_list.append((nation1,nation2))
            vec = [nation_elo_dict[nation1],nation_elo_dict[nation2]]
            #vec_normalized = preprocessing.normalize(vec, norm='l2')
            # all
            test_X.append(vec)
test_X_normalized = preprocessing.normalize(test_X, norm='l2')
test_y = score_gbdt.predict(test_X_normalized)

# points count
nation_point_dict = {}
for i in range(len(test_y)):
    print(vs_list[i],test_y[i])
    nation1 = vs_list[i][0]
    nation2 = vs_list[i][1]
    nation_point_dict.setdefault(nation1,0)
    nation_point_dict.setdefault(nation2,0)
    if test_y[i]>0:
        nation_point_dict[nation1]+=3
    elif test_y[i]<0:
        nation_point_dict[nation2]+=3
    else:
        nation_point_dict[nation1]+=1
        nation_point_dict[nation2]+=1
wf = open('./nation_point.csv','wb')
for (nation,point) in nation_point_dict.items():
    wf.write(nation_group_dict[nation]+','+nation+','+str(point)+'\n')
wf.close()    


def read_final16_nation(sorted_path):
    final16_nation_dict = {}
    rf = open(sorted_path,'rb')
    for line in rf.readlines():
        str_list = line.split(',')
        final16_nation_dict.setdefault(str_list[0],str_list[1])
    return final16_nation_dict

final16_nation_dict = read_final16_nation('nation_point_sort.csv')   
def read_final16list(path):
    final16list = []
    rf = open(path,'rb')
    for line in rf.readlines():
        str_list = line.split(',')
        if len(str_list)<2:
            final16list.append(line.strip())
        else:
            for stri in str_list:
                if stri in final16_nation_dict.keys():
                    final16list.append(stri)
                    break
    return final16list
 
final16list = read_final16list('./data/final16list.txt')   
 
def predict_match(nation1,nation2):
    vec = [nation_elo_dict[nation1],nation_elo_dict[nation2]]
    vec_normalized = preprocessing.normalize(np.array(vec).reshape(1, -1), norm='l2')
    score = score_gbdt.predict(vec_normalized)
    return score
    
def predict_winner(low,high,circle):
    circle += 1
    if high-low<2:
        score = predict_match(final16_nation_dict[final16list[low]],final16_nation_dict[final16list[high]])
        print pow(2,circle),(final16_nation_dict[final16list[low]],final16_nation_dict[final16list[high]]),score
        if score>=0:
            return low
        else:
            return high
    mid = (low+high)/2
    win1_idx = predict_winner(low,mid,circle)
    win2_idx = predict_winner(mid+1,high,circle)
    score = predict_match(final16_nation_dict[final16list[win1_idx]],final16_nation_dict[final16list[win2_idx]])
    print pow(2,circle),(final16_nation_dict[final16list[win1_idx]],final16_nation_dict[final16list[win2_idx]]),score
    if score>=0:
        return win1_idx
    else:
        return win2_idx

#
print 'Knockout'
champion_id = predict_winner(0,15,0)
print final16_nation_dict[final16list[champion_id]]




        