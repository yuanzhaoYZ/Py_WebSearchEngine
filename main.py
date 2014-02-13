import json
import urllib
import re
import urlnorm
from data_store_SQL import *

DEBUG = True 
N = 20 #number of pages required for the output
Q = "zeta gundam" # search terms
link_history = set()

def google_search(searchfor):
    #Google search
    result = []
    query = urllib.urlencode({'q': searchfor})
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
    search_response = urllib.urlopen(url)
    search_results = search_response.read()
    results = json.loads(search_results)
    #Extract data from JSON response
    data = results['responseData']
    if DEBUG:print 'Total results: %s' % data['cursor']['estimatedResultCount']
    hits = data['results']
    
    if DEBUG:print 'Top %d hits:' % len(hits)
    for h in hits: 
        #Get links to web pages
        seed_link = h['url']
        if DEBUG:print ' ', seed_link
        if seed_link not in link_history:
            result.append(seed_link)
            link_history.add(seed_link)
        else:
            if DEBUG:print seed_link , 'has been visited,skip... '
    return result
#    print 'For more results, see %s' % data['cursor']['moreResultsUrl']





#Main
#1.Contact Google for initial 4 seeds
links = google_search(Q)

for link in links:
    #2.Download the webpage
    link_response = urllib.urlopen(link)
    link_content = link_response.read()
    link_response.close()
    normalized_url = urlnorm.norm(link) 
    cache_path = './webpages/'+normalized_url+'.html'
    cache_file = open(cache_path, 'w')
    cache_file.write(link_content)
    cache_file.close()
    #3. Parse key term and Assign priority
    p = re.compile(Q, re.IGNORECASE)
    m = p.findall(link_content)
    priority = -len(m)
    print priority, ' ', link
    #4. Save info to DB
    put_page(link, priority, cache_path)

#5. Extract hyperlinks
seed = get_next_seed()
if DEBUG:print seed[0]

re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', str(get_page_content(seed[0])))

