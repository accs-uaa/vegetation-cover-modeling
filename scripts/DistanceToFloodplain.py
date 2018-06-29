# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Distance to Floodplain
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Created on: 2018-06-26
# Usage: Must be executed as an ArcPy Script.
# Description: "Distance to Floodplain" processes a stream network generated from a digital elevation model using TauDEM, the Circumboreal Vegetation Map, and the Landscape Level Ecological Mapping of Northern Alaska to create a coarse floodplain map for Northern Alaska. The euclidean distance to floodplain is calculated and output as an integer distance raster. The floodplain distribution is also output as a feature class. This tool must be executed after the "Distance to Streams (Large and Small)" tool because it requires the stream network feature class as an input.
# ---------------------------------------------------------------------------

# Import python libraries
import arcpy
import os
from arcpy.sa import *

# Set overwrite option
arcpy.env.overwriteOutput = True

# Define stream network
stream_network = arcpy.GetParameterAsText(0)

# Define input Landscape Level Ecological Mapping of Northern Alaska
northern_alaska_subsections = arcpy.GetParameterAsText(1)

# Define Circumboreal Vegetation Map
circumboreal_vegetation = arcpy.GetParameterAsText(2)

# Define study area
study_area = arcpy.GetParameterAsText(3)

# Define the snap raster
snap_raster = arcpy.GetParameterAsText(4)

# Define the cell size
cell_size = arcpy.GetParameterAsText(5)

# Define workspace geodatabase
work_geodatabase = arcpy.GetParameterAsText(6)

# Define output floodplain feature class
floodplain_feature = arcpy.GetParameterAsText(7)

# Define output distance to floodplain raster
floodplain_dist = arcpy.GetParameterAsText(8)

# Define intermediate datasets
arctic_floodplain = os.path.join(work_geodatabase, "arctic_floodplain")
boreal_floodplain = os.path.join(work_geodatabase, "boreal_floodplain")
stream_3 = os.path.join(work_geodatabase, "stream_3")
stream_4 = os.path.join(work_geodatabase, "stream_4")
stream_5 = os.path.join(work_geodatabase, "stream_5")
stream_6 = os.path.join(work_geodatabase, "stream_6")
stream_7 = os.path.join(work_geodatabase, "stream_7")
stream_8 = os.path.join(work_geodatabase, "stream_8")
stream_9 = os.path.join(work_geodatabase, "stream_9")
floodplain_merge = os.path.join(work_geodatabase, "floodplain_merge")
floodplain_dissolve = os.path.join(work_geodatabase, "floodplain_dissolve")

# Create a function to select streams based on stream order and apply a buffer based on stream order squared * 10 m
def bufferStreamOrder(inFeature_layer, n, outFeature):
    arcpy.AddMessage("Buffering streams by stream order...")
    # Set up arguments based on iteration number
    sqlQuery = "strmOrder = " + str(n)
    buffer_dist = str(n**2 * 10) + " meters"
    # Select stream network by stream order according to iteration number and copy to new feature class
    streamOrder_select = os.path.join(work_geodatabase, "streamOrder_select")
    arcpy.SelectLayerByAttribute_management (inFeature_layer, "NEW_SELECTION", sqlQuery)
    arcpy.CopyFeatures_management(inFeature_layer, streamOrder_select)
    arcpy.Buffer_analysis(streamOrder_select, outFeature, buffer_dist, "FULL", "ROUND", "ALL", "", "PLANAR")
    # Delete intermediate files
    arcpy.Delete_management(streamOrder_select)

# Make feature layer from stream network
stream_network_layer = "stream_network_layer"
arcpy.MakeFeatureLayer_management(stream_network, stream_network_layer)

# Iterate through stream orders 3-9 to select stream network layer by stream order and apply a buffer based on stream order squared * 10 m
i = 3
while i < 10:
    filename = "stream_" + str(i)
    streamOrder_feature = os.path.join(work_geodatabase, filename)
    bufferStreamOrder(stream_network_layer, i, streamOrder_feature)
    i = i + 1

# Make feature layer of Landscape Level Ecological Mapping of Northern Alaska
arcpy.AddMessage("Selecting floodplains from Landscape Level Ecological Mapping of Northern Alaska...")
northern_alaska_subsections_layer = "northern_alaska_subsections_layer"
arcpy.MakeFeatureLayer_management(northern_alaska_subsections, northern_alaska_subsections_layer)

# Select floodplains from Landscape Level Ecological Mapping of Northern Alaska and copy to new feature class
arcpy.SelectLayerByAttribute_management(northern_alaska_subsections_layer, "NEW_SELECTION", "PHYSIOGRAP = 'Floodplain'")
arcpy.CopyFeatures_management(northern_alaska_subsections_layer, arctic_floodplain)

# Make feature layer of Circumboreal Vegetation Map
arcpy.AddMessage("Selecting floodplains from Circumboreal Vegetation Map...")
circumboreal_vegetation_layer = "circumboreal_vegetation_layer"
arcpy.MakeFeatureLayer_management(circumboreal_vegetation, circumboreal_vegetation_layer)

# Select floodplains from Circumboreal Vegetation Map and copy to new feature class
arcpy.SelectLayerByAttribute_management(circumboreal_vegetation_layer, "NEW_SELECTION", "Physiograp = 'R'")
arcpy.CopyFeatures_management(circumboreal_vegetation_layer, boreal_floodplain, "", "0", "0", "0")

# Merge and dissolve floodplain datasets
floodplains = [stream_3, stream_4, stream_5, stream_6, stream_7, stream_8, stream_9, arctic_floodplain, boreal_floodplain]
arcpy.Merge_management(floodplains, floodplain_merge)
arcpy.Dissolve_management(floodplain_merge, floodplain_dissolve, "", "", "MULTI_PART", "DISSOLVE_LINES")
arcpy.Clip_analysis(floodplain_dissolve, study_area, floodplain_feature, "")

# Set the snap raster, cell size, and extent environments
arcpy.env.snapRaster = snap_raster
extent = arcpy.Describe(study_area).extent
arcpy.env.extent = extent

# Calculate euclidean distance from merged floodplain
arcpy.AddMessage("Calculating euclidean distance to floodplain...")
arcpy.gp.EucDistance_sa(floodplain_feature, floodplain_dist, "", cell_size, "")

# Delete intermediate files
arcpy.Delete_management(arctic_floodplain)
arcpy.Delete_management(boreal_floodplain)
arcpy.Delete_management(stream_3)
arcpy.Delete_management(stream_4)
arcpy.Delete_management(stream_5)
arcpy.Delete_management(stream_6)
arcpy.Delete_management(stream_7)
arcpy.Delete_management(stream_8)
arcpy.Delete_management(stream_9)
arcpy.Delete_management(floodplain_merge)
arcpy.Delete_management(floodplain_dissolve)