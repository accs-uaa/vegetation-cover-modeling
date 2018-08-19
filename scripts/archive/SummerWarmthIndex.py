# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Summer Warmth Index
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Created on: 2018-06-23
# Usage: Must be executed as an ArcPy Script.
# Description: "Summer Warmth Index" processes decadal average mean monthly temperature datasets for May through September to sum inter-decadal averages by number of days per month. No other formatting is performed by this tool.
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import os
from arcpy.sa import *

# Set overwrite option
arcpy.env.overwriteOutput = True

# Define input mean monthly temperature rasters for May
input_may = arcpy.GetParameterAsText(0)

# Define input mean monthly temperature rasters for June
input_june = arcpy.GetParameterAsText(1)

# Define input mean monthly temperature rasters for July
input_july = arcpy.GetParameterAsText(2)

# Define input mean monthly temperature rasters for August
input_august = arcpy.GetParameterAsText(3)

# Define input mean monthly temperature rasters for September
input_september = arcpy.GetParameterAsText(4)

# Define a workspace folder
work_folder = arcpy.GetParameterAsText(5)

#Define output raster
output_raster = arcpy.GetParameterAsText(6)

# Split input rasters string into a list
input_may = input_may.split(";")
input_june = input_june.split(";")
input_july = input_july.split(";")
input_august = input_august.split(";")
input_september = input_september.split(";")

# Define intermediate files and list of month variables
average_may = os.path.join(work_folder, "average_may.tif")
average_june = os.path.join(work_folder, "average_june.tif")
average_july = os.path.join(work_folder, "average_july.tif")
average_august = os.path.join(work_folder, "average_august.tif")
average_september = os.path.join(work_folder, "average_september.tif")
months = [[input_may, average_may], [input_june, average_june], [input_july, average_july], [input_august, average_august], [input_september, average_september]]

# Set the snap raster and cell size environments
arcpy.env.snapRaster = input_may[0]
arcpy.env.cellSize = input_may[0]

# Create a function for averaging the temperature rasters
def averageTemperature(inRasters, outRaster):
    # Set the raster sum initially equal to the first raster in the list
    arcpy.AddMessage("Summing input rasters...")
    rasterSum = Raster(inRasters[0])
    # Add the values of additional rasters in the list via a for loop
    for inRaster in inRasters[1:]:
        rasterSum += Raster(inRaster)
    # Find the mean of the raster sum and copy to output
    arcpy.AddMessage("Calculating mean of input rasters...")
    rasterMean = rasterSum/(len(inRasters))
    integerMean = Int(RoundDown((rasterMean * 10) + 0.5))
    arcpy.AddMessage("Copying results to output raster...")
    arcpy.CopyRaster_management(integerMean, outRaster, "", "", "-32768", "NONE", "NONE", "16_BIT_SIGNED", "NONE", "NONE", "TIFF", "NONE")

# Run average temperature function for each month set
for month in months:
    averageTemperature(month[0], month[1])

# Calculate summer warmth index and copy results to output raster
arcpy.AddMessage("Calculating summer warmth index...")
summerWarmth = (Raster(average_may) * 31) + (Raster(average_june) * 30) + (Raster(average_july) * 31) + (Raster(average_august) * 31) + (Raster(average_september) * 30)
arcpy.AddMessage("Copying results to output raster...")
arcpy.CopyRaster_management(summerWarmth, output_raster, "", "", "-32768", "NONE", "NONE", "16_BIT_SIGNED", "NONE", "NONE", "TIFF", "NONE")

# Delete intermediate files
arcpy.Delete_management(average_may)
arcpy.Delete_management(average_june)
arcpy.Delete_management(average_july)
arcpy.Delete_management(average_august)
arcpy.Delete_management(average_september)