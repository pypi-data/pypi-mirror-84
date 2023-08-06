# zacktools

### Useful tools created by zackdai

# install
`pip install zacktools`

or from git

`pip3 install git+https://github.com/ZackAnalysis/zacktools.git`

## pageparser

A tool for parse address,phone, email, facebook, twitter, linkedin, contact link, about us link from a webpage

### usage

`from zacktools import pageparser`

`import requests`

`res = requests.get('http://rel8ed.to')`

`result = pageparser.parse(res.content)`

`print(result)`

Note: MainAddress is an Object, and can be further extacted like:

print(result['Mainaddress'].city)

If want to convert to json directly, add parameters tojson=True

result = pageparser.parse(res.content, tojson=True)

