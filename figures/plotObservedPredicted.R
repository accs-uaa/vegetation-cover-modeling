# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Plot observed vs mean predicted foliar cover by species
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Last Updated: 2019-11-25
# Usage: Script should be executed in R 3.6.1+.
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
data_directory = 'N:/ACCS_Work/Projects/VegetationEcology/Data_Harmonization/Project_GIS/Data_Output/modelResults/'

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

# Define a function to filter predictions for AIM NPR-A
filterAIM = function(predictions, species_name) {
  predictions_aim = predictions %>%
    filter(project == 'AIM NPR-A')
  predictions_aim$species = species_name
  predictions_aim$prediction[predictions_aim$prediction < 0] = 0
  return(predictions_aim)
}

# Filter predictions from AIM NPR-A
ca_aim = filterAIM(ca_predictions, 'Carex aquatilis')
ea_aim = filterAIM(ea_predictions, 'Eriophorum angustifolium')
ev_aim = filterAIM(ev_predictions, 'Eriophorum vaginatum')
rt_aim = filterAIM(rt_predictions, 'Rhododendron tomentosum')
sp_aim = filterAIM(sp_predictions, 'Salix pulchra')
vv_aim = filterAIM(vv_predictions, 'Vaccinium vitis-idaea')

# Merge mean data frames
aim_predictions = do.call('rbind', list(ca_aim, ea_aim, ev_aim, rt_aim, sp_aim, vv_aim))

# Plot all species
x_max = max(aim_predictions$cover)
y_max = max(aim_predictions$prediction)
font = theme(strip.text = element_text(size=14, color='black', face='italic'),
             strip.background = element_rect(color = 'black', fill = 'white'),
             axis.text = element_text(size = 12),
             axis.text.x = element_text(color= 'black'),
             axis.text.y = element_text(color= 'black'),
             axis.title = element_text(size=14),
             axis.title.x = element_text(margin = margin(t=10)),
             axis.title.y = element_text(margin = margin(r=10))
             )
mean_plot = ggplot(data=aim_predictions, aes(x=cover, y=prediction)) +
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
tif_output = 'N:/ACCS_Work/Projects/VegetationEcology/Data_Harmonization/Documents/GradientCover_EcologicalApplications/Figures/Fig3.jpg'
ggsave(tif_output, plot=mean_plot, device='jpeg', path=NULL, scale=1, width=8, height=8, units='in', dpi=600, limitsize=TRUE)