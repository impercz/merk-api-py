# merk-api-py
Merk API Python client

## Installation

    pip install merk-api

## Usage

```python
from merkapi import Api

# by default client uses messagepack, but you can use less efficient json
a = Api('your_authentication_token', content_type='application/msgpack')

# get your subscriptions info (cz, sk)
r = a.subscriptions

# print returned dict
print(r.encdata)

# you can also access standard urllib3 response
print(r.data, r.status)

# implemented API calls

# suggest by 'regno', 'email' or 'name'
a.suggest(query, by, country_code)

# get full company data by regno
a.company(regno, country_code)

# multi get full company data
a.companies(regnos, country_code)

# get and cache enums
a.get_enums(country_code)
```

## Run tests

Client is tested in python 2.7 and 3.5. You can run tests in your environment:

    cd project/root
    py.test

or via tox:

    cd project/root
    tox
