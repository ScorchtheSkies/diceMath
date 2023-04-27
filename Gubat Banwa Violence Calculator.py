import numpy
from matplotlib import pyplot as plt

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

def violence(defDice,defThres,atkDice,atkThres,defCrit=0,atkCrit=10,skewer=False,unbalance=False,addHit=0,addDef=0,subHit=0,subDef=0):
    outcomes={}
    defVals=successes(defDice,defThres,defCrit,8)
    atkVals=successes(atkDice,atkThres,atkCrit)
    for a in atkVals:
        for d in defVals:
            dmod=d
            if skewer:
                dmod=max(dmod-1,0)
            dmod=max(dmod+addDef-subDef,0)
            amod=a
            if unbalance:
                amod=max(amod-1,0)
            amod=max(a+addHit-subHit,0)
            dmg=max(amod-dmod,0)
            if dmg in outcomes.keys():
                outcomes[dmg]+=defVals[d]*atkVals[a]
            else:
                outcomes[dmg]=defVals[d]*atkVals[a]
    return outcomes

def expDmg(defDice,defThres,atkDice,atkThres,defCrit=0,atkCrit=10,skewer=False,unbalance=False,addHit=0,addDef=0,subHit=0,subDef=0):
    viol=violence(defDice,defThres,atkDice,atkThres,defCrit,atkCrit,skewer,unbalance,addHit,addDef,subHit,subDef)
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

print(expDmg(3,6,3,5))

#expDmg(A,B,C,D)
#Standard: A = Defence teeth, B = 6, C = Attack Teeth, D = 6
#Attack/Defense Modifiers:
#Sharpness - Set D to 5
#Dullness - Set D to 7
#Unbalance - Add argument unbalance=True
#Protect - Add or modify argument addDef=1
#Conditioning - Add or modify argument addDef=1
#Vulnerability - Add or modify argument addHit=1
#Eviscerate - Add or modify argument subDef=1
#Sunder - Set B to 7
#Skewering - Add argument skewer=True