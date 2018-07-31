# coding=utf-8
from tools import * 
from pprint import pprint
import yaml
import time

def getRegions():
    regs = []
    for x in GetLinks(DownloadPage("http://m.avito.ru/region/621540")):
        time.sleep(0.2)
        def t(x):
            return dict(url="http://m.avito.ru" + x['url'], name=x['name'])
        x=t(x)
        if 'region' in x['url'] or 'location' in x['url']:
            x['url'] = 'http://m.avito.ru/items?location_id='+ filter(lambda c: c in "0123456789", x['url'])
            print x['url']
            regs.append(x)
    return regs[2:]

def writeRegions():
    d = getRegions()
    yaml.dump(d, open('regions.yaml', "w"))
if __name__ == '__main__':
    writeRegions()