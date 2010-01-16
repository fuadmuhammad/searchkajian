from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api.urlfetch_errors import *

from yos.yql import db
from yos.boss import ysearch

import os

class MainPage(webapp.RequestHandler):
  def get(self):
    try:
      query = self.request.get('q')
    except (TypeError,ValueError):
      query = 'nikah'
    rows = list()
    prev = None
    next = None
    if query != '':
	    try:
	      data = ysearch.search(query, more={'sites':'kajian.net,ilmoe.com,radiorodja.com,radiomuslim.com'})
	      results = db.create(data=data)
              rows = results.rows
              prev = data.prevpage
	      next = data.nextpage
            except (DownloadError):
	      pass
	    
	
    template_values = {
	'rows': rows,
	'query':query,
	'prev':prev,
	'next': next
    }
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))


application = webapp.WSGIApplication(
                                     [('/', MainPage)])

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
