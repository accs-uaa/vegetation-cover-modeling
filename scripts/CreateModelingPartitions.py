# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Create Modeling Partitions
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Created on: 2018-07-13
# Usage: Must be executed as an ArcPy Script.
# Description: "Create Modeling Partitions" creates a feature class of mapping data using 1.5 times as many absence points, drawn randomly from both the trace cover values and true absences, as presence points. A training feature class is created by partitioning 70% of each strata from the modeling data. A test feature class is created by partitioning the remaining 30% of each strata from the modeling data.
# ---------------------------------------------------------------------------

# Import modules
import arcpy
import os

# Set overwrite option
arcpy.env.overwriteOutput = True

# Define the input feature class containing the formatted taxon data
taxon_data = arcpy.GetParameterAsText(0)

# Define the workspace geodatabase
workspace_geodatabase = arcpy.GetParameterAsText(1)

# Define output feature class of training data
training_data = arcpy.GetParameterAsText(2)

# Define output feature class of test data
test_data = arcpy.GetParameterAsText(3)

# Create a function to create a mapping, training, and test partition for each strata
def partitionData (inLayer, sqlQuery, outTrain, outTest):
    strataFeature = os.path.join(workspace_geodatabase, "strataFeature")
    arcpy.SelectLayerByAttribute_management (inLayer, "NEW_SELECTION", sqlQuery)
    arcpy.CopyFeatures_management(inLayer, strataFeature)
    strataCount = int(arcpy.GetCount_management(strataFeature)[0])
    randomCount = int(strataCount * .7)
    strataDissolve = os.path.join(workspace_geodatabase, "strataDissolve")
    strata70 = os.path.join(workspace_geodatabase, "strata70")
    arcpy.Dissolve_management(strataFeature, strataDissolve, "", "", "MULTI_PART", "DISSOLVE_LINES")
    arcpy.CreateRandomPoints_management(workspace_geodatabase, "strata70", strataDissolve, "0 0 250 250", randomCount, "0 Meters", "POINT", "0")
    arcpy.MakeFeatureLayer_management(strataFeature, "strataLayer")
    arcpy.SelectLayerByLocation_management("strataLayer", "INTERSECT", strata70, "", "NEW_SELECTION", "NOT_INVERT")
    arcpy.CopyFeatures_management("strataLayer", outTrain)
    arcpy.Erase_analysis(strataFeature, outTrain, outTest, "")
    arcpy.Delete_management(strataFeature)
    arcpy.Delete_management(strataDissolve)
    arcpy.Delete_management(strata70)

# Create lists of the partitioned data by strata for the training and test sets
train_list = []
test_list = []

# Iterate through all presence strata to partition the data into mapping, training, and test sets
arcpy.MakeFeatureLayer_management(taxon_data, "taxon_data_layer")
i = 0
while i < 4:
    arcpy.AddMessage("Partitioning sites by strata (part " + str(i + 1) + " out of 4)...")
    filename = "strata_" + str(i)
    strataTrain = os.path.join(workspace_geodatabase, filename + "_train")
    strataTest = os.path.join(workspace_geodatabase, filename + "_test")
    queryStrata = "strata = " + str(i)
    partitionData("taxon_data_layer", queryStrata, strataTrain, strataTest)
    train_list.append(strataTrain)
    test_list.append(strataTest)
    i = i + 1

# Merge mapping, training, and test partition datasets
arcpy.AddMessage("Merging training partition dataset...")
arcpy.Merge_management(train_list, training_data)
arcpy.AddMessage("Merging test partition dataset...")
arcpy.Merge_management(test_list, test_data)

# Delete intermediate files
for feature in train_list:
    arcpy.Delete_management(feature)
for feature in test_list:
    arcpy.Delete_management(feature)