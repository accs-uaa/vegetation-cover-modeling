# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Calculate foliar cover correlation among species
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Last Updated: 2019-11-25
# Usage: Script should be executed in R 3.6.1+.
# Description: "Calculate foliar cover correlation among species" calculates and plots the correlation (r) among species for both observed and predicted foliar cover.
# ---------------------------------------------------------------------------

# Import required libraries
library(dplyr)
library(tidyr)
library(PerformanceAnalytics)

# Import data
ca_file = 'E:/VegetationEcology/Data_Harmonization/Project_GIS/Data_Output/modelResults/carex_aquatilis/prediction.csv'
ea_file = 'E:/VegetationEcology/Data_Harmonization/Project_GIS/Data_Output/modelResults/eriophorum_angustifolium/prediction.csv'
ev_file = 'E:/VegetationEcology/Data_Harmonization/Project_GIS/Data_Output/modelResults/eriophorum_vaginatum/prediction.csv'
rt_file = 'E:/VegetationEcology/Data_Harmonization/Project_GIS/Data_Output/modelResults/rhododendron_tomentosum/prediction.csv'
sp_file = 'E:/VegetationEcology/Data_Harmonization/Project_GIS/Data_Output/modelResults/salix_pulchra/prediction.csv'
vv_file = 'E:/VegetationEcology/Data_Harmonization/Project_GIS/Data_Output/modelResults/vaccinium_vitisidaea/prediction.csv'
ca_predictions = read.csv(ca_file, header=TRUE, stringsAsFactors = FALSE)
ea_predictions = read.csv(ea_file, header=TRUE, stringsAsFactors = FALSE)
ev_predictions = read.csv(ev_file, header=TRUE, stringsAsFactors = FALSE)
rt_predictions = read.csv(rt_file, header=TRUE, stringsAsFactors = FALSE)
sp_predictions = read.csv(sp_file, header=TRUE, stringsAsFactors = FALSE)
vv_predictions = read.csv(vv_file, header=TRUE, stringsAsFactors = FALSE)

# Define a function to filter predictions for AIM NPR-A
filterAIM = function(predictions) {
  predictions_aim = predictions %>%
    filter(project == 'AIM NPR-A')
  predictions_aim$prediction[predictions_aim$prediction < 0] = 0
  return(predictions_aim)
}

# Filter predictions from AIM NPR-A
ca_aim = meanAIM(ca_predictions)
ea_mean = meanAIM(ea_predictions)
ev_mean = meanAIM(ev_predictions)
rt_mean = meanAIM(rt_predictions)
sp_mean = meanAIM(sp_predictions)
vv_mean = meanAIM(vv_predictions)

# Rename columns
ca_aim = ca_aim %>%
  rename(ca_cover=cover) %>%
  rename(ca_prediction=prediction)
ev_aim = ev_aim %>%
  rename(ev_cover=cover) %>%
  rename(ev_prediction=prediction)
rt_aim = rt_aim %>%
  rename(rt_cover=cover) %>%
  rename(rt_prediction=prediction)
sp_aim = sp_aim %>%
  rename(sp_cover=cover) %>%
  rename(sp_prediction=prediction)
vv_aim = vv_aim %>%
  rename(vv_cover=cover) %>%
  rename(vv_prediction=prediction)

# Combine predictions for EV, RT, and VV into a single data frame
data_all = inner_join(ca_aim, ev_aim, by='siteID')
data_all = inner_join(data_all, rt_aim, by='siteID')
data_all = inner_join(data_all, sp_aim, by='siteID')
data_all = inner_join(data_all, vv_aim, by='siteID')

# Create cover data frame
data_cover = data_all %>%
  select(siteID, ca_cover, ev_cover, rt_cover, sp_cover, vv_cover)

# Create prediction data frame
data_prediction = data_all %>%
  select(siteID, ca_prediction, ev_prediction, rt_prediction, sp_prediction, vv_prediction)

# Test Pearson correlation for original observations
chart.Correlation(data_cover[2:6], histogram = TRUE, method = 'pearson')

# Test Pearson correlation for predictions
chart.Correlation(data_prediction[2:6], histogram = TRUE, method = 'pearson')