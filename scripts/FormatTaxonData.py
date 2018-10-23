# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Format Taxon Data
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Created on: 2018-07-13
# Usage: Must be executed as an ArcPy Script.
# Description: "Format Taxon Data" combines the cover data from a database query with the survey sites at which the species was not found. The cover values for points closer than a user-specified merge distance are averaged based on the analysis grid with the point closest to grid center retained. Cover values of zero in the presence data are merged with zero values generated from the absence data. Cover values are rounded to the nearest integer. Cover values equal to zero are assigned a 0 indicating absence and cover values greater than zero are assigned a 1 indicating presence.
# ---------------------------------------------------------------------------

# Import modules
import os
import arcpy
import arcpy.da as da
import numpy as np
import pandas as pd
from arcpy.sa import *

# Set overwrite option
arcpy.env.overwriteOutput = True

# Define the input feature class containing cover values for a taxon
cover_feature = arcpy.GetParameterAsText(0)

# Define the set of all possible sites
survey_sites = arcpy.GetParameterAsText(1)

# Define area of interest raster
area_of_interest = arcpy.GetParameterAsText(2)

# Define user-specified merge distance
merge_distance = arcpy.GetParameterAsText(3)

# Define set of predictor rasters
predictor_rasters = arcpy.GetParameterAsText(4)

# Define the workspace geodatabase
workspace_geodatabase = arcpy.GetParameterAsText(5)

# Define output feature class for averaged cover values at user-specified range
mean_cover_sites = arcpy.GetParameterAsText(6)

# Define output csv
output_csv = arcpy.GetParameterAsText(7)

# Split predictor rasters string into a list
predictor_rasters = predictor_rasters.split(";")

# Define intermediate files
aoi_poly = os.path.join(workspace_geodatabase, "aoi_poly")
survey_erase = os.path.join(workspace_geodatabase, "survey_erase")
absence_sites = os.path.join(workspace_geodatabase, "absence_sites")
presence_sites = os.path.join(workspace_geodatabase, "presence_sites")
merged_sites = os.path.join(workspace_geodatabase, "merged_sites")
cover_raster = os.path.join(workspace_geodatabase, "cover")
mean_cover = os.path.join(workspace_geodatabase, "mean_cover")
mean_cover_joined = os.path.join(workspace_geodatabase, "mean_cover_joined")
merged_sites_joined = os.path.join(workspace_geodatabase, "merged_sites_joined")

# Create a function to convert a feature class to csv
def featureToCSV(inFeature, inColumns, outCSV):
    arcpy.AddMessage("Converting feature class to csv...")
    feature_array = da.FeatureClassToNumPyArray(inFeature, ["SHAPE@XY"] + inColumns)
    feature_df = pd.DataFrame(feature_array, columns = inColumns)
    feature_df.to_csv(outCSV, header=True, index=False, sep=',', encoding='utf-8')

# Convert area of interest to polygon without simplifying
arcpy.AddMessage("Formatting absence cover data...")
arcpy.RasterToPolygon_conversion(area_of_interest, aoi_poly, "NO_SIMPLIFY", "VALUE")

# Erase survey sites in which the target taxon was present and clip the absence sites to the area of interest
arcpy.Erase_analysis(survey_sites, cover_feature, survey_erase, "")
arcpy.Clip_analysis(survey_erase, aoi_poly, absence_sites, "")

# Add a cover field to the absence sites with the cover value set to 0
arcpy.AddField_management(absence_sites, "cover", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.CalculateField_management(absence_sites, "cover", 0, "PYTHON", "")

# Add a project field to the absence sites with the value set to initialProject
arcpy.AddField_management(absence_sites, "project", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.CalculateField_management(absence_sites, "project", "!initialProject!", "PYTHON", "")

# Clip the cover feature to the area of interest
arcpy.AddMessage("Formatting presence cover data...")
arcpy.Clip_analysis(cover_feature, aoi_poly, presence_sites, "")

# Delete unmatched fields from presence and absence datasets
arcpy.DeleteField_management(presence_sites, "abundanceID;vegObserver1;vegObserver2;nameAccepted;tsnITIS")
arcpy.DeleteField_management(absence_sites, "initialProject;initialProjectTitle")

# Merge the presence and the absence sites
arcpy.AddMessage("Merging presence and absence cover data...")
arcpy.Merge_management([presence_sites, absence_sites], merged_sites)
arcpy.AddField_management(merged_sites, "originalID", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.CalculateField_management(merged_sites, "originalID", "!OBJECTID!", "PYTHON", "")

# Convert input cover values to raster using mean rule to average cover values for points within the merge distance
arcpy.AddMessage("Finding mean value of survey sites that overlap common grid cell...")
arcpy.env.snapRaster = area_of_interest
arcpy.PointToRaster_conversion(merged_sites, "cover", cover_raster, "MEAN", "NONE", merge_distance)

# Round the mean cover values to the nearest integer
integerRaster = Int(Raster(cover_raster) + 0.5)

# Remove the cover value from the merged sites feature class
arcpy.DeleteField_management(merged_sites, "cover")

# Convert the mean cover value raster to point
arcpy.RasterToPoint_conversion(integerRaster, mean_cover, "Value")

# Use a spatial join to add the mean cover value to the nearest point from the merged sites feature class and remove points that were not nearest to a mean cover point
arcpy.AddMessage("Pushing mean values to output and removing redundant sites...")
arcpy.SpatialJoin_analysis(mean_cover, merged_sites, mean_cover_joined, "JOIN_ONE_TO_ONE", "KEEP_ALL", "", "CLOSEST", "", "")
arcpy.SpatialJoin_analysis(merged_sites, mean_cover_joined, merged_sites_joined, "JOIN_ONE_TO_ONE", "KEEP_ALL", "", "CLOSEST", "", "")
arcpy.MakeFeatureLayer_management(merged_sites_joined, "merged_sites_joined_layer")
arcpy.SelectLayerByAttribute_management("merged_sites_joined_layer", "NEW_SELECTION", "OBJECTID = OriginalID_1")
arcpy.CopyFeatures_management("merged_sites_joined_layer", mean_cover_sites)
arcpy.AddField_management(mean_cover_sites, "cover", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.CalculateField_management(mean_cover_sites, "cover", "!grid_code!", "PYTHON", "")
arcpy.DeleteField_management(mean_cover_sites, "Join_Count;TARGET_FID;originalID;Join_Count_1;TARGET_FID_1;pointid;grid_code;project_1;siteCode_1;methodSurvey_1;methodCover_1;latitude_1;longitude_1;datum_1;POINT_X_1;POINT_Y_1;originalID_1;siteID_1;vascularScope_1;nonvascularScope_1;lichenScope_1;regression_1;date_1;plotDimensions_1")

# Add a stratification field to the mean cover data and define strata based on cover values
arcpy.AddField_management(mean_cover_sites, "strata", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
stratifyExpression = "stratifyCover(!cover!)"
stratifyCodeblock = """def stratifyCover(cover):
    if cover == 0:
        return 0
    elif 0 < cover <= 10:
        return 1
    elif 10 < cover <= 25:
        return 2
    elif cover > 25:
        return 3"""
arcpy.CalculateField_management(mean_cover_sites, "strata", stratifyExpression, "PYTHON3", stratifyCodeblock)

# Add a field that distinguishes cover values greater than 0%
arcpy.AddField_management(mean_cover_sites, "zero", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
zeroExpression = "zeroCover(!cover!)"
zeroCodeblock = """def zeroCover(cover):
    if cover == 0:
        return 0
    elif cover > 0:
        return 1"""
arcpy.CalculateField_management(mean_cover_sites, "zero", zeroExpression, "PYTHON3", zeroCodeblock)

# Add a field that distinguishes cover values greater than 10%
arcpy.AddField_management(mean_cover_sites, "ten", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
tenExpression = "tenCover(!cover!)"
tenCodeblock = """def tenCover(cover):
    if cover <= 10:
        return 0
    elif cover > 10:
        return 1"""
arcpy.CalculateField_management(mean_cover_sites, "ten", tenExpression, "PYTHON3", tenCodeblock)

# Add a field that distinguishes cover values greater than 25%
arcpy.AddField_management(mean_cover_sites, "twentyfive", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
twentyfiveExpression = "twentyfiveCover(!cover!)"
twentyfiveCodeblock = """def twentyfiveCover(cover):
    if cover <= 25:
        return 0
    elif cover > 25:
        return 1"""
arcpy.CalculateField_management(mean_cover_sites, "twentyfive", twentyfiveExpression, "PYTHON3", twentyfiveCodeblock)

# Extract predictor rasters to mean cover points
for predictor in predictor_rasters:
    arcpy.AddMessage("Extracting " + os.path.split(os.path.splitext(predictor)[0])[1] + " values to points...")
    ExtractMultiValuesToPoints(mean_cover_sites, predictor, "NONE")

# Convert feature class to numpy array and dataframe and export as csv
predictor_variables = ['aspect', 'compoundTopographic', 'dateFreeze_2000s', 'dateThaw_2000s', 'elevation', 'floodplainsDist', 'growingSeason_2000s', 'heatLoad', 'integratedMoisture', 'precipAnnual_2000s', 'roughness', 'siteExposure', 'slope', 'streamLargeDist', 'streamSmallDist', 'summerWarmth_2000s', 'surfaceArea', 'surfaceRelief', 'may_1_ultraBlue', 'may_2_blue', 'may_3_green', 'may_4_red', 'may_5_nearInfrared', 'may_6_shortInfrared1', 'may_7_shortInfrared2', 'may_evi2', 'may_nbr', 'may_ndmi', 'may_ndsi', 'may_ndvi', 'may_ndwi', 'june_1_ultraBlue', 'june_2_blue', 'june_3_green', 'june_4_red', 'june_5_nearInfrared', 'june_6_shortInfrared1', 'june_7_shortInfrared2', 'june_evi2', 'june_nbr', 'june_ndmi', 'june_ndsi', 'june_ndvi', 'june_ndwi', 'july_1_ultraBlue', 'july_2_blue', 'july_3_green', 'july_4_red', 'july_5_nearInfrared', 'july_6_shortInfrared1', 'july_7_shortInfrared2', 'july_evi2', 'july_nbr', 'july_ndmi', 'july_ndsi', 'july_ndvi', 'july_ndwi', 'august_1_ultraBlue', 'august_2_blue', 'august_3_green', 'august_4_red', 'august_5_nearInfrared', 'august_6_shortInfrared1', 'august_7_shortInfrared2', 'august_evi2', 'august_nbr', 'august_ndmi', 'august_ndsi', 'august_ndvi', 'august_ndwi', 'september_1_ultraBlue', 'september_2_blue', 'september_3_green', 'september_4_red', 'september_5_nearInfrared', 'september_6_shortInfrared1', 'september_7_shortInfrared2', 'september_evi2', 'september_nbr', 'september_ndmi', 'september_ndsi', 'september_ndvi', 'september_ndwi']
retain_variables = ['cover', 'project', 'siteID', 'siteCode', 'methodSurvey', 'methodCover', 'plotDimensions', 'vascularScope', 'nonvascularScope', 'lichenScope', 'date', 'datum', 'latitude', 'longitude', 'strata', 'zero', 'ten', 'twentyfive']
coordinates = ['POINT_X', 'POINT_Y']
all_variables = retain_variables + coordinates + predictor_variables
featureToCSV(mean_cover_sites, all_variables, output_csv)

# Delete intermediate files
arcpy.Delete_management(aoi_poly)
arcpy.Delete_management(survey_erase)
arcpy.Delete_management(absence_sites)
arcpy.Delete_management(presence_sites)
arcpy.Delete_management(merged_sites)
arcpy.Delete_management(cover_raster)
arcpy.Delete_management(mean_cover)
arcpy.Delete_management(mean_cover_joined)
arcpy.Delete_management(merged_sites_joined)