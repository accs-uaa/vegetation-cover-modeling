# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Random Forest Train and Predict for Classified Cover
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Created on: 2018-07-14
# Usage: Must be executed as an ArcPy Script.
# Description: "Random Forest Train and Test" trains a classification model using the presence and absence data in the training dataset. Subsequently, a regression model is trained using cover data for all presences in the training dataset. The classifcation and regression models are used to predict the presence and cover in the test dataset.
# ---------------------------------------------------------------------------

# Import modules
import os
import numpy as np
import arcpy
import arcpy.da as da
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
	
# Set overwrite option
arcpy.env.overwriteOutput = True

# Define feature class of input training dataset
training_data = arcpy.GetParameterAsText(0)

# Define feature class of input test dataset
predict_datasets = arcpy.GetParameterAsText(1)

# Define workspace folder
workspace_folder = arcpy.GetParameterAsText(2)

# Define name of variable that distinguishes cover values greater than 0%
zero_variable = arcpy.GetParameterAsText(3)
zero_variable = [zero_variable]

# Define name of variable that distinguishes cover values greater than 10%
ten_variable = arcpy.GetParameterAsText(4)
ten_variable = [ten_variable]

# Define name of variable that distinguishes cover values greater than 25%
twentyfive_variable = arcpy.GetParameterAsText(5)
twentyfive_variable = [twentyfive_variable]

# Define output folder
output_folder = arcpy.GetParameterAsText(6)

# Define list of covariates
predictor_variables = ['compoundTopographic', 'dateFreeze_2000s', 'dateThaw_2000s', 'elevation', 'floodplainsDist', 'growingSeason_2000s', 'heatLoad', 'integratedMoisture', 'precipAnnual_2000s', 'roughness', 'siteExposure', 'slope', 'streamLargeDist', 'streamSmallDist', 'summerWarmth_2000s', 'surfaceArea', 'surfaceRelief', 'aspect', 'l8_evi2', 'l8_green', 'l8_nbr', 'l8_ndmi', 'l8_ndsi', 'l8_ndvi', 'l8_ndwi', 'l8_nearInfrared', 'l8_red', 'l8_shortInfrared1', 'l8_shortInfrared2', 'l8_ultrablue', 'l8_blue']

# Define intermediate variables
coordinates = ['POINT_X', 'POINT_Y']
all_variables = predictor_variables + zero_variable + ten_variable + twentyfive_variable + coordinates
output_variables = coordinates + ['predict_0', 'predict_10', 'predict_25', 'classification']

# Split input predict datasets string into a list
predict_datasets = predict_datasets.split(";")

# Define a function to read threshold values from text file
def readThreshold(inFile):
   threshold_reader = open(inFile, "r")
   threshold = threshold_reader.readlines()
   threshold_reader.close()
   outThreshold = threshold[0]
   return outThreshold

# Define a function to convert feature class to data frame
def convertFeature(inData):
    inArray = da.FeatureClassToNumPyArray(inData, ["SHAPE@XY"] + predictor_variables + coordinates)
    outDataframe = pd.DataFrame(inArray, columns = predictor_variables + coordinates)
    return outDataframe

# Define a function to fit a random forest classifier using training data
def trainModel(x_train, y_train):
    # Fit a random forest classifier to the training dataset
    rf_classify = RandomForestClassifier(n_estimators = 5000, oob_score = True, class_weight = "balanced")
    rf_classify.fit(x_train, y_train)
    return rf_classify

# Define a function to use a random forest classifier to make a probability prediction, threshold the prediction, and output to dataframe
def predictModel(inModel, inThreshold, inDataframe, variable):
    prediction = inModel.predict_proba(inDataframe[predictor_variables])
    predict_index = [int((p[1] * 1000) + 0.5) for p in prediction]
    predict_index = np.asarray(predict_index)
    outThresholded = np.zeros(predict_index.shape)
    outThresholded[predict_index > inThreshold] = 1
    inDataframe = pd.concat([inDataframe, pd.DataFrame(outThresholded)], axis=1)
    inDataframe = inDataframe.rename(index=int, columns={0: variable})
    return inDataframe

# Define a function to create composite classification
def compositeClassification (row):
    if row['predict_0'] == 0:
        return 0
    elif row['predict_0'] == 1 and row['predict_10'] == 0:
        return 1
    elif row['predict_0'] == 1 and row['predict_10'] == 1 and row['predict_25'] == 0:
        return 2
    elif row['predict_0'] == 1 and row['predict_10'] == 1 and row['predict_25'] == 1:
        return 3

# Define a function to predict and export a predict dataset using input classifier models and thresholds	
def compositeModel(inModel_0, inModel_10, inModel_25, inThreshold_0, inThreshold_10, inThreshold_25, inData, outCSV):
    # Convert the input data to a data frame
    predict_df = convertFeature(inData)
    # Use the 0 classifier to make binary prediction and append results to predict dataframe
    predict_df = predictModel(inModel_0, inThreshold_0, predict_df, "predict_0")
    # Use the 10 classifier to make binary prediction and append results to predict dataframe
    predict_df = predictModel(inModel_10, inThreshold_10, predict_df, "predict_10")
    # Use the 25 classifier to make binary prediction and append results to predict dataframe
    predict_df = predictModel(inModel_25, inThreshold_25, predict_df, "predict_25")
    # Apply composite classification function to the predictions in the test dataframe
    predict_df['classification'] = predict_df.apply(lambda row: compositeClassification(row), axis=1)
    output_df = predict_df[output_variables]
    # Export the output dataframe to the output csv
    output_df.to_csv(outCSV, header=True, index=False, sep=',', encoding='utf-8')

# Read thresholds from text files in the workspace folder and store as variables
threshold_file_0 = os.path.join(workspace_folder, "threshold_0.txt")
threshold_file_10 = os.path.join(workspace_folder, "threshold_10.txt")
threshold_file_25 = os.path.join(workspace_folder, "threshold_25.txt")
threshold_0 = int(readThreshold(threshold_file_0))
threshold_10 = int(readThreshold(threshold_file_10))
threshold_25 = int(readThreshold(threshold_file_25))

# Convert training data to dataframe
train_array = da.FeatureClassToNumPyArray(training_data, ["SHAPE@XY"] + all_variables)
train_df = pd.DataFrame(train_array, columns = all_variables)

# Create a random forest model for the 0, 10, and 25 classifier
classify_0 = trainModel(train_df[predictor_variables], train_df[zero_variable[0]])
classify_10 = trainModel(train_df[predictor_variables], train_df[ten_variable[0]])
classify_25 = trainModel(train_df[predictor_variables], train_df[twentyfive_variable[0]])

# Run composite model for each watershed dataset
for watershed_data in predict_datasets:
    output_csv = os.path.join(output_folder, os.path.split(watershed_data)[1] + ".csv")
    compositeModel(classify_0, classify_10, classify_25, threshold_0, threshold_10, threshold_25, watershed_data, output_csv)