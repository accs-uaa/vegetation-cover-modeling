# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Calculate mean foliar cover
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Last Updated: 2019-11-25
# Usage: Script should be executed in R 3.6.1+.
# Description: "Calculate mean foliar cover" calculates the mean and standard deviation of foliar cover from AIM observations per species.

# Import libraries
library(dplyr)

# Define data directory
data_directory = 'N:/ACCS_Work/Projects/VegetationEcology/Data_Harmonization/Project_GIS/Data_Output/modelResults/'

# Set data files
ca_file = paste(data_directory, 'carex_aquatilis/prediction.csv', sep='')
ea_file = paste(data_directory, 'eriophorum_angustifolium/prediction.csv', sep='')
ev_file = paste(data_directory, 'eriophorum_vaginatum/prediction.csv', sep='')
rt_file = paste(data_directory, 'rhododendron_tomentosum/prediction.csv', sep='')
sp_file = paste(data_directory, 'salix_pulchra/prediction.csv', sep='')
vv_file = paste(data_directory, 'vaccinium_vitisidaea/prediction.csv', sep='')

# Define a function to filter data to AIM presenceobservations
aimFilter = function(input_file) {
  input_data = read.csv(input_file, header=TRUE, stringsAsFactors=FALSE)
  input_aim = input_data %>%
    filter(project == 'AIM NPR-A')
  return(input_aim)
}

# Filter input data to AIM observations only
ca_aim = aimFilter(ca_file)
ea_aim = aimFilter(ea_file)
ev_aim = aimFilter(ev_file)
rt_aim = aimFilter(rt_file)
sp_aim = aimFilter(sp_file)
vv_aim = aimFilter(vv_file)

# Analyze the mean and standard deviation for presences
print('Carex aquatilis: ')
mean(ca_aim$cover)
sd(ca_aim$cover)
print('Eriophorum angustifolium: ')
mean(ea_aim$cover)
sd(ea_aim$cover)
print('Eriophorum vaginatum: ')
mean(ev_aim$cover)
sd(ev_aim$cover)
print('Rhododendron tomentosum: ')
mean(rt_aim$cover)
sd(rt_aim$cover)
print('Salix pulchra: ')
mean(sp_aim$cover)
sd(sp_aim$cover)
print('Vaccinium vitis-idaea: ')
mean(vv_aim$cover)
sd(vv_aim$cover)