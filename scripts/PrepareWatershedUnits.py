# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Prepare Watershed Units
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Created on: 2018-06-27
# Usage: Must be executed as an ArcPy Script.
# Description: "Prepare watershed units" creates a unique feature class from the National Hydrography Dataset - Watershed Boundary Dataset for every 5th level hydrologic unit (watershed) within the area of interest and the predict area. The watershed units are pre-requisite to generating the prediction tables.
# ---------------------------------------------------------------------------

# Import modules
import arcpy
import os
from arcpy.sa import *

# Set overwrite option
arcpy.env.overwriteOutput = True

# Define the input watershed feature class from the Watershed Boundary Dataset
watersheds = arcpy.GetParameterAsText(0)

# Define the area of interest raster
area_of_interest = arcpy.GetParameterAsText(1)

# Define the predict area
predict_area = arcpy.GetParameterAsText(2)

# Define user-specified merge distance
merge_distance = arcpy.GetParameterAsText(3)

# Define the workspace folder
work_folder = arcpy.GetParameterAsText(4)

# Define empty geodatabase to store output watershed point features
output_geodatabase = arcpy.GetParameterAsText(5)

# Define intermediate files
predict_raster = os.path.join(work_folder, "predict_raster.tif")
predict_feature = os.path.join(output_geodatabase, "predict_feature")
watersheds_clip = os.path.join(output_geodatabase, "watersheds_clip")

# Create a function to create point grids from polygon features
def buildPointGrids(inFeature, outFeature)
    tempRaster = os.path.join(work_folder, "temp_gridpoints.tif")
    cell_size = arcpy.GetRasterProperties_management(area_of_interest, "CELLSIZEX")
    arcpy.PolygonToRaster_conversion(inFeature, "OBJECTID", tempRaster, "CELL_CENTER", "NONE", cell_size)
    arcpy.RasterToPoint_conversion(tempRaster, outFeature, "VALUE")
    arcpy.Delete_management(tempRaster)

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
arcpy.SplitByAttributes_analysis(watersheds_clip, output_workspace, ['HUC10'])

# List all watershed feature classes in the 
arcpy.env.workspace = output_geodatabase
featureClasses = arcpy.ListFeatureClasses()

# Loop through feature classes and convert them to rasters with the same cell size and grid as the area of interest
for feature in featureClasses:
    point_feature = feature + "_pointGrid"
    buildPointGrids(feature, point_feature)

# Delete intermediate files
arcpy.Delete_management(predict_raster)
arcpy.Delete_management(predict_feature)
arcpy.Delete_management(watersheds_clip)