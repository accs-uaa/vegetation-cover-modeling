# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Distance to Streams (Large and Small)
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Created on: 2018-06-26
# Usage: Must be executed as an ArcPy Script.
# Description: "Distance to Streams (Large and Small)" processes a Digital Elevation Model into a stream network attributed with stream order and then segregates streams of orders 3-9 (large streams) from streams of orders 1-2 (small streams). The euclidean distance to each type of stream is calculated and output as an integer distance raster. The stream network is also output as a feature class. The hydrographic area of influence must be larger than the study area to account for flow that enters the study area and influences stream order.
# ---------------------------------------------------------------------------

# Import python libraries
import arcpy
import os
from arcpy.sa import *

# Set overwrite option
arcpy.env.overwriteOutput = True

# Define input digital elevation model for Alaska
input_dem = arcpy.GetParameterAsText(0)

# Define hydrographic area of influence
area_of_influence = arcpy.GetParameterAsText(1)

# Define study area
study_area = arcpy.GetParameterAsText(2)

# Define the cell size
cell_size = arcpy.GetParameterAsText(3)

# Select the TauDEM Toolbox
TauDEM = arcpy.GetParameterAsText(4)

# Define the input number of processes
processes_number = arcpy.GetParameterAsText(5)

# Define workspace folder
work_folder = arcpy.GetParameterAsText(6)

# Define workspace geodatabase
work_geodatabase = arcpy.GetParameterAsText(7)

# Define output stream network feature class
stream_network = arcpy.GetParameterAsText(8)

# Define output distance to large streams raster
large_stream_dist = arcpy.GetParameterAsText(9)

# Define output distance to small streams raster
small_stream_dist = arcpy.GetParameterAsText(10)

# Import TauDEM Toolbox
arcpy.ImportToolbox(TauDEM, "TauDEM")

# Set the snap raster and cell size environments
arcpy.env.snapRaster = input_dem
arcpy.env.cellSize = cell_size

# Define intermediate variables
influence_dem = os.path.join(work_folder, "influence_dem.tif")
influence_dem_fel = os.path.join(work_folder, "influence_dem_fel.tif")
influence_dem_sd8 = os.path.join(work_folder, "influence_dem_sd8.tif")
influence_dem_p = os.path.join(work_folder, "influence_dem_p.tif")
influence_dem_ad8 = os.path.join(work_folder, "influence_dem_ad8.tif")
influence_dem_ss = os.path.join(work_folder, "influence_dem_ss.tif")
influence_dem_ssa = os.path.join(work_folder, "influence_dem_ssa.tif")
influence_dem_drp = os.path.join(work_folder, "influence_dem_drp.txt")
influence_dem_src = os.path.join(work_folder, "influence_dem_src.tif")
influence_dem_ord = os.path.join(work_folder, "influence_dem_ord.tif")
influence_dem_coord = os.path.join(work_folder, "influence_dem_coord.txt")
influence_dem_net = os.path.join(work_folder, "influence_dem_net.shp")
influence_dem_tree = os.path.join(work_folder, "influence_dem_tree.txt")
influence_dem_w = os.path.join(work_folder, "influence_dem_w.tif")
large_stream_line = os.path.join(work_geodatabase, "large_stream_line")
small_stream_line = os.path.join(work_geodatabase, "small_stream_line")

# Extract digital elevation model for Alaska to hydrographic area of influence
arcpy.AddMessage("Extracting raster to area of interest...")
outExtract = ExtractByMask(input_dem, area_of_influence)
arcpy.CopyRaster_management(outExtract, influence_dem, "", "", "", "NONE", "NONE", "16_BIT_SIGNED", "NONE", "NONE", "TIFF", "NONE")

# Run "Pit Remove" function from TauDEM
arcpy.AddMessage("Running pit remove...")
arcpy.PitRemove_TauDEM(influence_dem, "", "", processes_number, influence_dem_fel)

# Run "D8 Flow Direction" function from TauDEM
arcpy.AddMessage("Running D8 flow direction...")
arcpy.D8FlowDir_TauDEM(influence_dem_fel, processes_number, influence_dem_p, influence_dem_sd8)

# Run "D8 Contributing Area" function from TauDEM
arcpy.AddMessage("Running D8 contributing area...")
arcpy.D8ContributingArea_TauDEM(influence_dem_p, "", "", "true", processes_number, influence_dem_ad8)

# Run "Peuker Douglas Stream Definition" function from TauDEM
arcpy.AddMessage("Running Peuker Douglas stream definition...")
arcpy.PeukerDouglasStreamDef_TauDEM(influence_dem_fel, influence_dem_p, "0.4", "0.1", "0.05", "50", "false", "", "", influence_dem_ad8, processes_number, influence_dem_ss, influence_dem_ssa, influence_dem_src, influence_dem_drp, "true", "5", "500", "10", "true")

# Run "Stream Reach And Watershed" function from TauDEM
arcpy.AddMessage("Running stream reach and watershed...")
arcpy.StreamReachAndWatershed_TauDEM(influence_dem_fel, influence_dem_p, influence_dem_ad8, influence_dem_src, "", "false", processes_number, influence_dem_ord, influence_dem_tree, influence_dem_coord, influence_dem_net, influence_dem_w)

# Define the projection of the stream network output to match the input Digital Elevation Model
projection = arcpy.Describe(input_dem).spatialReference
arcpy.DefineProjection_management(influence_dem_net, projection)

# Clip stream network to study area polygon
arcpy.AddMessage("Clipping stream network to study area...")
arcpy.Clip_analysis(influence_dem_net, study_area, stream_network)

# Make a feature layer from the stream network
arcpy.AddMessage("Selecting large and small streams from stream network...")
arcpy.MakeFeatureLayer_management(influence_dem_net, "influence_dem_net_layer", "", "", "")

# Select large streams (orders 3-9) from the full extent stream network and copy to new feature class
arcpy.SelectLayerByAttribute_management("influence_dem_net_layer", "NEW_SELECTION", "\"strmOrder\" IN (3, 4, 5, 6, 7, 8, 9)")
arcpy.CopyFeatures_management("influence_dem_net_layer", large_stream_line, "", "0", "0", "0")

# Select small streams (orders 1-2) from the full extent stream network and copy to new feature class
arcpy.SelectLayerByAttribute_management("influence_dem_net_layer", "NEW_SELECTION", "\"strmOrder\" IN (1, 2)")
arcpy.CopyFeatures_management("influence_dem_net_layer", small_stream_line, "", "0", "0", "0")

# Calculate the Euclidean Distance from large streams
arcpy.AddMessage("Calculating euclidean distance to large streams...")
extent = arcpy.Describe(study_area).extent
arcpy.env.extent = extent
arcpy.gp.EucDistance_sa(large_stream_line, large_stream_dist, "", cell_size, "")

# Calculate the Euclidean Distance from small streams
arcpy.AddMessage("Calculating euclidean distance to small streams...")
arcpy.gp.EucDistance_sa(small_stream_line, small_stream_dist, "", cell_size, "")

# Delete intermediate files
arcpy.Delete_management(influence_dem)
arcpy.Delete_management(influence_dem_fel)
arcpy.Delete_management(influence_dem_sd8)
arcpy.Delete_management(influence_dem_p)
arcpy.Delete_management(influence_dem_ad8)
arcpy.Delete_management(influence_dem_ss)
arcpy.Delete_management(influence_dem_ssa)
if os.path.exists(influence_dem_drp) == True:
    os.remove(influence_dem_drp)
arcpy.Delete_management(influence_dem_src)
if os.path.exists(influence_dem_coord) == True:
    os.remove(influence_dem_coord)
arcpy.Delete_management(influence_dem_ord)
arcpy.Delete_management(influence_dem_net)
if os.path.exists(influence_dem_tree) == True:
    os.remove(influence_dem_tree)
arcpy.Delete_management(influence_dem_w)
arcpy.Delete_management(large_stream_line)
arcpy.Delete_management(small_stream_line)