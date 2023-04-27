from itertools import combinations_with_replacement
import numpy
def dice_results_weighted(n):
    poss = combinations_with_replacement([1, 2, 3, 4, 5, 6], n)
    weighted = []
    for comb in poss:
        numc=(comb.count(1),comb.count(2),comb.count(3),comb.count(4),comb.count(5),comb.count(6))
        rate=1
        for val in range(6):
            m=n+numc[val]-numpy.cumsum(numc)[val]
            k=numc[val]
            rate*=(numpy.math.factorial(m)/(numpy.math.factorial(k)*numpy.math.factorial(m-k)))
            # print(m,rate)
        if comb==():
            weighted.append(((0,0),rate/6**n))
        else:
            weighted.append((comb,rate/6**n))
    return weighted
def dice_results_weighted_d3(n):
    poss = combinations_with_replacement([1, 2, 3], n)
    weighted = []
    for comb in poss:
        numc=(comb.count(1),comb.count(2),comb.count(3))
        rate=1
        for val in range(3):
            m=n+numc[val]-numpy.cumsum(numc)[val]
            k=numc[val]
            rate*=(numpy.math.factorial(m)/(numpy.math.factorial(k)*numpy.math.factorial(m-k)))
            # print(m,rate)
        if comb==():
            weighted.append(((0,0),rate/3**n))
        else:
            weighted.append((comb,rate/3**n))
    return weighted
def avg_dmg(dmg,bd,cb,crit=False,multi=False):
    if crit:
        if multi:
            para=(dmg[0],cb[0]+bd[0],dmg[1],cb[1]+bd[1],dmg[2],cb[2]+bd[2],dmg[3])
            return avg_dmg_crit_m(para)
        else:
            para=(dmg[0]+cb[0]+bd[0],dmg[1]+cb[1]+bd[1],dmg[2]+cb[2]+bd[2],dmg[3])
            return avg_dmg_crit_nm(para)
    else:
        if multi:
            para=(dmg[0],bd[0],dmg[1],bd[1],dmg[2],bd[2],dmg[3])
            return avg_dmg_hit_m(para)
        else:
            para=(dmg[0]+bd[0],dmg[1]+bd[1],dmg[2]+bd[2],dmg[3])
            return avg_dmg_hit_nm(para)
def avg_dmg_hit_nm(dmg):
    (d6,d3,static,rely)=dmg
    avg=0
    d6res=dice_results_weighted(d6)
    d3res=dice_results_weighted_d3(d3)
    for i in d6res:
        for j in d3res:
            avg+=max(sum(i[0])+sum(j[0])+static,rely)*i[1]*j[1]
    return avg
def avg_dmg_hit_m(dmg):
    (d6,bd6,d3,bd3,static,bs,rely)=dmg
    avg=0
    d6res=dice_results_weighted(d6)
    bd6res=dice_results_weighted(bd6)
    d3res=dice_results_weighted_d3(d3)
    bd3res=dice_results_weighted(bd3)
    for i in d6res:
        for j in d3res:
            for k in bd6res:
                for l in bd3res:
                    avg+=max(sum(i[0])+sum(j[0])+0.5*sum(k[0])+0.5*sum(l[0])+static+0.5*bs,rely)*i[1]*j[1]*k[1]*l[1]
    return avg
def avg_dmg_crit_nm(dmg):
    (d6,d3,static,rely)=dmg
    avg=0
    d6res=dice_results_weighted(2*d6)
    d3res=dice_results_weighted_d3(2*d3)
    for i in d6res:
        for j in d3res:
            avg+=max(sum(i[0][-d6:])+sum(j[0][-d3:])+static,rely)*i[1]*j[1]
    return avg
def avg_dmg_crit_m(dmg):
    (d6,bd6,d3,bd3,static,bs,rely)=dmg
    avg=0
    d6res=dice_results_weighted(2*d6)
    bd6res=dice_results_weighted(2*bd6)
    d3res=dice_results_weighted_d3(2*d3)
    bd3res=dice_results_weighted(2*bd3)
    for i in d6res:
        for j in d3res:
            for k in bd6res:
                for l in bd3res:
                    avg+=max(sum(i[0][-d6:])+sum(j[0][-d3:])+0.5*sum(k[0][-bd6:])+0.5*sum(l[0][-bd3:])+static+0.5*bs,rely)*i[1]*j[1]*k[1]*l[1]
    return avg
def dmg_chance(query,hit,multi=False,rr=False):
    if query[9]>=query[10]:
        return 1
    else:
        return dmg_chance_crit(query,multi)*hit_rate(hit,rr)[2]+dmg_chance_hit(query,multi)*hit_rate(hit_stats,rr)[1]
def dmg_chance_hit(query,multi=False):
    d6,bd6,d3,bd3,static,bs,cd6,cd3,cds,rely,thresh=query
    chance=0
    if multi:
        d6res=dice_results_weighted(d6)
        d3res=dice_results_weighted_d3(d3)
        bd6res=dice_results_weighted(bd6)
        bd3res=dice_results_weighted_d3(bd3)
        for i in d6res:
            for j in d3res:
                for k in bd6res:
                    for l in bd3res:
                        if max((sum(i[0])+sum(j[0])+0.5*(sum(k[0])+sum(l[0])))+static+0.5*bs,rely)>=thresh:
                            chance+=i[1]*j[1]*k[1]*l[1] 
    else:
        d6res=dice_results_weighted(d6+bd6)
        d3res=dice_results_weighted_d3(d3+bd3)
        for i in d6res:
            for j in d3res:
                if max((sum(i[0])+sum(j[0]))+static+bs,rely)>=thresh:
                    chance+=i[1]*j[1]
    return chance
def dmg_chance_crit(query, multi=False):
    d6,bd6,d3,bd3,static,bs,cd6,cd3,cds,rely,thresh=query
    bd6+=cd6
    bd3+=cd3
    bs+=cds
    chance=0
    if multi:
        d6res=dice_results_weighted(2*d6)
        d3res=dice_results_weighted_d3(2*d3)
        bd6res=dice_results_weighted(2*bd6)
        bd3res=dice_results_weighted_d3(2*bd3)
        for i in d6res:
            for j in d3res:
                for k in bd6res:
                    for l in bd3res:
                        if max((sum(i[0][-d6:])+sum(j[0][-d3:])+0.5*(sum(k[0][-bd6:])+sum(l[0][-bd3:])))+static+0.5*bs,rely)>=thresh:
                            chance+=i[1]*j[1]*k[1]*l[1] 
    else:
        d6res=dice_results_weighted(2*(d6+bd6))
        d3res=dice_results_weighted_d3(2*(d3+bd3))
        for i in d6res:
            for j in d3res:
                if max((sum(i[0][-(d6+bd6):])+sum(j[0][-(d3+bd3):]))+static+bs,rely)>=thresh:
                    chance+=i[1]*j[1]
    return chance
def hit_rate(hit,rr=False):
    (thresh,mod,acc)=hit
    rate=0
    nocrit=0
    crit=0
    weight={x:0 for x in range(-5,27)}
    if -3>acc or acc>3:
        print("Impossible accuracy level")
        return (0,0,0)
    else:
        if acc>0:
            for i in range(1,21):
                for j in dice_results_weighted(acc):
                    weight[i+j[0][-1]]+=0.05*j[1]
        if acc<0:
            for i in range(1,21):
                for j in dice_results_weighted(-acc):
                    weight[i-j[0][-1]]+=0.05*j[1]
        if acc==0:
            for i in range(1,21):
                weight[i]+=0.05
    if rr:
        for y in weight:
            for z in weight:
                x=max(y,z)
                # print(x,y,z,weight[x],x+mod>=thresh)
                if x+mod>=thresh:
                    rate+=weight[y]*weight[z]
                    if thresh<=x+mod<20:
                        nocrit+=weight[y]*weight[z]
                    if x+mod>=20:
                        crit+=weight[y]*weight[z]
    else:
        for x in weight:
            if x+mod>=thresh:
                rate+=weight[x]
                if thresh<=x+mod<20:
                    nocrit+=weight[x]
                if x+mod>=20:
                    crit+=weight[x]
    return rate,nocrit,crit
def dpa(dmg=(1,0,0,0),hit=(10,0,0),bd=(0,0,0),cb=(0,0,0),multi=False,rr=False):
    hr=hit_rate(hit,rr)
    nd=avg_dmg(dmg,bd,cb,False,multi)
    cd=avg_dmg(dmg,bd,cb,True,multi)
    return nd*hr[1]+cd*hr[2]+dmg[3]*(1-hr[0])

damage_threshold=15
# target damage to meet
reroll=True
# reroll entire roll, eg. from particularise
multi_target=False
# if attack hits multiple targets
damage=(2,0,0,0)
# number of d6, number of d3, flat damage, reliable
hit_stats=(10,2,2)
# target evasion/e-defence, flat to-hit modifier, accuracy/difficulty (-3 -> 3)
bonus_damage=(2,0,0)
# bonus damage d6, bonus damage d3, bonus flat damage
crit_bonus=(1,0,0)
# bonus damage on crit d6, bonus damage on crit d3, bonus flat damage on crit
chance_for_damage=(damage[0],bonus_damage[0],damage[1],bonus_damage[1],damage[2],bonus_damage[2],crit_bonus[0],crit_bonus[1],crit_bonus[2],damage[3],damage_threshold)
# number of d6, number of bonus d6, number of d3, number of bonus d3, flat damage, bonus flat damage, number of bonus d6 on crit,
# number of bonus d3 on crit, bonus flat damage on crit, reliable, target damage
print('Ben attack profile (AMR, ROLAND, OP-Cal, Zero-In, Particularise)')
print('Hit rate: {:.3f}%'.format(100*hit_rate(hit_stats,reroll)[0]))
print('Hit without Crit: {:.3f}%'.format(100*hit_rate(hit_stats,reroll)[1]))
print('Crit rate: {:.3f}%'.format(100*hit_rate(hit_stats,reroll)[2]))
print('Average damage on hit: {:.3f}'.format(avg_dmg(damage,bonus_damage,crit_bonus,False,multi_target)))
print('Average damage on crit: {:.3f}'.format(avg_dmg(damage,bonus_damage,crit_bonus,True,multi_target)))
print('Expected damage per attack: {:.3f}'.format(dpa(dmg=damage,hit=hit_stats,bd=bonus_damage,cb=crit_bonus,multi=multi_target,rr=reroll)))
print('Chance of dealing at least {} damage on hit: {:.3f}%'.format(damage_threshold,100*dmg_chance_hit(chance_for_damage,multi_target)))
print('Chance of dealing at least {} damage on crit: {:.3f}%'.format(damage_threshold,100*dmg_chance_crit(chance_for_damage,multi_target)))
print('Chance of dealing at least {} damage: {:.3f}%'.format(damage_threshold,100*(dmg_chance(chance_for_damage,hit_stats,multi_target,reroll))))
print()

# damage_threshold=16
# # target damage to meet
# reroll=True
# # reroll entire roll, eg. from particularise
# multi_target=True
# # if attack hits multiple targets
# damage=(2,0,0,0)
# # number of d6, number of d3, flat damage, reliable
# hit_stats=(10,2,2)
# # target evasion/e-defence, flat to-hit modifier, accuracy/difficulty (-3 -> 3)
# bonus_damage=(1,0,0)
# # bonus damage d6, bonus damage d3, bonus flat damage
# crit_bonus=(0,0,0)
# # bonus damage on crit d6, bonus damage on crit d3, bonus flat damage on crit
# chance_for_damage=(damage[0],bonus_damage[0],damage[1],bonus_damage[1],damage[2],bonus_damage[2],crit_bonus[0],crit_bonus[1],crit_bonus[2],damage[3],damage_threshold)
# # number of d6, number of bonus d6, number of d3, number of bonus d3, flat damage, bonus flat damage, number of bonus d6 on crit,
# # number of bonus d3 on crit, bonus flat damage on crit, reliable, target damage
# print('Ren attack profile (Howitzer, ROLAND, AutoStab, Particularise, Solar Backdrop)')
# print('Hit rate: {:.3f}%'.format(100*hit_rate(hit_stats,reroll)[0]))
# print('Hit without Crit: {:.3f}%'.format(100*hit_rate(hit_stats,reroll)[1]))
# print('Crit rate: {:.3f}%'.format(100*hit_rate(hit_stats,reroll)[2]))
# print('Average damage on hit (per target): {:.3f}'.format(avg_dmg(damage,bonus_damage,crit_bonus,False,multi_target)))
# print('Average damage on crit (per target): {:.3f}'.format(avg_dmg(damage,bonus_damage,crit_bonus,True,multi_target)))
# print('Expected damage per attack (per target): {:.3f}'.format(dpa(dmg=damage,hit=hit_stats,bd=bonus_damage,cb=crit_bonus,multi=multi_target,rr=reroll)))
# print('Chance of dealing at least {} damage on hit: {:.3f}%'.format(damage_threshold,100*dmg_chance_hit(chance_for_damage,multi_target)))
# print('Chance of dealing at least {} damage on crit: {:.3f}%'.format(damage_threshold,100*dmg_chance_crit(chance_for_damage,multi_target)))
# print('Chance of dealing at least {} damage: {:.3f}%'.format(damage_threshold,100*(dmg_chance(chance_for_damage,hit_stats,multi_target,reroll))))
# print()

# damage_threshold=16
# # target damage to meet
# reroll=True
# # reroll entire roll, eg. from particularise
# multi_target=False
# # if attack hits multiple targets
# damage=(2,0,0,0)
# # number of d6, number of d3, flat damage, reliable
# hit_stats=(10,2,1)
# # target evasion/e-defence, flat to-hit modifier, accuracy/difficulty (-3 -> 3)
# bonus_damage=(2,0,0)
# # bonus damage d6, bonus damage d3, bonus flat damage
# crit_bonus=(0,0,0)
# # bonus damage on crit d6, bonus damage on crit d3, bonus flat damage on crit
# chance_for_damage=(damage[0],bonus_damage[0],damage[1],bonus_damage[1],damage[2],bonus_damage[2],crit_bonus[0],crit_bonus[1],crit_bonus[2],damage[3],damage_threshold)
# # number of d6, number of bonus d6, number of d3, number of bonus d3, flat damage, bonus flat damage, number of bonus d6 on crit,
# # number of bonus d3 on crit, bonus flat damage on crit, reliable, target damage
# print('Ren attack profile (Howitzer, ROLAND, OP-Cal, Particularise, Solar Backdrop)')
# print('Hit rate: {:.3f}%'.format(100*hit_rate(hit_stats,reroll)[0]))
# print('Hit without Crit: {:.3f}%'.format(100*hit_rate(hit_stats,reroll)[1]))
# print('Crit rate: {:.3f}%'.format(100*hit_rate(hit_stats,reroll)[2]))
# print('Average damage on hit (per target): {:.3f}'.format(avg_dmg(damage,bonus_damage,crit_bonus,False,multi_target)))
# print('Average damage on crit (per target): {:.3f}'.format(avg_dmg(damage,bonus_damage,crit_bonus,True,multi_target)))
# print('Expected damage per attack (per target): {:.3f}'.format(dpa(dmg=damage,hit=hit_stats,bd=bonus_damage,cb=crit_bonus,multi=multi_target,rr=reroll)))
# print('Chance of dealing at least {} damage on hit: {:.3f}%'.format(damage_threshold,100*dmg_chance_hit(chance_for_damage,multi_target)))
# print('Chance of dealing at least {} damage on crit: {:.3f}%'.format(damage_threshold,100*dmg_chance_crit(chance_for_damage,multi_target)))
# print('Chance of dealing at least {} damage: {:.3f}%'.format(damage_threshold,100*(dmg_chance(chance_for_damage,hit_stats,multi_target,reroll))))
# print()

damage_threshold=19
# target damage to meet
reroll=False
# reroll entire roll, eg. from particularise
multi_target=False
# if attack hits multiple targets
damage=[(1,0,0,1),(1,0,0,1),(1,0,0,1),(0,1,1,0)]
# number of d6, number of d3, flat damage, reliable
hit_stats=[(10,3,1),(10,3,0),(10,3,0),(10,3,0)]
# target evasion/e-defence, flat to-hit modifier, accuracy/difficulty (-3 -> 3)
bonus_damage=[(1,0,3),(0,0,0),(1,0,3),(2,0,3)]
# bonus damage d6, bonus damage d3, bonus flat damage
crit_bonus=[(0,0,0),(0,0,0),(0,0,0),(0,0,0)]
# bonus damage on crit d6, bonus damage on crit d3, bonus flat damage on crit
#chance_for_damage=(damage[0],bonus_damage[0],damage[1],bonus_damage[1],damage[2],bonus_damage[2],crit_bonus[0],crit_bonus[1],crit_bonus[2],damage[3],damage_threshold)
# number of d6, number of bonus d6, number of d3, number of bonus d3, flat damage, bonus flat damage, number of bonus d6 on crit,
# number of bonus d3 on crit, bonus flat damage on crit, reliable, target damage
print('Fire and Fury attack profile (3xHC+UncleSCM, ROLAND, Fusion Hemmorhage, Opening Argument, 0.5x I Kill With My Heart)')
#print('Hit rate: {:.3f}%'.format(100*hit_rate(hit_stats,reroll)[0]))
#print('Hit without Crit: {:.3f}%'.format(100*hit_rate(hit_stats,reroll)[1]))
#print('Crit rate: {:.3f}%'.format(100*hit_rate(hit_stats,reroll)[2]))
# print('Average damage on hit: {:.3f}'.format(avg_dmg(damage,bonus_damage,crit_bonus,False,multi_target)))
# print('Average damage on crit: {:.3f}'.format(avg_dmg(damage,bonus_damage,crit_bonus,True,multi_target)))
dpr=0
for i in range(4):
    dpr+=dpa(dmg=damage[i],hit=hit_stats[i],bd=bonus_damage[i],cb=crit_bonus[i],multi=multi_target,rr=reroll)
print('Expected damage per round: {:.3f}'.format(dpr))
# print('Chance of dealing at least {} damage on hit: {:.3f}%'.format(damage_threshold,100*dmg_chance_hit(chance_for_damage,multi_target)))
# print('Chance of dealing at least {} damage on crit: {:.3f}%'.format(damage_threshold,100*dmg_chance_crit(chance_for_damage,multi_target)))
# print('Chance of dealing at least {} damage: {:.3f}%'.format(damage_threshold,100*(dmg_chance(chance_for_damage,hit_stats,multi_target,reroll))))
print()