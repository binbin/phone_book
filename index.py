#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "libs"))

import cgi
import datetime


from google.appengine.ext.webapp import template

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db


from pinyin import PinYin 

import hashlib
import csv
import codecs


class Phone(db.Model):
  name = db.StringProperty()
  phone = db.IntegerProperty()
  department = db.StringProperty()
  department_pinyin = db.StringProperty()
  name_pinyin = db.StringProperty()
  hire_date = db.DateProperty()

class DownLoad(webapp.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'application/csv;charset=gbk'
    self.response.headers['Content-Disposition'] = 'attachment; filename=phonebook.csv'
    writer = csv.writer(self.response.out)
    
    phones = db.GqlQuery("SELECT * FROM Phone ORDER BY department_pinyin ASC ,name ASC")
    for phone in phones:
       # writer.write(codecs.BOM_UTF8) 
      writer.writerow([phone.name.encode('gbk'),phone.phone,phone.department.encode('gbk')])

class MainPage(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'templates','index.html')
    self.response.out.write(template.render(path,{}))
    # user = users.get_current_user()

    # if user:
    #   self.response.headers['Content-Type'] = 'text/plain'
    #   self.response.out.write('Hello, ' + user.nickname())
    # else:
    #   self.redirect(users.create_login_url(self.request.uri))
class DeleteUser(webapp.RequestHandler):
    def get(self):
      # key = cgi.escape(self.request.get("key"))
      path = os.path.join(os.path.dirname(__file__), 'templates','delete_success.html')

      key = self.request.get("key")
      Phone.get(key).delete()
      self.response.out.write('true')
      """try:
        key = self.request.get("key")
        Phone.get(key).delete()
        # self.redirect('/list?edit=yes')  
        # self.response.out.write(template.render(path,{'message':'已删除成功！'}))
        self.response.out.write('true')
      except Exception as e:
        # self.response.out.write(template.render(path,{'message':'用户不存在！'}))
        self.response.out.write('false')"""


class PhoneBookList(webapp.RequestHandler):

  def get(self):
    phones = db.GqlQuery("SELECT * FROM Phone ORDER BY department_pinyin ASC ,name ASC")  
    path = os.path.join(os.path.dirname(__file__), 'templates','list.html')

    m = False
    edit = self.request.get("edit")

    if edit:
      md5=hashlib.md5(edit).hexdigest()
      if md5 == '7348b2953e9f331671f0b9aa350d8fc7':
        m = True
    

    self.response.out.write(template.render(path,{'phones':phones,'edit':m}))

  def post(self):
    p = PinYin(dict_file=os.path.join(os.path.dirname(__file__), 'libs','pinyin','word.data'))
    p.load_word()

    phone = Phone()
    phone.name = cgi.escape(self.request.get("name"))
    phone.phone = int(cgi.escape(self.request.get("phone")))
    phone.department = cgi.escape(self.request.get("department"))
    phone.name_pinyin = ''.join(p.hanzi2pinyin(string=phone.name))
    phone.department_pinyin = ''.join(p.hanzi2pinyin(string=phone.department))
    phone.hire_date = datetime.datetime.now().date()
    phone.put()
    
    

    path = os.path.join(os.path.dirname(__file__), 'templates','success.html')
    self.response.out.write(template.render(path,{}))

    # self.redirect('/list')

    

    # self.response.out.write('<html><body>You wrote:<pre>')
    # self.response.out.write(''.join(p.hanzi2pinyin(string=phone.name)))
    # self.response.out.write('</pre></body></html>') 

application = webapp.WSGIApplication(
                                     [('/', MainPage),('/list', PhoneBookList),('/delete', DeleteUser),('/download', DownLoad)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()