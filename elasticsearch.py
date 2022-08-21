import requests as requests


def post_request(endpoint, data):
    response = requests.post(endpoint, data=data, headers={'content-type': 'application/json', 'charset': 'UTF-8'})

    return response


def builk_insert():
    endpoint = 'http://localhost:9200/_bulk'
    file = 'data/data_es.dump'

    with open(file) as f:
        contents = f.read()
        res = post_request(endpoint, contents)
        print('res=', res, res.text)


def search():
    endpoint = 'http://localhost:9200/test/_search'

    res = post_request(endpoint, None)
    print('res=', res, res.text)


def export():
    endpoint = 'http://localhost:9200/test/_search'
    withIndex = True
    withId = True

    res = post_request(endpoint, None)
    print('res=', res, res.text)
    if res.ok:
        json = res.json()
        print('json', json)
        print('hits', json['hits'])
        if json is not None and json['hits'] is not None and json['hits']['hits'] is not None:
            list = json['hits']['hits']
            res = ''
            for item in list:
                s = ''
                if withIndex:
                    s = '"_index" : "%s"' % (item['_index'])
                if withId:
                    if len(s) > 0:
                        s += ', '
                    s += '"_id" : "%s"' % (item['_id'])
                res += '{ "index" : { %s } }\n' % s
                res += str(item['_source']) + "\n"
            print(res)


# builk_insert()

# search()

export()
