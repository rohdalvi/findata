import sqlite3
import os
import requests
import json
from alpha_vantage.timeseries import TimeSeries

#alpha vantage api key
API_KEY = 'QDV2O0R71QVANO46'

def databaseSetUp(filename):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+filename)
    cur = conn.cursor()
    return cur, conn

def getAVdata(symbol, interval):
    print("Fetching for " + symbol + " for every " + interval)

    base_url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={}&interval={}&apikey={}"  
    request_url = base_url.format(symbol, interval, API_KEY) 

    r = requests.get(request_url)
    data = r.text
    data_dict = json.loads(data)
    relevant_data_dict = data_dict['Time Series ' + '(' + interval + ')']

    return relevant_data_dict

def createDatabase(relevant_data_dict, cur, conn):
    cur.execute("DROP TABLE IF EXISTS stockData")
    cur.execute("CREATE TABLE stockData (time TEXT PRIMARY KEY, closingPrice FLOAT)")

    for time in relevant_data_dict:
        closingPrice = relevant_data_dict[time]['4. close']
        cur.execute("INSERT INTO stockData (time, closingPrice) VALUES (?,?)",(time, closingPrice))

    conn.commit()

def main():
    cur, conn = databaseSetUp('AVdata.db')
    data = getAVdata("AAPL", "60min")
    createDatabase(data, cur, conn)
    print("Finished!")

if __name__ == "__main__":
    main()

