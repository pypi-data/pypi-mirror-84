import math
import copy

def calculate_rank(vector):
  a={}
  rank=1
  for num in sorted(vector,reverse=True):
    if num not in a:
      a[num]=rank
      rank=rank+1
  return[a[i] for i in vector]


def normalize_data(data,weights):
    for i in range(0,len(data[0])):
        calc = 0
        for j in range(0,len(data)):
            calc += data[j][i]**2
        calc = math.sqrt(calc)
        for j in range(0,len(data)):
            data[j][i] = (data[j][i]/calc)*weights[i]
    return data


def calculateVpVn(data,impacts):
    VJB = []
    VJW = []
    for i in range(0,len(data[0])):
        maxele = 0
        minele = 99999999
        for j in range(0,len(data)):
            if data[j][i]>maxele:
                maxele = data[j][i]
            if data[j][i]<minele:
                minele = data[j][i]

        if impacts[i] == '+':
            VJB.append(maxele)
            VJW.append(minele)
        else:
            VJW.append(maxele)
            VJB.append(minele)
    return VJB,VJW


def calculateSpSn(data,VJB,VJW):
    SIP = []
    SIN = []
    for i in range(0,len(data)):
        total_sip = 0
        total_sin = 0
        for j in range(0,len(data[0])):
            total_sip += (data[i][j] - VJB[j])**2
            total_sin += (data[i][j] - VJW[j])**2
        SIP.append(math.sqrt(total_sip))
        SIN.append(math.sqrt(total_sin))
    
    return SIP,SIN


def TopsisScore(df,weights,impacts):
    data = df.values
    data = data[:,1:]
    data = data.tolist()
    total_weight = sum(weights)
    result = map(lambda x: x/total_weight, weights)
    weights = list(result)
    data = normalize_data(data,weights)
    VJB,VJW = calculateVpVn(data,impacts)
    SIP,SIN = calculateSpSn(data,VJB,VJW)
    SIT = []
    for i in range(0,len(SIP)):
        SIT.append(SIP[i]+SIN[i])
    
    total = []
    for i in range(0,len(SIP)):
        total.append(SIN[i]/SIT[i])
    ranktotal = calculate_rank(total)
    final = copy.deepcopy(df)
    final['Topsis Score'] = total
    final['Rank'] = ranktotal
    return final