# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Create Area of Interest
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Created on: 2018-06-06
# Usage: Must be executed as an ArcPy Script.
# Description: "Create Area of Interest" creates an area of interest raster from a polygon study area that is matched to the shared extent of the unformatted predictor rasters and a user-specified snap raster and cell size. This tool assumes that the polygon study area and the predictor rasters are in the same projection.
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import os
from arcpy.sa import *

# Set overwrite option
arcpy.env.overwriteOutput = True

# Define the polygon study area feature class
study_area = arcpy.GetParameterAsText(0)

# Define input rasters
input_rasters = arcpy.GetParameterAsText(1)

# Define the cell size
cell_size = arcpy.GetParameterAsText(2)

# Define the snap raster
snap_raster = arcpy.GetParameterAsText(3)

# Define the output area of interest raster
area_of_interest = arcpy.GetParameterAsText(4)

# Define the output area of interest feature class
area_of_interest_feature = arcpy.GetParameterAsText(5)

# Set the snap raster environment
arcpy.env.snapRaster = snap_raster

# Convert the polygon study area to a raster using the user-specified cell size and snap raster
arcpy.AddMessage("Converting study area to a raster...")
arcpy.PolygonToRaster_conversion(study_area, "OBJECTID", area_of_interest, "CELL_CENTER", "NONE", cell_size)

# Split input rasters string into a list
input_rasters = input_rasters.split(";")

# Set the cell size environment
arcpy.env.cellSize = int(cell_size)

# Create a function to refine the initial area of interest based on the data extent of the unformatted predictor rasters
def refineAOI(area, predictor):
    # Extract initial area of interest to predictor raster
    arcpy.AddMessage("Refining area of interest...")
    outExtract = ExtractByMask(area, predictor)
    arcpy.Delete_management(area)
    arcpy.CopyRaster_management(outExtract, area, "", "", "", "NONE", "NONE", "1_BIT", "NONE", "NONE", "TIFF", "NONE")

# Iterate the refine AOI function for each raster selected as an input
for input_raster in input_rasters:
    refineAOI(area_of_interest, input_raster)

# Convert the area of interest raster to a feature class
arcpy.RasterToPolygon_conversion(area_of_interest, area_of_interest_feature, "NO_SIMPLIFY", "VALUE")