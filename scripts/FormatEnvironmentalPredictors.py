# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Format Environmental Predictors
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Created on: 2018-06-06
# Usage: Must be executed as an ArcPy Script.
# Description: "Format Environmental Predictors" processes an input raster stack for use as predictive variables in a classification or regression model by extracting to the area of interest and matching the cell size and grid. This tool assumes that the input rasters are already in the desired projection for analysis.
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy, os
from arcpy.sa import *

# Set overwrite option
arcpy.env.overwriteOutput = True

# Define input raster
input_rasters = arcpy.GetParameterAsText(0)

# Define area of interest
area_of_interest = arcpy.GetParameterAsText(1)

# Define resampling technique
data_type = arcpy.GetParameterAsText(2)

#Define output folder
output_folder = arcpy.GetParameterAsText(3)

# Determine cell size of Area of Interest
cell_size = arcpy.GetRasterProperties_management(area_of_interest, "CELLSIZEX")

# Set the snap raster environment
arcpy.env.snapRaster = area_of_interest

# Split input rasters string into a list
input_rasters = input_rasters.split(";")

# Create a function to format predictor rasters
def formatRaster(inRaster, outRaster):
    # Extract projected raster to the area of interest
    arcpy.AddMessage("Extracting raster to area of interest...")
    outExtract = ExtractByMask(inRaster, area_of_interest)
    arcpy.AddMessage("Preparing output raster...")
    if data_type == "Continuous":
        arcpy.CopyRaster_management(outExtract, outRaster, "", "", "", "NONE", "NONE", "32_BIT_FLOAT", "NONE", "NONE")
    elif data_type == "Discrete":
        arcpy.CopyRaster_management(outExtract, outRaster, "", "", "", "NONE", "NONE", "16_BIT_SIGNED", "NONE", "NONE")

# Iterate the format raster function for each raster selected as an input
for input_raster in input_rasters:
    filename = os.path.split(input_raster)[1]
    output_raster = os.path.join(output_folder, filename)
    formatRaster(input_raster, output_raster)