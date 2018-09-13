# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Prepare Watershed Units
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Created on: 2018-09-09
# Usage: Must be executed as an ArcPy Script.
# Description: "Prepare watershed units" creates individual point shapefiles with regularly gridded points on a grid that matches the area of interest for each watershed in the watershed feature class. Watersheds must be pre-processed to fit within the area of interest and predict area. This script does not format the watershed units.
# ---------------------------------------------------------------------------

# Import modules
import os
import arcpy
from arcpy.sa import *

# Set overwrite option
arcpy.env.overwriteOutput = True

# Define the input watershed feature class from the Watershed Boundary Dataset
watersheds =  arcpy.GetParameterAsText(0)

# Define the area of interest raster
area_of_interest = arcpy.GetParameterAsText(1)

# Define the workspace folder
workspace_folder = arcpy.GetParameterAsText(2)

# Define an empty watershed geodatabase
watershed_geodatabase = arcpy.GetParameterAsText(3)

# Define empty folder to store output watershed point csv files
output_folder = arcpy.GetParameterAsText(4)

# Create a function to create point grids from polygon features
def buildPointGrids(inFeature, tempRaster, cell_size, outShapefile):
    # Convert from polygon to raster and raster to point to create point grid
    arcpy.PolygonToRaster_conversion(inFeature, "OBJECTID", tempRaster, "CELL_CENTER", "NONE", cell_size)
    # Determine if raster contains only NoData values
    noData = int(arcpy.GetRasterProperties_management(tempRaster, 'ALLNODATA')[0])
    if noData == 0:
        # Convert raster to point grid
        arcpy.RasterToPoint_conversion(tempRaster, outShapefile, "VALUE")
        # Add XY Coordinates to feature class in the NAD_1983_Alaska_Albers projection
        arcpy.AddXY_management(outShapefile)
        # Delete intermediate files
        arcpy.Delete_management(tempRaster)
    elif noData == 1:
        arcpy.AddMessage("All values for this watershed are nodata...")
        # Delete intermediate files
        arcpy.Delete_management(tempRaster)

# Set the snap raster and cell size environments
arcpy.env.snapRaster = area_of_interest
arcpy.env.cellSize = area_of_interest

# Split watersheds by attribute and store as independent feature classes in an empty geodatabase
arcpy.AddMessage("Splitting unique watersheds into independent feature classes...")
arcpy.SplitByAttributes_analysis(watersheds, watershed_geodatabase, ['HUC10'])

# List all watershed feature classes in the watershed geodatabase
arcpy.env.workspace = watershed_geodatabase
featureClasses = arcpy.ListFeatureClasses()
featureClasses_length = len(featureClasses)

# Loop through feature classes and convert them to point grids with the same cell size and grid as the area of interest
cell_size = arcpy.GetRasterProperties_management(area_of_interest, "CELLSIZEX")
grid_raster = os.path.join(workspace_folder, "grid_raster.tif")
count = 1
for feature in featureClasses:
    arcpy.AddMessage("Converting watershed to point grid for watershed " + str(count) + " of " + str(featureClasses_length) + "...")
    input_feature = os.path.join(watershed_geodatabase, feature)
    output_shapefile = os.path.join(output_folder, feature + ".shp")
    buildPointGrids(input_feature, grid_raster, cell_size, output_shapefile)
    count = count + 1