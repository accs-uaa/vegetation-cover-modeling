# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Extract Features to Points
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Created on: 2018-09-08
# Usage: Must be executed as an R script in R, RStudio, or RStudio Server. This script has been designed to run in RStudio Server on a Google Cloud virtual machine with 4 vCPUs and 16 GB of CPU memory with an Ubuntu operating system (18.04 LTS).
# Description: "Extract Features to Points" creates a csv table of predictor variable values for all input watersheds on a regular point grid.
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
watersheds_folder = readline(prompt='Enter location of watersheds directory: ')
predictors_folder = readline(prompt='Enter location of predictors directory: ')
output_folder = readline(prompt='Enter location of output directory: ')

# Enter numerical range to subset the list of watersheds
list_range = 1:28

# Generate a list of all watersheds in the watersheds directory
watersheds_list = list.files(watersheds_folder, pattern='shp$', full.names=TRUE)

# Subset the watersheds list based on the list range
watersheds_list = watersheds_list[list_range]
watersheds_length = length(watersheds_list)

# Generate a stack of all predictor variables
predictors_all = list.files(predictors_folder, pattern='tif$', full.names=TRUE)
predictor_stack = stack(predictors_all)

# Define a function to read a watershed dataframe, extract data, and export to csv
extractPredictorData = function(inWatershed, inStack, outTable) {
  watershed_data = readOGR(dsn=inWatershed)
  watershed_data@data <- data.frame(watershed_data@data, extract(inStack, watershed_data))
  write.csv(watershed_data@data, file=outTable)
}

# Extract predictor data to each watershed in the watersheds directory
count = 1
for (watershed in watersheds_list) {
  print(paste('Extracting predictor data to watershed ', count, ' of ', watersheds_length, '...', sep=''))
  count = count + 1
  output_table = paste(output_folder, '/', sub(pattern = "(.*)\\..*$", replacement = "\\1", basename(watershed)), '.csv', sep='')
  extractPredictorData(watershed, predictor_stack, output_table)
}