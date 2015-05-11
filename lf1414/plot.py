'''

plot.py

Author: Lily Fung
Date: May 10, 2015
NYU - DS-1007: Programming for Data Science

This program plots the results of the analysis in a visual way using bokeh plotting,
and its hovertool capabilities to display address, possible residential units, and score
based on proximity to desirable features (school, hospital, transit).

'''


import analysis
import data

import sys
import numpy
from collections import OrderedDict
from bokeh.plotting import *
from bokeh.objects import HoverTool


def plot_all():

	output_file("brooklyn_lots.html", title="Brooklyn Vacant Lots for Residential Development")

	TOOLS="pan,wheel_zoom,box_zoom,reset,hover,previewsave"


	figure(title = "Brooklyn Lots for Residential Development")

	def plot_brooklyn():
		all_lots_x = data.all_brooklyn_lots['XCoord']
		all_lots_y = data.all_brooklyn_lots['YCoord']

		circle(all_lots_x, all_lots_y,
    	    color='silver', fill_alpha=0.2, size=1)

	source = ColumnDataSource(data=dict(
		Address=analysis.vacant_lots['Address'], 
		Score=analysis.vacant_lots['Score'],
		Max_Units=analysis.vacant_lots['Resid_Units'],
		Nearest_School=analysis.vacant_lots['Nearest_School'], 
		Nearest_Hospital=analysis.vacant_lots['Nearest_Hospital'], 
		Nearest_Transit=analysis.vacant_lots['Nearest_Transit']
    	)
  	)

	def plot_vacant_lots():

		all_vl_x = analysis.vacant_lots['XCoord']
		all_vl_y = analysis.vacant_lots['YCoord']

		square(all_vl_x, all_vl_y,
			color='green', fill_alpha=0.2, size=7, legend='Vacant Lot', source=source, tools=TOOLS, plot_width=1100, plot_height=1100,)

	def plot_schools():
		all_school_x = data.schools['XCoord']
		all_school_y = data.schools['YCoord']

		triangle(all_school_x, all_school_y,
			color='blue', fill_alpha=0.2, size=3, legend='Public School')

	def plot_hospitals():
		all_hosp_x = data.hospitals['XCoord']
		all_hosp_y = data.hospitals['YCoord']

		square_cross(all_hosp_x, all_hosp_y,
			color='red', fill_alpha=0.2, size=3, legend='Hospital')

	def plot_transit():
		all_trans_x = data.transit['XCoord']
		all_trans_y = data.transit['YCoord']

		diamond(all_trans_x, all_trans_y,
			color='purple', fill_alpha=1, size=3, legend='Transit Station')

	plot_vacant_lots()
	hold()
	plot_schools()
	hold()
	plot_hospitals()
	hold()
	plot_transit()

	hover = curplot().select(dict(type=HoverTool))

	hover.tooltips = OrderedDict([
		("Address", "@Address"), 
		("Possible Residential Units", "@Max_Units"),
		("Score", "@Score"), 
		("Nearest School (mi.)", "@Nearest_School"), 
		("Nearest Hospital (mi.)", "@Nearest_Hospital"), 
		("Nearest Transit Stop (mi.)", "@Nearest_Transit")])

	show()

if __name__ == '__main__':
	plot_all()