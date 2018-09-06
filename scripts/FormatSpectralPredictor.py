# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Format Spectral Predictor
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Created on: 2018-06-23
# Usage: Must be executed as an ArcPy Script.
# Description: "Format Spectral Predictor" processes input tiles of single band imagery for use as predictive variables in a classification or regression model by converting the float rasters to 16-bit signed or unsigned integers, mosaicking into a single continuous surface, filling no data cells by extension of nearest neighbors, and extracting to the area of interest.
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import os
from arcpy.sa import *

# Set overwrite option
arcpy.env.overwriteOutput = True

# Define input imagery tiles
input_tiles = arcpy.GetParameterAsText(0)

# Define input area of interest raster
area_of_interest = arcpy.GetParameterAsText(1)

# Define the scaling factor
scaling_factor = arcpy.GetParameterAsText(2)
scaling_factor = int(scaling_factor)

# Define Raster Bit Depth
bit_depth = arcpy.GetParameterAsText(3)

# Define workspace folder
work_folder = arcpy.GetParameterAsText(4)

# Define the output raster
output_raster = arcpy.GetParameterAsText(5)

# Split input rasters string into a list
input_tiles = input_tiles.split(";")

# Define No Data ValueError
if bit_depth == '16_BIT_UNSIGNED':
    no_data = 65535
elif bit_depth == '16_BIT_SIGNED':
    no_data = -32768

# Define intermediate files
mosaicRaster = os.path.join(work_folder, "mosaicRaster.tif")
projectRaster = os.path.join(work_folder, "projectRaster.tif")

# Create a function to format spectral tiles
def integerTile(inTile, outTile):
    arcpy.AddMessage("Converting tile from float to integer...")
    # Convert float tile to integer tile
    integerTile = Int(RoundDown((Raster(inTile) * scaling_factor) + 0.5))
    # Convert integer tile to 16 bit signed tile
    arcpy.CopyRaster_management(integerTile, outTile, "", "", no_data, "NONE", "NONE", bit_depth, "NONE", "NONE", "TIFF", "NONE")
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
arcpy.MosaicToNewRaster_management(output_tiles, work_folder, "mosaicRaster.tif", projectionOriginal, bit_depth, cellOriginal, "1", "MEAN", "FIRST")

# Set the snap raster to the mosaic
arcpy.env.snapRaster = mosaicRaster

# Create a null raster from the mosaic to identify no data cells
arcpy.AddMessage("Identifying no data cells...")
nullRaster = SetNull(IsNull(mosaicRaster), 1, "VALUE = 1")
# Extrapolate missing data using nearest neighbors
arcpy.AddMessage("Filling no data cells based on extension of nearest neighbors...")
filledRaster = Nibble(mosaicRaster, nullRaster, "DATA_ONLY", "PROCESS_NODATA", "")

# Reproject the filled raster to match the area of interest
arcpy.AddMessage("Reprojecting and resampling output to match area of interest...")
arcpy.env.snapRaster = area_of_interest
projectionFinal = arcpy.Describe(area_of_interest).spatialReference
cellFinalX = arcpy.GetRasterProperties_management(area_of_interest, "CELLSIZEX")
cellFinalY = arcpy.GetRasterProperties_management(area_of_interest, "CELLSIZEY")
cellFinal = str(cellFinalX) + " " + str(cellFinalY)
arcpy.ProjectRaster_management(filledRaster, projectRaster, projectionFinal, "BILINEAR", cellFinal, "WGS_1984_(ITRF00)_To_NAD_1983", "", projectionOriginal)

# Extract projected raster to area of interest
arcpy.AddMessage("Extracting output to area of interest...")
arcpy.env.cellSize = area_of_interest
outExtract = ExtractByMask(projectRaster, area_of_interest)
arcpy.CopyRaster_management(outExtract, output_raster, "", "", no_data, "NONE", "NONE", bit_depth, "NONE", "NONE", "TIFF", "NONE")

# Delete intermediate files
for output_tile in output_tiles:
    arcpy.Delete_management(output_tile)
arcpy.Delete_management(mosaicRaster)
arcpy.Delete_management(projectRaster)