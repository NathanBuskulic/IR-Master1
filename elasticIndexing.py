import numpy as np
import json
from utils import *
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Document, Date, Nested, Boolean, \
    analyzer, InnerDoc, Completion, Keyword, Text

request_body = {
	    "settings" : {
                "index": {
                    "similarity":{
                        "default":{
                            "type":"LM Dirichlet similarity"
                            }
                        }
                    },
	        "number_of_shards": 1,
	        "number_of_replicas": 0
	    },

	    'mappings': {
	        '_doc': {
	            'properties': {
	                'content': {'index': 'true', 'type': 'text', "analyzer":"standard"},
	                'id': {'index': 'false', 'type': 'text'},
	            }}}
	}




ES_HOST = {"host" : "localhost", "port" : 9200}
es = Elasticsearch(hosts = [ES_HOST], timeout=300)
if es.indices.exists('my_index'):
    es.indices.delete('my_index')
    print('DELETED')
res = es.indices.create(index = 'my_index', body = request_body)

allDoc = getContentPilotRun("cran/cran.all.1400")
for i in allDoc:
    jerome = {'content':allDoc[i], 'id':i}
    outcome = es.index(index='my_index',doc_type='_doc',id=str(i),body=jerome)
    print(outcome)

#ES_HOST = {"host" : "localhost", "port" : 9200}
#es = Elasticsearch(hosts = [ES_HOST], timeout=300)
#res = es.indices.create(index = 'my_index', body = request_body)
#print(res)
