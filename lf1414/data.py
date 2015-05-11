'''

data.py

Author: Lily Fung
Date: May 10, 2015
NYU - DS-1007: Programming for Data Science

This program acts as a package which reads the data from the Excel files and loads them as dataframes.
NYC Department of City Planning PLUTO
Source: http://www.nyc.gov/html/dcp/html/bytes/applbyte.shtml

Available Datasets:
- all_brooklyn_lots
- vacant_lots
- schools
- hospitals
- transit

'''

import pandas as p
import numpy as np
import sys


'''Pandas Dataframe: all_brooklyn_lots'''
#Create global variable dataframe: all_brooklyn_lots
try:
	all_brooklyn_lots = p.read_csv('brooklyn_taxable_lots.csv')
except:
	print "Error: brooklyn_taxable_lots.csv was not found. Please make sure this file has been downloaded."

#Drop all unnecessary columns
try:
	all_brooklyn_lots = all_brooklyn_lots[['BBL', 'BldgClass', 'LotArea', 'ResidFAR', 'Address','XCoord', 'YCoord']]
except:
	print "Error: Corrupt data. Please re-download the data."

'''Pandas Dataframe: vacant_lots'''
try:
	vacant_lots = p.read_csv('vacant_lots.csv')
	vacant_lots = vacant_lots.set_index(['Unnamed: 0'])
except:
#Truncates all_brooklyn_lots to dataframe vacant_lots, for vacant lots where zoning allows for residential units.
#Vacant lots are any lots where building class is V1, V2, V3, V9 because they will be most easily acquired for residential development purposes.
	vacant_lots = all_brooklyn_lots.loc[(all_brooklyn_lots['BldgClass'].isin(['V1', 'V2', 'V3', 'V9']))]
#Vacant lots where residential units could possibly be built on must have Residential FAR
	vacant_lots = vacant_lots.loc[vacant_lots['ResidFAR'] > 0]
#Drop all rows with missing values
	vacant_lots = (vacant_lots.dropna()).reset_index()
	vacant_lots.to_csv('vacant_lots.csv')


'''Pands Dataframe: schools'''
try:
	schools = p.read_csv('schools.csv')
	schools = schools.set_index('Unnamed: 0')
except:
#Truncates all_brooklyn_lots to dataframe schools, for public schools.
	schools = all_brooklyn_lots[(all_brooklyn_lots['BldgClass'] == 'W1')]
	schools = schools[['BBL', 'Address', 'XCoord', 'YCoord']]
	schools = schools.reset_index()
	schools.to_csv('schools.csv')

'''Pandas Dataframe: hospitals'''
try:
	hospitals = p.read_csv('hospitals.csv')
	hospitals = hospitals.set_index('Unnamed: 0')
except:
#Truncates all_brooklyn_lots to dataframe vacant_lots, for vacant lots where zoning allows for residential units.
#Vacant lots are any lots where building class I1 through I9.
	hospitals = all_brooklyn_lots.loc[(all_brooklyn_lots['BldgClass'].isin(['I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8' 'I9']))]
	hospitals = hospitals[['BBL', 'Address', 'XCoord', 'YCoord']]
#Drop all rows with missing values
	hospitals = hospitals.dropna()
	hospitals = hospitals.reset_index()
	hospitals.to_csv('hospitals.csv')

'''Pandas Dataframe: transit'''
try:
	transit = p.read_csv('transit.csv')
	transit = transit.set_index('Unnamed:0')
except:
	transit = all_brooklyn_lots.loc[(all_brooklyn_lots['BldgClass'].isin(['U6', 'U7']))]
	transit = transit[['BBL', 'Address', 'XCoord', 'YCoord']]
	transit = transit.dropna()
	transit = transit.reset_index()
	transit.to_csv('transit.csv')

###Tests###

#print all_brooklyn_lots.head
# print list(all_brooklyn_lots.columns.values)
#print bldg_class_dict.head
# print list(bldg_class_dict.columns.values)
#print lirr_stations.head
# print list(lirr_stations.columns.values)
#print subway_stations.head
# print list(subway_stations.columns.values)
#print vacant_lots