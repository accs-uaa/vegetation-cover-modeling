# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Average Climate Data
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Created on: 2018-06-23
# Usage: Must be executed as an ArcPy Script.
# Description: "Average Climate Data" processes decadal average climate datasets to find the mean for multiple decades. No other formatting is performed by this tool.
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import os
from arcpy.sa import *

# Set overwrite option
arcpy.env.overwriteOutput = True

# Define input raster
input_rasters = arcpy.GetParameterAsText(0)

#Define output raster
output_raster = arcpy.GetParameterAsText(1)

# Split input rasters string into a list
input_rasters = input_rasters.split(";")

# Set the snap raster and cell size environments
arcpy.env.snapRaster = input_rasters[0]
arcpy.env.cellSize = input_rasters[0]

# Create a function for averaging the climate rasters
def averageClimate(inRasters, outRaster):
    # Set the raster sum initially equal to the first raster in the list
    arcpy.AddMessage("Summing input rasters...")
    rasterSum = Raster(inRasters[0])
    # Add the values of additional rasters in the list via a for loop
    for inRaster in inRasters[1:]:
        rasterSum += Raster(inRaster)
    # Find the mean of the raster sum and copy to output
    arcpy.AddMessage("Calculating mean of input rasters...")
    rasterMean = rasterSum/(len(inRasters))
    integerMean = Int(RoundDown(rasterMean + 0.5))
    arcpy.AddMessage("Copying results to output raster...")
    arcpy.CopyRaster_management(integerMean, outRaster, "", "", "-32768", "NONE", "NONE", "16_BIT_SIGNED", "NONE", "NONE", "TIFF", "NONE")

# Execute the average climate function for the input rasters
averageClimate(input_rasters, output_raster)