import sys

import requests


def post_request(endpoint, data):
    response = requests.post(endpoint, data=data, headers={'content-type': 'application/json', 'charset': 'UTF-8'})

    return response


def get_request(endpoint, data):
    response = requests.get(endpoint, data=data, headers={'content-type': 'application/json', 'charset': 'UTF-8'})

    return response


def get_repository(endpoint):
    res = get_request(endpoint, None)
    print('res', res, res.json())


def get_info(json):
    res = {'name': str(json['full_name']), 'creation': json['created_at'], 'last_update': json['updated_at'],
           'size': json['size']}

    return res


def complete(item, endpoint: str):
    res = get_request(endpoint + '/branches/master', None)
    date = None
    if res.ok and res is not None:
        json = res.json()
        print('res=', json)
        # if json is not None and json['commit'] is not None:
        date = json['commit']['commit']['committer']['date']

        item['last_commit'] = date


def list_fork(endpoint):
    res = get_request(endpoint, None)

    if not res.ok:
        print('res', res, res.json(), file=sys.stderr)
        exit(1)

    print('res', res, res.json())

    if not res.ok:
        exit(1)

    res = res.json()

    project = get_info(res)
    complete(project, endpoint)

    resultat = str(project)

    fork = res['forks_url']
    if len(fork) > 0:
        fork_list = get_request(fork, None)
        for item in fork_list.json():
            tmp = get_info(item)
            complete(tmp, endpoint)
            resultat += '\n' + str(tmp)

    print('fork:', resultat)


endpoint = 'https://api.github.com/repos/zxh0/jvm.go'

# get_repository(endpoint)

list_fork(endpoint)
