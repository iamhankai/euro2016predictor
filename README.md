## Euro Cup 2016 Predictor
Simply, this predictor is based on typical "feature+classifier" machine learning framework.

- feature: ELO rating, win/draw/lose rate, goal/fumble from 1920
- label: goal difference between team1 and team2
- classifier: Random Forest Classifier

The code is a little in chaos due to limited time. Maybe I'll update it.

## Run
environment: Python2.7, scikit-learn package;

1. run `group_stage.py` to get group stage results (./result/nation_point.csv and ./result/promoted_nation.csv);
2. run `knockout_stage.py` to get final results (./result/knockout_result.csv).

## Prediction Results
#### Champion
**Germany** <img src="http://images.huanqiu.com/sarons/2012/12/d08afac79e262eeedec18bf20f3e8815.png" width = "30" height = "18" alt="Germany" align=center /> 

#### Knockout Stage
| round | team1 | team2 | result |
|-------|-------------|-------------|--------|
| 16 | france | ukraine | 3 |
| 16 | spain | italy | 1 |
| 16 | england | romania | 1 |
| 16 | portugal | ireland | 3 |
| 16 | germany | romania | 2 |
| 16 | belgium | czechia | 1 |
| 16 | switzerland | poland | 2 |
| 16 | slovakia | austria | 1 |
| 8 | france | spain | 1 |
| 8 | england | portugal | 3 |
| 8 | germany | belgium | 1 |
| 8 | switzerland | slovakia | 1 |
| 4 | france | england | 1 |
| 4 | germany | switzerland | 2 |
| 2 | france | germany | -1 |

#### Group Stage
**Standings**

| group | team | points | goal difference |
|-------|------------------|--------|-----------------|
| a | switzerland | 7 | 3 |
| a | france | 5 | 1 |
| a | romania | 4 | 1 |
| a | albania | 0 | -5 |
| b | england | 5 | 3 |
| b | slovakia | 5 | 2 |
| b | wales | 2 | -2 |
| b | russia | 2 | -3 |
| c | germany | 7 | 4 |
| c | ukraine | 4 | -1 |
| c | poland | 4 | -1 |
| c | northern ireland | 1 | -2 |
| d | spain | 9 | 3 |
| d | czechia | 4 | 1 |
| d | turkey | 2 | -1 |
| d | croatia | 1 | -3 |
| e | belgium | 7 | 2 |
| e | ireland | 5 | 1 |
| e | italy | 4 | 0 |
| e | sweden | 0 | -3 |
| f | portugal | 9 | 6 |
| f | austria | 6 | 3 |
| f | hungary | 3 | -4 |
| f | iceland | 0 | -5 |

**Matches Details**
>((team1,team2),result)    
(('france', 'romania'), 0)  
(('france', 'albania'), 1)  
(('france', 'switzerland'), 0)  
(('romania', 'albania'), 2)  
(('romania', 'switzerland'), -1)  
(('albania', 'switzerland'), -2)  
(('england', 'russia'), 3)  
(('england', 'wales'), 0)  
(('england', 'slovakia'), 0)  
(('russia', 'wales'), 0)  
(('russia', 'slovakia'), 0)  
(('wales', 'slovakia'), -2)  
(('germany', 'ukraine'), 2)  
(('germany', 'poland'), 2)  
(('germany', 'northern ireland'), 0)  
(('ukraine', 'poland'), 0)  
(('ukraine', 'northern ireland'), 1)  
(('poland', 'northern ireland'), 1)  
(('spain', 'czechia'), 1)  
(('spain', 'turkey'), 1)  
(('spain', 'croatia'), 1)  
(('czechia', 'turkey'), 0)  
(('czechia', 'croatia'), 2)  
(('turkey', 'croatia'), 0)  
(('belgium', 'italy'), 1)  
(('belgium', 'ireland'), 0)  
(('belgium', 'sweden'), 1)  
(('italy', 'ireland'), 0)  
(('italy', 'sweden'), 1)  
(('ireland', 'sweden'), 1)  
(('portugal', 'iceland'), 2)  
(('portugal', 'austria'), 1)  
(('portugal', 'hungary'), 3)  
(('iceland', 'austria'), -2)  
(('iceland', 'hungary'), -1)  
(('austria', 'hungary'), 2)  

## Thanks
historcal data from [fedebayle](https://github.com/fedebayle/brazil2014_learning/blob/master/rawdata_elo.txt)  
euro2016 data from [nowaycomputer](https://github.com/nowaycomputer/euro2016/blob/master/data.csv)

