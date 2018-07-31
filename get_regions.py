# coding=utf-8
from tools import * 
import yaml



def getRegions():
    l = GetLinks(DownloadPage("http://www.avito.ru/?ru=east"))
    l += GetLinks(DownloadPage("http://www.avito.ru"))
    
    banlist = ['info', 'profile', 'registration', 'additem', 'job', 'help', 'contact', 'map', 'rossiya', "?"]
    needlist = ['avito']

    okUrl = []
    for url, name in map (lambda x: [x['url'], x['name'].encode('utf-8')], l):
        ok = map (lambda x:x not in url, banlist)
        ok += map (lambda x:x in url, needlist)
        ok = reduce(lambda a, b:a and b, ok, True)
        if ok:
            pages = 0
            okUrl.append(dict(url="http://" + str(url[2:]), name=name, pages=pages))
            for p in GetLinks(DownloadPage(okUrl[-1]['url'])):
                if p['name'] == 'Последняя':
                    num = p['url'].split('p=')[-1]
                    okUrl[-1]['pages'] = int(num)
                    print okUrl[-1]
            
    return okUrl

def writeRegions():
    d = getRegions()
    yaml.dump(d, open('regions.yaml', "w"))
    print d
if __name__ == '__main__':
    writeRegions()
    
