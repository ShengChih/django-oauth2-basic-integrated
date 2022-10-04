# test.py
import json


def application(env, start_response):
    start_response('200 OK', [('Content-Type','application/json')])
    body = bytes(json.dumps({'message': 'OK'}), 'utf-8') # or test.encode('utf-8')
    return [body]