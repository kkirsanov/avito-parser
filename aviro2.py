# coding=utf8
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

class AviroGrabber():
    def __init__(self, url):
        self.tmp = tempfile.mkstemp()
        self.url = url
        self.step = 0
        self.place = ""
        self.type = ""
        self.debug = True  # False
        self.deadline = 30
        self.app = QApplication(sys.argv)
        self.web = QWebView()
        self.web.loadFinished.connect(self.onDone)
        self.web.loadProgress.connect(self.percent)
    def stop(self):
        if self.debug:
            print "timeout"
        self.app.exit()
    def parse(self):
        self.web.load(QUrl(self.url))
        
        if self.debug:
            self.web.show()
        
        QTimer.singleShot(self.deadline * 1000, self.stop)
        self.app.exec_()

        data = ['tesseract', self.tmp[1] + '.jpg', self.tmp[1], '-psm7']
        process = subprocess.Popen(data, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
        process.communicate()
        try:
            txt = open(self.tmp[1] + '.txt', "r")
            txt = "".join(txt.readlines())
            t1 = txt.replace("\n", "")
            t1 = txt.replace("o", "0")
            
            t1 = filter(lambda x:x in "0123456789", t1)
            if t1[0] == '5':
                t1 = '8' + t1[1:]
        
            os.unlink(self.tmp[1])
            os.unlink(self.tmp[1] + '.jpg')
            os.unlink(self.tmp[1] + '.txt')
            return dict(phone=t1,place=self.place, catalog=self.type)
        except Exception, e:
            print e
    def percent(self, p):
        # print p
        self.web.update()
        pass
    def searchCode(self):
        import random
        self.app.processEvents()
        width = 200
        for x in self.web.page().mainFrame().findAllElements('img'):
            if 'pkey' in x.attribute("src"):
                # time.sleep(0.1)
                geom = x.geometry()
                if geom.height() < 1:
                    print "wrongsize"
                    return
                size = QSize(geom.width(), geom.height())
                image = QImage(size, QImage.Format_ARGB32)
                paint = QPainter(image)
                x.render(paint)
                paint.end()
                image.save(self.tmp[1] + ".jpg", "JPG")
                self.app.exit()
        QTimer.singleShot(4000, self.searchCode)
    def onDone(self, val):
        self.searchCode()
        if self.step == 0:
            self.web.page().mainFrame().evaluateJavaScript(u"""
            if (typeof okNum === "undefined"){
                var okNum = -1;
                $('a.aj').each(function(index, para) {
                    if ($(para).html().indexOf("номер")>1)
                        okNum = para; 
                });
                $(okNum).click();
            };
            """);
            # time.sleep(0.2)
            self.step = 1
        if self.step == 1:
            if self.debug:
                print "step 2"
            self.place = self.web.page().mainFrame().findFirstElement("#map").toInnerXml().split(">")[1].split("<")[0]
            self.place=unicode(self.place)
            
            self.type=self.web.page().mainFrame().findFirstElement(".item_breadcrumbs").toPlainText()
            self.type=self.web.page().mainFrame().findFirstElement(".b_d_l").toPlainText().split(":")[-1]
            
            print self.type
            self.type=unicode(self.type)
            self.searchCode()
            
if __name__ == "__main__":
    a = AviroGrabber('http://www.avito.ru/moskva/planshety_i_elektronnye_knigi/acer_n311_98935350')
    print a.parse()
