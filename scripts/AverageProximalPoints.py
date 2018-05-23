# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Average and Merge Proximal Points
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Created on: 2018-05-22
# Usage: Must be executed as an ArcPy Script.
# Description: "Average Proximal Covers" finds points that are within a user-specified distance of each other, takes the mean of the cover values, and retains one of the proximal points at random.
# ---------------------------------------------------------------------------

# Import modules
import os
import arcpy
	
# Set overwrite option
arcpy.env.overwriteOutput = True

# Define the set of input feature class containing cover values for a taxon
taxon_cover = arcpy.GetParameterAsText(0)

# Define study area raster to be used as snap raster
snap_raster = arcpy.GetParameterAsText(1)

# Define user-specified merge distance
merge_distance = arcpy.GetParameterAsText(2)

# Define the workspace folder
workspace_folder = arcpy.GetParameterAsText(3)

# Define the workspace geodatabase
workspace_geodatabase = arcpy.GetParameterAsText(4)

# Define output feature class for averaged cover values at user-specified range
output_feature = arcpy.GetParameterAsText(5)

# Define intermediate files
cover_raster = os.path.join(workspace, "cover.tif")
taxon_copy

# Convert input cover values to raster using mean rule
arcpy.env.snapRaster = snap_raster
arcpy.PointToRaster_conversion(taxon_cover, "cover", cover_raster, "MEAN", "NONE", merge_distance)

# Delete original cover field from input
