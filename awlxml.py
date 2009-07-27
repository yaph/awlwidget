#!/usr/bin/env python
import re
from xml.dom import minidom

def getRequestUrl(awl_url):
  m = re.search('www\.amazon.(.*?)/gp/registry/(?:wishlist/)?([^/&\?]+)', awl_url)
  awl_domain = m.group(1)
  awl_id = m.group(2)

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
    asin = getText(item.getElementsByTagName("ASIN")[0])
    title = getText(item.getElementsByTagName("Title")[0])
    url = getText(item.getElementsByTagName("DetailPageURL")[0])
    price = getText(item.getElementsByTagName("FormattedPrice")[0])
        
    medium_image = item.getElementsByTagName("MediumImage")[0];
    img_src = getText(medium_image.getElementsByTagName("URL")[0])
        
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