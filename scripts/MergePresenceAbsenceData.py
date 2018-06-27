# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Merge Presence and Absence Data
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Created on: 2018-05-22
# Usage: Must be executed as an ArcPy Script.
# Description: "Merge Presence Absence Data" combines the presence cover data from a database query with the survey sites at which the species was not found. The cover values for points closer than a user-specified merge distance are averaged based on the analysis grid with the point closest to grid center retained. Cover values of zero in the presence data will be merged with zero values generated from the absence data. In the resulting dataset, zero and trace cover are indistinguishable.
# ---------------------------------------------------------------------------

# Import modules
import arcpy
import os

# Set overwrite option
arcpy.env.overwriteOutput = True

# Define the input feature class containing cover values for a taxon
cover_feature = arcpy.GetParameterAsText(0)

# Define the set of all possible sites
survey_sites = arcpy.GetParameterAsText(1)

# Define area of interest raster to be used as snap raster
snap_raster = arcpy.GetParameterAsText(2)

# Define user-specified merge distance
merge_distance = arcpy.GetParameterAsText(3)

# Define the workspace geodatabase
workspace_geodatabase = arcpy.GetParameterAsText(4)

# Define output feature class for averaged cover values at user-specified range
mean_cover_sites = arcpy.GetParameterAsText(5)

# Define output feature class for redundant sites removed from data selection
removed_sites = arcpy.GetParameterAsText(6)

# Define intermediate files
absence_sites = os.path.join(workspace_geodatabase, "absence_sites")
presence_sites = os.path.join(workspace_geodatabase, "presence_sites")
merged_sites = os.path.join(workspace_geodatabase, "merged_sites")
cover_raster = os.path.join(workspace_geodatabase, "cover")
mean_cover = os.path.join(workspace_geodatabase, "mean_cover")
mean_cover_joined = os.path.join(workspace_geodatabase, "mean_cover_joined")
merged_sites_joined = os.path.join(workspace_geodatabase, "merged_sites_joined")

# Erase survey sites in which the target taxon was present
arcpy.AddMessage("Formatting absence cover data...")
arcpy.Erase_analysis(survey_sites, cover_feature, absence_sites, "")
arcpy.AddXY_management(absence_sites)

# Add a cover field to the absence sites with the cover value set to 0
arcpy.AddField_management(absence_sites, "cover", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.CalculateField_management(absence_sites, "cover", 0, "PYTHON", "")

# Add a project field to the absence sites with the value set to initialProject
arcpy.AddField_management(absence_sites, "project", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.CalculateField_management(absence_sites, "project", "!initialProject!", "PYTHON", "")

# Create a copy of the cover feature class for attribute modification
arcpy.CopyFeatures_management(cover_feature, presence_sites)

# Delete unmatched fields from presence and absence datasets
arcpy.DeleteField_management(presence_sites, "ID;date;vegObserver1;vegObserver2;nameAccepted;tsnITIS")
arcpy.DeleteField_management(absence_sites, "ID;initialProject;initialProjectTitle;plotDimensions;vascularScope;nonvascularScope;lichenScope")

# Merge the presence and the absence sites
arcpy.AddMessage("Merging presence and absence cover data...")
arcpy.Merge_management([presence_sites, absence_sites], merged_sites)
arcpy.AddField_management(merged_sites, "originalID", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.CalculateField_management(merged_sites, "originalID", "!OBJECTID!", "PYTHON", "")

# Convert input cover values to raster using mean rule to average cover values for points within the merge distance
arcpy.AddMessage("Finding mean value of survey sites that overlap common grid cell...")
arcpy.env.snapRaster = snap_raster
arcpy.PointToRaster_conversion(merged_sites, "cover", cover_raster, "MEAN", "NONE", merge_distance)

# Remove the cover value from the merged sites feature class
arcpy.DeleteField_management(merged_sites, "cover")

# Convert the mean cover value raster to point
arcpy.RasterToPoint_conversion(cover_raster, mean_cover, "Value")

# Use a spatial join to add the mean cover value to the nearest point from the merged sites feature class and remove points that were not nearest to a mean cover point
arcpy.AddMessage("Pushing mean values to output and removing redundant sites...")
arcpy.SpatialJoin_analysis(mean_cover, merged_sites, mean_cover_joined, "JOIN_ONE_TO_ONE", "KEEP_ALL", "", "CLOSEST", "", "")
arcpy.SpatialJoin_analysis(merged_sites, mean_cover_joined, merged_sites_joined, "JOIN_ONE_TO_ONE", "KEEP_ALL", "", "CLOSEST", "", "")
arcpy.MakeFeatureLayer_management(merged_sites_joined, "merged_sites_joined_layer")
arcpy.SelectLayerByAttribute_management("merged_sites_joined_layer", "NEW_SELECTION", "OBJECTID = OriginalID_1")
arcpy.CopyFeatures_management("merged_sites_joined_layer", mean_cover_sites)
arcpy.AddField_management(mean_cover_sites, "cover", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.CalculateField_management(mean_cover_sites, "cover", "!grid_code!", "PYTHON", "")
arcpy.DeleteField_management(mean_cover_sites, "Join_Count;TARGET_FID;originalID;Join_Count_1;TARGET_FID_1;pointid;grid_code;project_1;siteCode_1;methodSurvey_1;methodCover_1;latitude_1;longitude_1;datum_1;POINT_X_1;POINT_Y_1;originalID_1")

# Export the redundant points that were removed from the available data
arcpy.SelectLayerByAttribute_management("merged_sites_joined_layer", "NEW_SELECTION", "OBJECTID <> OriginalID_1")
arcpy.CopyFeatures_management("merged_sites_joined_layer", removed_sites)
arcpy.AddField_management(removed_sites, "cover", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.CalculateField_management(removed_sites, "cover", "!grid_code!", "PYTHON", "")
arcpy.DeleteField_management(removed_sites, "Join_Count;TARGET_FID;originalID;Join_Count_1;TARGET_FID_1;pointid;grid_code;project_1;siteCode_1;methodSurvey_1;methodCover_1;latitude_1;longitude_1;datum_1;POINT_X_1;POINT_Y_1;originalID_1")

# Delete intermediate files
arcpy.Delete_management(absence_sites)
arcpy.Delete_management(presence_sites)
arcpy.Delete_management(merged_sites)
arcpy.Delete_management(cover_raster)
arcpy.Delete_management(mean_cover)
arcpy.Delete_management(mean_cover_joined)
arcpy.Delete_management(merged_sites_joined)