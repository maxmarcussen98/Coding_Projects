import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import gzip
import json
import gzip


def parse(path): 
	g = gzip.open(path, 'rb') 
	for l in g: 
		yield eval(l) 

def getDF(path): 
	i = 0 
	df = {} 
	for d in parse(path): 
		df[i] = d 
		i += 1 
	return pd.DataFrame.from_dict(df, orient='index')


def get_meta_DF(path): 
	i = 0 
	df = {} 
	for d in parse(path): 
		df[i] = d 
		i += 1 	
#	df = pd.DataFrame.from_dict(df, orient='index').dropna()
	return pd.DataFrame.from_dict(df, orient='index')


def product_tseries(df, asin, density=False):
	one_product = df[df['asin'] == asin]
	years = []
	for t in one_product["reviewTime"]:
		time = int(t[-4:])
		years.append(time)
	start, end = min(years), max(years)
	plt.hist(years, bins=range(start, end), density=density)
	plt.show()

def month_distribution(df):
	grouped = df.groupby('asin')
	review_dict = {}
	for product, review_df in grouped:
		review_dict[product] = 12 * [0]
		for time_string in review_df['reviewTime']:
			month = int(time_string[:2].lstrip('0'))
			review_dict[product][month - 1] += 1
	return review_dict

def quarterly_distribution(df):
	grouped = df.groupby('asin')
	review_dict = {}
	for product, review_df in grouped:
		review_dict[product] = 4 * [0]
		for time_string in review_df['reviewTime']:
			month = int(time_string[:2].lstrip('0'))
			if month < 4:
				review_dict[product][0] += 1
			if (month > 3) and (month < 7):	
				review_dict[product][1] += 1
			if (month > 6) and (month < 10):	
				review_dict[product][2] += 1
			if (month > 9) and (month < 13):	
				review_dict[product][3] += 1
	return review_dict
