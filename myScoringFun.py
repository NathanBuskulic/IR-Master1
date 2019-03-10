import numpy as np
import json
import string
from utils import *
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Document, Date, Nested, Boolean, \
    analyzer, InnerDoc, Completion, Keyword, Text


ES_HOST = {"host" : "localhost", "port" : 9200}
es = Elasticsearch(hosts = [ES_HOST], timeout=300)

result = es.termvectors(index='my_index', doc_type='_doc', fields='content', term_statistics=True,id='1',positions=False,offsets=False)

def getQueryCollectionCount(listOfTerms,es):
    ''' Return a dictionnary with for each term in the query, the count of this term throughout the entire collection'''
    result = {}
    #print(listOfTerms)
    for word in listOfTerms:
        es.search()
        #We search for a document with that word inside
        querySearch = es.search(index='my_index',doc_type="_doc",body={'query':{'bool': {'filter' : {'term' : {"content" : word}}}}},size=1)
        #print(querySearch['hits']['hits'])
        #We get the id of the document
        #print(querySearch
        if len(querySearch['hits']['hits']) != 0:
            idToLook = querySearch['hits']['hits'][0]['_id']
            # We get the statistics from that document that include the entire index
            termvectors = es.termvectors(index='my_index', doc_type='_doc', fields='content', term_statistics=True,id=idToLook,positions=False,offsets=False)
            result[word] = termvectors['term_vectors']['content']['terms'][word]['ttf']
        else:
            result[word] = 0
    return result

    
def getDocSize(docStats):
    ''' Return the total doc size from the docStats'''
    result = 0
    termDict = docStats['term_vectors']['content']['terms']
    for i in termDict:
        result += termDict[i]['term_freq']
    return result


def dirichletSmoothing(t,docStats,mu,docSize,tCollectionFrequency):
    ''' return P(t|D) with a dirichlet smoothing '''

    # We check if the term appears in the document or not
    termDict = docStats['term_vectors']['content']['terms']
    result = 0
    if t in termDict:
        result += termDict[t]['term_freq'] + mu * tCollectionFrequency[t]
    else:
        result += mu * tCollectionFrequency[t]

    result = result / (docSize + mu)
    return result


def probabilityTermInQuery(t,listTermQuery):
    ''' Return P(t|~Q), which is the estimate of the word t in the initial query. '''

    return listTermQuery.count(t)/len(listTermQuery)


def tokenizeQuery(query,es):
    ''' Given a string query, tokenize it into terms '''
    result = []
    tokenization = es.indices.analyze(index="my_index",body={"analyzer" : "standard", "text" : query})
    tokens = tokenization['tokens']
    for i in range(len(tokens)):
        result.append(tokens[i]['token'])
    return result


def probaQueryGivenDocument(queryTerms,doc):
    ''' return P(Q|D) '''
    result = 1
    lenDoc = sum([i.strip(string.punctuation).isalpha() for i in doc.split()])
    for term in queryTerms:
        result = result * (doc.count(term) / lenDoc)
    return result


def probaTermInDoc(term, doc):
    ''' Return P(t|D) for relevant documents  '''

    lenDoc = sum([i.strip(string.punctuation).isalpha() for i in doc.split()])
    return doc.count(term) / lenDoc


def probaTermExtendedRelevantDoc(term,listDoc,probaQueryDocList):
    ''' return P(t | 0q) '''
    result = 0
    for i in range(len(listDoc)):
        result += probaTermInDoc(term,listDoc[i]) * probaQueryDocList[i]
    if result != 0:
        return result/len(listDoc)
    else:
        return result
    

def wikiScoringMethod(query,doc_id,lambdaParam,es,queryCollectionCount,queryTerms,relevantDoc):
    ''' Scoring function of the paper (simplified for now) 
        Given a query and a doc id, recalculate the score of that document
        We assume equal priors here'''

    global queryTermsC
    result = 0
    queryTerms = tokenizeQuery(query,es)
    docStats = es.termvectors(index='my_index', doc_type='_doc', fields='content', term_statistics=False,id=doc_id,positions=False,offsets=False)
    #queryCollectionCount = getQueryCollectionCount(set(queryTerms),es)
    docSize = getDocSize(docStats)

    # We construct the proba of the qury per document:
    probaQueryDoc = []
    for doc in relevantDoc:
        probaQueryDoc.append(probaQueryGivenDocument(queryTerms,doc))
    

    # We apply the formula
    for t in set(queryTerms):
        dirichSmooth = dirichletSmoothing(t,docStats,200,docSize,queryCollectionCount)
        if dirichSmooth != 0:
            probaTerm = lambdaParam * probabilityTermInQuery(t,queryTerms) + (1 -lambdaParam) * probaTermExtendedRelevantDoc(t, relevantDoc, probaQueryDoc)
            result += probaTerm * np.log(dirichSmooth)
        else:
            result = -10000

    return result


#print(wikiScoringMethod("The aerodynamics of wind slipstream in the experiments?",'2',es))
#print(getDocSize(result))
#print(getQueryCollectionCount(['aerodynamics'],es))
#tokenization = es.indices.analyze(index="my_index",body={"analyzer" : "standard", "text" : "has has has anyone investigated the shear buckling of stiffened plates ."})
#print(tokenizeQuery("has has has anyone investigated the shear buckling wimp shear of stiffened plates .",es))
