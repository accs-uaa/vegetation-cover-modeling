# Install required libraries if they are not already installed.
Required_Packages <- c("randomForest")
New_Packages <- Required_Packages[!(Required_Packages %in% installed.packages()[,"Package"])]
if (length(New_Packages) > 0) {
  install.packages(New_Packages)
}

# Import required libraries: randomForest.
library(randomForest)

# Define raw train and test data
train_file_raw = 'E:/VegetationEcology/Data_Harmonization/Project_GIS/Data_Output/testRegression/train_raw.csv'
test_file_raw = 'E:/VegetationEcology/Data_Harmonization/Project_GIS/Data_Output/testRegression/test_raw.csv'
# Define scaled train and test data
train_file_scaled = 'E:/VegetationEcology/Data_Harmonization/Project_GIS/Data_Output/testRegression/train_scaled.csv'
test_file_scaled = 'E:/VegetationEcology/Data_Harmonization/Project_GIS/Data_Output/testRegression/test_scaled.csv'

# Import raw train and test data
train_data_raw = read.csv(train_file_raw, header=TRUE, sep=',')
test_data_raw = read.csv(test_file_raw, header=TRUE, sep=',')
# Import scaled train and test data
train_data_scaled = read.csv(train_file_scaled, header=TRUE, sep=',')
test_data_scaled = read.csv(test_file_scaled, header=TRUE, sep=',')

# Define variable sets
predictor_metrics = c('compoundTopographic', 'dateFreeze_2000s', 'dateThaw_2000s', 'elevation', 'floodplainsDist', 'growingSeason_2000s', 'heatLoad', 'integratedMoisture', 'precipAnnual_2000s', 'roughness', 'siteExposure', 'slope', 'streamLargeDist', 'streamSmallDist', 'summerWarmth_2000s', 'surfaceArea', 'surfaceRelief', 'aspect', 'may_2_blue', 'may_evi2', 'may_nbr', 'may_ndmi', 'may_ndsi', 'may_ndvi', 'may_ndwi', 'june_2_blue', 'june_evi2', 'june_nbr', 'june_ndmi', 'june_ndsi', 'june_ndvi', 'june_ndwi', 'july_2_blue', 'july_evi2', 'july_nbr', 'july_ndmi', 'july_ndsi', 'july_ndvi', 'july_ndwi', 'august_2_blue', 'august_evi2', 'august_nbr', 'august_ndmi', 'august_ndsi', 'august_ndvi', 'august_ndwi', 'september_2_blue', 'september_evi2', 'september_nbr', 'september_ndmi', 'september_ndsi', 'september_ndvi', 'september_ndwi')
zero_variable = 'zero'
cover = 'cover'
coverLog = 'coverLog'
strata = 'strata'
retain_variables = c('project', 'siteID', 'siteCode', 'methodSurvey', 'methodCover')
coordinates = c('POINT_X', 'POINT_Y')
all_variables = retain_variables + coordinates + predictor_metrics + zero_variable + strata + cover + coverLog
scale_variables = predictor_metrics
print('Variable sets loaded.')

# Fit a random forest model to the raw train data and cover
fit_raw_cover = randomForest(x = train_data_raw[, predictor_metrics], y = train_data_raw[, cover], ntree = 100, importance = TRUE, proximity = TRUE)
# Predict the raw test data
predict_raw_cover = predict(object=fit_raw_cover, newdata=test_data_raw[, predictor_metrics], type='response')

# Fit a random forest model to the raw train data and coverLog
fit_raw_coverLog = randomForest(x = train_data_raw[, predictor_metrics], y = train_data_raw[, coverLog], ntree = 100, importance = TRUE, proximity = TRUE)
# Predict the raw test data
predict_raw_coverLog = predict(object=fit_raw_coverLog, newdata=test_data_raw[, predictor_metrics], type='response')


