import requests
import json

def get_related_words(search_term):
    """
    input: a search term we want to query google's trends with
    output: the related search terms in a list
    """

    # TODO: be able to request within a time frame
    base_url = "http://www.google.com/trends/fetchComponent?hl=en-US"
    query = "q=" + search_term
    cid = "cid=TOP_QUERIES_0_0"
    export = "export=3"
    s = '&'
    url = s.join((base_url, query, cid, export))

    r = requests.get(url)
    if r.status_code != 200:
        print "Could not make request"
        return

    try:
        related_json = json.loads(r.content[62:-2])
    except:
        print "Could not retrieve json"
        return

    related_words = [row['c'][0]['v'] for row in related_json['table']['rows']]

    # TODO: make a logging info file
    print "Google trends related terms similar to: " + search_term
    print related_words

    return related_words
