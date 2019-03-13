import numpy as np
import json
import os
import sys
import datetime
import locale

from utils import *
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Document, Date, Nested, Boolean, \
    analyzer, InnerDoc, Completion, Keyword, Text

request_body = {
	    "settings" : {
                "index": {
                    "similarity":{
                        "default":{
                            "type":"LMDirichlet"
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
    print('Deleted')
res = es.indices.create(index = 'my_index', body = request_body)

#allDoc = getContentPilotRun("cran/cran.all.1400")

nrFolders = 1

for x in range(nrFolders) :
    bulk_data = []
    directory = "E:\Marjo\GOV2\gov2-corpus\GX" + str(x).zfill(3);
    for filename in os.listdir(directory):
        if not filename.endswith(".gz"):

            fp = open(directory + "\\" + filename, 'rb')
            content = fp.read().decode('utf-8', errors='ignore') # because of Chinese characters and other strange characters
            docList = getAllDocumentFromFile(content)
            fp.close()
            for doc in docList :
                jerome = {'content':doc[1], 'id':doc[0]}
                outcome = es.index(index='my_index',doc_type='_doc',id=doc[0],body=jerome)
                print(doc[0])


#ES_HOST = {"host" : "localhost", "port" : 9200}
#es = Elasticsearch(hosts = [ES_HOST], timeout=300)
#res = es.indices.create(index = 'my_index', body = request_body)
#print(res)
