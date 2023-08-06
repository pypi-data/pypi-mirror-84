#-*- coding:utf8 -*-
### code by chengxz 2020/11/3 ####

from elasticsearch import Elasticsearch

class TcEs():
    def __init__(self,hosts,port):
        self.ES = Elasticsearch(hosts,port=port)

    def insert(self,index,doc_type,id,body):
        result = self.ES.index(index=index,doc_type=doc_type,body=body,id=id)
        return result['created']
    def delete(self,index,doc_type,id):
        result = self.ES.delete(index=index,doc_type=doc_type,id=id)
        assert result['result'] == 'deleted'
    def delete_by_query(self,index,doc_type,body):
        result = self.ES.delete_by_query(index=index,doc_type=doc_type,body=body)
        #print(result)
        return result['deleted']
    def update(self,index,doc_type,id,body):
        result = self.ES.update(index=index,doc_type=doc_type,id=id,body=body)
        assert result['result'] == 'updated'
    def get(self,index,doc_type,id):
        result = self.ES.get(index=index,doc_type=doc_type,id=id)
        return result['_source']
    def search(self,index,doc_type,body):
        result = self.ES.search(index=index,doc_type=doc_type,body=body)
        total = result['hits']['total']
        all_data = []
        if total > 0:
            hits = result['hits']['hits']
            for hit in hits:
                all_data.append(hit['_source'])
        return all_data
