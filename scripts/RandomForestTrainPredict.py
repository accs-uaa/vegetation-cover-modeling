# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Train and Predict Random Forest Classification and Regression
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Created on: 2018-06-28
# Usage: Must be executed as an ArcPy Script.
# Description: "Train and Predict Random Forest Classification and Regression" creates separate classification and regression random forest models based on the full taxon dataset and then uses the models to iterate through predictions by watershed. The models are saved as external files for reuse. The watershed predictions are exported as csv files into a user-specified output location with names based on the 10-digit Hydrologic Unit Code (HUC). This tool must be run after the "Train and Test Random Forest Classification and Regression".
# ---------------------------------------------------------------------------

# Import modules
import os
import numpy as np
import arcpy
import arcpy.da as da
import pandas
import seaborn
import matplotlib.pyplot as plot
import arcgisscripting as arcscr
import SSUtilities as utils
import xlsxwriter
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib

# Set overwrite option
arcpy.env.overwriteOutput = True

# Define feature class of formatted cover data with the presence and cover of a single taxon or taxa aggregate
taxon_data = arcpy.GetParameterAsText(0)

# Define name of the variable that contains the presence-absence classification
classification_variable = arcpy.GetParameterAsText(1)

# Define name of the variable that contains the cover variable
cover_variable = arcpy.GetParameterAsText(2)

# Define list of predictor variables
predictor_variables = arcpy.GetParameterAsText(3)

# Define geodatabase that contains the watershed prediction units
watershed_geodatabase = arcpy.GetParameterAsText(4)

# Define prediction output folder
outDirectory = arcpy.GetParameterAsText(5)

# Define output classification model file
model_classification = arcpy.GetParameterAsText(6)

# Define output regression model file
model_regression = arcpy.GetParameterAsText(7)

# Define intermediate variables
predictor_variables = [ENTER LIST OF PREDICTOR VARIABLES]
coordinates = ['POINT_X', 'POINT_Y']
all_variables = predictor_variables + classification_variable + cover_variable + coordinates
watershed_variables = predictor_variables + coordinates

# Create a function to import feature class into pandas dataframe
def featureDataFrame(inFeature, variables, outArray, outDataFrame):
    outArray = da.FeatureClassToNumPyArray(inFeature, ["SHAPE@XY"] + variables)
	outDataFrame = pandas.DataFrame(outArray, columns = variables)

# Create a function to convert watershed points into pandas data frames, run predictions, and export as tables
def predictWatershed(inDataFrame, classificationModel, regressionModel, outTable):
	# Predict the data using the classification model and concatenate to original data frame
	classPredict = classificationModel.predict(inDataFrame[predictor_variables])
	inDataFrame = pandas.concat([inDataFrame, pandas.DataFrame(classPredict).rename('presence')], axis=1)
	# Predict the data using the regression model and concatenate to original data frame
	regressPredict = regressionModel.predict(inDataFrame[predictor_variables])
	inDataFrame = pandas.concat([inDataFrame, pandas.DataFrame(regressPredict).rename('cover')], axis=1)
	# Export watershed data frame to csv table
	inDataFrame.to_csv(outTable, header=False, index=False, sep=',', encoding='utf-8')

# Convert input taxon points into pandas data frame
featureDataFrame(taxon_data, all_variables, taxon_array, taxon_dataFrame)

# Fit a random forest classifier to the taxon presence data and save the model
rfClass = RandomForestClassifier(n_estimators = 5000, oob_score = True)
rfClass.fit(taxon_dataFrame[predictor_variables], taxon_dataFrame[classification_variable['presence']])
joblib.dump(rfClass, model_classification)

# Fit a random forest regressior to the taxon cover data and save the model
rfRegress = RandomForestRegressor(n_estimators = 5000, oob_score = True)
rfRegress.fit(taxon_dataFrame[predictor_variables], taxon_dataFrame[classification_variable['cover']])
joblib.dump(rfRegress, model_regression)

# Iterate "feature to data frame" and "predict watershed" functions for all watersheds
arcpy.env.workspace = watershed_geodatabase
watershedFeatures = arcpy.ListFeatureClasses()
for watershed in watershedFeatures:
    featureDataFrame(watershed, watershed_variables, watershed_array, watershed_dataFrame)
	filename = os.path.split(watershed)[1] + ".csv"
	watershed_table = os.path.join(outDirectory, filename)
	predictWatershed(watershed_dataFrame, rfClass, rfRegress, watershed_table)