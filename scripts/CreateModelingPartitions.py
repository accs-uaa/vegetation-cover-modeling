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

# Define output feature class of mapping data
mapping_classification = arcpy.GetParameterAsText(2)

# Define output feature class of training data
training_classification = arcpy.GetParameterAsText(3)

# Define output feature class of test data
test_classification = arcpy.GetParameterAsText(4)

# Define intermediate files
all_absences = os.path.join(workspace_geodatabase, "all_absences")
all_presences = os.path.join(workspace_geodatabase, "all_presences")
absences_dissolve = os.path.join(workspace_geodatabase, "absences_dissolve")
absences_random = os.path.join(workspace_geodatabase, "absences_random")
absences_mapping = os.path.join(workspace_geodatabase, "absences_mapping")
absences_test = os.path.join(workspace_geodatabase, "absences_test")
absences_train = os.path.join(workspace_geodatabase, "absences_train")

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

# Segregrate a feature class of all presence sites
arcpy.AddMessage("Segregating presence sites...")
arcpy.MakeFeatureLayer_management(taxon_data, "taxon_data_layer")
arcpy.SelectLayerByAttribute_management ("taxon_data_layer", "NEW_SELECTION", "presence = 1")
arcpy.CopyFeatures_management("taxon_data_layer", all_presences)

# Determine number of presence records and calculate target number of absence records
presenceCount = int(arcpy.GetCount_management(all_presences)[0])
absenceCount = int(presenceCount * 1.5)

# Segregate a feature class of all absence sites
arcpy.AddMessage("Performing random selection of absence sites...")
arcpy.SelectLayerByAttribute_management ("taxon_data_layer", "NEW_SELECTION", "presence = 0")
arcpy.CopyFeatures_management("taxon_data_layer", all_absences)

# Dissolve absences into a single multipart feature and randomly select number of absences based on calculated absence count
arcpy.Dissolve_management(all_absences, absences_dissolve, "", "", "MULTI_PART", "DISSOLVE_LINES")
arcpy.CreateRandomPoints_management(workspace_geodatabase, "absences_random", absences_dissolve, "0 0 250 250", absenceCount, "1000 Meters", "POINT", "0")
arcpy.MakeFeatureLayer_management(all_absences, "absenceLayer")
arcpy.SelectLayerByLocation_management("absenceLayer", "INTERSECT", absences_random, "", "NEW_SELECTION", "NOT_INVERT")
arcpy.CopyFeatures_management("absenceLayer", absences_mapping)

# Partition the randomly selected absence data using the partition function
arcpy.AddMessage("Partitioning randomly selected absence sites...")
arcpy.MakeFeatureLayer_management(absences_mapping, "absences_mapping_layer")
absenceQuery = "presence = 0"
partitionData("absences_mapping_layer", absenceQuery, absences_train, absences_test)

# Create lists for mapping, training, and test sets
mapping_list = [absences_mapping, all_presences]
train_list = [absences_train, ]
test_list = [absences_test, ]

# Iterate through all presence strata to partition the data into mapping, training, and test sets
arcpy.AddMessage("Partitioning presence sites by strata...")
arcpy.MakeFeatureLayer_management(all_presences, "presences_layer")
i = 1
while i < 5:
    filename = "strata_" + str(i)
    strataTrain = os.path.join(workspace_geodatabase, filename + "_train")
    strataTest = os.path.join(workspace_geodatabase, filename + "_test")
    queryStrata = "strata = " + str(i)
    partitionData("presences_layer", queryStrata, strataTrain, strataTest)
    train_list.append(strataTrain)
    test_list.append(strataTest)
    i = i + 1

# Merge mapping, training, and test partition datasets
arcpy.AddMessage("Merging mapping, training, and test partition datasets...")
arcpy.Merge_management(mapping_list, mapping_data)
arcpy.Merge_management(train_list, training_data)
arcpy.Merge_management(test_list, test_data)

# Delete intermediate files
arcpy.Delete_management(all_absences)
arcpy.Delete_management(absences_dissolve)
arcpy.Delete_management(absences_random)
for feature in mapping_list:
    arcpy.Delete_management(feature)
for feature in train_list:
    arcpy.Delete_management(feature)
for feature in test_list:
    arcpy.Delete_management(feature)