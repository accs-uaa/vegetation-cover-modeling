# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Convert Predictions to Raster
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Created on: 2018-09-09
# Usage: Must be executed as an R script in R, RStudio, or RStudio Server. This script has been designed to run in RStudio Server on a Google Cloud virtual machine with 4 vCPUs and 16 GB of CPU memory with an Ubuntu operating system (18.04 LTS).
# Description: "Convert Predictions to Raster" processes the composite predictions in csv tables into rasters and mosaics all raster tiles into a single output.
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
predictions_folder = readline(prompt='Enter location of predictions directory: ')
rasters_folder = readline(prompt='Enter location of directory to store raster tiles: ')
final_raster = readline(prompt='Enter file path and name of final raster: ')

# # Generate a list of all predictions in the predictions directory
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

# Generate a list of all raster tiles in rasters directory
rasters_list = list.files(rasters_folder, pattern='img$', full.names=TRUE)
rasters_length = length(rasters_list)

# Merge raster tiles
raster_1 = raster(rasters_list[1])
raster_2 = raster(rasters_list[2])
print('Merging rasters 1 and 2...')
merge_raster = merge(raster_1, raster_2)
for (count in 3:rasters_length) {
  print(paste('Adding raster ', count, ' of ', rasters_length, '...', sep=''))
  raster_add = raster(rasters_list[count])
  merge_raster = merge(merge_raster, raster_add)
}

# Export merged raster
writeRaster(merge_raster, final_raster, format='HFA')