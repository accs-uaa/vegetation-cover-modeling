# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Create Study Area
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Created on: 2018-10-28
# Usage: Must be executed as an ArcPy Script.
# Description: "Create Study Area" creates a continuous gradient raster of spatial certainty based on the 95% confidence interval of sampled environmental variation and calculates a smoothed study area polygon from a user-determined certainty threshold.
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import os
from arcpy.sa import *

# Set overwrite option
arcpy.env.overwriteOutput = True

# Define the area of interest
area_of_interest = arcpy.GetParameterAsText(0)

# Define the study area
study_area = arcpy.GetParameterAsText(1)

# Define the merged species distribution-abundance raster
species_raster = arcpy.GetParameterAsText(2)

# Define the output species distribution-abundance raster
output_raster = arcpy.GetParameterAsText(3)

# Set the snap raster environment
arcpy.env.snapRaster = area_of_interest

# Convert values less than 0 to 0
arcpy.AddMessage("Reconciling prediction values...")
conditional_raster = Con(species_raster, 0, species_raster, "VALUE < 0")

# Convert to integer
arcpy.AddMessage("Converting values to integers...")
integer_raster = Int(conditional_raster + 0.5)

# Extract raster to study area
arcpy.AddMessage("Extracting prediction to study area...")
extract_raster = ExtractByMask(integer_raster, study_area)

# Export final raster to output file
arcpy.AddMessage("Exporting raster to output...")
arcpy.CopyRaster_management(extract_raster, output_raster, "", "", -128, "NONE", "NONE", "8_BIT_SIGNED", "NONE", "NONE", "TIFF", "NONE")