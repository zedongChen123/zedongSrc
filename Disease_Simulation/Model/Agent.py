# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 13:39:25 2017

@author: zedong
@Item:Agent-based simulation for degue fever 
"""
import random
path='E:\\degueFeverSimulation\\startSet\\street.csv'
spath='E:\\degueFeverSimulation\\transfer\\popmaxic2.csv'
npath='E:\\degueFeverSimulation\\result\\population\\'
#定义个体（Agent）
#Agent 状态属性（state）0：健康 1：患病  2：康复（免疫） 3：潜伏状态
class Person(object):
    def __init__(self,ID,UnID,State=0,InfectedDate=0,Sex=None,Age=None):
        self.id=ID
        self.state=State
        self.infectedDate=InfectedDate
        self.unid=UnID
        
#定义地理单元Unit(街道)
# StartCase:起始患病人数  Population  总人数    AgentArr   (Agent对象集合)  insideMove 内部移动  inMove 迁入  outMove 迁出
class Unit(object):
    def __init__(self,UnID,CasesCount,Population,AgentArr,IncreaseCase,CureTime,insideMove,inMove,outMove):
        self.CasesCount=CasesCount
        self.Population=Population
        self.AgentArr=AgentArr
        self.IncreaseCase=IncreaseCase
        self.CureTime=CureTime
        self.insideMove=insideMove
        self.inMove=inMove
        self.outMove=outMove
        

#实例化每个Unit内的对象Agent
def CreatAgent_Unit(TargetNumber,UnID):
    AgentArr={}.fromkeys(UnID+str(i) for i in range(TargetNumber))
    for ID in AgentArr:
        AgentArr[ID]=Person(ID,UnID)
    return AgentArr
    
#根据设置起始患病Agent
def InfectedAgent_S(AgentArr,CasesNumber):
    IDlist=list(x for x in AgentArr.keys())
    AgentNumber=int(len(IDlist))#总人数
    RDlist=[]
    InfectedCount=0
    if CasesNumber==0:
        InfectedCount=0
    else:
        RDlist=random.sample(IDlist,CasesNumber)
        for key in AgentArr:
            if key in RDlist:
                AgentArr[key].state=1
                InfectedCount+=1
    #InfectedCount患病病例数  AgentArr Agent集合  AgentNumber总人数  
    return InfectedCount,AgentArr,AgentNumber

#健康状态变为患病状态（潜伏）
def IncreaseCaseAgent(AgentArr,IncreaseCase):
    SDlist=list(x for x in AgentArr.keys())
    RDlist=[]
    if len(SDlist)<IncreaseCase:
        RDlist=SDlist
    else:
        RDlist=random.sample(SDlist,IncreaseCase)
    for key in RDlist:
        if AgentArr[key].state==0:
            AgentArr[key].state=3
            AgentArr[key].infectedDate=0
    return AgentArr

#给每个患病的人进行生病周期计数
def InfectedDateCount(AgentArr):
    SDlist=list(x for x in AgentArr.keys() if AgentArr[x].state==1 or AgentArr[x].state==3)
    for key in SDlist:
        AgentArr[key].infectedDate+=1
    return AgentArr

#给每个患病的人进行生病周期计数
def InfectedDateStart(AgentArr):
    SDlist=list(x for x in AgentArr.keys() if AgentArr[x].state==1)
    for key in SDlist:
        AgentArr[key].infectedDate=4
    return AgentArr
    
#潜伏期的人变为病患(6天)
def TurnToInfected(AgentArr):
    SDlist=list(x for x in AgentArr.keys() if AgentArr[x].state==3)
    for key in SDlist:
        if AgentArr[key].infectedDate>=6:
            AgentArr[key].state=1
    return AgentArr

#达到一定时间后，患病的人变为健康的人，且具有免疫性（2）
def RecoverdAgent(AgentArr,Unit_CureTime):
    SDlist=list(x for x in AgentArr.keys() if AgentArr[x].state==1)
    for key in SDlist:
        if AgentArr[key].infectedDate>=Unit_CureTime:
            AgentArr[key].state=2
    return AgentArr

#Agent集合移除变化
def AgentOut_unit(AgentArr,AgentChange):
    IDlist=list(x for x in AgentArr.keys())
    RDlist=list(x for x in AgentChange.keys())
    sublist=list(set(IDlist)&set(RDlist))
    for akey in sublist:
        del AgentArr[akey]
    return AgentArr

#根据街道之间的人口移动，随机决定每个街道患病Agent（包括潜伏期）
def InfectedMove(popMoved,agentArr):
    MoveAgentArr={}
    IDlist=list(x for x in agentArr.keys())
    RDlist=[]
    RDlist=random.sample(IDlist,int(popMoved))
    for key in RDlist:
        MoveAgentArr[key]=agentArr[key]
    return MoveAgentArr

#新增患病人数(潜伏)
def IncreaseCount(PopNumber,insideMove,inMove,outMove):
    IncreaseCase=0
    IncreaseCase=round((0.2951606*(insideMove/PopNumber)+0.3096230*(inMove/PopNumber)+0.3080822*(outMove/PopNumber))*10000)
    return IncreaseCase
'''
#每个街道具有感染能力病原体统计
def InfectionCount(AgentArr):
    InfectionCount=0
    IDlist=list(x for x in AgentArr.keys())
    for key in IDlist:
        if AgentArr[key].state==1 or (AgentArr[key].state==3 and AgentArr[key].infectedDate>=3):
            InfectionCount+=1
    return InfectionCount
'''
#统计每个街道的病例数据
def CasesCount_Unit(AgentArr):
    CasesCount=0
    SDlist=list(x for x in AgentArr.keys() if AgentArr[x].state==1)
    CasesCount=int(len(SDlist))   
    return CasesCount
 
def SEIR():
    F3=open(npath+str(indexDate)+".csv",'w')
    #人口移动后街道内部疾病进行传播（SEIR）
    for x in UnitDict:
        #新增的感染者
        AgentArrs[x]=IncreaseCaseAgent(AgentArrs[x],IncreaseCount(PopArrs[x],insideArrs[x],inArrs[x],outArrs[x]))
        #患病周期进行计数
        AgentArrs[x]=InfectedDateCount(AgentArrs[x])
        #患病者状态发生改变：潜伏期-患病（>=6）;患病-康复（当地治愈时间）
        AgentArrs[x]=TurnToInfected(AgentArrs[x])
        AgentArrs[x]=RecoverdAgent(AgentArrs[x],UnitDict[x].CureTime)
        #统计各地区病例数据
        CasesCount=CasesCount_Unit(AgentArrs[x])
        #写入每日数据（总人口、病例数）
        F3.write(str(x)+',')
        F3.write(str(PopArrs[x])+',')
        F3.write(str(CasesCount)+'\n')
    F3.close() 
           
#读取初始化文件
F1=open(path,'r')
countLine=0
UnitDict={}
while True:
    line=F1.readline()
    if(countLine>0):
        if line:
            data=line.split(',')
            streetCode=int(data[2])
            population=int(data[3])
            startCase=int(data[4])
            cureTimeDay=int(data[5])
            InfectedCount,AgentArr,AgentNumber=InfectedAgent_S(CreatAgent_Unit(population,str(streetCode)),startCase)
            UnitArr=Unit(str(streetCode),InfectedCount,AgentNumber,AgentArr,0,cureTimeDay,0,0,0)
            UnitDict[streetCode]=UnitArr
        else:
            break
    countLine+=1
F1.close()

#第一天转移前先进行内部传播
AgentArrs={}
PopArrs={}
insideArrs={}
inArrs={}
outArrs={} 
for x in UnitDict:
    UnitDict[x].AgentArr=InfectedDateStart(UnitDict[x].AgentArr)
    AgentArrs[x]=UnitDict[x].AgentArr
    PopArrs[x]=UnitDict[x].Population
    insideArrs[x]=UnitDict[x].insideMove
    inArrs[x]=UnitDict[x].inMove
    outArrs[x]=UnitDict[x].outMove
    
#实现各街道总人口的转移
F2=open(spath,'r')
countLine=0
dateCount=0
while True:
    line=F2.readline()
    print (countLine)
    if(countLine>0):
        if line:
           data=line.split(',')
           sourceCode=int(data[2])
           targetCode=int(data[5])
           popNumber=round(int(data[6])/10)
           arriveDate=int(data[7])
           if dateCount==0:
               indexDate=arriveDate
               dateCount+=1
               
           if indexDate==arriveDate:
               #每个街道总人口的变化
               PopArrs[sourceCode]=PopArrs[sourceCode]-popNumber
               PopArrs[targetCode]=PopArrs[targetCode]+popNumber
               if(sourceCode==targetCode):
                   insideArrs[sourceCode]+=popNumber
               else:
                   outArrs[sourceCode]+=popNumber
                   inArrs[targetCode]+=popNumber    
                    #每个街道人口集合的变化
                   '''
                   AgentChange=InfectedMove(popNumber,AgentArrs[sourceCode]) 
                   AgentArrs[sourceCode]=AgentOut_unit(AgentArrs[sourceCode],AgentChange) 
                   AgentArrs[targetCode]=dict(AgentArrs[targetCode],**AgentChange)
                   '''
                              
           else :
                SEIR()
                for x in UnitDict:
                    insideArrs[x]=0
                    outArrs[x]=0
                    inArrs[x]=0
                indexDate=arriveDate
                if(sourceCode==targetCode):
                   insideArrs[sourceCode]+=popNumber
                else:
                   outArrs[sourceCode]+=popNumber
                   inArrs[targetCode]+=popNumber    
                    #每个街道人口集合的变化
                   '''
                   AgentChange=InfectedMove(popNumber,AgentArrs[sourceCode]) 
                   AgentArrs[sourceCode]=AgentOut_unit(AgentArrs[sourceCode],AgentChange) 
                   AgentArrs[targetCode]=dict(AgentArrs[targetCode],**AgentChange)
                   '''
        else:
            SEIR()
            break
    countLine+=1
F2.close()
    
         