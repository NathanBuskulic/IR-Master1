import numpy as np
import json
from utils import *
from rerank import rerank
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Document, Date, Nested, Boolean, \
    analyzer, InnerDoc, Completion, Keyword, Text


ES_HOST = {"host" : "localhost", "port" : 9200}
es = Elasticsearch(hosts = [ES_HOST], timeout=300)

relevanceJudg = getRelevancePilotRun("cran/cranqrel")
statisticResult = {'P@10':[],'AvP':[],'RR':[],'Recall':[]}

queries = getQueriesPilotRun("cran/cran.qry")
queries = {i : queries[i] for i in queries if i <= 225}
for i in queries:
    # We get the first pass of result
    result = es.search(index='my_index',doc_type="_doc",explain=False,_source=False,size=100,body={'query':{'match': {"content" : queries[i]}}})

    # We rerank everything
    result = rerank(queries[i],result,es)
    
    relevanceRank = []
    for j in range(0,10):
        # Create the relevance ranking
        relevanceRank.append(int(int(result[j]) in relevanceJudg[i]))
    print(relevanceRank)

    statisticResult['P@10'].append(evaluationPrecision(relevanceRank))
    statisticResult['AvP'].append(evaluationAveragePrecision(relevanceRank,len(relevanceJudg[i])))
    statisticResult['RR'].append(evaluationRR(relevanceRank))
    statisticResult['Recall'].append(evaluationRecall(relevanceRank,len(relevanceJudg[i])))

finalStat = {'P@10' : np.mean(statisticResult['P@10']),
             'MAP' : np.mean(statisticResult['AvP']),
             'MRR' : np.mean(statisticResult['RR']),
             'Recall' : np.mean(statisticResult['P@10'])}

print(finalStat)

#result = es.search(index="my_index",doc_type="_doc",explain=True,body={'query':{'match': {"content" : 'aerodynamics slipstream wind'}}})

#print(result)