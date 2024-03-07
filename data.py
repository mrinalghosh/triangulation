import requests
import os
import json
import logging


CURRENCY_FILE = 'currency.json'


def download_currencies() -> dict:
    url = 'https://openexchangerates.org/api/currencies.json'
    r = requests.get(url)
    return r.json()


def download(curr) -> dict:
    url = f'https://open.er-api.com/v6/latest/{curr}'
    r = requests.get(url)
    return r.json()['rates']  # NOTE: contains <curr>: 1


def save(data: dict, file):
    with open(file, 'w') as f:
        json.dump(data, f)
        logging.info(f'Wrote data to {file}')


def load(file):
    with open(file, 'r') as f:
        # NOTE: context manager acts as a 'finally' clause
        data = json.load(f)
        logging.info(f'Loaded data from {file}')
        return data


# clean data?

# process into graph-like structure?


if __name__ == '__main__':
    # setup logging
    logging.basicConfig()
    logging.root.setLevel(level=logging.INFO)

    # (down)load currency names
    if os.path.exists(CURRENCY_FILE):
        currencies = load(CURRENCY_FILE)
    else:
        currencies = download_currencies()
        save(currencies, CURRENCY_FILE)

    print(currencies)

    # print(download('USD'))
