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
input_file = 'E:/VegetationEcology/Data_Harmonization/supplemental/r2_vaccinium_vitisidaea.csv'
input_data = read.csv(input_file, header=TRUE, stringsAsFactors = TRUE)

# Create a linear model to determine if performance difference is significant
difference = lm(input_data$r_score~input_data$type)
summary(difference)