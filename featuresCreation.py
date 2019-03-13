import numpy as np
from utils import getTopics
import wikipedia as wkp
from myScoringFun import tokenizeQuery
from elasticsearch import Elasticsearch


def find_all(bigStr,substr):
    ''' return all the occurences of a substring in a string'''
    start = 0
    result = []
    index = bigStr.find(substr)
    while index != -1:
        result.append(index)
        start = index + len(substr)
        index = bigStr.find(substr,start)
    return result
    

#print(find_all("test test test test","test"))

# We assume we have the wikipedia page in a nice string format
def TF(query, wkpage):
    return len(find_all(wkpage,query)) / len(wkpage)


def SPR(query,wkpage):
    allOcc = find_all(wkpage,query)
    #print(allOcc)
    if len(allOcc) != 0:
        return allOcc[len(allOcc) - 1] - allOcc[0]
    else:
        return -1


def allPos(query, wkpage):
    allOcc = find_all(wkpage,query)
    return [i/len(wkpage) for i in allOcc]


def QCT(query,wkpage):
    return int(wkpage.find(query) != -1)

def lenQuery(query,es):
    '''  get the number of terms in the query '''
    tokenized = tokenizeQuery(query,es)
    return len(tokenized)


def createFullFeatureVector(query,document,es):
    ''' create the feature vector that aggregate all the feature of all NGram + full query'''

    # We get the different terms
    terms = tokenizeQuery(query,es)

    result = []
    
    # We go through the 5 first terms
    for i in range(5):
        if len(terms) > i:
            result += createFeatureVectorNGram(terms[i],document,es)
        else:
            result += [-1 for i in range(7)]

    # We add the result of the full query
    result += createFeatureVectorNGram(query,document,es)
    print(result)
    return result


    

def createFeatureVectorNGram(query,document,es):
    ''' Take a NGram (a term here) and get all the features for that NGram '''
    # For now, just uses the full query and not n-Grams
    result = [
        TF(query,document),
        SPR(query,document),
        QCT(query,document),
        lenQuery(query,es)
    ]

    allPositions = allPos(query,document)
    allPositions = allPositions + [-1 for i in range(len(allPositions),3)]

    result = result + allPositions[:3]
    
    #print(result)
    return result

def getTrainingDataset(fileName,es):
    ''' return a tuple (X,Y) where X is a list of feature vector and Y are the associated labels '''

    flux = open(fileName,'r')
    queries = getTopics("topics.txt")

    X = []
    Y = []
    
    for line in flux:
        # We get the informations
        lineSplit = line.split(" ")
        queryNumber = int(lineSplit[0])
        print(queryNumber)
        relevantPositions = [int(i) for i in lineSplit[1:]]
        print(relevantPositions)
        
        # We get the query name
        query = queries[queryNumber]
        wikiSearch = wkp.search(query, results=10)

        for i in range(len(wikiSearch)):
            try:
                doc = wkp.page(wikiSearch[i]).content
                featureVec = createFullFeatureVector(query,doc,es)
                X.append(featureVec)

                # get the label
                if i in relevantPositions:
                    Y.append(1)
                else:
                    Y.append(0)
            except wkp.exceptions.DisambiguationError:
                pass
            except wkp.exceptions.PageError:
                pass

    return (X,Y)
                

#wkpage = "test test test testtest"
#query = "test"
#print(SPR(query,wkpage))


#ES_HOST = {"host" : "localhost", "port" : 9200}
#es = Elasticsearch(hosts = [ES_HOST], timeout=300)
#res = getTrainingDataset("queryToWk.txt",es)
#flux = open("trainingDataset.txt",'w+')
#(X,Y) = res
#for i in range(len(X)):
#    myStr = ""
#    for j in range(len(X[i])):
#        myStr += " " + str(X[i][j])
#    myStr = myStr[1:]
#    flux.write(myStr + "|" + str(Y[i]) + "\n")
#flux.close
