# -*- coding: utf-8 -*-
"""
Created on Thu Jun 09 22:17:53 2016

@author: hankai
"""

def read_euro2016(path):
    rf = open(path,'rb')
    rf.readline()
    nation_info_dict = {}
    group_nation_dict = {'a':[],'b':[],'c':[],'d':[],'e':[],'f':[]}
    for line in rf.readlines():
        str_list = line.strip().split(',')
        # group-nation
        group_nation_dict.setdefault(str_list[0],[]).append(str_list[2])
        # nation-info
        info_dict = {'group':'0','elo':0}
        nation_info_dict.setdefault(str_list[2],info_dict)
        nation_info_dict[str_list[2]]['group'] = str_list[0]
        nation_info_dict[str_list[2]]['elo'] = float(str_list[3])/2000
    return nation_info_dict,group_nation_dict
    