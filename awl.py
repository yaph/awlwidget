#!/usr/bin/env python
import re
import time
import base64
import hashlib
import hmac

import urlparse
from settings import *
from urllib import urlencode
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

  host = 'ecs.amazonaws.' + awl_domain
  base_url = 'http://' + host + '/onca/xml'
  
  url_params = {'Operation':'ListLookup',
                'Service':'AWSECommerceService',
                'AWSAccessKeyId':SETTINGS_AWS_ACCESS_KEY_ID,
                'ListId':awl_id,
                'ListType':'WishList',
                'ResponseGroup':'Large',
                'Version':'2006-09-11'}
  
  if '' != awl_tag:
    url_params['AssociateTag'] = awl_tag
  
  # Request signing code from http://cloudcarpenters.com/blog/amazon_products_api_request_signing/
  # Add a ISO 8601 compliant timestamp (in GMT)
  url_params['Timestamp'] = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
  
  # Sort the URL parameters by key
  keys = url_params.keys()
  keys.sort()
  # Get the values in the same order of the sorted keys
  values = map(url_params.get, keys)
  
  # Reconstruct the URL paramters and encode them
  url_string = urlencode(zip(keys,values))
  url_string = url_string.replace('+'," ")
  url_string = url_string.replace(':',":")
  
  #Construct the string to sign
  string_to_sign = "GET\n%(host)s\n/onca/xml\n%(url_string)s" % {'host':host,'url_string':url_string}

  # Sign the request
  signature = hmac.new(key=SETTINGS_AWS_SECRET_ACCESS_KEY,
                       msg=string_to_sign,
                       digestmod=hashlib.sha256).digest()
  # Base64 encode the signature
  signature = base64.encodestring(signature)
  
  # Make the signature URL safe
  signature = signature.replace('+','+')
  signature = signature.replace('=','=')
  url_string += "&Signature;=%s" % signature
  
  request_url = base_url + '?%s' % url_string

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