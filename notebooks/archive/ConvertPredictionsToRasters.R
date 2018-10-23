# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Convert Predictions to Raster
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Created on: 2018-09-09
# Usage: Must be executed as an R script in R, RStudio, or RStudio Server. This script has been designed to run in RStudio Server on a Google Cloud virtual machine with 4 vCPUs and 16 GB of CPU memory with an Ubuntu operating system (18.04 LTS).
# Description: "Convert Predictions to Raster" processes the composite predictions in csv tables into rasters in img format. Raster outputs are in the same coordinate system that watersheds were exported in but will not be associated with that projection. Rasters should be mosaicked using the "Mosaic to New Raster" tool in ArcGIS after this process.
# ---------------------------------------------------------------------------

# Install required libraries if they are not already installed.
Required_Packages <- c('sp', 'raster', 'rgdal', 'stringr')
New_Packages <- Required_Packages[!(Required_Packages %in% installed.packages()[,"Package"])]
if (length(New_Packages) > 0) {
  install.packages(New_Packages)
}

# Import required libraries for geospatial processing: sp, raster, rgdal, and stringr.
library(sp)
library(raster)
library(rgdal)
library(stringr)

# Capture arguments by user input
predictions_folder = '/home/twnawrocki_rstudio/predictions/prediction_vacciniumvitisidaea'
rasters_folder = '/home/twnawrocki_rstudio/rasters/raster_vacciniumvitisidaea'

# Generate a list of all predictions in the predictions directory
predictions_list = list.files(predictions_folder, pattern='csv$', full.names=TRUE)
predictions_length = length(predictions_list)

# Define a function to convert the prediction csv to a raster and export an img raster file
convertPredictions = function(inTable, outRaster) {
  watershed_data = read.csv(inTable)
  raster_data = watershed_data[,c('POINT_X', 'POINT_Y', 'classification')]
  watershed_raster = rasterFromXYZ(raster_data, res=c(30,30), crs=NA, digits=5)
  writeRaster(watershed_raster, outRaster, format='HFA')
}

# Create img raster file for each prediction table in the predictions directory
count = 1
for (prediction in predictions_list) {
  print(paste('Converting prediction to raster for watershed ', count, ' of ', predictions_length, '...', sep=''))
  count = count + 1
  output_raster = paste(rasters_folder, '/', sub(pattern = "(.*)\\..*$", replacement = "\\1", basename(prediction)), '.img', sep='')
  convertPredictions(prediction, output_raster)
}