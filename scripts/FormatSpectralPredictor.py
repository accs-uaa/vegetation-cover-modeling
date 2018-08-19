# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Format Spectral Predictor
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Created on: 2018-06-23
# Usage: Must be executed as an ArcPy Script.
# Description: "Format Spectral Predictor" processes input tiles of single band imagery for use as predictive variables in a classification or regression model by converting the float rasters to 32-bit signed integers, mosaicking into a single continuous surface, reprojecting to match the projection of the area of interest, resampling to match the cell size and snap raster of the area of interest, and extracting to the area of interest.
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import os
from arcpy.sa import *

# Set overwrite option
arcpy.env.overwriteOutput = True

# Define input imagery tiles
input_tiles = arcpy.GetParameterAsText(0)

# Define workspace folder
work_folder = arcpy.GetParameterAsText(1)

# Define the output raster
output_raster = arcpy.GetParameterAsText(2)

# Split input rasters string into a list
input_tiles = input_tiles.split(";")

# Create a function to format spectral tiles
def integerTile(inTile, outTile):
    arcpy.AddMessage("Converting tile from float to integer...")
    # Convert float tile to integer tile
    integerTile = Int(RoundDown((Raster(inTile) * 1000000) + 0.5))
    # Convert integer tile to 16 bit signed tile
    arcpy.CopyRaster_management(integerTile, outTile, "", "", "-2147483648", "NONE", "NONE", "32_BIT_SIGNED", "NONE", "NONE", "TIFF", "NONE")
    # Add output tile to list of output tiles
    output_tiles.append(outTile)

# Create empty list to store output tiles
output_tiles = []

# Iterate the format raster function for each raster selected as an input
for input_tile in input_tiles:
    converted_tile = os.path.join(work_folder, os.path.split(input_tile)[1])
    integerTile(input_tile, converted_tile)

# Mosaic the formatted tiles into a single continuous surface
arcpy.AddMessage("Compiling tiles into a continuous surface...")
arcpy.env.snapRaster = input_tiles[0]
projectionOriginal = arcpy.Describe(input_tiles[0]).spatialReference
cellOriginal = arcpy.GetRasterProperties_management(input_tiles[0], "CELLSIZEX")
mosaicRaster = os.path.join(work_folder, "mosaicRaster.tif")
arcpy.MosaicToNewRaster_management(output_tiles, work_folder, "mosaicRaster.tif", projectionOriginal, "32_BIT_SIGNED", cellOriginal, "1", "MEAN", "FIRST")
	
# Remove and replace no data values within raster with 5 cell grid average
arcpy.AddMessage("Interpolating missing data...")
filled_raster = CON(isnull(mosaicRaster), FOCALMEAN(mosaicRaster, rectangle,5,5), mosaicRaster)
arcpy.CopyRaster_management(filled_raster, output_raster, "", "", "-2147483648", "NONE", "NONE", "32_BIT_SIGNED", "NONE", "NONE", "TIFF", "NONE")

# Delete intermediate files
for output_tile in output_tiles:
    arcpy.Delete_management(output_tile)
arcpy.Delete_management(mosaicRaster)