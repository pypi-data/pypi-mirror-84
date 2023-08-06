from bs4 import BeautifulSoup, Comment
from collections import Counter
import pyap, re

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

def parsePage(page,domain='', tojson=False):
    result = {}        
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
      result['contactlink'] = ([l for l in innerLinks if 'contact' in l or 'location' in l] + [''])[0]
      result['aboutlink'] = ([l for l in innerLinks if 'about' in l] + [''])[0]

    result['title'] = soup.find('title').text.replace('\n','').strip()
    result['email'] = ';'.join(re.findall(r'([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)', vis))
    result['phone'] = ';'.join(re.findall(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', vis))

    if addresses:
        result['Mainaddress'] = addresses[-1]
        result['addresses'] = addresses
    if tojson:
      if 'Mainaddress' in result:
        result['Mainaddress'] = str(result['Mainaddress'])
      if ['addresses'] in result:
        result['addresses'] = [str(a) for a in result['addresses']]
    return result