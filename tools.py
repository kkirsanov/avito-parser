def DownloadPage(url, headers=None):
    if headers == None:
        headers = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    else:
        pass
        
    from mechanize import Browser, _http
    
    br = Browser()    
    br.set_handle_robots(False)
    br.addheaders = headers
    
    page = br.open(url)
    return page.read()

def GetLinks(html):
    from BeautifulSoup import BeautifulSoup, SoupStrainer
    tmp = []
    for link in BeautifulSoup(html, parseOnlyThese=SoupStrainer('a')):
        if link.has_key('href'):
            tmp.append(dict(url=link['href'],name=link.getText()))
    return tmp


#"<div class="t_i_i .*<a href="(.*)".*<span>(.*)</span>"