import pytrends.request as tr
import google_creds

USERNAME = google_creds.username
PASSWORD = google_creds.password

def get_related_words(search_term):
    """
    input: a search term we want to query google's trends with
    output: the related search terms in a list
    """
    r = tr.TrendReq(USERNAME, PASSWORD)
    trends = r.related({'q':'clothing'}, 'top')
    return [t['c'][0]['v'] for t in trends["table"]["rows"]]
