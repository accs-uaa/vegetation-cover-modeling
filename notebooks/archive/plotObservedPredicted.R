library(ggplot2)
input_file = 'K:/VegetationEcology/Data_Harmonization/Project_GIS/Data_Output/testRegression/prediction_quant_mean.csv'
predictions = read.csv(input_file, header=TRUE, stringsAsFactors = FALSE)
font_size = theme(axis.title = element_text(size=14), axis.text = element_text(size = 12))
title = 'Observed vs predicted values of cover'
x_label = 'Observed cover (%)'
y_label = 'Predicted cover (%)'
plot = ggplot(data=predictions, aes(cover, prediction)) +
  theme_bw() +
  labs(title=title) +
  labs(x=x_label, y=y_label) +
  geom_point(shape=1) +
  geom_smooth(method=lm,
              se=FALSE) +
  font_size
plot