import numpy as np
from myScoringFun import wikiScoringMethod, tokenizeQuery, getQueryCollectionCount
from elasticsearch import Elasticsearch

def rerank(query,previousRanking,es):
    ''' Given a rannking, rerank all the documents accordingly to the new wikiScoreFunction  '''
    # Get all of the doc Id of the previous ranking
    idOfRanking = getListFromRanking(previousRanking)
    # We will store here every doc_Id with the new score

    queryTerms = tokenizeQuery(query,es)
    queryCollectionCount = getQueryCollectionCount(set(queryTerms),es)
    
    resultWithScore = []
    # We calculate all the new scores
    for id in idOfRanking:
        resultWithScore.append((id,wikiScoringMethod(query,id,es,queryCollectionCount,queryTerms)))

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

ES_HOST = {"host" : "localhost", "port" : 9200}
es = Elasticsearch(hosts = [ES_HOST], timeout=300)
query = "aerodynamics of the slipstream in the experiments"
result = es.search(index='my_index',doc_type="_doc",explain=False,_source=False,size=20,body={'query':{'match': {"content" : query}}})
print(getListFromRanking(result))
print(rerank(query,result,es))
