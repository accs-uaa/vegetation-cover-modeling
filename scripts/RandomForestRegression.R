# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Random Forest Regression with Spatial and Temporal Prediction
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Created on: 2017-10-17
# Usage: Must be executed as an R Script. Script is set up to integrate with python but can be modified to run from an R command interface.
# Description: This tool provides a Random Forest regression with variable selection and best model fit determined using data-driven approaches.
# ---------------------------------------------------------------------------

# Install required libraries if they are not already installed.
Required_Packages = c("randomForest", "rfUtilities", "sp", "raster", "rgdal", "stringr", "ROCR")
New_Packages = Required_Packages[!(Required_Packages %in% installed.packages()[,"Package"])]
if (length(New_Packages) > 0) {
  install.packages(New_Packages)
}

# Import required libraries: randomForest, rfUtilities, sp, raster, rgdal, stringr, ROCR.
library(randomForest)
library(rfUtilities)
library(sp)
library(raster)
library(rgdal)
library(stringr)
library(ROCR)

# Set seed
set.seed(415)

# Set workspace folder from command line input.
Workspace = 'L:\\VegetationEcology\\NorthSlopeDataHarmonization\\Data_SalixPulchra\\Results_SalixPulchra'
setwd(Workspace)

# Import arguments passed by python.
Arguments = read.table("Regression_Arguments.txt", header = FALSE)

# Interpret arguments passed from python.
Predictor_Folder_Model = as.vector(Arguments[,1])
Predictor_Folder_Current = as.vector(Arguments[,2])
Predictor_Folder_Future = as.vector(Arguments[,3])
Species_Shapefile = as.vector(Arguments[,4])
Output_Raster_Current = as.vector(Arguments[,5])
Output_Raster_Future = as.vector(Arguments[,6])
Trees = as.numeric(as.vector(Arguments[,7]))
Permutations = as.numeric(as.vector(Arguments[,8]))

# Create raster stack for model fit
cat("Creating raster stack for fitting model using training data...\n")
Raster_List_Model = list.files(Predictor_Folder_Model, pattern="img$", full.names = TRUE)
Raster_Stack_Model = stack(Raster_List_Model)

# Create current raster stack for spatial prediction.
cat("Creating raster stack for current predictor variables...\n")
Raster_List_Current = list.files(Predictor_Folder_Current, pattern="img$", full.names = TRUE)
Raster_Stack_Current = stack(Raster_List_Current)

# Create future raster stack for spatial and temporal prediction.
cat("Creating raster stack for future predictor variables...\n")
Raster_List_Future = list.files(Predictor_Folder_Future, pattern="img$", full.names = TRUE)
Raster_Stack_Future = stack(Raster_List_Future)

# Convert shapefile into spatial data frame and extract raster data.
cat("Creating species data frame...\n")
Species_Data = readOGR(dsn = Species_Shapefile)
Species_Data@data = data.frame(Species_Data@data, extract(Raster_Stack_Model, Species_Data))

# Perform predictor variable subset selection
Variables = rf.modelSel(x = Species_Data@data[, 2:ncol(Species_Data@data)], y = Species_Data@data[, "Cover"], imp.scale = "mir", ntree = Trees, r = c(0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1))
Selected = Variables$selvars

# Output text file of selected subset of predictor variables
sink("Vars.txt")
cat(Selected)
sink()

# Fit random forest based on subset of predictor variables
Fit = randomForest(x = Species_Data@data[, Selected], y = Species_Data@data[, "Cover"], ntree = Trees, importance = TRUE, norm.votes = TRUE, proximity = TRUE)

# Export graph of all variable importances.
png(file = "plots\\VariableImportance_All.png")
plot(Variables, imp = "all")
dev.off()

# Predict current raster
cat("Exporting current raster...\n")
Raster_Variables_Current = stack(paste(Predictor_Folder_Current, paste(rownames(Fit$importance), "img", sep="."), sep="/"))
predict(Raster_Variables_Current, Fit, Output_Raster_Current, type = "response", index = 2, na.rm = TRUE, overwrite = TRUE, progress = "window")

# Predict future raster.
cat("Exporting future raster...\n")
Raster_Variables_Future = stack(paste(Predictor_Folder_Future, paste(rownames(Fit$importance), "img", sep="."), sep="/"))
predict(Raster_Variables_Future, Fit, Output_Raster_Future, type = "response", index = 2, na.rm = TRUE, overwrite = TRUE, progress = "window")