# coding=utf-8
from subprocess import Popen
import leveldb
import multiprocessing
import json
from pprint import pprint
import tools
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *
import time
import os
import tempfile

import subprocess
from aviro_parser import AviroParser
from timeit import itertools


def parse(x):
    k, v = x
    v = json.loads(v)
    if v.has_key('phone'):
        if v.phone!="":
            return 
    import zmq
    context = zmq.Context()
    
    p = context.socket(zmq.REP)
    port = p.bind_to_random_port('tcp://127.0.0.1')
    
    proc = Popen("/usr/bin/python aviro_parser.py -p %d" % port, shell=True)
    d = p.recv()
    p.send_json(v)
    newd = p.recv_json()
    p.send('ok')
    proc.wait()
    v.update(newd)
    return (k, v)
def loadProxy():
    f = open ("prx.lst")
    p = []
    for l in f:
        p.append(l.split(':'))
        p[-1][-1] = int(filter(lambda x:x in "0123456789", p[-1][-1]))
    return p

if __name__ == "__main__":
    proxylst = loadProxy()
    pool = multiprocessing.Pool(len(proxylst)/2)
    db = leveldb.LevelDB('db')
    db.RangeIter('0', '9999999999')
    cnt = 0
    bucket = []
    for i in db.RangeIter('0', '9999999999'):
        k, v = i
        if json.loads(v).has_key('parsed'):
            continue
            
        bucket.append([k, v])
        if len(bucket) >= len(proxylst):
            for i, b in enumerate(bucket):
                d = json.loads(b[1])
                d['proxy'] = proxylst[i][0]
                d['proxyp'] = proxylst[i][1]
                bucket[i][1] = json.dumps(d)
                
            data = pool.map(parse, bucket)
            if data:
                try:
                    for k, v in data:
                        print v
                        db.Put(k, json.dumps(v))
                except Excption,e:
                    print e
                    pass
            bucket = []
            time.sleep(10)
            #exit()
