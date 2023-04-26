from itertools import combinations_with_replacement
import numpy
import time
from matplotlib import pyplot as plt
def dice_results_weighted(n):
    poss = combinations_with_replacement([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], n)
    weighted = []
    for comb in poss:
        numc=(comb.count(1),comb.count(2),comb.count(3),comb.count(4),comb.count(5),comb.count(6),comb.count(7),comb.count(8),comb.count(9),comb.count(10))
        rate=1
        for val in range(10):
            m=n+numc[val]-numpy.cumsum(numc)[val]
            k=numc[val]
            rate*=(numpy.math.factorial(m)/(numpy.math.factorial(k)*numpy.math.factorial(m-k)))
            # print(m,rate)
        if comb==():
            weighted.append(((0,0),rate/10**n))
        else:
            weighted.append((comb,rate/10**n))
    return weighted

def xd10khy(x,y):
    if y>x:
        return 0
    out=0
    for i in dice_results_weighted(x):
        out+=sum(i[0][-y:])*i[1]
    return out

def trinomial(x,px,y,py,n):
    if(x+y<=n):
        pXxYy=(numpy.math.factorial(n)/(numpy.math.factorial(x)*numpy.math.factorial(y)*numpy.math.factorial(n-x-y)))*(px**x)*(py**y)*((1-px-py)**(n-x-y))
    else:
        pXxYy=0
    return pXxYy

def successes(dice,thres,critnum=0,diceSize=10):
    vals={}
    if critnum>0:
        for i in range(2*dice+1):
            vals[i]=0
        py=(diceSize+1-critnum)/diceSize
        px=(diceSize+1-thres)/diceSize-py
        for x in range(dice+1):
            for y in range(dice+1-x):
                if(x+y<=dice):
                    vals[x+2*y]+=trinomial(x,px,y,py,dice)
    else:
        for i in range(dice+1):
            vals[i]=0
        px=(diceSize+1-thres)/diceSize
        for x in range(dice+1):
            if(x<=dice):
                vals[x]+=trinomial(x,px,0,0,dice)
    return vals

def violence(defDice,defThres,atkDice,atkThres,defCrit=0,atkCrit=10):
    outcomes={}
    defVals=successes(defDice,defThres,defCrit,8)
    atkVals=successes(atkDice,atkThres,atkCrit)
    for a in atkVals:
        for d in defVals:
            if max(a-d,0) in outcomes.keys():
                outcomes[max(a-d,0)]+=defVals[d]*atkVals[a]
            else:
                outcomes[max(a-d,0)]=defVals[d]*atkVals[a]
    return outcomes

def expDmg(defDice,defThres,atkDice,atkThres,defCrit=0,atkCrit=10):
    viol=violence(defDice,defThres,atkDice,atkThres,defCrit=0,atkCrit=10)
    sum=0
    for d in viol:
        sum+=d*viol[d]
    return sum

def graphDict(probList):
    graphCount=len(probList)
    fig, axs = plt.subplots(graphCount)
    for count, probs in enumerate(probList):
        results = probs.keys()
        probabilities = [x*100 for x in probs.values()]
        axs[count].bar(results, probabilities)
    plt.show()
# startTime=time.time()
# total=0
# probs=successes(3,6,10)
# for i in probs:
#     total+=probs[i]
# print(total)
# print(probs)
# print("Calculation Time = "+str(time.time()-startTime)+"s")
# print(violence(2,6,3,6))
# print(successes(3,6,critnum=10))
# print(successes(2,6,diceSize=8))
# graphDict([violence(2,6,3,6),successes(3,6,critnum=10),successes(2,6,diceSize=8)])

print(expDmg(3,6,3,5))