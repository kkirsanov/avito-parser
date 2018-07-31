#!/usr/bin/python
# Run unix date command 3 times 

import leveldb
import json

cnt = 0
f = open("z.csv", "r")
f2 = open("z3.csv", "w")

ph = set()
for l in f:
    d = l.split('\t')
    try:
        if d[-5][0] == '8':
            d[-5] = "7"+d[-5][1:]
        p = d[-5]
        if p not in ph:
            st = "\t".join(d)
            # print st
            f2.write(st)
            ph.add(d[-5])
        else:
            pass
            
    except:
        pass
f2.close()
print len(ph)
