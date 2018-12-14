from elasticsearch import Elasticsearch

es = Elasticsearch(hosts="https://search-sachinrana2k18-vglslnc4s2vn26pd7gqq7i45pe.us-east-1.es.amazonaws.com")
res = es.search(index="testapp", doc_type="testvalue", body={"query": {"match": {"name": "voltage"} and {"value": "71"} and  }})
print("%d documents found" % res['hits']['total'])
for doc in res['hits']['hits']:
    print(doc)