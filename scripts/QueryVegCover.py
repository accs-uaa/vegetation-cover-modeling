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

# Define the taxon to be queried
taxon = arcpy.GetParameterAsText(4)

# Define the workspace folder
workspace_folder = arcpy.GetParameterAsText(5)

# Define the workspace geodatabase
workspace_geodatabase = arcpy.GetParameterAsText(6)

# Define the output feature class
query_output = arcpy.GetParameterAsText(7)

# Define intermediate files
temp_csv = os.path.join(workspace_folder, "database_export.csv")
temp_feature = os.path.join(workspace_geodatabase, "database_export")

# Set up the MySQL connection
arcpy.AddMessage("Initializing database connection...")
connection = mysql.connector.connect(user = database_user, password = database_password, host = database_host, database = database_name)
cursor = connection.cursor()

# Set up query
single_query = ("""SELECT abundance.abundanceID as 'ID'
, project.shortName as 'project'
, site.siteCode as 'siteCode'
, methodSurvey.methodSurvey as 'methodSurvey'
, methodCover.methodCover as 'methodCover'
, abundance.vegObserveDate as 'date'
, personnel1.name as 'vegObserver1'
, personnel2.name as 'vegObserver2'
, site.latitude as 'latitude'
, site.longitude as 'longitude'
, datum.datum as 'datum'
, speciesAccepted.nameAccepted as 'nameAccepted'
, speciesAccepted.tsnAccepted as 'tsnITIS'
, abundance.cover as 'cover'
FROM abundance
 JOIN site ON abundance.siteID = site.siteID
 JOIN method ON site.methodID = method.methodID
 JOIN methodSurvey ON method.methodSurveyID = methodSurvey.methodSurveyID
 JOIN methodCover ON method.methodCoverID = methodCover.methodCoverID
 JOIN project ON abundance.projectID = project.projectID
 JOIN speciesAdjudicated ON abundance.adjudicatedID = speciesAdjudicated.adjudicatedID
 JOIN speciesAccepted ON speciesAdjudicated.acceptedID = speciesAccepted.acceptedID
 JOIN datum ON site.datumID = datum.datumID
 JOIN personnel personnel1 ON abundance.vegObserver1ID = personnel1.personnelID
 LEFT JOIN personnel personnel2 ON abundance.vegObserver2ID = personnel2.personnelID
WHERE speciesAccepted.nameAccepted = %s""")

# Execute query and fetch results
arcpy.AddMessage("Pushing query results to output...")
cursor.execute(single_query, (taxon,))
result = cursor.fetchall()

# Create column names as a list
column_names = [column[0] for column in cursor.description]

# Write column names and results to temporary csv file
csv_output = open(temp_csv, 'w')
csv_writer = csv.writer(csv_output, lineterminator = '\n')
csv_writer.writerow(column_names)
csv_writer.writerows(result)
csv_output.close()

# Close MySQL connection
cursor.close()
connection.close()
	
# Set the spatial references (4269 is GCS_North_American_1983; 3338 is NAD_1983_Alaska_Albers)
geographic = arcpy.SpatialReference(4269)
projected = arcpy.SpatialReference(3338)

# Convert csv data to feature class
arcpy.management.XYTableToPoint(temp_csv, temp_feature, "longitude", "latitude", "", geographic)
arcpy.Project_management(temp_feature, query_output, projected)

# Add XY Coordinates to feature class in the NAD_1983_Alaska_Albers projection
arcpy.AddXY_management(query_output)

# Delete intermediate files
arcpy.Delete_management(temp_feature)
if os.path.exists(temp_csv):
    os.remove(temp_csv)