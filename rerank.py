import numpy as np
from myScoringFun import wikiScoringMethod, tokenizeQuery, getQueryCollectionCount
from elasticsearch import Elasticsearch
import wikipedia as wkp
from sklearn.svm import SVC
from featuresCreation import createFullFeatureVector

global TRAINED

def rerank(query,previousRanking,es):
    ''' Given a rannking, rerank all the documents accordingly to the new wikiScoreFunction  '''
    # Get all of the doc Id of the previous ranking
    idOfRanking = getListFromRanking(previousRanking)
    # We will store here every doc_Id with the new score

    queryTerms = tokenizeQuery(query,es)
    queryCollectionCount = getQueryCollectionCount(set(queryTerms),es)

    # get RelevantDoc
    relevantDoc = getRelevantDoc(query,es)
    
    resultWithScore = []
    # We calculate all the new scores
    for id in idOfRanking:
        resultWithScore.append((id,wikiScoringMethod(query,id,0.3,es,queryCollectionCount,queryTerms,relevantDoc)))

    # We sort everything out
    print(resultWithScore)
    sortedResult = sorted(resultWithScore,key=lambda x : x[1],reverse=True)
    return [i[0] for i in sortedResult]


def getListFromRanking(ranking):
    ''' from a result class of elasticSearch, create a simple list of the doc id'''
    result = []
    listRanking = ranking["hits"]["hits"]
    for i in range(len(listRanking)):
        result.append(listRanking[i]['_id'])
    return result


def getTrainingDataset(fileName):
    ''' Return (X,Y) of a dataset from textfile '''
    flux = open(fileName,'r')
    X = []
    Y = []
    for line in flux:
        firstSplit = line.split("|")
        Y.append(int(firstSplit[1]))
        Xsplit = firstSplit[0].split(" ")
        XTmp = []
        for i in Xsplit:
            XTmp.append(float(i))
        X.append(XTmp)
    #print(X,Y)
    return (X,Y)


def getRelevantDoc(query,es):
    ''' Return relevant document from wikipedia '''
    # For now take the two first results of wikipedia
    # print(query)
    # resultsWkp = wkp.search(query,results=2)
    # print(resultsWkp)
    # docs = []
    # for title in resultsWkp:
    #     docs.append(wkp.page(title).content)

    #return docs

    # New version :
    # Train the SVM:
    print(query)
    (X,Y) = getTrainingDataset("trainingDataset.txt") 
    clf = SVC(gamma='auto')
    clf.fit(X,Y)
    print("TRAINED!")

    relevDoc = []
    # get the relevant documents
    print(query)
    wkSearch = wkp.search(query,results=10)
    for title in wkSearch:
        try:
            wkPage = wkp.page(title).content
            featVec = np.array(createFullFeatureVector(query,wkPage,es))
            featVec = featVec.reshape(1,-1)
            #print(featVec)
            pred = clf.predict(featVec)
            if pred == 1:
                print("SVM predicted document to be relevant")
                relevDoc.append(wkPage)
        except wkp.exceptions.DisambiguationError:
            pass
        except wkp.exceptions.PageError:
            pass
    return relevDoc
            




    

#ES_HOST = {"host" : "localhost", "port" : 9200}
#es = Elasticsearch(hosts = [ES_HOST], timeout=300)
#query = "aerodynamics of the slipstream in the experiments"
#result = es.search(index='my_index',doc_type="_doc",explain=False,_source=False,size=20,body={'query':{'match': {"content" : query}}})
#print(getListFromRanking(result))
#print(rerank(query,result,es))
