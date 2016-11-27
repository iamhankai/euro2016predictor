# -*- coding: utf-8 -*-
"""
Created on Wed Jun 08 15:27:53 2016

@author: hankai
"""

import numpy as np
import data_loader.read_history_count as read_history_count
import data_loader.read_euro2016info as read_euro2016info

def points_count(vs_list, result):
	## points count
    nation_point_goal_dict = {}
    for i in range(len(result)):
        print(vs_list[i],result[i])
        nation1 = vs_list[i][0]
        nation2 = vs_list[i][1]
        nation_point_goal_dict.setdefault(nation1,[0,0])
        nation_point_goal_dict.setdefault(nation2,[0,0])
        nation_point_goal_dict[nation1][1]+=result[i]
        nation_point_goal_dict[nation2][1]-=result[i]
        if result[i]>0:
            nation_point_goal_dict[nation1][0]+=3
        elif result[i]<0:
            nation_point_goal_dict[nation2][0]+=3
        else:
            nation_point_goal_dict[nation1][0]+=1
            nation_point_goal_dict[nation2][0]+=1
    # sort
    nation_point_goal_dict=sorted(nation_point_goal_dict.items(), key=lambda d: d[1],reverse=True)
    return nation_point_goal_dict
	
def eurocup24promotion(group_sorted_dict, promoted_file_path):
    promoted_file=open('./result/promoted_nation.csv','wb')
    group3rd_dict={}
	# top 2 teams in each group
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
	# best 4 3rd team in all groups
    group3rd_dict=sorted(group3rd_dict.items(), key=lambda d: d[1][1],reverse=True)
    cnt = 1
    for (groupid,(nation,point_goal)) in group3rd_dict:        
        if cnt>4:
            break
        promoted_file.write(groupid+','+nation+','+str(point_goal[0])+','+str(point_goal[1])+'\n')
        cnt+=1
    promoted_file.close() 
	
    
if __name__=='__main__':    
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.cross_validation import cross_val_score
        
    ## train
    history_path = './data/rawdata_elo.txt'
    nation_record_dict = read_history_count.nation_record_count(history_path)
    train_X,train_y = read_history_count.read_train(history_path,False)  
    score_gbdt =  RandomForestClassifier(n_estimators=50, max_depth=None,
        min_samples_split=2, random_state=666)
    scores = cross_val_score(score_gbdt, train_X, train_y)
    print scores.mean() 
    # The mean square error
    score_gbdt.fit(train_X, train_y)
    print("trainset mean square error: %.2f" % np.mean((score_gbdt.predict(train_X) - train_y) ** 2))
    
    ## predict    
    euro2016_path = './data/euro2016.csv'
    nation_info_dict,group_nation_dict = read_euro2016info.read_euro2016(euro2016_path)
    test_X = []
    vs_list = []
    for g in group_nation_dict.keys():
        for i in range(4):
            for j in range(i+1,4):
                nation1 = group_nation_dict[g][i]
                nation2 = group_nation_dict[g][j]
                vs_list.append((nation1,nation2))
                nation1_record = read_history_count.get_nation1_record(nation_record_dict,nation1)
                nation2_record = read_history_count.get_nation1_record(nation_record_dict,nation2)
                elo1 = nation_info_dict[nation1]['elo']
                elo2 = nation_info_dict[nation2]['elo']
                vec = [elo1,elo2]
                vec.extend(nation1_record)
                vec.extend(nation2_record)
                # save all samples
                test_X.append(vec)
    test_y = score_gbdt.predict(test_X)

    ## points count
    nation_point_goal_dict = points_count(vs_list,test_y)
	
    # group analysis and write it to a file
    group_sorted_dict = {}
    wf = open('./result/nation_point.csv','wb')
    for (nation,point_goal) in nation_point_goal_dict:
        group = nation_info_dict[nation]['group']
        group_sorted_dict.setdefault(group,[])
        group_sorted_dict[group].append((nation,point_goal))
        wf.write(group+','+nation+','+str(point_goal[0])+','+str(point_goal[1])+'\n')
    wf.close()  
    
    ## promote
    promoted_file_path='./result/promoted_nation.csv'
    eurocup24promotion(group_sorted_dict, promoted_file_path)

