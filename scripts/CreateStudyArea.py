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

# Define the formatted July NDWI raster
july_ndwi = arcpy.GetParameterAsText(1)

# Define the merged sample representation raster
sample_representation = arcpy.GetParameterAsText(2)

# Define conversion threshold
threshold = arcpy.GetParameterAsText(3)

# Define the workspace geodatabase
workspace_geodatabase = arcpy.GetParameterAsText(4)

# Define the workspace folder
workspace_folder = arcpy.GetParameterAsText(5)

# Define the output spatial certainty raster
spatial_certainty = arcpy.GetParameterAsText(6)

# Define the output polygon study area feature class
study_area = arcpy.GetParameterAsText(7)

# Define intermediate datasets
certainty_resample = os.path.join(workspace_folder, "certainty_resample.tif")
initial_studyarea = os.path.join(workspace_geodatabase, "initial_studyarea")
simplify_studyarea = os.path.join(workspace_geodatabase, "simplify_studyarea")

# Set the snap raster environment
arcpy.env.snapRaster = area_of_interest

# Convert the -1 values in the sample representation raster to 0
arcpy.AddMessage("Pre-processing sample representation...")
conditional_sample = Con(sample_representation, 0, sample_representation, "VALUE = -1")

# Convert July NDWI to an unvegetated surface based on a threshold
arcpy.AddMessage("Calculating unvegetated surface from NDWI...")
unvegetated_surface = Con(july_ndwi, 0, 100, "VALUE < -1000")

# Add the sample representation and the unvegetated surface
arcpy.AddMessage("Identifying areas of unvegetated surface in sample representation...")
sample_withwater = conditional_sample + unvegetated_surface

# Set the unvegetated surfaces to no data
arcpy.AddMessage("Removing unvegetated surfaces from sample representation...")
sample_nowater = SetNull(sample_withwater, sample_withwater, "VALUE > 1")

# Calculate raster mean within a 1.5 km grid
arcpy.AddMessage("Calculating spatial certainty of sample representation...")
sample_zonal = FocalStatistics(sample_nowater, NbrRectangle(50, 50, "CELL"), "MEAN", "DATA" )
extract_zonal = ExtractByMask(sample_zonal, area_of_interest)
arcpy.CopyRaster_management(extract_zonal, spatial_certainty, "", "", -9999, "NONE", "NONE", "32_BIT_FLOAT", "NONE", "NONE", "TIFF", "NONE")

# Resample spatial certainty to 1 km grid
arcpy.AddMessage("Resampling spatial certainty to 1 km grid...")
arcpy.Resample_management(spatial_certainty, certainty_resample, "1000", "BILINEAR")

# Set the values below a threshold to null
arcpy.AddMessage("Converting spatial certainty to study area raster...")
threshold = int(threshold)/100
resample_null = SetNull(certainty_resample, 1, "VALUE < %f" % threshold)

# Convert raster to polygon
arcpy.AddMessage("Converting raster to polygon...")
arcpy.RasterToPolygon_conversion(resample_null, initial_studyarea, "SIMPLIFY", "VALUE", "SINGLE_OUTER_PART", "")

# Simplify the polygon
arcpy.AddMessage("Simplifying study area polygon...")
arcpy.SimplifyPolygon_cartography(initial_studyarea, simplify_studyarea, "POINT_REMOVE", 1000, 1000000000, "", "NO_KEEP", "")

# Smooth the polygon
arcpy.AddMessage("Smoothing study area polygon...")
arcpy.SmoothPolygon_cartography(simplify_studyarea, study_area, "PAEK", 50000, "FIXED_ENDPOINT", "NO_CHECK")

# Delete intermediate files
arcpy.Delete_management(certainty_resample)
arcpy.Delete_management(initial_studyarea)
arcpy.Delete_management(simplify_studyarea)