# coding=utf8

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
import threading
from BeautifulSoup import BeautifulSoup
class AviroParser():
    def __init__(self, url, proxy=None, proxyp=None):
        self.url = url
        self.step = 0
        self.price = ""
        self.city = ""
        self.user = ""
        self.phone = ""
        self.catalog = ""
        self.debug = False
        self.deadline = 20
        self.app = QApplication(sys.argv)
        self.web = QWebView()
        self.web.loadFinished.connect(self.onDone)
        self.web.loadProgress.connect(self.percent)
        if proxy:
            QNetworkProxy.setApplicationProxy(QNetworkProxy(QNetworkProxy.HttpProxy, proxy, proxyp))
    def stop(self):
        if self.debug:
            print "timeout"
        self.app.processEvents()
        self.app.closeAllWindows()
        self.app.processEvents()
        self.app.quit()
        import PyQt4
        PyQt4.QtGui.qApp.closeAllWindows()
        # self.app.exit()
    def parse(self):
        self.web.load(QUrl(self.url))
        self.timer = QTimer()
        self.timer.start(500)  # You may change this if you wish.
        self.timer.timeout.connect(lambda: None) 
        
        QTimer.singleShot(self.deadline * 1000, self.stop)
        self.app.exec_()
        return dict(phone=filter(lambda x:x in "0123456789", self.phone), price=self.price, user=self.user, city=self.city, catalog=self.catalog)
    def percent(self, p):
        self.web.update()
        pass
    def searchCode(self):
        import random
        self.app.processEvents()
        z = unicode(self.web.page().mainFrame().findFirstElement(".m_item_call_link").toPlainText())
        if len (z) > 5:
            self.phone = unicode(z)
            self.stop()
        else:
            QTimer.singleShot(1000, self.searchCode)
    def onDone(self, val):
        self.searchCode()
        if self.step == 0:
            z = self.web.page().mainFrame().findFirstElement("#showPhoneBtn")
            z.evaluateJavaScript("var evObj = document.createEvent('MouseEvents');evObj.initEvent( 'click', true, true );this.dispatchEvent(evObj);")
            time.sleep(0.2)
            self.step = 1
        if self.step == 1:
            t = self.web.page().mainFrame().toHtml()
            b = BeautifulSoup(unicode(t))
            li = b.findAll('li')
            data = {}
            for l in li:
                if u'Цена' in unicode(l):
                    self.price = filter(lambda x:x in "0123456789", l.getText())
                if u'Продавец' in unicode(l):
                    self.user = l.getText()
                if u'Город' in unicode(l):
                    self.city = l.getText()
                if u'Категория' in unicode(l):
                    self.catalog = l.getText()

a = None        
if __name__ == "__main__":
    # a = AviroParser('http://m.avito.ru/item/94859171')
    # print a.parse()
    # b = AviroParser('http://m.avito.ru/item/94859171')
    # print b.parse()
    
    # exit()
    import os
    os.putenv("DISPLAY", ":99")
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-p", "--port", dest="port",
                  help="port")
    
    (options, args) = parser.parse_args()
    
    #print options.port
    import zmq
    context = zmq.Context()
    p = context.socket(zmq.REQ)
    p.connect("tcp://127.0.0.1:%s" % options.port)
    p.send("Hi")
    data = p.recv_json()
    #print data
    if data.has_key('proxy'):
        a = AviroParser(data['url'], data['proxy'], data['proxyp'])
    else:
        a = AviroParser(data['url'])
    
    data2 = a.parse()
    p.send_json(data2)
    p.recv()
    
    """
    def avitoParse(url):
        a = AviroParser(url)
        data = a.parse()
        return data
    
    print avitoParse('http://m.avito.ru/item/100006995')
    for x in range(10):
        time.sleep(1)
        print x
        
    print avitoParse('http://m.avito.ru/item/100009739')
    """
    
