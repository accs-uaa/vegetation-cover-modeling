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
workspace_geodatabase = arcpy.GetParameterAsText(4)

# Define output folder
output_folder = arcpy.GetParameterAsText(5)

# Define intermediate files
absence_sites = os.path.join(workspace_geodatabase, "absence_sites")

# Create a function to convert the tabular data to raster

Raster function in R?




# Set intermediate variables
watershed_csv = "K:\\VegetationEcology\\NorthSlopeDataHarmonization\\TestData\\watershed.csv"
watershed_Layer = "watershed_Layer"
watershed_points_predicted = "K:\\VegetationEcology\\NorthSlopeDataHarmonization\\Project_GIS\\DataHarmonization_GIS.gdb\\watershed_points_predicted"
watershed_raster_predicted = "K:\\VegetationEcology\\NorthSlopeDataHarmonization\\Project_GIS\\DataHarmonization_GIS.gdb\\watershed_raster_predicted"

# Process: Make XY Event Layer
arcpy.MakeXYEventLayer_management(watershed_csv, "Field27", "Field28", watershed_Layer, "PROJCS['NAD_1983_Alaska_Albers',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Albers'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-154.0],PARAMETER['Standard_Parallel_1',55.0],PARAMETER['Standard_Parallel_2',65.0],PARAMETER['Latitude_Of_Origin',50.0],UNIT['Meter',1.0]];-13752200 -8948200 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision", "")

# Process: Copy Features
arcpy.CopyFeatures_management(watershed_Layer, watershed_points_predicted, "", "0", "0", "0")

# Process: Point to Raster
tempEnvironment0 = arcpy.env.snapRaster
arcpy.env.snapRaster = "K:\\VegetationEcology\\NorthSlopeDataHarmonization\\Project_GIS\\DataHarmonization_GIS.gdb\\Watershed_Test_Raster"
arcpy.PointToRaster_conversion(watershed_points_predicted, "Field29", watershed_raster_predicted, "MOST_FREQUENT", "NONE", "60")
arcpy.env.snapRaster = tempEnvironment0