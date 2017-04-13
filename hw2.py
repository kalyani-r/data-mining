fp=open("1474246156_5639381_train_drugs.data","r")
result=[]
i=0
s=[]
negfc={}
posfc={}
commfc={}
allfc={}
import math
for para in fp:
    result.append(para[:1])
    s.append(para.split())

for i in range(len(s)):
    if s[i][0]=='0':
        for j in range(1,len(s[i])):
            if s[i][j] in negfc:
                negfc[s[i][j]]+=1
            else:
                negfc[s[i][j]]=1
    else:
        for   k in range(1,len(s[i])):
            if s[i][k] not in posfc:
                posfc[s[i][k]]=1
            else:
                posfc[s[i][k]]+=1
for i in negfc:
    if i in posfc and i not in commfc:
        commfc[i]=negfc[i]+posfc[i]
allfc=commfc.copy()
left={}
print(len(commfc))
print()
for i in negfc:
    if i not in allfc:
        left[i]=negfc[i]
for i in posfc:
    if i not in allfc:
        left[i]=posfc[i]
allfc.update(left)
oo=0
sumneg=sum(negfc.values())
sumpos=sum(posfc.values())
zerop=result.count('0')
onep=result.count('1')
fw=open("output.data","w+")
fp1=open("1474246156_56856_test.data","r")
totalfeatuescount=sum(allfc.values())
for para in fp1:
    s=para.split()
    logofzero=0
    logofone=0
    uniqueneg=0
    uniquepos=0
    uniquecommon=0
    notall=0
    #print("para")
    #print(len(s))
    for i in range(len(s)):

        if s[i] not in allfc:
            notall+=1
            continue
        if s[i] in commfc:
            uniquecommon+=1

        feaproball=allfc[s[i]]/totalfeatuescount
        if s[i] in negfc:
            featuregivenzero=negfc[s[i]]/sumneg
            if (featuregivenzero > 0):
                logofzero += math.log(featuregivenzero / feaproball)
            if s[i] not in posfc and featuregivenzero > 0:
                uniqueneg+=math.log(featuregivenzero / feaproball)

        if s[i] in posfc:
            featuregivenone =posfc[s[i]]/sumpos
            if(featuregivenone>0):
                logofone+=math.log(featuregivenone/feaproball)
            if s[i] not in negfc and featuregivenone>0:
                uniquepos+=math.log(featuregivenone/feaproball)

    oo+=1
    #pri="   line   " + str(oo)+"    uniqueneg  "+str(uniqueneg)+"   uniquepos   "+str(uniquepos)+"  uniquecommon    "+str(uniquecommon)+"   notall  "+str(notall)
    pri="   line   " + str(oo)+"    uniqueneg  "+str(uniqueneg)+"   uniquepos   "+str(uniquepos)
    print(pri)
    if uniquepos>=uniqueneg and logofone<logofzero:
        print("positive")
    elif uniquepos==uniqueneg:
        print("none")
    #print(pri)
    if uniquepos>=uniqueneg and logofone<logofzero:
        print(oo)
        fw.write('1\n')
    elif(logofzero>logofone):
        fw.write('0\n')
    else:
        fw.write('1\n')


