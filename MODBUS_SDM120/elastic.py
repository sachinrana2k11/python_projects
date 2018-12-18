from elasticsearch import Elasticsearch

#es = Elasticsearch(hosts="https://search-sachinrana2k18-vglslnc4s2vn26pd7gqq7i45pe.us-east-1.es.amazonaws.com")
es = Elasticsearch(hosts="https://ohiRuOFiH:8c6861f1-d1dc-4322-8819-c072f5bfe9b1@scalr.api.appbase.io")


res = es.search(index="arnowa", doc_type="pointvalues", body={"query": {"match": {"name": "Current"}}})
print("%d documents found" % res['hits']['total'])
for doc in res['hits']['hits']:
    print(doc)