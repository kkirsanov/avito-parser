# coding=utf-8
class Gender:
    def __init__(self):
        fm = open('mnames.txt')
        ff = open('fnames.txt')
        self.f = set()
        self.m = set()
        for l in fm:
            
            l = unicode(l.replace("\n", '').replace(")", '')).lower()
            if l:
                if '-' in l:
                    self.m.add(l.split('-')[0])
                    #self.m.add(l.split('-')[1])
                self.m.add(l)
        for l in ff:
            l = unicode(l.replace("\n", '').replace(")", '')).lower()
            if l:
                if '-' in l:
                    self.f.add(l.split('-')[0])
                    #self.f.add(l.split('-')[1])
                self.f.add(l)
        ff.close()
        fm.close()
    def isMale(self, name):
        if name.lower() in self.m:
            return True
    def isFemale(self, name):
        if name.lower() in self.f:
            return True   
    def classify(self, name):
        if len(name) < 3:
            return "unknown"
        if self.isMale(name):
            return "male"
        if self.isFemale(name):
            return "female"
        return "unknown"
if __name__ == '__main__':
    
    #sort names
    """
    n=set()
    for l in open('mnames.txt'):
        n.add(l.replace('\n','').replace(')',''))
    
    l = list(n)
    f2=open('mnames2.txt', "w")
    l.sort()
    for n in l:
        f2.write(n+'\n')
    exit()
    """
    from tools import * 
    import re
    from BeautifulSoup import BeautifulSoup, SoupStrainer

    def getNames(url):
        def splitUp(st):
            def isUp(x):
                if x in "ЙФЯЦЫЧУВСКАМЕПИНРТГОЬШЛБЩДЮЖЗЭХЪ":
                    return True
                return False
        
            res = []
            for x in st:
                if isUp(x):
                    res.append("")
                if len(res) == 0:
                    res.append(x)
                else:
                    res[-1] += x
            return res
        
        
        page = DownloadPage(url)
        soup = BeautifulSoup(page)
        data = soup.findAll('td')[-3:]
        
        d = data[0].text + " " + data[1].text + " " + data[2].text
        names = []
        for x in splitUp(d):
            try:
                names.append(x.split(' ')[0])
            except:
                pass
    
        return names
    
    
    z = getNames('http://vse-imena.com/imena-m18-05.html')
    url = 'http://vse-imena.com/'
    p = DownloadPage(url)
    
    # m male g female
    gp = re.findall(r"imena-g[0-9]+\.html", p)
    print gp
    urls = []
    for p in gp:    
        u = p.split('.')[0]
        url = 'http://vse-imena.com/' + p
        
        page = DownloadPage(url)
        links = GetLinks(page)
        print url
        urls.append('http://vse-imena.com/' + p)
        for l in links:
            if u in l['url']:
                urls.append('http://vse-imena.com/' + l['url'])

    for x in urls:
        print x
    f = open('fnames.txt', "w")
    for u in urls:
        print u
        for n in getNames(u):
            f.write(n + "\n")
    f.close()
