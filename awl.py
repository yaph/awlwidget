#!/usr/bin/env python
import re
import time
import base64
import hashlib
import hmac

import urlparse
from settings import *
from xml.dom import minidom

def getRequestUrl(awl_url, list_type, awl_id):
  # defaults
  if '' == awl_id:
    awl_id = SETTINGS_AWL_ID
  awl_tag = ''
  awl_domain = 'com'
  
  url_parts = urlparse.urlsplit(awl_url)
  host = url_parts.netloc
  path = url_parts.path
  query = url_parts.query

  if re.search('amazon\.', host) and path != '':
    host_parts = host.rsplit('.')
    awl_domain = host_parts.pop()
    
    if '' == list_type:
      pat_rewrite = re.compile('^/gp/registry/(?:wishlist/)?([^/&\?]+)')
      if pat_rewrite.search(path):
        m = pat_rewrite.search(path)
        awl_id = m.group(1)

  if 'com' == awl_domain:
    awl_tag = 'awlwidget-20'

  elif 'de' == awl_domain:
    awl_tag = 'awlwidget-21'

  request_url = 'http://ecs.amazonaws.'
  request_url += awl_domain
  request_url += '/onca/xml?Service=AWSECommerceService&Version=2005-03-23&Operation=ListLookup'
  request_url += '&SubscriptionId=0DP08TDRREQ2K9PN1GR2'
  if '' != awl_tag:
    request_url += '&AssociateTag=' + awl_tag
  request_url += '&ListId=' + awl_id + '&ListType=WishList&ResponseGroup=Large'
  
  return request_url

def getList(xml):
  dom = minidom.parseString(xml)
  items = []
  
  if dom.getElementsByTagName("Errors"):
    return 'error'

  for item in dom.getElementsByTagName("Item"):
    
    # product asin
    if len(item.getElementsByTagName("ASIN")):
      asin = getText(item.getElementsByTagName("ASIN")[0])
    else:
      asin = ''
    
    # product title
    if len(item.getElementsByTagName("Title")):
      title = getText(item.getElementsByTagName("Title")[0])
    else:
      title = ''
      
    # product url
    if len(item.getElementsByTagName("DetailPageURL")):
      url = getText(item.getElementsByTagName("DetailPageURL")[0])
    else:
      url = ''
    
    # product price
    if len(item.getElementsByTagName("FormattedPrice")):
      price = getText(item.getElementsByTagName("FormattedPrice")[0])
    else:
      price = ''
    
    # product image
    if len(item.getElementsByTagName("MediumImage")):
      medium_image = item.getElementsByTagName("MediumImage")[0];
      img_src = getText(medium_image.getElementsByTagName("URL")[0])
    elif (len(item.getElementsByTagName("SmallImage"))):
      small_image = item.getElementsByTagName("SmallImage")[0];
      img_src = getText(small_image.getElementsByTagName("URL")[0])
    elif (len(item.getElementsByTagName("LargeImage"))):
      large_image = item.getElementsByTagName("LargeImage")[0];
      img_src = getText(large_image.getElementsByTagName("URL")[0])
    else:
      img_src = ''

    items.append({'asin': asin,
                  'title': title,
                  'url': url,
                  'img_src': img_src,
                  'price': price,
                })

  dom.unlink()
  return items

def getText(node):
  for n in node.childNodes:
    if n.nodeType == node.TEXT_NODE:
      return n.data
  return None
