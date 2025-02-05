import TDA_auth

import pandas as pd
import requests
import os
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

client_id = TDA_auth.client_id
access_token = TDA_auth.access_token

''' milliseconds since epoch ''' 

def timestamp(dt):
	dt = pd.to_datetime(dt).to_pydatetime()
	epoch = datetime.utcfromtimestamp(0)
	return int((dt - epoch).total_seconds() * 1000.0) 	

''' set endDate to tomorrow's date to get today's candle too '''

endDate = datetime.today().date()
startDate = datetime.today().date() - relativedelta(years = 10)

def historical(symbol, startDate = startDate, endDate = endDate, ext = 'true'):
	resp = requests.get('https://api.tdameritrade.com/v1/marketdata/' + symbol + '/pricehistory',
						headers={'Authorization': 'Bearer ' + access_token},
						params={'apikey': client_id,
								'periodType': 'year',
								'period': 20,
								'frequencyType': 'daily',
								'frequency': 1,
								'endDate': timestamp(endDate),
								'startDate': timestamp(startDate), 
								'needExtendedHoursData': ext })
	print(resp.status_code)
	''' print(resp.json().keys())
	 	print(resp.json()['symbol'] == symbol) '''
	data = pd.DataFrame(resp.json()['candles'])
	data['datetime'] = pd.to_datetime(data['datetime'], unit = 'ms').dt.date
	return data


def search_instruments(proj, symbol):
	# posssible projections:
	# symbol-search			symbol ex: 'SPY'
	# symbol-regex					 : 'SPY.*'		
	# desc-search					 : 'FakeCompany'
	# desc-regex					 : 'XYZ.[A-C]'
	# fundamental					 : 'SPY'
	#
	resp = requests.get('https://api.tdameritrade.com/v1/instruments',
						headers={'Authorization': 'Bearer ' + access_token},
						params={'apikey': client_id,
								'symbol': symbol,
								'projection': proj})
	# print(resp.status_code)
	# print(resp.json().keys())
	return resp.json()

def quotes(symbol):
	resp = requests.get('https://api.tdameritrade.com/v1/marketdata/quotes',
						headers={'Authorization': 'Bearer ' + access_token},
						params={'apikey': client_id,
								'symbol': symbol})
	return resp.json()

def option_chain(symbol):
	resp = requests.get('https://api.tdameritrade.com/v1/marketdata/chains',
						headers={'Authorization': 'Bearer ' + access_token},
						params={'apikey': client_id,
								'symbol': symbol,
								'contractType': 'ALL',
								'strikeCount': 100,
								'includeQuotes': 'True',
								'strategy': 'SINGLE', 
									# 'ANALYTICAL'  
									# (allows use of the volatility, underlyingPrice, 
									# interestRate, and daysToExpiration params 
									# to calculate theoretical values)
									#
									# COVERED, VERTICAL, CALENDAR, 
									# STRANGLE, STRADDLE, BUTTERFLY, 
									# CONDOR, DIAGONAL, COLLAR, or ROLL. 
									# Default is SINGLE.}
								'interval': '', # Strike interval for spread strategy chains
								'strike': '', # Provide a strike price to return options only at that strike price.
								'range': 'ALL' ,
										# ITM: In-the-money
										# NTM: Near-the-money
										# OTM: Out-of-the-money
										# SAK: Strikes Above Market
										# SBK: Strikes Below Market
										# SNK: Strikes Near Market
										# ALL: All Strikes
								'fromDate': '',
								'toDate': '',
								'volatility': '',
								'underlyingPrice': '',
								'interestRate': '',
								'daysToExpiration': '',
								'expMonth': 'ALL', 
									# Return only options expiring in the specified month. 
									# Month is given in the three character format.
									# Example: JAN
								'optionType': 'ALL'})
									# Type of contracts to return. Possible values are:
									# S: Standard contracts
									# NS: Non-standard contracts
									# ALL: All contracts
	return resp.json()


def get_accounts(fields):
	resp = requests.get('https://api.tdameritrade.com/v1/accounts',
						headers={'Authorization': 'Bearer ' + access_token},
						params={'fields': fields})
	return resp.json()


