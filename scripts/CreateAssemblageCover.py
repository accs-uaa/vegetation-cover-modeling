# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Create Species Assemblage Cover
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Created on: 2018-05-22
# Usage: Must be executed as an ArcPy Script.
# Description: This tool combines points for a user-specified list of taxa and sums the cover values of the inputs.
# ---------------------------------------------------------------------------

# Import modules
import os
import arcpy
from arcpy import env
	
# Set overwrite option
arcpy.env.overwriteOutput = True

# Define the set of input feature classes
input_features = arcpy.GetParameterAsText(0)

# Define text file
text_file = arcpy.GetParameterAsText(1)

# Define output feature class
output_feature = arcpy.GetParameterAsText(2)

# Define the workspace folder
#workspace = arcpy.GetParameterAsText(5)

# Define the output feature class
#query_output = arcpy.GetParameterAsText(6)

# Define intermediate files

# Write text file of multi-value input
text_writer = open(text_file, 'w')
text_writer.write(input_features)
text_writer.write(output_feature)
text_writer.close()

# Convert multi-value input to list
input_features = input_features.split(';')

# Create field mapping for cover
fieldmap_cover = arcpy.FieldMap()
fieldmappings = arcpy.FieldMappings()

# Get the field name for cover
cover_field = "cover"

# Add fields to the field mapping
for input in input_features:
    fieldmap_cover.addInputField(input, cover_field)

# Add the output field
cover_name = fieldmap_cover.outputField
cover_name.name = "cover2"
fieldmap_cover.outputField = cover_name

# Set merge rule to sum
fieldmap_cover.mergeRule = "Sum"

# Add field map to the field mappings object
fieldmappings.addFieldMap(fieldmap_cover)

# Create the output feature class using the field mappings object
arcpy.Merge_management(input features, output_feature, fieldmappings)


