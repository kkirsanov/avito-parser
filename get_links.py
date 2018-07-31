# coding=utf-8
import multiprocessing
import itertools
import yaml
"""
def downloadPage(workurl):
    import zmq, time, json
    print workurl
    #import random
    #time.sleep(1 + random.randint(0, 5))
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://127.0.0.1:5000")
    # socket.connect("ipc:///tmp/parser")
    cnt = 0
    while True:
        try:
            print "downloading ", workurl['url'],
            data = DownloadPage('http://anonymouse.org/cgi-bin/anon-www.cgi/' + workurl['url'])
            print 'done'
            break
        except Exception, e:
            cnt += 1
            if cnt > 10:
                break
            continue
            print e, cnt, workurl['url']
    socket.send_json(dict(action='SET', name=workurl['url'].encode('utf-8'), data=data.encode('utf-8')))
    socket.recv()
    # print workurl    
"""


import re


def parseList(txt):
    from BeautifulSoup import BeautifulSoup
    t = BeautifulSoup(txt)
    print t
    t.find_all("div")
    
        
import tools
def getItems(x):
    print x
    exit()
    
    for i in range(10):
        try:
            print x
            z=tools.DownloadPage(x)
            return parseList(z)
            break
        except Exception, e:
            print "URL fail", x, e
            time.sleep(1)
            continue
    return z
if __name__ == '__main__':
    d = yaml.load(open('regions.yaml', "r"))
    workurls = []
    for region in d:
        if region['name']==u"Москва":
            urls = {region['url'] + "?p=" + str(x) for x in range(region['pages'])}
            
            for url in urls:
                workurls.append(dict(name=region['name'], url=url))

    import time
    from pprint import pprint

    pprint( getItems(workurls[0]['url']))
    #pprint.pprint(workurls)
    #t0 = time.time()
    #pool = multiprocessing.Pool(50)
    #pool.map(downloadPage, workurls[20:120])
    #print time.time() - t0
