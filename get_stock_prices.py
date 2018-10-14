import requests
import pandas as pd
import datetime
import os
import sys


def rest_api_call(URL, params):
    response = requests.get(URL, params=params)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # non-200 status code
        return "Error: " + str(e)
        sys.exit(1)

    json_data = response.json()
    if 'error' in json_data:
        print(json_data)
        sys.exit(1)
    return json_data


def get_stock_data(ticker, start_date, end_date):
    """
    Gets historical stock data of given tickers between dates from SimFin
    :param ticker: company, or companies whose data is to fetched
    :type ticker: string or list of strings
    :param start_date: starting date for stock prices
    :type start_date: string of date "YYYY-mm-dd"
    :param end_date: end date for stock prices
    :type end_date: string of date "YYYY-mm-dd"
    :return: stock_data.csv
    """
    i = 1
    api_key = os.getenv("APIKEY", "SDaO2kTUS2hlwWMXBVGc5HSI4Rb6GP6a")
    params = {"api-key": api_key}
    resp = rest_api_call('https://simfin.com/api/v1/info/find-id/ticker/'+ticker, params=params)
    company_id = resp[0]['simId']
    params = {"api-key": api_key, "start": start_date, "end": end_date}
    resp = rest_api_call('https://simfin.com/api/v1/companies/id/' + str(company_id) + '/shares/prices', params=params)
    prices = {datetime.datetime.strptime(item['date'], "%Y-%m-%d"): float(item['closeAdj']) for item in resp['priceData']}
    df = pd.DataFrame(list(prices.items()), columns=['date', 'closeAdj'])
    df.sort_values('date').to_csv("stock_prices.csv", header=False, index=False)


if __name__ == "__main__":
    start_date = (datetime.datetime.today()+datetime.timedelta(-90)).strftime('%Y-%m-%d')
    end_date = datetime.datetime.today().strftime('%Y-%m-%d')
    get_stock_data("AAPL", start_date, end_date)
    # get_snp500(start_date, end_Date)