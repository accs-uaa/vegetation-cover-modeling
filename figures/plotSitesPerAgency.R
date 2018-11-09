# Import required libraries
library(dplyr)
library(ggplot2)
library(ggpmisc)
library(readxl)
library(tidyr)
library(pander)
library(scales)

# Import data
input_file = 'E:/VegetationEcology/Data_Harmonization/supplemental/sites_vascular_modelArea_count.csv'
agency_sites = read.csv(input_file, header=TRUE, stringsAsFactors = FALSE)

# Define a function to generate a bar chart
bar_chart = function(inData, x_variable, y_variable, x_label, y_label) {
  font_size = theme(axis.title = element_text(size=14), axis.text = element_text(size = 12))
  plot = ggplot(data=inData, aes(x=reorder(x_variable, -y_variable), y=y_variable)) +
    theme_bw() +
    theme(axis.text.x = element_text(angle=90, hjust=1, vjust=0.3)) +
    theme(axis.text.x = element_text(color= "black")) +
    theme(axis.text.y = element_text(color= "black")) +
    theme(axis.title.x = element_text(margin = margin(t=10))) +
    theme(axis.title.y = element_text(margin = margin(r=10))) +
    geom_bar(stat='identity',
             colour = 'white',
             fill = 'gray',
             alpha = 1) +
    geom_text(aes(label=y_variable), position=position_dodge(width=0.9), vjust=-0.25) +
    labs(x=x_label, y=y_label) +
    scale_x_discrete(labels=wrap_format(25)) +
    font_size
  return(plot)
}
    
# Create a histogram of sites per agency ordered from largest to smallest
agency_chart = bar_chart(agency_sites, agency_sites$Agency, agency_sites$Count, "Jurisdiction", "Number of vegetation plots")
agency_chart

# Save output chart
output = 'E:/VegetationEcology/Data_Harmonization/Documents/Figures/Fig3.tif'
ggsave(output, plot=agency_chart, device='tiff', path=NULL, scale=1, width=7, height=7, units='in', dpi=600, limitsize=TRUE)