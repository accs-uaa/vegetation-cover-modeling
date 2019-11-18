# Import required libraries
library(dplyr)
library(ggplot2)
library(ggpmisc)
library(readxl)
library(tidyr)
library(gridExtra)
library(scales)

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

# Define a function to calculate mean predictions for AIM NPR-A
meanAIM = function(predictions) {
  predictions_aim = predictions %>%
    filter(project == 'AIM NPR-A') %>%
    group_by(siteID, cover) %>%
    summarize(prediction = mean(prediction))
  return(predictions_aim)
}

# Find mean predictions from AIM NPR-A
ca_mean = meanAIM(ca_predictions)
ea_mean = meanAIM(ea_predictions)
ev_mean = meanAIM(ev_predictions)
rt_mean = meanAIM(rt_predictions)
sp_mean = meanAIM(sp_predictions)
vv_mean = meanAIM(vv_predictions)

# Define function for line histogram
line_histogram = function(inData, x_variable, title, x_label, y_label) {
  scale_max = max(x_variable)
  font_size = theme(axis.title = element_text(size=12), axis.text = element_text(size = 10))
  breaks = c(0, 0.9, 10, 25, 50, scale_max)
  plot = ggplot(data=inData, aes(x=x_variable)) +
    theme_bw() +
    theme(axis.text.x = element_text(color= "black")) +
    theme(axis.text.y = element_text(color= "black")) +
    theme(axis.title.x = element_text(margin = margin(t=10))) +
    theme(axis.title.y = element_text(margin = margin(r=10))) +
    theme(plot.title = element_text(hjust = 0.5, face="italic")) +
    geom_histogram(breaks=breaks, color='grey45',
                   alpha=0.3,
                   aes(x=x_variable, y=(..count..)/183)) +
    geom_freqpoly(binwidth=1,
                  aes(x=x_variable, y=(..count..)/183)) +
    labs(title=title) +
    labs(x=x_label, y=y_label) +
    scale_x_continuous(breaks=seq(20, 100, by=20), limits=c(0,100)) +
    scale_y_continuous(breaks=seq(0, 0.6, by=0.1), limits=c(0,0.6)) +
    font_size
  return(plot)
}

# Plot each species
ca_plot = line_histogram(ca_mean, ca_mean$cover, 'Carex aquatilis', 'Foliar cover (%)', 'Smoothed observation density')
ea_plot = line_histogram(ea_mean, ea_mean$cover, 'Eriophorum angustifolium', 'Foliar cover (%)', 'Smoothed observation density')
ev_plot = line_histogram(ev_mean, ev_mean$cover, 'Eriophorum vaginatum', 'Foliar cover (%)', 'Smoothed observation density')
rt_plot = line_histogram(rt_mean, rt_mean$cover, 'Rhododendron tomentosum', 'Foliar cover (%)', 'Smoothed observation density')
sp_plot = line_histogram(sp_mean, sp_mean$cover, 'Salix pulchra', 'Foliar cover (%)', 'Smoothed observation density')
vv_plot = line_histogram(vv_mean, vv_mean$cover, 'Vaccinium vitis-idaea', 'Foliar cover (%)', 'Smoothed observation density')

# Combine plots into a single output and export
output = 'E:/VegetationEcology/Data_Harmonization/Documents/Figures/Fig5.tif'
plot_grid = grid.arrange(ca_plot, ea_plot, ev_plot, rt_plot, sp_plot, vv_plot, nrow=3)
ggsave(output, plot=plot_grid, device='tiff', path=NULL, scale=1, width=8, height=10, units='in', dpi=600, limitsize=TRUE)