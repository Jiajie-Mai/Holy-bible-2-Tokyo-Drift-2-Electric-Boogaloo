import json
from urllib import request
from random import sample

#API for IEX Trading
#you need to get the stock and place it btwn stub and ender
IEXTRADING_TEST = "https://api.iextrading.com/1.0/stock/aapl/batch?types=quote,news,chart&range=1m&last=10"
IEX_STUB = "https://api.iextrading.com/1.0/"
IEX_ENDER = "/batch?types=quote&range=1m&last=10"
IEX_SYMBOLS = "ref-data/symbols"

#API for Random Dog Images
DOG_STUB = "https://dog.ceo/api/breeds/image/random"

# get json from api
def apiRetrieve(URL_STUB, URL_other):
    '''general api retrieval function'''
    URL=URL_STUB+URL_other
    response = request.urlopen(URL)
    s = response.read()
    d = json.loads(s.decode('utf-8'))
    return d

def randSymbols(n):
    '''returns a generator of n distinct random stock symbols, their names, and % change in price'''
    d = apiRetrieve(IEX_STUB, IEX_SYMBOLS)
    return ((i["symbol"],i["name"],priceChange(i["symbol"])) for i in sample(d,n))

def priceChange(sym):
    s = apiRetrieve(IEX_STUB + "stock/", sym + IEX_ENDER)
    return float(s["quote"]["changePercent"])*100

if __name__ == "__main__":
    for j in randSymbols(5):
        print(j)
        print(priceChange(j[0]))
