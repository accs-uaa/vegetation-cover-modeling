# Import required libraries
library(dplyr)
library(ggplot2)
library(ggpmisc)
library(readxl)
library(tidyr)
library(gridExtra)
library(scales)
library(splitstackshape)
library(data.table)

# Import data
input_file = 'E:/VegetationEcology/Data_Harmonization/supplemental/CorrelationSamplingPoints_Species.csv'
input_data = read.csv(input_file, header=TRUE, stringsAsFactors = TRUE)

# Define variables
variables = c('carex_aquatilis', 'eriophorum_vaginatum', 'rhododendron_tomentosum', 'salix_pulchra', 'vaccinium_vitisidaea')

# Create a linear model to determine correlation between sedge PFT and dominant sedges
difference = lm(input_data$sedge_pft~input_data$sedge_dominant)
summary(difference)