#!/usr/bin/env python
import gae_utils as gae
import awl
import urllib2
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainHandler(gae.BaseHandler):
    def get(self):
        awl_id = self.request.get("awl_id")
        awl_domain = self.request.get("awl_domain")
        if awl_id and awl_domain:
            request_url = awl.getRequestUrl(awl_id, awl_domain)
            print 1
            print request_url
            try:
                response = urllib2.urlopen(request_url)
                items = awl.getList(response.read())
                self.set_template_value('items', items)
                self.generate('text/html', 'widget.html')
            except:
                self.generate('text/html', 'error.html')
        else:
            self.generate('text/html', 'error.html')

def main():
    application = webapp.WSGIApplication([
        ('/widgetbox', MainHandler),
        ],
        debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
      main()