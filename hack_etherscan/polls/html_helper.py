
try:
    # For Python 3.0 and later
    from urllib.request import build_opener
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import build_opener


from bs4 import BeautifulSoup

def get_html_by_url(url):
    opener = build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    response = opener.open(url)
    html = response.read()
    soup = BeautifulSoup(html)
    return soup