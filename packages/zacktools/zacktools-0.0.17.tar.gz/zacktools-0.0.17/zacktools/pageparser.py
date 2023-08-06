from bs4 import BeautifulSoup, Comment
from collections import Counter
import pyap, re, requests

def visiableText(page):
    soup = BeautifulSoup(page, 'lxml')
    comm = soup.findAll(text=lambda text:isinstance(text, Comment))
    [c.extract() for c in comm]
    alltags = soup.findAll(text=True)
    visable_tags = [t for t in alltags if t.parent.name not in 
                        ['style', 'script','script','img', 'head', 'title', 
                        'meta','link','footer','base','applet','iframe','embed',
                        'nodembed','object','param','source','[document]']]
    visible =  '\n'.join([re.sub(r'[\t/]+',' ', t) for t in visable_tags])
    visible = re.sub(r' +\n','\n', visible)
    visible = re.sub(r'\n+','\n', visible)
    return re.sub(r' +', ' ', visible)

def toDomain(link):
    return (re.sub(r'^(https?://)?(www\d?\.)?','', link).split('/')+[''])[0].strip()

def parse(page,domain='', tojson=False):
    result = {
              'title':'', 
              'contactLink':'', 
              'aboutLink':'', 
              'email':'',
              'phone':'',
              'mainAddress':'',
              'addresses':[],
              'facebook':'',
              'twitter':'',
              'instagram':'',
              'linkedin':''
              }        
    soup = BeautifulSoup(page,'lxml')
    vis = visiableText(page)
    addresses = pyap.parse(vis, country='CA')
    addresses += pyap.parse(vis, country='US')
    allLinks = [s.get('href') for s in soup.select('a[href]')]
    allLinks = [s for s in allLinks if 'javascript' not in s and 'void' not in s]
    if allLinks:
      for social in ['facebook', 'twitter', 'instagram','linkedin']:
        result[social] = ([l for l in allLinks if social in l]+[''])[0]
      if not domain:
        domain = Counter([toDomain(l) for l in allLinks]).most_common(1)[0][0]
      else:
        domain = toDomain(domain)

      innerLinks = [f'http://{domain}'+s if s.startswith('/') else s for s in allLinks if s.startswith('/') or domain in s]
      result['contactLink'] = ([l for l in innerLinks if 'contact' in l or 'location' in l] + [''])[0]
      result['aboutLink'] = ([l for l in innerLinks if 'about' in l] + [''])[0]

    result['title'] = soup.find('title').text.replace('\n','').strip() if soup.find('title') else ''
    result['email'] = ';'.join(re.findall(r'([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)', vis))
    result['phone'] = ';'.join(re.findall(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', vis))

    if not addresses and result['aboutLink']:
      try:
        res = requests.get(result['aboutLink'])
        resvis = visiableText(res.content)
        addresses = pyap.parse(resvis, country='CA')
        addresses += pyap.parse(resvis, country='US')
      except:
        pass

    if addresses:
        result['mainAddress'] = addresses[-1]
        result['addresses'] = addresses
    if tojson:
      if 'mainAddress' in result:
        result['mainAddress'] = str(result['mainAddress'])
      if 'addresses' in result:
        result['addresses'] = [str(a) for a in result['addresses']]
    return result
