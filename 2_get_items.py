# coding=utf-8
from tools import * 
from pprint import pprint
import yaml
import multiprocessing
import time
import itertools
import leveldb
import json

def mkQuery(location, page):    
    return "http://m.avito.ru/items?limit=200&location_id=%s&category_id=&page=%d" % (location, page)

def safeGet(url, cnt=10, pause=1):
    for x in range(cnt):
        try:
            print url
            return DownloadPage(url)
        except Exception, e:
            print e, url, x
            time.sleep(cnt * pause)
    return ""
from BeautifulSoup import BeautifulSoup       
def parsePage(url):
    
    data = []
    page = safeGet(url)
    if page == "":
        return []
    soup = BeautifulSoup(page)
    z = soup.findAll('a', 'img')

    for x in z:
        d = dict(url="http://m.avito.ru" + x['href'])
        for s in x.findAll('span', 'title'):
            d['title'] = s.text
        data.append(d)
    
    return data   
    
def saveData(data):
    db = ldb()
    id = data['url'].split('/')[-1]
    if db.get(id):
        pass
    else:
        db.put(id, data)
        
if __name__ == '__main__':
    # items = yaml.load(open('items.yaml'))
    # print len(items)
    # exit()
    t0 = time.time()
    regions = yaml.load(open('regions.yaml'))
    oldRegions = yaml.load(open("regions_cnt.yaml"))
    for r in regions:
        r['pages'] = []
        url = r['url']
        name = r['name']
        
        #if not(u"Моск" in r['name'] or u'Санкт' in r['name']):
        #    continue
        f = lambda x:filter(lambda c:c in "0123456789", x)
        cnt = 0
        for old in oldRegions:
            if old['name'] == r['name']:
                cnt = old['pages'] * 47
                if cnt > 200 * 250:
                    cnt = 200 * 250
                # print old['pages'], cnt
        for x in range(1, cnt / 200):
            purl = mkQuery(f(url), x)
            r['pages'].append(purl)
        # http://m.avito.ru/items?limit=20&location_id=662000&category_id=&page=2
    pool = multiprocessing.Pool(3)
    data = []
    
    db = leveldb.LevelDB('db')

    for r in regions:
        #if u"Моск" in r['name'] or u'Санкт' in r['name']:
        print r['name']

        items = pool.map(parsePage, r['pages'])
        for item in items:
            for i in item:
                d = dict(region=r['name'], title=i['title'], url=i['url'])
                id = d['url'].split('/')[-1]
                db.Put(id, json.dumps(d))