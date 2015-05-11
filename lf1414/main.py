'''

BROOKLYN VACANT LOTS FOR RESIDENTIAL DEVELOPMENT PROJECT

main.py

Author: Lily Fung
Date: May 10, 2015
NYU - DS-1007: Programming for Data Science

This program was written as a final project for DS-1007 Spring 2015.
It takes PLUTO data from the NYC Department of City Planning and breaks it down to identify
vacant lots which are possibly zoned for residential development.
It does quality analysis to calculate:
- Number of possible residential units that can be built based on lot size and zoning;
- Proximity to nearest public school
- Proximity to nearest hospital/clinic
- Proximity to nearest transit

Notes:
The plotting relies on bokeh package. The installation instructions can be found
here if not already installed:
http://bokeh.pydata.org/en/latest/docs/installation.html

Modules:

data.py - reads and unloads the data, preparing it for analysis
importable variables:
- all_brooklyn_lots
- vacant_lots
- schools
- hospitals
- transit

analysis.py - does the calculations and appends new columns to the main data set
importable variables:
- vacant_lots
importable functions:
- calc_pot_res_units()
- calc_nearest()
- score()
- produce_csv()

plot.py - plots the analyzed dataframe using bokeh, which has capabilities and usage
similar to matplotlib, but with the addition of extra tools
importable functions:
- plot_all()

'''

import data
import analysis
import plot

if __name__ == '__main__':
	analysis.calc_pot_res_units()
	analysis.calc_nearest()
	analysis.score()
	analysis.produce_csv()
	plot.plot_all()