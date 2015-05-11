'''

analysis.py

Author: Lily Fung
Date: May 10, 2015
NYU - DS-1007: Programming for Data Science

This program analyzes the datasets, with functions to calculate number of
possible residential units that can be built on a site and gives a score based
on distance to nearest school or hospital.

Issues: Distance to nearest subway station proved to be difficult because the data was in UTM
latitude and longitude, but the PLUTO taxable lots data X and Y coordinates are in New York -
Long Island State Plane. To the best extent possible, the PLUTO data has some information on lots designated
as railroad and transportation, and we will use that as an approximation for distance to nearest transit.

importable variables:
- vacant_lots
importable functions:
- calc_pot_res_units()
- calc_nearest()
- score()

'''

import numpy as np

from data import vacant_lots
from data import schools
from data import hospitals
from data import transit


'''Calculating Total Number of Possible Residential Units to be Built'''
def calc_pot_res_units():
	### Defining one potential residential unit for 2 people max as 400 sf
	sf_per_unit = 400

	#ResidFAR = how many Floor-Area-Ratios can be residential. Therefore, possible residential
	# sf = lotArea*ResidFAR
	resid_units = vacant_lots.LotArea * vacant_lots.ResidFAR
	vacant_lots['Resid_Units'] = resid_units/sf_per_unit
	return vacant_lots


# This function takes a 'row' from vacant_lot dataframe, and a feature dataframe set.
# Acceptable features = schools, hospitals, lirr stations, subway stations
def nearest(lot, feature):
# Distance is in feet, conversion factor: 1 mile = 5280 feet
	feature['Distance'] = ((feature.XCoord - lot['XCoord'])**2 + (feature.YCoord - lot['YCoord'])**2).apply(np.sqrt)/5280
	return feature['Distance'].min()


'''Calculating/Adding Nearest_School, Nearest_Hospital, Nearest_Subway Distance to Vacant Lots Data Frame'''
'''Done all in one function to iterate only once across dataframe'''
def calc_nearest():
	nearest_school_distance = []
	nearest_hospital_distance = []
	nearest_transit_distance = []

	for index, row in vacant_lots.iterrows():
	
		row['Nearest_School'] = round(nearest(row, schools),2)
		nearest_school_distance.append(row['Nearest_School'])

		row['Nearest_Hospital'] = round(nearest(row, hospitals),2)
		nearest_hospital_distance.append(row['Nearest_Hospital'])

		row['Nearest_Transit'] = round(nearest(row, transit),2)
		nearest_transit_distance.append(row['Nearest_Transit'])

	vacant_lots['Nearest_School'] = nearest_school_distance
	vacant_lots['Nearest_Hospital'] = nearest_hospital_distance
	vacant_lots['Nearest_Transit'] = nearest_transit_distance

	return vacant_lots

#Score takes into account the nearest-distances and assigns a score 0 to 100 based on
#proximity to desirable features. 
def score():
	score_list = []
	best_school_dist = vacant_lots['Nearest_School'].min()
	best_hosp_dist = vacant_lots['Nearest_Hospital'].min()
	best_trans_dist = vacant_lots['Nearest_Transit'].min()

	for index, row in vacant_lots.iterrows():

		if row['Nearest_School'] == 0:
			school_score = 100
		else:
			school_score = best_school_dist/row['Nearest_School']*100

		if row['Nearest_Hospital'] == 0:
			hosp_score = 100
		else:
			hosp_score = best_hosp_dist/row['Nearest_Hospital']*100

		if row['Nearest_Transit'] == 0:
			trans_score = 100
		else:
			trans_score = best_trans_dist/row['Nearest_Transit']*100

		# Score is computed simply as sum of the scores calculated above
		score = round((school_score+hosp_score+trans_score)/1.222,1)
		# this scalar 1.11466765248 is based on the top resulting score possible calculated
		# meant to normalize scores to 100 as max.
		row['Score'] = score
		score_list.append(row['Score'])

	vacant_lots['Score'] = score_list

def std_score():
	score_by_std = []
	school_mean = vacant_lots['Nearest_School'].mean()
	school_std = vacant_lots['Nearest_School'].std()

	hosp_mean = vacant_lots['Nearest_Hospital'].mean()
	hosp_std = vacant_lots['Nearest_Hospital'].std()

	trans_mean = vacant_lots['Nearest_Transit'].mean()
	trans_std = vacant_lots['Nearest_Transit'].std()

	for index, row in vacant_lots.iterrows():
		school_score = -1/((row['Nearest_School'] - school_mean)/school_std)
		hosp_score = -1/((row['Nearest_Hospital'] - hosp_mean)/hosp_std)
		trans_score = -1/((row['Nearest_Transit'] - trans_mean)/trans_std)
		score_tot = school_score+hosp_score+trans_score
		score_by_std.append(score_tot)

	vacant_lots['Score_by_STD'] = score_by_std

def produce_csv():
	vacant_lots.to_csv('vacant_lots_analysis.csv')

### Tests ###
# print vacant_lots
calc_pot_res_units()
calc_nearest()
score()
# print vacant_lots['Score'].max(), vacant_lots['Score'].min()
# print vacant_lots