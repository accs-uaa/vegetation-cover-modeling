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
import seaborn as sns
import matplotlib.pyplot as plot
import xlsxwriter
from sklearn.ensemble import RandomForestClassifier
	
# Set overwrite option
arcpy.env.overwriteOutput = True

# Define feature class of input training dataset
training_data = r"E:\VegetationEcology\Data_Harmonization\Project_GIS\DataHarmonization_GIS.gdb\Train_SalixAlaxensis"

# Define feature class of input test dataset
test_data = r"E:\VegetationEcology\Data_Harmonization\Project_GIS\DataHarmonization_GIS.gdb\Test_SalixAlaxensis"

# Define workspace folder
workspace_folder = r"E:\VegetationEcology\Data_Harmonization\Project_GIS\Data_Output\SalixAlaxensis"

# Define workspace_geodatabase
workspace_geodatabase = r"K:\VegetationEcology\NorthSlopeDataHarmonization\Project_GIS\DataHarmonization_GIS.gdb"

# Define name of variable that distinguishes cover values greater than 0%
zero_variable = 'zero'
zero_variable = [zero_variable]

# Define name of variable that distinguishes cover values greater than 10%
ten_variable = 'ten'
ten_variable = [ten_variable]

# Define name of variable that distinguishes cover values greater than 25%
twentyfive_variable = 'twentyfive'
twentyfive_variable = [twentyfive_variable]

# Define output html report
output_report = r"E:\VegetationEcology\Data_Harmonization\Project_GIS\Data_Output\SalixAlaxensis\salix-alaxensis-report.html"

# Define output species name
output_name = "Salix alaxensis"

# Define list of covariates
predictor_variables = ['compoundTopographic', 'dateFreeze_2000s', 'dateThaw_2000s', 'elevation', 'floodplainsDist', 'growingSeason_2000s', 'heatLoad', 'integratedMoisture', 'precipAnnual_2000s', 'roughness', 'siteExposure', 'slope', 'streamLargeDist', 'streamSmallDist', 'summerWarmth_2000s', 'surfaceArea', 'surfaceRelief', 'aspect', 'l8_evi2', 'l8_green', 'l8_nbr', 'l8_ndmi', 'l8_ndsi', 'l8_ndvi', 'l8_ndwi', 'l8_nearInfrared', 'l8_red', 'l8_shortInfrared1', 'l8_shortInfrared2', 'l8_ultrablue', 'l8_blue']

# Define intermediate variables
retain_variables = ['cover', 'project', 'siteID', 'siteCode', 'methodSurvey', 'methodCover']
coordinates = ['POINT_X', 'POINT_Y']
all_variables = predictor_variables + zero_variable + ten_variable + twentyfive_variable + retain_variables + coordinates

# Define a function to plot Pearson correlation of predictor variables
def plotVariableCorrelation(x_train, outFile):
    # Calculate Pearson correlation coefficient between the predictor variables, where -1 is perfect negative correlation and 1 is perfect positive correlation
    correlation = train_df[predictor_variables].astype('float64').corr()
    # Generate a mask for the upper triangle of plot
    mask = np.zeros_like(correlation, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    # Set up the matplotlib figure
    f, ax = plot.subplots(figsize=(11, 9))
    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    # Draw the heatmap with the mask and correct aspect ratio
    correlation_plot = sns.heatmap(correlation, mask=mask, cmap=cmap, vmax=.3, center=0, square=True, linewidths=.5, cbar_kws={"shrink": .5})
    correlation_figure = correlation_plot.get_figure()
    correlation_figure.savefig(outFile, bbox_inches="tight", dpi=300)
    # Clear plot workspace
    plot.clf()
    plot.close()

# Define a function to plot receiver operating characteristic curve
def plotCurveROC(y_test, inProbability, outROCFile):
    # Calculate the false positive rate, true positive rate, and tested thresholds using the sklearn roc_curve function
    false_positive_rate, true_positive_rate, thresholds_roc = roc_curve(y_test, inProbability)
    # Calculate the area under curve based on the false positive rate and true positive rate
    roc_auc = auc(false_positive_rate, true_positive_rate)
    # Set up the plot for the roc curve
    roc_figure = plot.figure()
    lw = 2
    plot.title('Receiver Operating Characteristic')
    plot.plot(false_positive_rate, true_positive_rate, color='darkorange', lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)
    plot.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plot.xlim([0.0, 1.0])
    plot.ylim([0.0, 1.05])
    plot.ylabel('True Positive Rate')
    plot.xlabel('False Positive Rate')
    plot.legend(loc='lower right')
    roc_figure.savefig(outROCFile, bbox_inches="tight", dpi=300)
    # Clear plot workspace
    plot.clf()
    plot.close()

# Define a function to plot variable importances
def plotVariableImportances(inModel, x_train, outVariableFile):
    # Get numerical feature importances
    importances = list(inModel.feature_importances_)
    # List of tuples with variable and importance
    feature_list = list(x_train.columns)
    feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]
    # Sort the feature importances by most important first
    feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
    # Initialize the plot and set figure size
    variable_figure = plot.figure()
    plot.style.use('fivethirtyeight')
    fig_size = plot.rcParams["figure.figsize"]
    fig_size[0] = 12
    fig_size[1] = 9
    plot.rcParams["figure.figsize"] = fig_size
    # Create list of x locations for plotting
    x_values = list(range(len(importances)))
    # Make a bar chart of the variable importances
    plot.bar(x_values, importances, orientation = 'vertical')
    # Tick labels for x axis
    plot.xticks(x_values, feature_list, rotation='vertical')
    # Axis labels and title
    plot.ylabel('Importance'); plot.xlabel('Variable'); plot.title('Variable Importances');
    # Export
    variable_figure.savefig(outVariableFile, bbox_inches="tight", dpi=300)
    # Clear plot workspace
    plot.clf()
    plot.close()

# Define a function to 
def thresholdMetrics(inIndex, inProbability, inValue, y_test):
    outThresholded = np.zeros(inIndex.shape)
    outThresholded[inIndex > inValue] = 1
    confusion_test = confusion_matrix(y_test, outThresholded)
    true_negative = confusion_test[0,0]
    false_negative = confusion_test[1,0]
    true_positive = confusion_test[1,1]
    false_positive = confusion_test[0,1]
    outSensitivity = true_positive / (true_positive + false_negative)
    outSpecificity = true_negative / (true_negative + false_positive)
    outAUC = roc_auc_score(y_test, inProbability)
    outAccuracy = (true_negative + true_positive) / (true_negative + false_positive + false_negative + true_positive)
    return (outThresholded, outSensitivity, outSpecificity, outAUC, outAccuracy)
	
# Define a function to fit a random forest classifier using training data and determine a best classification threshold using the test data
def trainTestModel(x_train, y_train, x_test, y_test, testData, variable, outROCFile, outVariableFile):
    # Fit a random forest classifier to the training dataset
    rf_classify = RandomForestClassifier(n_estimators = 5000, oob_score = True, class_weight = "balanced")
    rf_classify.fit(x_train, y_train)
    # Use the random forest classifier to predict probabilities for the test dataset
    test_prediction = rf_classify.predict_proba(x_test)
    # Convert the positive class probabilities to a list of probabilities
    test_probability = [p[1] for p in test_prediction]
    # Convert the postitive class probabilities to an index between 0 and 1000
    test_index = [int((p[1] * 1000) + 0.5) for p in test_prediction]
    # Iterate through numbers between 0 and 1000 to output a list of sensitivity and specificity values per threshold number
    i = 1
    test_index = np.asarray(test_index)
    sensitivity_list = []
    specificity_list = []
    while i < 1000:
        test_thresholded, sensitivity_test, specificity_test, auc_test, accuracy_test = thresholdMetrics(test_index, test_probability, i, y_test)
        sensitivity_list.append(sensitivity_test)
        specificity_list.append(specificity_test)
        i = i + 1
    # Calculate a list of absolute value of difference between sensitivity and specificity and find the optimal threshold
    difference_list = [a - b for a, b in zip(sensitivity_list, specificity_list)]
    value, threshold = min((value, threshold) for (threshold, value) in enumerate(difference_list) if value >= 0)
    # Calculate the prediction index to a binary 0 or 1 output using the optimal threshold
    test_thresholded, sensitivity_test, specificity_test, auc_test, accuracy_test = thresholdMetrics(test_index, test_probability, threshold, y_test)
    # Concatenate thresholded predictions to test data frame
    testData = pd.concat([testData, pd.DataFrame(test_thresholded)], axis=1)
    testData = testData.rename(index=int, columns={0: variable})
    # Export a receiver operating characteristic curve
    plotCurveROC(y_test, test_probability, outROCFile)
    # Export a variable importance plot
    plotVariableImportances(rf_classify, x_train, outVariableFile)
    return [threshold, sensitivity_test, specificity_test, auc_test, accuracy_test, rf_classify.oob_score_, testData]

# Define a function to output threshold to text file
def thresholdOut(inThreshold, outThresholdFile):
    file = open(outThresholdFile, 'w')
    file.write(inThreshold)
    file.close()

# Convert training and test partitions into numpy arrays
train_array = da.FeatureClassToNumPyArray(training_data, ["SHAPE@XY"] + all_variables)
test_array = da.FeatureClassToNumPyArray(test_data, ["SHAPE@XY"] + all_variables)
spatial_reference = arcpy.Describe(training_data).spatialReference

# Convert numpy arrays to data frames
train_df = pd.DataFrame(train_array, columns = all_variables)
test_df = pd.DataFrame(test_array, columns = all_variables)

# Create a plots folder if it does not exist
plots_folder = os.path.join(workspace_folder, "plots")
if not os.path.exists(plots_folder):
    os.makedirs(plots_folder)

# Export a Pearson Correlation plot for the predictor variables
variableCorrelation = os.path.join(plots_folder, "variableCorrelation.png")
plotVariableCorrelation(train_df[predictor_variables], variableCorrelation)

# Train and test a random forest classifier to distinguish cover values greater than 0%
rocFile_0 = os.path.join(plots_folder, "roc_0.png")
variableFile_0 = os.path.join(plots_folder, "variableImportance_0.png")
threshold_0, sensitivity_0, specificity_0, auc_0, accuracy_0, oob_score_0, test_df = trainTestModel(train_df[predictor_variables], train_df[zero_variable[0]], test_df[predictor_variables], test_df[zero_variable[0]], test_df, "predict_0", rocFile_0, variableFile_0)

# Train and test a random forest classifier to distinguish cover values greater than 10%
rocFile_10 = os.path.join(plots_folder, "roc_10.png")
variableFile_10 = os.path.join(plots_folder, "variableImportance_10.png")
threshold_10, sensitivity_10, specificity_10, auc_10, accuracy_10, oob_score_10, test_df = trainTestModel(train_df[predictor_variables], train_df[ten_variable[0]], test_df[predictor_variables], test_df[ten_variable[0]], test_df, "predict_10", rocFile_10, variableFile_10)

# Train and test a random forest classifier to distinguish cover values greater than 25%
rocFile_25 = os.path.join(plots_folder, "roc_25.png")
variableFile_25 = os.path.join(plots_folder, "variableImportance_25.png")
threshold_25, sensitivity_25, specificity_25, auc_25, accuracy_25, oob_score_25, test_df = trainTestModel(train_df[predictor_variables], train_df[twentyfive_variable[0]], test_df[predictor_variables], test_df[twentyfive_variable[0]], test_df, "predict_25", rocFile_25, variableFile_25)

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

# Apply composite classification function to the predictions in the test dataframe
test_df['classification'] = test_df.apply(lambda row: compositeClassification(row), axis=1)

# Export data frame to excel
test_df.to_excel(os.path.join(workspace_folder, 'test.xls'))

# Write a text file for each classifier containing the threshold value that minimizes the absolute value difference between specificity and sensitivity
outThreshold_0 = os.path.join(workspace_folder, 'threshold_0.txt')
outThreshold_10 = os.path.join(workspace_folder, 'threshold_10.txt')
outThreshold_25 = os.path.join(workspace_folder, 'threshold_25.txt')
thresholdOut(str(threshold_0), outThreshold_0)
thresholdOut(str(threshold_10), outThreshold_10)
thresholdOut(str(threshold_25), outThreshold_25)

# Write html text file
output_text = os.path.splitext(output_report)[0] + ".txt"
text_file = open(output_text, "w")
text_file.write("<html>\n")
text_file.write("<head>\n")
text_file.write("<meta http-equiv=\"pragma\" content=\"no-cache\">\n")
text_file.write("<meta http-equiv=\"Expires\" content=\"-1\">\n")
text_file.write("</head>\n")
text_file.write("<body>\n")
text_file.write("<div style=\"width:90%;max-width:1000px;margin-left:auto;margin-right:auto\">\n")
text_file.write("<h1 style=\"text-align:center;\">Classified Cover Modeling Performance for " + output_name + "</h1>\n")
text_file.write(r"<br>" + "\n")
text_file.write(r"<h2>Model Performance</h2>" + "\n")
text_file.write("<p>Model performance is measured by sensitivity, specificity, accuracy, and area under curve (auc) for each of the model components. Each component is a binary classifier that distinguishes between a break in cover. The breaks are coded as follows: the '0' classifier distinguishes cover values greater than 0%, the '10' classifier distinguishes between cover values greater than 10%, and the '25' classifier distinguishes between cover values greater than 25%. Each component was trained separately and a threshold that minimized the absolute value difference between sensitivity and specificity where sensitivity was greater than specificity was selected against an independent partition of test data. All model metrics except the bootstrap are relative to the independent partition of test data.</p>\n")
text_file.write(r"<h3>Performance of '0' Classifier</h3>" + "\n")
text_file.write("<p><b>Sensitivity</b> of the '0' Classifier is <b>" + str(round(sensitivity_0, 3)) + "</b></p>\n")
text_file.write("<p><b>Specificity</b> of the '0' Classifier is <b>" + str(round(specificity_0, 3)) + "</b></p>\n")
text_file.write("<p>Overall <b>Accuracy</b> of the '0' Classifier is <b>" + str(round(accuracy_0, 3)) + "</b></p>\n")
text_file.write("<p>The '0' Classifier <b>Out Of Bag Score</b> is <b>" + str(round(oob_score_0, 3)) + "</b></p>\n")
text_file.write("<p><b>AUC value</b> of the '0' Classifier is <b>" + str(round(auc_0, 3)) + "</b></p>\n")
text_file.write("<p>The Receiver Operating Characteristic Curve and Variable Importances plots for the '0' Classifier are shown below:</p>\n")
text_file.write("<a target='_blank' href='plots\\roc_0.png'><img style='display:inline-block;max-width:480px;width:100%;' src='plots\\roc_0.png'></a>\n")
text_file.write("<a target='_blank' href='plots\\variableImportance_0.png'><img style='display:inline-block;max-width:480px;width:100%;' src='plots\\variableImportance_0.png'></a>\n")
text_file.write(r"<h3>Performance of '10' Classifier</h3>" + "\n")
text_file.write("<p><b>Sensitivity</b> of the '10' Classifier is <b>" + str(round(sensitivity_10, 3)) + "</b></p>\n")
text_file.write("<p><b>Specificity</b> of the '10' Classifier is <b>" + str(round(specificity_10, 3)) + "</b></p>\n")
text_file.write("<p>Overall <b>Accuracy</b> of the '10' Classifier is <b>" + str(round(accuracy_10, 3)) + "</b></p>\n")
text_file.write("<p>The '10' Classifier <b>Out Of Bag Score</b> is <b>" + str(round(oob_score_10, 3)) + "</b></p>\n")
text_file.write("<p><b>AUC value</b> of the '10' Classifier is <b>" + str(round(auc_10, 3)) + "</b></p>\n")
text_file.write("<p>The Receiver Operating Characteristic Curve and Variable Importances plots for the '10' Classifier are shown below:</p>\n")
text_file.write("<a target='_blank' href='plots\\roc_10.png'><img style='display:inline-block;max-width:480px;width:100%;' src='plots\\roc_10.png'></a>\n")
text_file.write("<a target='_blank' href='plots\\variableImportance_10.png'><img style='display:inline-block;max-width:480px;width:100%;' src='plots\\variableImportance_10.png'></a>\n")
text_file.write(r"<h3>Performance of '25' Classifier</h3>" + "\n")
text_file.write("<p><b>Sensitivity</b> of the '25' Classifier is <b>" + str(round(sensitivity_25, 3)) + "</b></p>\n")
text_file.write("<p><b>Specificity</b> of the '25' Classifier is <b>" + str(round(specificity_25, 3)) + "</b></p>\n")
text_file.write("<p>Overall <b>Accuracy</b> of the '25' Classifier is <b>" + str(round(accuracy_25, 3)) + "</b></p>\n")
text_file.write("<p>The '25' Classifier <b>Out Of Bag Score</b> is <b>" + str(round(oob_score_25, 3)) + "</b></p>\n")
text_file.write("<p><b>AUC value</b> of the '25' Classifier is <b>" + str(round(auc_25, 3)) + "</b></p>\n")
text_file.write("<p>The Receiver Operating Characteristic Curve and Variable Importances plots for the '25' Classifier are shown below:</p>\n")
text_file.write("<a target='_blank' href='plots\\roc_25.png'><img style='display:inline-block;max-width:480px;width:100%;' src='plots\\roc_25.png'></a>\n")
text_file.write("<a target='_blank' href='plots\\variableImportance_25.png'><img style='display:inline-block;max-width:480px;width:100%;' src='plots\\variableImportance_25.png'></a>\n")
text_file.write(r"<h2>Variable Correlation</h2>" + "\n")
text_file.write("<p>The plot below explores variable correlation. No attempt was made to remove highly correlated variables (shown in the plot dark blue).</p>\n")
text_file.write("<a target='_blank' href='plots\\variableCorrelation.png'><img style='display:inline-block;width:100%;' src='plots\\variableCorrelation.png'></a>\n")
text_file.write("</div>\n")
text_file.write("</body>\n")
text_file.write("</html>\n")
text_file.close()

# Rename HTML Text to HTML
if os.path.exists(output_report) == True:
    os.remove(output_report)
os.rename(output_text, output_report)