## Python client for Barchart OnDemand

Get access to market data and the OnDemand APIs in just a few lines of code.

### Installation

#### From pypi

```
pip install ondemand
```

#### From Source

```
python setup.py install
```

### Usage

```python
import ondemand

od = ondemand.OnDemandClient(api_key='CHANGE_ME')

# or if you are using a free sandbox API

od = ondemand.OnDemandClient(api_key='CHANGE_ME', end_point='https://marketdata.websol.barchart.com/')

# if you want data in a format other than json. xml also supported

od = ondemand.OnDemandClient(api_key='CHANGE_ME', format='csv')

# get quote data for Apple and Microsoft
quotes = od.quote('AAPL,MSFT')['results']

for q in quotes:
    print('Symbol: %s, Last Price: %s' % (q['symbol'], q['lastPrice']))

# get 1 minutes bars for Apple
resp = od.history('AAPL', 'minutes', maxRecords=50, interval=1)

# generic request by API name
resp = od.get('getQuote', symbols='AAPL,EXC', fields='bid,ask')

# or, get the crypto
resp = od.crypto('^BTCUSD,^LTCUSD')
```

### Interactive Python Notebook Example

https://colab.research.google.com/drive/1D8389Q8qQzbppqFxwpUOobheZ2jb3Gp4

### Version

- 1.0 - 7/27/2017 -- init
