# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Format Environmental Predictors
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Created on: 2018-06-06
# Usage: Must be executed as an ArcPy Script.
# Description: "Format Environmental Predictors" processes an input raster stack for use as predictive variables in a classification or regression model by extracting to the area of interest and matching the cell size and grid. This tool assumes that the input rasters are already in the desired projection for analysis and that all raster values can be represented as integers without significant data loss.
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import os
from arcpy.sa import *

# Set overwrite option
arcpy.env.overwriteOutput = True

# Define input rasters
input_rasters = arcpy.GetParameterAsText(0)

# Define the area of interest raster
area_of_interest = arcpy.GetParameterAsText(1)

#Define output folder
output_folder = arcpy.GetParameterAsText(2)

# Set the snap raster and cell size environments
arcpy.env.snapRaster = area_of_interest
arcpy.env.cellSize = area_of_interest

# Split input rasters string into a list
input_rasters = input_rasters.split(";")

# Create a function to format predictor rasters
def formatRaster(inRaster, extractMask, outRaster):
    # Convert input raster to integer
    arcpy.AddMessage("Enforcing integer number format...")
    integerRaster = Int(RoundDown(Raster(inRaster) + 0.5))
    # Extract projected raster to the area of interest
    arcpy.AddMessage("Extracting raster to area of interest...")
    outExtract = ExtractByMask(integerRaster, extractMask)
    # Copy results to outRaster
    arcpy.AddMessage("Preparing output raster...")
    arcpy.CopyRaster_management(outExtract, outRaster, "", "", "-32768", "NONE", "NONE", "16_BIT_SIGNED", "NONE", "NONE", "TIFF", "NONE")

# Iterate the format raster function for each raster selected as an input
for input_raster in input_rasters:
    output_raster = os.path.join(output_folder, os.path.split(input_raster)[1])
    formatRaster(input_raster, area_of_interest, output_raster)