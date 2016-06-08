# -*- coding: utf-8 -*-
"""
Created on Wed Jun 08 15:27:53 2016

@author: hankai
"""

import numpy as np
import history_count

class GroupStage:
    # 初始化
    nation_info_dict = {}
    group_nation_dict = {'a':[],'b':[],'c':[],'d':[],'e':[],'f':[]}
    elo_max = 2000.0
    def __init__(self):
        pass
        
    def read_euro2016(self,path):
        rf = open(path,'rb')
        rf.readline()
        for line in rf.readlines():
            str_list = line.split(',')
            # group-nation
            self.group_nation_dict.setdefault(str_list[0],[]).append(str_list[2])
            # nation-info
            info_dict = {'group':'0','elo':0}
            self.nation_info_dict.setdefault(str_list[2],info_dict)
            self.nation_info_dict[str_list[2]]['group'] = str_list[0]
            self.nation_info_dict[str_list[2]]['elo'] = float(str_list[3])/self.elo_max
        return self
            
    
if __name__=='__main__':    
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.cross_validation import cross_val_score
        
    euro2016group = GroupStage()
    history_path = './data/rawdata_elo.txt'
    nation_record_dict=history_count.nation_record_count(history_path)
    train_X,train_y = history_count.read_train(history_path,False)  
    score_gbdt =  RandomForestClassifier(n_estimators=50, max_depth=None,
        min_samples_split=2, random_state=666)
    scores = cross_val_score(score_gbdt, train_X, train_y)
    print scores.mean() 
    # The mean square error
    score_gbdt.fit(train_X, train_y)
    print("trainset mean square error: %.2f" % np.mean((score_gbdt.predict(train_X) - train_y) ** 2))
    
    # predict    
    euro2016_path = './data/euro2016.csv'
    euro2016group.read_euro2016(euro2016_path)
    test_X = []
    group_list = ['a','b','c','d','e','f']
    vs_list = []
    for g in group_list:
        for i in range(4):
            for j in range(i+1,4):
                nation1 = euro2016group.group_nation_dict[g][i]
                nation2 = euro2016group.group_nation_dict[g][j]
                vs_list.append((nation1,nation2))
                nation1_record = history_count.get_nation1_record(nation_record_dict,nation1)
                nation2_record = history_count.get_nation1_record(nation_record_dict,nation2)
                elo1 = euro2016group.nation_info_dict[nation1]['elo']
                elo2 = euro2016group.nation_info_dict[nation2]['elo']
                vec = [elo1,elo2]
                vec.extend(nation1_record)
                vec.extend(nation2_record)
                # all
                test_X.append(vec)
    test_y = score_gbdt.predict(test_X)
    
    # points count
    nation_point_goal_dict = {}
    for i in range(len(test_y)):
        print(vs_list[i],test_y[i])
        nation1 = vs_list[i][0]
        nation2 = vs_list[i][1]
        nation_point_goal_dict.setdefault(nation1,[0,0])
        nation_point_goal_dict.setdefault(nation2,[0,0])
        nation_point_goal_dict[nation1][1]+=test_y[i]
        nation_point_goal_dict[nation2][1]-=test_y[i]
        if test_y[i]>0:
            nation_point_goal_dict[nation1][0]+=3
        elif test_y[i]<0:
            nation_point_goal_dict[nation2][0]+=3
        else:
            nation_point_goal_dict[nation1][0]+=1
            nation_point_goal_dict[nation2][0]+=1
    # sort
    nation_point_goal_dict=sorted(nation_point_goal_dict.items(), key=lambda d: d[1],reverse=True)
    # group analysis
    group_sorted_dict = {}        
    wf = open('./nation_point.csv','wb')
    for (nation,point_goal) in nation_point_goal_dict:
        group = euro2016group.nation_info_dict[nation]['group']
        group_sorted_dict.setdefault(group,[])
        group_sorted_dict[group].append((nation,point_goal))
        wf.write(group+','+nation+','+str(point_goal[0])+','+str(point_goal[1])+'\n')
    wf.close()    
    # promote
    promoted_file=open('promoted_nation.csv','wb')
    group3rd_dict={}
    for group in group_sorted_dict.keys():
        cnt = 1
        for (nation,point_goal) in group_sorted_dict[group]:
            if cnt>3:
                continue
            if cnt==3:
                group3rd_dict.setdefault(group+str(cnt),(nation,point_goal))
                continue
            promoted_file.write(group+str(cnt)+','+nation+','+str(point_goal[0])+','+str(point_goal[1])+'\n')
            cnt+=1
    group3rd_dict=sorted(group3rd_dict.items(), key=lambda d: d[1][1],reverse=True)
    cnt = 1
    for (groupid,(nation,point_goal)) in group3rd_dict:        
        if cnt>4:
            break
        promoted_file.write(groupid+','+nation+','+str(point_goal[0])+','+str(point_goal[1])+'\n')
        cnt+=1
    promoted_file.close()    
    

