# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Prepare Watershed Units
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Created on: 2018-06-27
# Usage: Must be executed as an ArcPy Script.
# Description: "Prepare watershed units" creates a unique feature class from the National Hydrography Dataset - Watershed Boundary Dataset for every 5th level hydrologic unit (watershed) within the area of interest and the predict area. The watershed units are pre-requisite to generating the prediction tables.
# ---------------------------------------------------------------------------

# Import modules
import os
import arcpy
import arcpy.da as da
import numpy as np
import pandas as pd
from arcpy.sa import *

# Set overwrite option
arcpy.env.overwriteOutput = True

# Define the input watershed feature class from the Watershed Boundary Dataset
watersheds =  arcpy.GetParameterAsText(0)

# Define the area of interest raster
area_of_interest = arcpy.GetParameterAsText(1)

# Define the predict area
predict_area = arcpy.GetParameterAsText(2)

# Define input rasters
input_rasters = arcpy.GetParameterAsText(3)

# Define the workspace folder
workspace_folder = arcpy.GetParameterAsText(4)

# Define workspace geodatabase
workspace_geodatabase = arcpy.GetParameterAsText(5)

# Define empty geodatabase to store output watershed point features
output_geodatabase = arcpy.GetParameterAsText(6)

# Define empty folder to store output watershed point csv files
output_folder = arcpy.GetParameterAsText(7)

# Split input rasters string into a list
input_rasters = input_rasters.split(";")

# Define intermediate files
predict_raster = os.path.join(workspace_folder, "predict_raster.tif")
predict_feature = os.path.join(workspace_geodatabase, "predict_feature")
watersheds_clip = os.path.join(workspace_geodatabase, "watersheds_clip")
tempRaster = os.path.join(workspace_folder, "temp_gridpoints.tif")

# Create a function to create point grids from polygon features
def buildPointGrids(inFeature):
    # Convert from polygon to raster and raster to point to create point grid
    arcpy.AddMessage("Building watershed point grid...")
    arcpy.PolygonToRaster_conversion(inFeature, "OBJECTID", tempRaster, "CELL_CENTER", "NONE", cell_size)
    # Delete input feature so that it can be replaced with point grid
    arcpy.Delete_management(inFeature)
    arcpy.RasterToPoint_conversion(tempRaster, inFeature, "VALUE")
    # Add XY Coordinates to feature class in the NAD_1983_Alaska_Albers projection
    arcpy.AddXY_management(inFeature)
    # Extract values of predictor variables to point grid
    arcpy.AddMessage("Extracting predictor variables to point grid...")
    ExtractMultiValuesToPoints(inFeature, input_rasters, "NONE")
    # Delete intermediate files
    arcpy.Delete_management(tempRaster)

# Create a function to convert a feature class to csv
def featureToCSV(inFeature, inColumns, outCSV):
    arcpy.AddMessage("Converting feature class to csv...")
    feature_array = da.FeatureClassToNumPyArray(inFeature, ["SHAPE@XY"] + inColumns)
    feature_df = pd.DataFrame(feature_array, columns = inColumns)
    feature_df.to_csv(outCSV, header=True, index=False, sep=',', encoding='utf-8')

# Set the snap raster and cell size environments
arcpy.env.snapRaster = area_of_interest
arcpy.env.cellSize = area_of_interest

# Extract area of interest to predict area
arcpy.AddMessage("Refining predict area based on area of interest...")
outExtract = ExtractByMask(area_of_interest, predict_area)
arcpy.CopyRaster_management(outExtract, predict_raster, "", "", "", "NONE", "NONE", "1_BIT", "NONE", "NONE", "TIFF", "NONE")
arcpy.RasterToPolygon_conversion(predict_raster, predict_feature, "NO_SIMPLIFY", "VALUE")

# Clip watersheds to the refined predict feature
arcpy.AddMessage("Clipping watersheds to refined predict area...")
arcpy.Clip_analysis(watersheds, predict_feature, watersheds_clip)

# Split watersheds by attribute and store as feature dataset
arcpy.AddMessage("Splitting unique watersheds into feature dataset...")
arcpy.SplitByAttributes_analysis(watersheds_clip, output_geodatabase, ['HUC10'])

# List all watershed feature classes in the 
arcpy.env.workspace = output_geodatabase
featureClasses = arcpy.ListFeatureClasses()

# Loop through feature classes and convert them to point grids with the same cell size and grid as the area of interest and the user input set of predictor variables
cell_size = arcpy.GetRasterProperties_management(area_of_interest, "CELLSIZEX")
for feature in featureClasses:
    feature = os.path.join(output_geodatabase, feature)
    output_csv = os.path.join(output_folder, feature + ".csv")
    buildPointGrids(feature)
    predictor_variables = ['compoundTopographic', 'dateFreeze_2000s', 'dateThaw_2000s', 'elevation', 'floodplainsDist', 'growingSeason_2000s', 'heatLoad', 'integratedMoisture', 'precipAnnual_2000s', 'roughness', 'siteExposure', 'slope', 'streamLargeDist', 'streamSmallDist', 'summerWarmth_2000s', 'surfaceArea', 'surfaceRelief', 'aspect', 'l8_evi2', 'l8_green', 'l8_nbr', 'l8_ndmi', 'l8_ndsi', 'l8_ndvi', 'l8_ndwi', 'l8_nearInfrared', 'l8_red', 'l8_shortInfrared1', 'l8_shortInfrared2', 'l8_ultrablue', 'l8_blue']
    coordinates = ['POINT_X', 'POINT_Y']
    all_variables = predictor_variables + coordinates
    featureToCSV(feature, all_variables, output_csv)

# Delete intermediate files
arcpy.Delete_management(predict_raster)
arcpy.Delete_management(predict_feature)
arcpy.Delete_management(watersheds_clip)