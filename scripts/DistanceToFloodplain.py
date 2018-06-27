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

# Define workspace folder
work_folder = arcpy.GetParameterAsText(6)

# Define workspace geodatabase
work_geodatabase = arcpy.GetParameterAsText(7)

# Define output floodplain feature class
floodplain = arcpy.GetParameterAsText(8)

# Define output distance to floodplain raster
floodplain_dist = arcpy.GetParameterAsText(9)



# Process: Make Feature Layer (4)
arcpy.MakeFeatureLayer_management(Input_National_Hydrography_Dataset_Flowlines_Alaska, CYR_AE_C_NationalHydrographyDataset_Layer, "", "", "OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;Permanent_Identifier Permanent_Identifier VISIBLE NONE;FDate FDate VISIBLE NONE;Resolution Resolution VISIBLE NONE;GNIS_ID GNIS_ID VISIBLE NONE;GNIS_Name GNIS_Name VISIBLE NONE;LengthKM LengthKM VISIBLE NONE;ReachCode ReachCode VISIBLE NONE;FlowDir FlowDir VISIBLE NONE;WBArea_Permanent_Identifier WBArea_Permanent_Identifier VISIBLE NONE;FType FType VISIBLE NONE;FCode FCode VISIBLE NONE;Enabled Enabled VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE")

# Process: Select Layer By Attribute (4)
arcpy.SelectLayerByAttribute_management(CYR_AE_C_NationalHydrographyDataset_Layer, "NEW_SELECTION", "GNIS_ID IS NOT NULL")

# Process: Select Layer By Attribute (3)
arcpy.SelectLayerByAttribute_management(CYR_AE_C_NationalHydrographyDataset_GNISID, "REMOVE_FROM_SELECTION", "GNIS_ID = '-1'")

# Process: Copy Features (4)
arcpy.CopyFeatures_management(CYR_AE_C_NationalHydrographyDataset_CanadaRemove, CYR_AE_C_NationalHydrographyDataset_Flowlines_Named, "", "0", "0", "0")

# Process: Dissolve (4)
arcpy.Dissolve_management(CYR_AE_C_NationalHydrographyDataset_Flowlines_Named, CYR_AE_C_NationalHydrographyDataset_Flowlines_NameDiss, "GNIS_ID", "", "MULTI_PART", "DISSOLVE_LINES")

# Process: Simplify Line
arcpy.SimplifyLine_cartography(CYR_AE_C_NationalHydrographyDataset_Flowlines_NameDiss, CYR_AE_C_NationalHydrographyDataset_Flowlines_Simple200, "BEND_SIMPLIFY", "200 Meters", "FLAG_ERRORS", "NO_KEEP", "NO_CHECK", "")

# Process: Make Feature Layer
arcpy.MakeFeatureLayer_management(Input_Northern_Alaska_Subsections, CYR_TES_C_NorthernAlaskaSubsections_Layer, "", "", "OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;FID_NOAK_S FID_NOAK_S VISIBLE NONE;ECOREGION ECOREGION VISIBLE NONE;PHYSIOGRAP PHYSIOGRAP VISIBLE NONE;LITHOLOGY LITHOLOGY VISIBLE NONE;SUBSECTION SUBSECTION VISIBLE NONE;SECTION_ SECTION_ VISIBLE NONE;GEN_GEOL GEN_GEOL VISIBLE NONE;SUBSECT_CO SUBSECT_CO VISIBLE NONE;Soil_Lands Soil_Lands VISIBLE NONE;Elev_ave_N Elev_ave_N VISIBLE NONE;PRISM_ave_ PRISM_ave_ VISIBLE NONE;Biome Biome VISIBLE NONE;Eco_Landsc Eco_Landsc VISIBLE NONE;FID_noak2 FID_noak2 VISIBLE NONE;flag flag VISIBLE NONE;ORIG_FID ORIG_FID VISIBLE NONE;Shape_Leng Shape_Leng VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE;Shape_Area Shape_Area VISIBLE NONE")

# Process: Select Layer By Attribute
arcpy.SelectLayerByAttribute_management(CYR_TES_C_NorthernAlaskaSubsections_Layer, "NEW_SELECTION", "PHYSIOGRAP = 'Floodplain'")

# Process: Copy Features
arcpy.CopyFeatures_management(CYR_TES_C_NorthernAlaskaSubsections_Layer__2_, CYR_TES_C_NorthernAlaskaSubsections_Floodplains, "", "0", "0", "0")

# Process: Dissolve (3)
arcpy.Dissolve_management(CYR_TES_C_NorthernAlaskaSubsections_Floodplains, CYR_TES_C_NorthernAlaskaSubsections_Floodplains_Diss, "", "", "MULTI_PART", "DISSOLVE_LINES")

# Process: Erase
arcpy.Erase_analysis(Input_Circumboreal_Vegetation_Map, Input_Northern_Alaska_Subsections, CYR_TES_C_CircumborealVegetationMap_Erase, "")

# Process: Make Feature Layer (2)
arcpy.MakeFeatureLayer_management(CYR_TES_C_CircumborealVegetationMap_Erase, CYR_TES_C_CircumborealVegetation_Layer, "", "", "OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;BioClimAdj BioClimAdj VISIBLE NONE;Clim_MAAT Clim_MAAT VISIBLE NONE;Clim_GrowDD5 Clim_GrowDD5 VISIBLE NONE;Clim_MAP Clim_MAP VISIBLE NONE;Clim_Cont Clim_Cont VISIBLE NONE;Physiography Physiography VISIBLE NONE;Elev_m Elev_m VISIBLE NONE;Geology Geology VISIBLE NONE;Permafrost Permafrost VISIBLE NONE;Disturbance Disturbance VISIBLE NONE;Province Province VISIBLE NONE;GeogSector GeogSector VISIBLE NONE;GrowthForm GrowthForm VISIBLE NONE;Formation Formation VISIBLE NONE;FormSectCode FormSectCode VISIBLE NONE;GeogVari GeogVari VISIBLE NONE;Notes Notes VISIBLE NONE;Mapper Mapper VISIBLE NONE;Area_AlbAK Area_AlbAK VISIBLE NONE;Area_AlbAK_km2 Area_AlbAK_km2 VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE;Shape_Area Shape_Area VISIBLE NONE;Shape_length Shape_length VISIBLE NONE;Shape_area Shape_area VISIBLE NONE")

# Process: Select Layer By Attribute (2)
arcpy.SelectLayerByAttribute_management(CYR_TES_C_CircumborealVegetation_Layer, "NEW_SELECTION", "Physiography = 'R'")

# Process: Copy Features (2)
arcpy.CopyFeatures_management(CYR_TES_C_CircumborealVegetation_Layer__3_, CYR_TES_C_CircumborealVegetationMap_Floodplains, "", "0", "0", "0")

# Process: Dissolve (2)
arcpy.Dissolve_management(CYR_TES_C_CircumborealVegetationMap_Floodplains, CYR_TES_C_CircumborealVegetationMap_Floodplains_Diss, "", "", "MULTI_PART", "DISSOLVE_LINES")

# Process: Make Feature Layer (5)
arcpy.MakeFeatureLayer_management(CYR_AE_C_NationalHydrographyDataset_Flowlines_Simple200, CYR_AE_C_NationalHydrography_Named_Layer, "", "", "")

# Process: Select Layer By Attribute (5)
arcpy.SelectLayerByAttribute_management(CYR_AE_C_NationalHydrography_Named_Layer, "NEW_SELECTION", "Shape_Length >= 36000 AND Shape_Length < 100000")

# Process: Copy Features (5)
arcpy.CopyFeatures_management(CYR_AE_C_NationalHydrography_Named_Layer250, CYR_AE_C_NationalHydrographyDataset_Flowlines_Named_250, "", "0", "0", "0")

# Process: Clip (2)
arcpy.Clip_analysis(CYR_AE_C_NationalHydrographyDataset_Flowlines_Named_250, Input_Study_Area_Boundary, CYR_AE_C_NationalHydrographyDataset_Flowlines_250_Clip, "")

# Process: Make Feature Layer (3)
arcpy.MakeFeatureLayer_management(CYR_AE_C_NationalHydrographyDataset_Flowlines_250_Clip, CYR_AE_C_NationalHydrographyDataset_250Clip_Layer, "", "", "")

# Process: Dissolve (5)
arcpy.Dissolve_management(Input_Northern_Alaska_Subsections, CYR_TES_C_NorthernAlaskaSubsections_Diss, "", "", "MULTI_PART", "DISSOLVE_LINES")

# Process: Select Layer By Location
arcpy.SelectLayerByLocation_management(CYR_AE_C_NationalHydrographyDataset_250Clip_Layer, "COMPLETELY_WITHIN", CYR_TES_C_NorthernAlaskaSubsections_Diss, "", "NEW_SELECTION", "NOT_INVERT")

# Process: Delete Features
arcpy.DeleteFeatures_management(CYR_AE_C_NationalHydrographyDataset_250Clip_Layer__4_)

# Process: Copy Features (3)
arcpy.CopyFeatures_management(CYR_AE_C_NationalHydrographyDataset_250Clip_Layer__3_, CYR_AE_C_NationalHydrographyDataset_250Erase, "", "0", "0", "0")

# Process: Buffer (2)
arcpy.Buffer_analysis(CYR_AE_C_NationalHydrographyDataset_250Erase, CYR_AE_C_NationalHydrographyDataset_Flowlines_250Buffer, "250 Meters", "FULL", "ROUND", "ALL", "", "PLANAR")

# Process: Select Layer By Attribute (6)
arcpy.SelectLayerByAttribute_management(CYR_AE_C_NationalHydrography_Named_Layer, "NEW_SELECTION", "Shape_Length >= 100000 AND Shape_Length < 200000")

# Process: Copy Features (6)
arcpy.CopyFeatures_management(CYR_AE_C_NationalHydrography_Named_Layer300, CYR_AE_C_NationalHydrographyDataset_Flowlines_Named_300, "", "0", "0", "0")

# Process: Clip (3)
arcpy.Clip_analysis(CYR_AE_C_NationalHydrographyDataset_Flowlines_Named_300, Input_Study_Area_Boundary, CYR_AE_C_NationalHydrographyDataset_Flowlines_300_Clip, "")

# Process: Make Feature Layer (6)
arcpy.MakeFeatureLayer_management(CYR_AE_C_NationalHydrographyDataset_Flowlines_300_Clip, CYR_AE_C_NationalHydrographyDataset_300Clip_Layer, "", "", "")

# Process: Select Layer By Location (2)
arcpy.SelectLayerByLocation_management(CYR_AE_C_NationalHydrographyDataset_300Clip_Layer, "COMPLETELY_WITHIN", CYR_TES_C_NorthernAlaskaSubsections_Diss, "", "NEW_SELECTION", "NOT_INVERT")

# Process: Delete Features (2)
arcpy.DeleteFeatures_management(CYR_AE_C_NationalHydrographyDataset_300Clip_Layer__2_)

# Process: Copy Features (9)
arcpy.CopyFeatures_management(CYR_AE_C_NationalHydrographyDataset_300Clip_Layer__3_, CYR_AE_C_NationalHydrographyDataset_300Erase, "", "0", "0", "0")

# Process: Buffer (3)
arcpy.Buffer_analysis(CYR_AE_C_NationalHydrographyDataset_300Erase, CYR_AE_C_NationalHydrographyDataset_Flowlines_300Buffer, "300 Meters", "FULL", "ROUND", "ALL", "", "PLANAR")

# Process: Select Layer By Attribute (7)
arcpy.SelectLayerByAttribute_management(CYR_AE_C_NationalHydrography_Named_Layer, "NEW_SELECTION", "Shape_Length >= 200000 AND Shape_Length < 400000")

# Process: Copy Features (7)
arcpy.CopyFeatures_management(CYR_AE_C_NationalHydrography_Named_Layer450, CYR_AE_C_NationalHydrographyDataset_Flowlines_Named_450, "", "0", "0", "0")

# Process: Clip (4)
arcpy.Clip_analysis(CYR_AE_C_NationalHydrographyDataset_Flowlines_Named_450, Input_Study_Area_Boundary, CYR_AE_C_NationalHydrographyDataset_Flowlines_450_Clip, "")

# Process: Make Feature Layer (7)
arcpy.MakeFeatureLayer_management(CYR_AE_C_NationalHydrographyDataset_Flowlines_450_Clip, CYR_AE_C_NationalHydrographyDataset_450Clip_Layer, "", "", "")

# Process: Select Layer By Location (3)
arcpy.SelectLayerByLocation_management(CYR_AE_C_NationalHydrographyDataset_450Clip_Layer, "COMPLETELY_WITHIN", CYR_TES_C_NorthernAlaskaSubsections_Diss, "", "NEW_SELECTION", "NOT_INVERT")

# Process: Delete Features (3)
arcpy.DeleteFeatures_management(CYR_AE_C_NationalHydrographyDataset_450Clip_Layer__2_)

# Process: Copy Features (10)
arcpy.CopyFeatures_management(CYR_AE_C_NationalHydrographyDataset_450Clip_Layer__3_, CYR_AE_C_NationalHydrographyDataset_450Erase, "", "0", "0", "0")

# Process: Buffer (4)
arcpy.Buffer_analysis(CYR_AE_C_NationalHydrographyDataset_450Erase, CYR_AE_C_NationalHydrographyDataset_Flowlines_450Buffer, "450 Meters", "FULL", "ROUND", "ALL", "", "PLANAR")

# Process: Select Layer By Attribute (8)
arcpy.SelectLayerByAttribute_management(CYR_AE_C_NationalHydrography_Named_Layer, "NEW_SELECTION", "Shape_Length >= 400000")

# Process: Copy Features (8)
arcpy.CopyFeatures_management(CYR_AE_C_NationalHydrography_Named_Layer600, CYR_AE_C_NationalHydrographyDataset_Flowlines_Named_600, "", "0", "0", "0")

# Process: Clip (5)
arcpy.Clip_analysis(CYR_AE_C_NationalHydrographyDataset_Flowlines_Named_600, Input_Study_Area_Boundary, CYR_AE_C_NationalHydrographyDataset_Flowlines_600_Clip, "")

# Process: Make Feature Layer (8)
arcpy.MakeFeatureLayer_management(CYR_AE_C_NationalHydrographyDataset_Flowlines_600_Clip, CYR_AE_C_NationalHydrographyDataset_600Clip_Layer, "", "", "")

# Process: Select Layer By Location (4)
arcpy.SelectLayerByLocation_management(CYR_AE_C_NationalHydrographyDataset_600Clip_Layer, "COMPLETELY_WITHIN", CYR_TES_C_NorthernAlaskaSubsections_Diss, "", "NEW_SELECTION", "NOT_INVERT")

# Process: Delete Features (4)
arcpy.DeleteFeatures_management(CYR_AE_C_NationalHydrographyDataset_600Clip_Layer__2_)

# Process: Copy Features (11)
arcpy.CopyFeatures_management(CYR_AE_C_NationalHydrographyDataset_600Clip_Layer__3_, CYR_AE_C_NationalHydrographyDataset_600Erase, "", "0", "0", "0")

# Process: Buffer (5)
arcpy.Buffer_analysis(CYR_AE_C_NationalHydrographyDataset_600Erase, CYR_AE_C_NationalHydrographyDataset_Flowlines_600Buffer, "600 Meters", "FULL", "ROUND", "ALL", "", "PLANAR")

# Process: Merge
arcpy.Merge_management("L:\\REA_Files\\CYR_REA\\CYR_2016_1\\Vector\\Inputs\\geoscientific\\CYR_Geoscientific.gdb\\CYR_TES_C_NorthernAlaskaSubsections_Floodplains_Diss;L:\\REA_Files\\CYR_REA\\CYR_2016_1\\Vector\\Inputs\\geoscientific\\CYR_Geoscientific.gdb\\CYR_TES_C_CircumborealVegetationMap_Floodplains_Diss;L:\\REA_Files\\CYR_REA\\CYR_2016_1\\Vector\\Inputs\\inlandwaters\\CYR_AE_C_NationalHydrographyDataset.gdb\\CYR_AE_C_NationalHydrographyDataset_Flowlines_250Buffer;L:\\REA_Files\\CYR_REA\\CYR_2016_1\\Vector\\Inputs\\inlandwaters\\CYR_AE_C_NationalHydrographyDataset.gdb\\CYR_AE_C_NationalHydrographyDataset_Flowlines_300Buffer;L:\\REA_Files\\CYR_REA\\CYR_2016_1\\Vector\\Inputs\\inlandwaters\\CYR_AE_C_NationalHydrographyDataset.gdb\\CYR_AE_C_NationalHydrographyDataset_Flowlines_450Buffer;L:\\REA_Files\\CYR_REA\\CYR_2016_1\\Vector\\Inputs\\inlandwaters\\CYR_AE_C_NationalHydrographyDataset.gdb\\CYR_AE_C_NationalHydrographyDataset_Flowlines_600Buffer", CYR_TES_C_Floodplains, "BUFF_DIST \"BUFF_DIST\" true true false 0 Double 0 0 ,First,#,L:\\REA_Files\\CYR_REA\\CYR_2016_1\\Vector\\Inputs\\inlandwaters\\CYR_AE_C_NationalHydrographyDataset.gdb\\CYR_AE_C_NationalHydrographyDataset_Flowlines_250Buffer,BUFF_DIST,-1,-1,L:\\REA_Files\\CYR_REA\\CYR_2016_1\\Vector\\Inputs\\inlandwaters\\CYR_AE_C_NationalHydrographyDataset.gdb\\CYR_AE_C_NationalHydrographyDataset_Flowlines_300Buffer,BUFF_DIST,-1,-1,L:\\REA_Files\\CYR_REA\\CYR_2016_1\\Vector\\Inputs\\inlandwaters\\CYR_AE_C_NationalHydrographyDataset.gdb\\CYR_AE_C_NationalHydrographyDataset_Flowlines_450Buffer,BUFF_DIST,-1,-1,L:\\REA_Files\\CYR_REA\\CYR_2016_1\\Vector\\Inputs\\inlandwaters\\CYR_AE_C_NationalHydrographyDataset.gdb\\CYR_AE_C_NationalHydrographyDataset_Flowlines_600Buffer,BUFF_DIST,-1,-1;ORIG_FID \"ORIG_FID\" true true false 0 Long 0 0 ,First,#,L:\\REA_Files\\CYR_REA\\CYR_2016_1\\Vector\\Inputs\\inlandwaters\\CYR_AE_C_NationalHydrographyDataset.gdb\\CYR_AE_C_NationalHydrographyDataset_Flowlines_250Buffer,ORIG_FID,-1,-1,L:\\REA_Files\\CYR_REA\\CYR_2016_1\\Vector\\Inputs\\inlandwaters\\CYR_AE_C_NationalHydrographyDataset.gdb\\CYR_AE_C_NationalHydrographyDataset_Flowlines_300Buffer,ORIG_FID,-1,-1,L:\\REA_Files\\CYR_REA\\CYR_2016_1\\Vector\\Inputs\\inlandwaters\\CYR_AE_C_NationalHydrographyDataset.gdb\\CYR_AE_C_NationalHydrographyDataset_Flowlines_450Buffer,ORIG_FID,-1,-1,L:\\REA_Files\\CYR_REA\\CYR_2016_1\\Vector\\Inputs\\inlandwaters\\CYR_AE_C_NationalHydrographyDataset.gdb\\CYR_AE_C_NationalHydrographyDataset_Flowlines_600Buffer,ORIG_FID,-1,-1")

# Process: Dissolve
arcpy.Dissolve_management(CYR_TES_C_Floodplains, Output_Floodplains, "", "", "MULTI_PART", "DISSOLVE_LINES")

