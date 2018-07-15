# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Convert Predictions to Raster
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Created on: 2018-06-27
# Usage: Must be executed as an ArcPy Script.
# Description: "Convert Predictions to Raster" converts tables of contiguous gridded points with model outputs into a single raster with the cell size and grid equivalent to the area of interest raster. The value field should be set to the field containing the output predicted value of the model.
# ---------------------------------------------------------------------------

# Import modules
import arcpy
import os
from arcpy.sa import *

# Set overwrite option
arcpy.env.overwriteOutput = True

# Define the input tables that contain the watershed model predictions
input_tables = arcpy.GetParameterAsText(0)

# Define the area of interest raster
area_of_interest = arcpy.GetParameterAsText(1)

# Define the workspace geodatabase
workspace_geodatabase = arcpy.GetParameterAsText(2)

# Define output folder
output_folder = arcpy.GetParameterAsText(3)

# Split input tables string into a list
input_tables = input_tables.split(";")

# Determine spatial reference from area of interest
spatial_reference = arcpy.Describe(area_of_interest).spatialReference

# Set snap raster environment and determine cell size relative to area of interest
arcpy.env.snapRaster = area_of_interest
cell_size = arcpy.GetRasterProperties_management(area_of_interest, "CELLSIZEX")

# Create a function to convert the tabular data to raster
def csvToRaster(inCSV, spatial_reference, cell_size, outRaster):
    inLayer = "prediction_layer"
    predict_feature = os.path.join(workspace_geodatabase, "predict_feature")
    arcpy.MakeXYEventLayer_management(inCSV, "POINT_X", "POINT_Y", inLayer, spatial_reference, "")
    arcpy.CopyFeatures_management(inLayer, predict_feature, "", "0", "0", "0")
    arcpy.PointToRaster_conversion(predict_feature, "classification", outRaster, "MAXIMUM", "NONE", cell_size)
    arcpy.Delete_management(predict_feature)

# Run the csv to raster function for all input csv files
for csv in input_tables:
   filename = os.path.split(os.path.splitext(csv)[0])[1]
   output_raster = os.path.join(output_folder, filename + ".tif")
   csvToRaster(csv, spatial_reference, cell_size, output_raster)