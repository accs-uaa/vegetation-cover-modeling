# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Convert Watershed Units To Raster
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Created on: 2018-06-27
# Usage: Must be executed as an ArcPy Script.
# Description: "Convert Watershed Units To Raster" converts tables of gridded points into a raster with the cell size and grid equivalent to the area of interest raster. The value field should be set to the field containing the output predicted value of the model.
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
