#-*- coding:utf8 -*-
### code by chengxz 2020/11/3 ####

from tces import TcEs
import random,string

es = TcEs(['172.17.9.13','172.17.9.33','172.17.9.25'],port=19300)

def test_es_insert():
    body = {"name": 'chengxz', 'sex': 'male', 'age': 17}
    id = int(''.join(random.sample(string.digits*10,5)))
    assert es.insert('index_test','beijing',id,body) == True

def test_es_delete():
    body = {"name": 'Mary', 'sex': 'female', 'age': 18}
    id = int(''.join(random.sample(string.digits * 10, 5)))
    assert es.insert('index_test', 'beijing', id, body) == True
    es.delete('index_test','beijing',id)

def test_es_delete_by_query():
    body = {"name": 'chengxz', 'sex': 'female', 'age': 18}
    id = int(''.join(random.sample(string.digits * 10, 5)))
    assert es.insert('index_test', 'beijing', id, body) == True
    body2 = {'query':{'match':{'name':'chengxz'}}}
    assert es.delete_by_query('index_test','beijing',body2) >= 1

def test_es_get():
    name = ''.join(random.sample(string.ascii_letters , 10))
    body = {"name": name, 'sex': 'female', 'age': 18}
    id = int(''.join(random.sample(string.digits * 10, 5)))
    assert es.insert('index_test', 'beijing', id, body) == True

    result  = es.get('index_test','beijing',id=id)
    assert result['name'] == name

def test_es_search():
    name = ''.join(random.sample(string.ascii_letters , 10))
    body = {"name": name, 'sex': 'female', 'age': 18}
    id = int(''.join(random.sample(string.digits * 10, 5)))
    assert es.insert('index_test', 'beijing', id, body) == True

    body2 = {'query':{'match_all':{}}}
    result = es.search('index_test','beijing',body2)
    assert len(result) >= 1

def test_es_update():
    name = ''.join(random.sample(string.ascii_letters , 10))
    body = {"name": name, 'sex': 'female', 'age': 18}
    id = int(''.join(random.sample(string.digits * 10, 5)))
    assert es.insert('index_test', 'beijing', id, body) == True

    body2 = {"script":"ctx._source.age=99"}
    es.update('index_test','beijing',id=id,body=body2)


if __name__ == "__main__":
    test_es_insert()
    test_es_delete()
    test_es_delete_by_query()
    test_es_get()
    test_es_update()
    test_es_search()