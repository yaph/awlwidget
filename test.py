#!/usr/bin/env python
import re

urls = ['http://www.amazon.com/gp/registry/wishlist/R0W5YU2DDZMQ?ewqewqdsafgerf',
        'http://www.amazon.com/gp/registry/3W21I9FROFNII&eqweqwe',
        'http://www.amazon.de/gp/registry/wishlist/3F103ORY69L40/ref=cm_wl_rlist_go']

for url in urls:
  m = re.search('www\.amazon.(.*?)/gp/registry/(?:wishlist/)?([^/&\?]+)', url)
  awl_domain = m.group(1)
  awl_id = m.group(2)
  print(url) + "\n"
  print(awl_domain) + "\n"
  print(awl_id) + "\n"