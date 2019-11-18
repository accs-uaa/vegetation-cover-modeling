# Import required libraries
library(dplyr)
library(ggplot2)
library(ggpmisc)
library(readxl)
library(tidyr)
library(gridExtra)
library(scales)
library(BEST)

# Define data directory
data_directory = 'K:/ACCS_Work/Projects/VegetationEcology/Data_Harmonization/Project_GIS/Data_Output/modelResults/'

# Import data
species_file = paste(data_directory, 'carex_aquatilis/prediction.csv', sep='')
species_predictions = read.csv(species_file, header=TRUE, stringsAsFactors = FALSE)

# Define a function to calculate mean cover 
meanAll = function(predictions) {
  predictions_aim = predictions %>%
    filter(project == 'AIM NPR-A') %>%
    group_by(siteID, cover) %>%
    summarize(prediction = mean(prediction))
  return(predictions_aim)
}

# Define a function to calculate mean cover 
meanPresence = function(predictions) {
  predictions_aim = predictions %>%
    filter(project == 'AIM NPR-A') %>%
    filter(cover >= 1) %>%
    group_by(siteID, cover) %>%
    summarize(prediction = mean(prediction))
  return(predictions_aim)
}

# Find mean predictions from AIM NPR-A
mean_all = meanAll(species_predictions)
mean_presence = meanPresence(species_predictions)

# Analyze the mean and standard deviation for all
mean(mean_all$cover)
sd(mean_all$cover)

# Analyze the mean and standard deviation for presences
mean(mean_presence$cover)
sd(mean_presence$cover)