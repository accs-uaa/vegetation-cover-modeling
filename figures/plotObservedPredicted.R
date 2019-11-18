# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Plot observed vs mean predicted foliar cover by species
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Created on: 2019-03-31
# Usage: Code chunks must be executed sequentially in R Studio or R Studio Server installation. Created using R Studio version 1.1.456 and R 3.5.1.
# Description: "Plot observed vs mean predicted foliar cover by species" creates a plot (Figure 3) showing the observed vs mean predicted values with theoretical 1:1 ratio line and loess smoothed conditional mean.
# ---------------------------------------------------------------------------

# Import required libraries
library(dplyr)
library(ggplot2)
library(ggpmisc)
library(readxl)
library(tidyr)
library(gridExtra)
library(scales)

# Define data directory
data_directory = 'K:/ACCS_Work/Projects/VegetationEcology/Data_Harmonization/Project_GIS/Data_Output/modelResults/'

# Import data
ca_file = paste(data_directory, 'carex_aquatilis/prediction.csv', sep='')
ea_file = paste(data_directory, 'eriophorum_angustifolium/prediction.csv', sep='')
ev_file = paste(data_directory, 'eriophorum_vaginatum/prediction.csv', sep='')
rt_file = paste(data_directory, 'rhododendron_tomentosum/prediction.csv', sep='')
sp_file = paste(data_directory, 'salix_pulchra/prediction.csv', sep='')
vv_file = paste(data_directory, 'vaccinium_vitisidaea/prediction.csv', sep='')
ca_predictions = read.csv(ca_file, header=TRUE, stringsAsFactors = FALSE)
ea_predictions = read.csv(ea_file, header=TRUE, stringsAsFactors = FALSE)
ev_predictions = read.csv(ev_file, header=TRUE, stringsAsFactors = FALSE)
rt_predictions = read.csv(rt_file, header=TRUE, stringsAsFactors = FALSE)
sp_predictions = read.csv(sp_file, header=TRUE, stringsAsFactors = FALSE)
vv_predictions = read.csv(vv_file, header=TRUE, stringsAsFactors = FALSE)

# Define a function to calculate mean predictions for AIM NPR-A
meanAIM = function(predictions, species_name) {
  predictions_aim = predictions %>%
    filter(project == 'AIM NPR-A') %>%
    group_by(siteID, cover) %>%
    summarize(prediction = mean(prediction))
  predictions_aim$species = species_name
  return(predictions_aim)
}

# Find mean predictions from AIM NPR-A
ca_mean = meanAIM(ca_predictions, 'Carex aquatilis')
ea_mean = meanAIM(ea_predictions, 'Eriophorum angustifolium')
ev_mean = meanAIM(ev_predictions, 'Eriophorum vaginatum')
rt_mean = meanAIM(rt_predictions, 'Rhododendron tomentosum')
sp_mean = meanAIM(sp_predictions, 'Salix pulchra')
vv_mean = meanAIM(vv_predictions, 'Vaccinium vitis-idaea')

# Merge mean data frames
mean_predictions = do.call('rbind', list(ca_mean, ea_mean, ev_mean, rt_mean, sp_mean, vv_mean))

# Plot all species
x_max = max(mean_predictions$cover)
y_max = max(mean_predictions$prediction)
font = theme(strip.text = element_text(size=14, color='black', face='italic'),
             strip.background = element_rect(color = 'black', fill = 'white'),
             axis.text = element_text(size = 12),
             axis.text.x = element_text(color= 'black'),
             axis.text.y = element_text(color= 'black'),
             axis.title = element_text(size=14),
             axis.title.x = element_text(margin = margin(t=10)),
             axis.title.y = element_text(margin = margin(r=10))
             )
mean_plot = ggplot(data=mean_predictions, aes(x=cover, y=prediction)) +
  theme_bw() +
  font +
  geom_smooth(method='loess',
              color="#406190",
              fill="#b7c9de",
              size=0.5,
              linetype=2) +
  geom_point(alpha = 0.25) +
  geom_segment(x=0,
               y=0,
               xend=100,
               yend=100,
               size=0.5,
               linetype=1) +
  facet_wrap(~species, ncol=2) +
  labs(x='Observed foliar cover (%)', y='Predicted foliar cover (%)') +
  coord_fixed(ratio=1) +
  scale_x_continuous(breaks=seq(0, 100, by=10), limits=c(0,x_max), expand = c(0.01, 0)) +
  scale_y_continuous(breaks=seq(0, 100, by=10), limits=c(0,y_max), expand = c(0.02, 0))

# Save and export jpg at 600 dpi
tif_output = 'K:/ACCS_Work/Projects/VegetationEcology/Data_Harmonization/Documents/GradientCover_EcologicalApplications/Figures/Fig3.jpg'
ggsave(tif_output, plot=mean_plot, device='jpeg', path=NULL, scale=1, width=8, height=8, units='in', dpi=600, limitsize=TRUE)