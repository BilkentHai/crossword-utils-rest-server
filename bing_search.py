# -*- coding: utf-8 -*-


########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64, json, re

def search(query,count):
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': 'b8ae452574a7410bbdfcc2990be1b562' # subscription code to bing search api
    }
    
    params = urllib.parse.urlencode({
        # Request parameters
        'q': query + ("" if query == "crossword" else " -crossword"), # avoid using crossword websites
        'count': count,
        'offset': '0',
        'mkt': 'en-us',
        'safesearch': 'Moderate',
    })

    print(params)
    
    try:
        conn = http.client.HTTPSConnection('api.cognitive.microsoft.com')
        conn.request("GET", "/bing/v5.0/search?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        json_data = json.loads(data)
        
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    return extract_Urls(json_data)

def extract_Urls(json_data):
    raw_list = []
    url_list = []
    
    for item in json_data['webPages']['value']:
        raw_list.append(item['url'])
    
    for url in raw_list:
        url = re.findall(r"http.*(http.*)&p=DevEx", url)
        url = urllib.parse.unquote(url[0])
        url_list.append(url)
    
    filter_banned_domains(url_list)
    return url_list

def filter_banned_domains(Url_list):
    for item in Url_list:
        if "wikipedia.org" in item:
            Url_list.remove(item)
        
####################################