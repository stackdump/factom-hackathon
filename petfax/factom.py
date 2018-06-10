VERSION = 'v1'
import os
import requests
import json
import base64

API = os.environ.get('FACTOM_HOST')
KEY = os.environ.get('FACTOM_KEY')
URL = API + '/' + VERSION

HEADERS = {
   "Content-Type": "application/json",
   "factom-provider-token": KEY,
}

def _encode(data):
    if not data: 
        return ''

    return base64.b64encode(data.encode()).decode()

def _decode(data):
    if not data: 
        return ''

    return base64.b64decode(data)

def _decode_response(data):
    res = json.loads(data)

    # TODO: decode content if it exists

    if 'items' in res:
        for _item in res['items']:
            if 'external_ids' in _item:
                _item['external_ids'] = [ _decode(_id) for _id in _item['external_ids'] ]
    elif 'external_ids' in res:
            res['external_ids'] = [ _decode(_id) for _id in res['external_ids'] ]

    return res

def info():
    """ get api info """
    res = requests.request("GET", URL, headers=HEADERS)
    return _decode_response(res.content)

def chains():
    """ get api info """
    res = requests.request("GET", URL + '/chains', headers=HEADERS)
    return _decode_response(res.content)

def create_chain(external_ids=None, content=None, callback_url=None, callback_stages=None):
    """ """
    print ('create_chain => ', external_ids, content)

    _ids = [ _encode(extid) for extid in external_ids ]
    payload = json.dumps({"external_ids": _ids, "content": _encode(content) })
    res = requests.request("POST", URL + '/chains', data=payload, headers=HEADERS)
    return _decode_response(res.content)

def chain_search(external_ids=None):
    """ """
    _ids = [ _encode(extid) for extid in external_ids ]
    payload = json.dumps({"external_ids": _ids})
    res = requests.request("POST", URL + '/chains/search', data=payload, headers=HEADERS)
    return _decode_response(res.content)

def chain_info(chain_id=None):
    """ """
    res = requests.request("GET", URL + '/chains/%s' % chain_id, headers=HEADERS)
    return _decode_response(res.content)

def chain_entries(chain_id=None):
    """ """
    res = requests.request("GET", URL + '/chains/%s/entries' % chain_id, headers=HEADERS)
    return _decode_response(res.content)

def chain_add_entry(chain_id=None, external_ids=None, content=None, callback_url=None, callback_stages=None):
    """ """
    _ids = [ _encode(extid) for extid in external_ids ]
    payload = json.dumps({"external_ids": _ids, "content": _encode(content) })
    res = requests.request("POST", URL + '/chains/%s/entries' % chain_id, data=payload, headers=HEADERS)
    return _decode_response(res.content)

def chain_entry_search(chain_id=None, external_ids=None):
    """ """
    _ids = [ _encode(extid) for extid in external_ids ]
    payload = json.dumps({"external_ids": _ids})
    res = requests.request("POST", URL + '/chains/%s/entries/search' % chain_id, data=payload, headers=HEADERS)
    return _decode_response(res.content)

def chain_entry_first(chain_id=None):
    """ """
    res = requests.request("GET", URL + '/chains/%s/entries/first' % chain_id, headers=HEADERS)
    return _decode_response(res.content)

def chain_entry_last(chain_id=None):
    """ """
    res = requests.request("GET", URL + '/chains/%s/entries/last' % chain_id, headers=HEADERS)
    return _decode_response(res.content)

def chain_get_entry(chain_id=None, entry_hash=None):
    """ """
    res = requests.request("GET", URL + '/chains/%s/entries/%s' % (chain_id, entry_hash), headers=HEADERS)
    return _decode_response(res.content)
