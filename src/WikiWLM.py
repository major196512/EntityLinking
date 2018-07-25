import requests
import math
import os
import json

N = 570000000
save_dir1 = './SaveData'
save_dir2 = save_dir1 + '/Backlink'

def GetID(title):
    request = {}
    request['action'] = 'query'
    request['titles'] = title
    request['format'] = 'json'
    request['formatversion'] = 2
    
    req = request.copy()
    result = requests.get('https://en.wikipedia.org/w/api.php', params=req).json()
    if 'error' in result:
        raise Error(result['error'])
    if 'warnings' in result:
        print(result['warnings'])
    if 'query' in result:
        return result['query']['pages'][0]['pageid']

def query(title):
    if not os.path.isdir(save_dir1):
        os.mkdir(save_dir1)
        
    if not os.path.isdir(save_dir2):
        os.mkdir(save_dir2)
       
    ret = []
    file_id = GetID(title)
    file_str = save_dir2 + '/' + str(file_id)
    if os.path.isfile(file_str):
        with open(file_str, 'r') as f:
            ret = json.load(f)
    
    else:
        request = {}
        request['action'] = 'query'
        request['titles'] = title
        request['prop']= 'linkshere'
        request['lhlimit'] = 500
        request['format'] = 'json'
        request['formatversion'] = 2

        lastContinue = {}

        while True:
            req = request.copy()
            req.update(lastContinue)
            result = requests.get('https://en.wikipedia.org/w/api.php', params=req).json()
            if 'error' in result:
                raise Error(result['error'])
            if 'warnings' in result:
                print(result['warnings'])
            if 'query' in result:
                t = result['query']['pages'][0]['linkshere']
                for i in range(len(t)):
                    ret += [t[i]['pageid']]
                #ret += result['query']['pages'][0]['linkshere']
            if 'continue' not in result:
                break
            lastContinue = result['continue']
        
        with open(file_str, 'w') as f:
            json.dump(ret, f, indent='\t')
        
    return set(ret)

def WLM(entity1, entity2):
    set1 = query(entity1)
    set2 = query(entity2)
    
    len1 = len(set1)
    len2 = len(set2)
    
    ret1 = math.log(max(len1, len2)) - math.log(len(set1 & set2))
    ret2 = math.log(N) - math.log(min(len1, len2))
    
    return ret1 / ret2