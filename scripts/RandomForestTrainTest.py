# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Random Forest Binary Classification
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Created on: 2018-04-24
# Usage: Must be executed as an ArcPy Script.
# Description: This tool provides a Random Forest binary classification that runs from ArcGIS Pro.
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

try:
    from sklearn.ensemble import RandomForestClassifier
except:
    arcpy.AddError("This script requires that scikit-learn is installed in the ArcGIS Python Environment. Use conda to add scikit-learn and try again.")
	
# Set overwrite option
arcpy.env.overwriteOutput = True

# Define feature class of input classified points
train_points = r'SalixPulchra_Train_Clip'
test_points = r'SalixPulchra_Test_Clip'
watershed_points = r'Watershed_Test'
outDirectory = r'K:\VegetationEcology\NorthSlopeDataHarmonization\TestData'
outGeodatabase = r'K:\VegetationEcology\NorthSlopeDataHarmonization\Project_GIS\DataHarmonization_GIS.gdb'

# Define name of variable that contains the supervised classifications
#classification_variable = arcpy.GetParameterAsText(1)

# Define folder location of predictor rasters
#predictor_location = arcpy.GetParameterAsText(2)

# Define output geodatabase
#output_text_report = arcpy.GetParameterAsText(3)

# Define intermediate variables
predictor_variables = ['DateThaw', 'DistFloodplain', 'DistLargeLakes', 'DistLargeStreams', 'DistSmallLakes', 'DistSmallStreams', 'Elevation', 'Exposure', 'GroundTemp', 'GrowingSeason', 'LinearAspect', 'Moisture', 'OrganicThickness', 'OrganicWetness', 'PrecipFall', 'PrecipSpring', 'PrecipSummer', 'PrecipWinter', 'Roughness', 'SDF_September', 'Slope', 'SoilCarbon', 'TempFall', 'Wetlands', 'Wetness', 'ActiveLayer']
classification_variable = ['present']
coordinates = ['POINT_X', 'POINT_Y']
all_variables = predictor_variables + classification_variable + coordinates

# Convert input points into numpy array
train_array = da.FeatureClassToNumPyArray(train_points, ["SHAPE@XY"] + all_variables)
test_array = da.FeatureClassToNumPyArray(test_points, ["SHAPE@XY"] + all_variables)
watershed_array = da.FeatureClassToNumPyArray(watershed_points, ["SHAPE@XY"] + predictor_variables + coordinates)
spatial_reference = arcpy.Describe(train_points).spatialReference

# Convert numpy array to pandas data frame
train_data = pandas.DataFrame(train_array, columns = all_variables)
test_data = pandas.DataFrame(test_array, columns = all_variables)
watershed_data = pandas.DataFrame(watershed_array, columns = predictor_variables + coordinates)

# Calculate Pearson correlation coefficient between the predictor variables, where -1 is perfect negative correlation and 1 is perfect positive correlation
correlation = train_data.astype('float64').corr()

# Plot the correlation coefficients as correlation matrix and output as png
correlation_plot = seaborn.heatmap(correlation, cmap=seaborn.diverging_palette(220, 10, as_cmap = True),
square = True, annot = True, linecolor = 'k', linewidths = 1)
plot.xticks(rotation=90)
plot.yticks(rotation=0)
correlation_figure = correlation_plot.get_figure()
correlation_figure.savefig(os.path.join(outDirectory, 'correlation_plot.png'))

# Fit a random forest classifier to the training set
random_forest = RandomForestClassifier(n_estimators = 5000, oob_score = True)
random_forest.fit(train_data[predictor_variables], train_data[classification_variable[0]])

# Use the random forest classifier to predict the test set
train_prediction = random_forest.predict(train_data[predictor_variables])
test_prediction = random_forest.predict(test_data[predictor_variables])
watershed_prediction = random_forest.predict(watershed_data[predictor_variables])

# Concatenate predictions to original data frame
train_data_predicted = pandas.concat([train_data, pandas.DataFrame(train_prediction)], axis=1)
test_data_predicted = pandas.concat([test_data, pandas.DataFrame(test_prediction)], axis=1)
watershed_data_predicted = pandas.concat([watershed_data, pandas.DataFrame(watershed_prediction)], axis=1)
watershed_data_predicted

# Export data frame to excel
train_data_predicted.to_excel(os.path.join(outDirectory, 'train.xls'))
test_data_predicted.to_excel(os.path.join(outDirectory, 'test.xls'))
watershed_data_predicted.to_csv(os.path.join(outDirectory, 'watershed.csv'), header=False, index=False, sep=',', encoding='utf-8')

# Set intermediate variables
watershed_csv = "K:\\VegetationEcology\\NorthSlopeDataHarmonization\\TestData\\watershed.csv"
watershed_Layer = "watershed_Layer"
watershed_points_predicted = "K:\\VegetationEcology\\NorthSlopeDataHarmonization\\Project_GIS\\DataHarmonization_GIS.gdb\\watershed_points_predicted"
watershed_raster_predicted = "K:\\VegetationEcology\\NorthSlopeDataHarmonization\\Project_GIS\\DataHarmonization_GIS.gdb\\watershed_raster_predicted"

# Process: Make XY Event Layer
arcpy.MakeXYEventLayer_management(watershed_csv, "Field27", "Field28", watershed_Layer, "PROJCS['NAD_1983_Alaska_Albers',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Albers'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-154.0],PARAMETER['Standard_Parallel_1',55.0],PARAMETER['Standard_Parallel_2',65.0],PARAMETER['Latitude_Of_Origin',50.0],UNIT['Meter',1.0]];-13752200 -8948200 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision", "")

# Process: Copy Features
arcpy.CopyFeatures_management(watershed_Layer, watershed_points_predicted, "", "0", "0", "0")

# Process: Point to Raster
tempEnvironment0 = arcpy.env.snapRaster
arcpy.env.snapRaster = "K:\\VegetationEcology\\NorthSlopeDataHarmonization\\Project_GIS\\DataHarmonization_GIS.gdb\\Watershed_Test_Raster"
arcpy.PointToRaster_conversion(watershed_points_predicted, "Field29", watershed_raster_predicted, "MOST_FREQUENT", "NONE", "60")
arcpy.env.snapRaster = tempEnvironment0