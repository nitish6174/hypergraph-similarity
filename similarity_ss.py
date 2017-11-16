import json
import numpy as np
import copy
import collections
import hashlib


EPSILON = 0.0001
F = 128

def hashfunc(x):
    return int(hashlib.md5(x).hexdigest(), 16)


def computeQuality(graph):
    scores = [0]*graph["n"]
    for edge in graph["edges"]:
        for vertex in edge:
            scores[vertex]+=1
    return scores

def getNorm(a,b):
    n = len(a)
    diff = 0
    for i in range(0,n):
        diff += abs(b[i] - a[i])
    return abs(diff)

def computeQualityPageRank(graph, scores):
    l = graph['n']

    scoresnp = np.zeros(l)
    scoresnp = [float(scores[i])/sum(scores) for i in range(len(scores))]

    pageRankMatrix = np.zeros((l,l))

    for edge in graph["edges"]:
        for i in range(len(edge)):
            for j in range(i+1, len(edge)):
                pageRankMatrix[edge[i]][edge[j]]+=1
                pageRankMatrix[edge[j]][edge[i]]+=1


    for i in range(len(pageRankMatrix)):
        totalsum = sum(pageRankMatrix[i])
        if totalsum !=0:
            for j in range(len(pageRankMatrix)):
                pageRankMatrix[i][j]= float(pageRankMatrix[i][j])/totalsum
               


    scorestemp = np.zeros((l))
    graphT = np.transpose(pageRankMatrix)
    
    while True:
        rtemp = np.zeros((l))
        rtemp += np.matmul(graphT, scoresnp)
        rnorm = sum(rtemp)
        rtemp /= rnorm
        # print(r)
        # print(rtemp)
        if getNorm(scoresnp,rtemp) < EPSILON:
            break
        scoresnp = copy.deepcopy(rtemp)


    return rtemp

def computeQualityEdges(graph, quality, scores):
    length = len(graph['edges'])
    qualityEdges = [0]*length

    for i in range(len(graph['edges'])): 
        for j in range(len(graph['edges'][i])):
            qualityEdges[i]+= float(quality[graph['edges'][i][j]])/scores[graph['edges'][i][j]]

    return qualityEdges


def computeScore(value1, value2):
    x = (value1 ^ value2) & ((1 << F) - 1)
    #Hamming distance = XOR 2 binary strings and calculate no. of set bits.
    ans = 0
    while x:
        ans += 1
        x &= x - 1
    return 1 - float(ans)/F

def build_by_features(features):
    v = [0] * F
    masks = [1 << i for i in range(F)]
    if isinstance(features, dict):
        features = features.items()
    for f in features:
        assert isinstance(f, collections.Iterable)
        h = hashfunc(f[0].encode('utf-8'))
        w = f[1]
        for i in range(F):
            v[i] += w if h & masks[i] else -w
    ans = 0
    for i in range(F):
        if v[i] > 0:
            ans |= masks[i]
    
    return ans



if __name__ == '__main__':
    with open("data/generated_hypergraphs.json") as f:
        graphs = json.load(f)

    l = len(graphs)
    quality = [[0]]*l
    qualityEdges = [[0]]*l 

    for i in range(l):
        scores = computeQuality(graphs[i])
        quality[i] = computeQualityPageRank(graphs[i], scores)
        qualityEdges[i] = computeQualityEdges(graphs[i], quality[i], scores)

    features = [dict() for x in range(l)]

    for i in range(l):
        for j in range(len(scores)):
            features[i]["v" + str(j)] = quality[i][j]

    for i in range(l):
        for j in range(len(graphs[i]['edges'])):
            str1 = ""
            for vertex in sorted(graphs[i]['edges'][j]):
                str1+= "v" + str(vertex)    
            features[i][str1] = qualityEdges[i][j]


    for i in range(l):
        for j in range(i+1,l):
            score = computeScore(build_by_features(features[i]), build_by_features(features[j]))
            print str(graphs[i]["label"]) + " " + str(graphs[j]["label"]) + " " + str(score)