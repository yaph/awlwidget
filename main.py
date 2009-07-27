#!/usr/bin/env python
# TODO use gae_utils.py to avoid code duplication and move templates to templates dir
import cgi
import os
import awl

from google.appengine.ext import webapp
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
  def get(self):

    self.response.headers['Content-Type'] = 'text/html'

    awl_url = self.request.get("awl_url")

    # workaround if amazon url contains parameters
    # would be better if url form widgetbox was urlencoded
    list_type = self.request.get("type")
    awl_id = self.request.get("id")

    if awl_url:
      request_url = awl.getRequestUrl(awl_url, list_type, awl_id)
      result = urlfetch.fetch(request_url)

      if 200 == result.status_code:
        items = awl.getList(result.content)

        template_values = {
          'items': items,
        }
      
        path = os.path.join(os.path.dirname(__file__), 'widget.html')
        self.response.out.write(template.render(path, template_values))
    
    else:
      path = os.path.join(os.path.dirname(__file__), 'error.html')
      self.response.out.write(template.render(path, {}))

application = webapp.WSGIApplication(
                                     [('/widgetbox', MainPage)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()