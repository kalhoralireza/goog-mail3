import sys
import re
import urllib3
import certifi

def StripTags(text):
    """
    This function will remove tags from the http response.
    <tag>This will be the result.<tag> --output--> This will be the result.
    source of this piece of code: https://github.com/leebaird/discover/blob/2288368603885dbb1938061af995a8e13e6459e0/mods/goog-mail.py#L9
    """
    finished = 0
    while not finished:
        finished = 1
        start = text.find('<') # finds index of first tag in text
        if start >= 0:
            stop = text[start:].find('>')
            if stop >= 0:
                text = text[:start] + text[start+stop+1:]
                finished = 0
    return text

def google_this(text, count=50):
    """
    This function will search for <text> in googel and googel groups and returns
    the results in form of a list.
    for more results, change <count>.
    """
    http = urllib3.PoolManager(ca_certs=certifi.where())
    page_counter = 0
    results = list()
    headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)'}
    try:
        while page_counter < count:
            search_query = 'https://groups.google.com/groups?q='+str(text)+'&hl=en&lr=&ie=UTF-8&start=' + repr(page_counter) + '&sa=N'
            search_query_web = 'https://www.google.com/search?q=%40'+str(text)+'&hl=en&lr=&ie=UTF-8&start=' + repr(page_counter) + '&sa=N'
            response = http.request("GET", search_query, headers=headers)
            response_web = http.request("GET", search_query_web, headers=headers)
            results.append(response.data.decode('utf-8'))
            results.append(response_web.data.decode('utf-8'))
            page_counter += 10
    
    except IOError:
        print("[!] Cannot connect to Google.")
    return results
    
def filter(responses: list, regex: str):
    """
    Will be filter responses or a string, through a regex and returns the unique results.
    """
    uniq_results = {}
    for response in responses:
        results = (re.findall(regex, StripTags(response)))
        for result in results:
            uniq_results[result] = 1
    return uniq_results

def usage():
    print("Extracts emails from Google results.")
    print("Edited version of some old tool(python 2).")
    print("Usage: python3 goog-mail.py <domain>")
    sys.exit(1)

def main():
    # check if domain name passed to script.
    if len(sys.argv) != 2:
        usage()
    domain_name = sys.argv[1]
    regex = f'([\w\.\-]+@'+domain_name+')' # a regex for filtering emails that are like xxxx@domain_name.xxx
    web_contents = google_this(domain_name)
    emails = filter(web_contents, regex)
    for email in emails.keys():
        print(email)


if __name__ == '__main__':
    main()