# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Query Vegetation Cover by Species
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Created on: 2018-05-22
# Usage: Must be executed as an ArcPy Script.
# Description: This tool queries the online MySQL Alaska Vegetation Plots Database for a species or a list of species.
# ---------------------------------------------------------------------------

# Import modules
import os
import arcpy
import csv
import mysql.connector
	
# Set overwrite option
arcpy.env.overwriteOutput = True

# Setup database credentials for query
database_user = arcpy.GetParameterAsText(0)
database_password = arcpy.GetParameterAsText(1)
database_host = arcpy.GetParameterAsText(2)
database_name = arcpy.GetParameterAsText(3)

# Define the query type as either a single species query or list query
type = arcpy.GetParameterAsText(4)

# Define the species or species list to be queried
species = arcpy.GetParameterAsText(5)

# Define the workspace
workspace = arcpy.GetParameterAsText(6)

# Define the output feature class
query_output = arcpy.GetParameterAsText(7)

# Set up the MySQL connection
arcpy.AddMessage("Initializing database connection...")
connection = mysql.connector.connect(user = database_user, password = database_password, host = database_host, database = database_name)
cursor = connection.cursor()

# Set up query for single species
single_query = ("SELECT abundance.abundanceID as 'ID'"
", project.shortName as 'project'"
", site.siteCode as 'siteCode'"
", methodSurvey.methodSurvey as 'methodSurvey'"
", methodCover.methodCover as 'methodCover'"
", abundance.vegObserveDate as 'date'"
", personnel1.name as 'vegObserver1'"
", personnel2.name as 'vegObserver2'"
", site.latitude as 'latitude'"
", site.longitude as 'longitude'"
", datum.datum as 'datum'"
", speciesAccepted.nameAccepted as 'nameAccepted'"
", speciesAccepted.tsnAccepted as 'tsnITIS'"
", abundance.cover as 'cover'"
"FROM abundance"
" JOIN site ON abundance.siteID = site.siteID"
" JOIN method ON site.methodID = method.methodID"
" JOIN methodSurvey ON method.methodSurveyID = methodSurvey.methodSurveyID"
" JOIN methodCover ON method.methodCoverID = methodCover.methodCoverID"
" JOIN project ON abundance.projectID = project.projectID"
" JOIN speciesAdjudicated ON abundance.adjudicatedID = speciesAdjudicated.adjudicatedID"
" JOIN speciesAccepted ON speciesAdjudicated.acceptedID = speciesAccepted.acceptedID"
" JOIN datum ON site.datumID = datum.datumID"
" JOIN personnel personnel1 ON abundance.vegObserver1ID = personnel1.personnelID"
" LEFT JOIN personnel personnel2 ON abundance.vegObserver2ID = personnel2.personnelID"
"WHERE speciesAccepted.nameAccepted = %s")

# Set up query for list of species
multiple_query = ("SELECT abundance.abundanceID as 'ID'"
", project.shortName as 'project'"
", site.siteCode as 'siteCode'"
", methodSurvey.methodSurvey as 'methodSurvey'"
", methodCover.methodCover as 'methodCover'"
", abundance.vegObserveDate as 'date'"
", personnel1.name as 'vegObserver1'"
", personnel2.name as 'vegObserver2'"
", site.latitude as 'latitude'"
", site.longitude as 'longitude'"
", datum.datum as 'datum'"
", speciesAccepted.nameAccepted as 'nameAccepted'"
", speciesAccepted.tsnAccepted as 'tsnITIS'"
", abundance.cover as 'cover'"
"FROM abundance"
" JOIN site ON abundance.siteID = site.siteID"
" JOIN method ON site.methodID = method.methodID"
" JOIN methodSurvey ON method.methodSurveyID = methodSurvey.methodSurveyID"
" JOIN methodCover ON method.methodCoverID = methodCover.methodCoverID"
" JOIN project ON abundance.projectID = project.projectID"
" JOIN speciesAdjudicated ON abundance.adjudicatedID = speciesAdjudicated.adjudicatedID"
" JOIN speciesAccepted ON speciesAdjudicated.acceptedID = speciesAccepted.acceptedID"
" JOIN datum ON site.datumID = datum.datumID"
" JOIN personnel personnel1 ON abundance.vegObserver1ID = personnel1.personnelID"
" LEFT JOIN personnel personnel2 ON abundance.vegObserver2ID = personnel2.personnelID"
"WHERE speciesAccepted.nameAccepted IN (%s)")

# Execute query
arcpy.AddMessage("Executing query...")
if type == "single species":
    result = cursor.execute(single_query, (species))
elif type == "species list":
    result = cursor.execute(multiple_query, (species))
else:
    arcpy.AddError("Query type not recognized.")

# Set up csv writer as object
arcpy.AddMessage("Pushing query results to output...")
temp_csv = os.path.join(Workspace, "temp.csv")
c = csv.writer(open(temp_csv,"wb")

# Write rows from result to temporary csv
for row in result:
    c.writerow(row)
	
# Close MySQL connection
cursor.close()
connection.close()
	
# Convert csv data to feature class
arcpy.MakeXYEventLayer_management(temp_csv, "longitude", "latitude", temp_csv_layer, "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision", "")
arcpy.Project_management(temp_csv_layer, query_output, "PROJCS['NAD_1983_Alaska_Albers',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Albers'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-154.0],PARAMETER['Standard_Parallel_1',55.0],PARAMETER['Standard_Parallel_2',65.0],PARAMETER['Latitude_Of_Origin',50.0],UNIT['Meter',1.0]]", "", "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", "NO_PRESERVE_SHAPE", "", "NO_VERTICAL")

# Delete intermediate files
if os.path.exists(temp_csv):
    os.remove(temp_csv)