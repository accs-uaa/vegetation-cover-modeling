# Import required libraries
library(dplyr)
library(ggplot2)
library(ggpmisc)
library(readxl)
library(tidyr)
library(gridExtra)
library(scales)

# Import data
ca_file = 'K:/VegetationEcology/Data_Harmonization/Project_GIS/Data_Output/modelResults/carex_aquatilis/prediction.csv'
ea_file = 'K:/VegetationEcology/Data_Harmonization/Project_GIS/Data_Output/modelResults/eriophorum_angustifolium/prediction.csv'
ev_file = 'K:/VegetationEcology/Data_Harmonization/Project_GIS/Data_Output/modelResults/eriophorum_vaginatum/prediction.csv'
rt_file = 'K:/VegetationEcology/Data_Harmonization/Project_GIS/Data_Output/modelResults/rhododendron_tomentosum/prediction.csv'
sp_file = 'K:/VegetationEcology/Data_Harmonization/Project_GIS/Data_Output/modelResults/salix_pulchra/prediction.csv'
vv_file = 'K:/VegetationEcology/Data_Harmonization/Project_GIS/Data_Output/modelResults/vaccinium_vitisidaea/prediction.csv'
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

# Define function for scatter plot
scatter_plot = function(inData, x_variable, y_variable, title, x_label, y_label) {
  scale_max = max(x_variable)
  font_size = theme(axis.title = element_text(size=12), axis.text = element_text(size = 10))
  plot = ggplot(data=inData, aes(x=x_variable, y=y_variable)) +
    theme_bw() +
    theme(axis.text.x = element_text(color= "black")) +
    theme(axis.text.y = element_text(color= "black")) +
    theme(axis.title.x = element_text(margin = margin(t=10))) +
    theme(axis.title.y = element_text(margin = margin(r=10))) +
    theme(plot.title = element_text(hjust = 0.5, face="italic")) +
    geom_point() +
    geom_smooth(method='loess',
                color="black",
                fill="grey20",
                size=0.5) +
    geom_segment(x=0,
                 y=0,
                 xend=scale_max,
                 yend=scale_max,
                 size=0.5,
                 linetype=2) +
    labs(title=title) +
    labs(x=x_label, y=y_label) +
    coord_fixed(ratio=1) +
    scale_x_continuous(breaks=seq(20, 100, by=20), limits=c(0,scale_max)) +
    scale_y_continuous(breaks=seq(20, 100, by=20), limits=c(0,scale_max)) +
    font_size
  return(plot)
}

# Plot each species
ca_plot = scatter_plot(ca_mean, ca_mean$cover, ca_mean$prediction, "Carex aquatilis", "Observed foliar cover (%)", "Predicted foliar cover (%)")
ea_plot = scatter_plot(ea_mean, ea_mean$cover, ea_mean$prediction, "Eriophorum angustifolium", "Observed foliar cover (%)", "Predicted foliar cover (%)")
ev_plot = scatter_plot(ev_mean, ev_mean$cover, ev_mean$prediction, "Eriophorum vaginatum", "Observed foliar cover (%)", "Predicted foliar cover (%)")
rt_plot = scatter_plot(rt_mean, rt_mean$cover, rt_mean$prediction, "Rhododendron tomentosum", "Observed foliar cover (%)", "Predicted foliar cover (%)")
sp_plot = scatter_plot(sp_mean, sp_mean$cover, sp_mean$prediction, "Salix pulchra", "Observed foliar cover (%)", "Predicted foliar cover (%)")
vv_plot = scatter_plot(vv_mean, vv_mean$cover, vv_mean$prediction, "Vaccinium vitis-idaea", "Observed foliar cover (%)", "Predicted foliar cover (%)")

# Combine plots into a single output and export
output = 'K:/VegetationEcology/Data_Harmonization/Documents/Figures/Fig6.tif'
plot_grid = grid.arrange(ca_plot, ea_plot, ev_plot, rt_plot, sp_plot, vv_plot, nrow=3)
ggsave(output, plot=plot_grid, device='tiff', path=NULL, scale=1, width=8, height=10, units='in', dpi=600, limitsize=TRUE)