# coding=utf-8
#!/usr/bin/python
# Run unix date command 3 times 

import leveldb
import json

cnt = 0
f = open("out.csv", "w")
db = leveldb.LevelDB('db_new')

# for i, x in enumerate(db.RangeIter()):
#    print i 

from names import Gender

G = Gender()

exit()
#for x in G.f:
#    print type(x), x
#print G.classify(unicode(u'Наталья'))
#exit()

def writef(x, f):
    def tw(data):
        try:
            f.write(data.replace("\t", "").replace("\n", ""))
        except:
            pass
            
        f.write('\t')
    try:
        tw(x['city'].replace(u"Город", ''))
        tw(x['region'])
        if x['phone'][0] == '8':
            x['phone'] = "7" + x['phone'][1:]
            
        tw(x['phone'])
        x['user'] = x['user'].replace(u'Продавец', '')
        
        tw(x['user'])
        
        cl = x['user'].split(' ')
        cl = map (G.classify, cl)
        gender ='unknown'
        if 'male' in cl:
            gender = 'male'
        if 'female' in cl:
            gender='female'
        tw(gender)                
        tw(x['title'])
        tw(x['catalog'])
        tw(x['price'])
        
    except:
        pass
    f.write('\n')
def flt(x):
    return unicode(x).replace("\t", "").replace("\n", "")
ph = set()
cnt = 0
for k, v in db.RangeIter():
    v = json.loads(v)

    try:
        if v.has_key('phone'):
            if v['phone'][0] == '8':
                
                v['phone'] = '7' + v['phone'][1:] 
            if v['phone'] not in ph:
                ph.add(v['phone'])
                writef(v, f)
            else:
                pass
            
    except Exception as e:
        pass
        # print e
    # writef(v, f)
    # print v
    # exit()
    # if v.has_key('parsed'):
    # for _k, _v in v.iteritems():
    #    print _k, v
        # f.write(flt(_v))
        # f.write('\t')
    # print ""
    # f.write('\n')

