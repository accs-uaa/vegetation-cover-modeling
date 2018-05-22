# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Random Forest Model Analysis
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Created on: 2017-01-22
# Usage: Must be executed as an R Script. Script is set up to integrate with python but can be modified to run from an R command interface.
# Description: This tool provides a Random Forest model with variable selection and best model fit determined using data-driven approaches.
# ---------------------------------------------------------------------------

# Install required libraries if they are not already installed.
Required_Packages = c("randomForest", "rfUtilities", "sp", "raster", "rgdal", "stringr", "ROCR", "dplyr")
New_Packages = Required_Packages[!(Required_Packages %in% installed.packages()[,"Package"])]
if (length(New_Packages) > 0) {
  install.packages(New_Packages)
}

# Import required libraries: randomForest, rfUtilities, sp, raster, rgdal, stringr, ROCR.
library(randomForest)
library(rfUtilities)
library(sp)
library(raster)
library(rgdal)
library(stringr)
library(ROCR)
library(dplyr)

# Set seed
set.seed(415)

# Set working directory by user input
userDirectory = choose.dir()
setwd(userDirectory)

# Read csv data of training and test set
training_data = read.csv("K:\\VegetationEcology\\NorthSlopeDataHarmonization\\TestData\\train.csv")
test_data = read.csv("K:\\VegetationEcology\\NorthSlopeDataHarmonization\\TestData\\test.csv")

# Convert species presence to factor in training and test datasets
training_data$present = as.factor(training_data$present)
test_data$present = as.factor(test_data$present)

# Create model kappa function
Kappa_Function = function(actual, model) {
  Table = table(actual=actual,predicted=predict(model,OOB=TRUE))
  A = Table[2,2]
  B = Table[1,2]
  C = Table[2,1]
  D = Table[1,1]
  Kappa_Value = ((A+D)-(((A+C)*(A+B)+(B+D)*(C+D))/(A+B+C+D)))/((A+B+C+D)-
                                                                  (((A+C)*(A+B)+(B+D)*(C+D))/(A+B+C+D)))
  return(Kappa_Value)
}

# Perform 100 iterations of variable selection and model fit to find three best performing models based on model kappa.
cat("Starting model fit iteration 1 of 100...\n")
Kappa_List = numeric()
Variables = rf.modelSel(x = training_data[, 4:ncol(training_data)], y = training_data[, "present"], imp.scale = "mir", ntree = 5000, r = c(0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1))
Selected <- Variables$selvars
Fit <- randomForest(x = training_data[, Selected], y = training_data[, "present"], ntree = 5000, importance = TRUE, norm.votes = TRUE, proximity = TRUE)
Model_Kappa <- Kappa_Function(training_data[, "present"], Fit)
Kappa_List <- c(Kappa_List, Model_Kappa)
Kappa_Sorted <- sort(unique(Kappa_List), decreasing = TRUE)
Variables_1 <- Variables
Selected_1 <- Selected
Fit_1 <- Fit
Model_Kappa_1 <- Model_Kappa
Variables_2 <- Variables
Selected_2 <- Selected
Fit_2 <- Fit
Model_Kappa_2 <- Model_Kappa
Variables_3 <- Variables
Selected_3 <- Selected
Fit_3 <- Fit
Model_Kappa_3 <- Model_Kappa
for (Count in 2:100) {
  cat(paste("Starting model fit iteration ", Count, " of 100...\n", sep=""))
  Variables <- rf.modelSel(x = training_data[, 4:ncol(training_data)], y = training_data[, "present"], imp.scale = "mir", ntree = 5000, r = c(0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1))
  Selected <- Variables$selvars
  Fit <- randomForest(x = training_data[, Selected], y = training_data[, "present"], ntree = 5000, importance = TRUE, norm.votes = TRUE, proximity = TRUE)
  Model_Kappa <- Kappa_Function(training_data[, "present"], Fit)
  Kappa_List <- c(Kappa_List, Model_Kappa)
  Kappa_Sorted <- sort(unique(Kappa_List), decreasing = TRUE)
  if (Model_Kappa >= Kappa_Sorted[1]) {
    Variables_1 <- Variables
    Selected_1 <- Selected
    Fit_1 <- Fit
    Model_Kappa_1 <- Model_Kappa
  } else if ((Model_Kappa >= Kappa_Sorted[2]) & (Model_Kappa < Kappa_Sorted[1])) {
    Variables_2 <- Variables
    Selected_2 <- Selected
    Fit_2 <- Fit
    Model_Kappa_2 <- Model_Kappa
  } else if ((Model_Kappa >= Kappa_Sorted[3]) & (Model_Kappa < Kappa_Sorted[2])) {
    Variables_3 <- Variables_3
    Selected_3 <- Selected
    Fit_3 <- Fit
    Model_Kappa_3 <- Model_Kappa
  }
}

# Perform cross validation of three best performing model iterations based on model kappa.
cat("Cross validating best performing model (based on model kappa)...\n")
CrossValidation_1 <- rf.crossValidation(Fit_1, training_data[, Selected_1], p = 0.10, n = 1000, ntree = 5000)
CV_Kappa_1 <- mean(CrossValidation_1$cross.validation$cv.oob$kappa)
cat("Cross validating second best performing model (based on model kappa)...\n")
CrossValidation_2 <- rf.crossValidation(Fit_2, training_data[, Selected_2], p = 0.10, n = 1000, ntree = 5000)
CV_Kappa_2 <- mean(CrossValidation_2$cross.validation$cv.oob$kappa)
cat("Cross validating third best performing model (based on model kappa)...\n")
CrossValidation_3 <- rf.crossValidation(Fit_3, training_data[, Selected_3], p = 0.10, n = 1000, ntree = 5000)
CV_Kappa_3 <- mean(CrossValidation_3$cross.validation$cv.oob$kappa)

# Select best performing model based on cross validation kappa.
cat("Selecting best performing model based on cross validation kappa...\n")
Max_CV_Kappa <- max(CV_Kappa_1, CV_Kappa_2, CV_Kappa_3)
if (CV_Kappa_1 == Max_CV_Kappa) {
  Final_Variables <- Variables_1
  Final_Selected <- Selected_1
  Final_Fit <- Fit_1
  Final_Model_Kappa <- Model_Kappa_1
  Final_CrossValidation <- CrossValidation_1
  Final_CV_Kappa <- CV_Kappa_1
} else if (CV_Kappa_2 == Max_CV_Kappa) {
  Final_Variables <- Variables_2
  Final_Selected <- Selected_2
  Final_Fit <- Fit_2
  Final_Model_Kappa <- Model_Kappa_2
  Final_CrossValidation <- CrossValidation_2
  Final_CV_Kappa <- CV_Kappa_2
} else if (CV_Kappa_3 == Max_CV_Kappa) {
  Final_Variables <- Variables_3
  Final_Selected <- Selected_3
  Final_Fit <- Fit_3
  Final_Model_Kappa <- Model_Kappa_3
  Final_CrossValidation <- CrossValidation_3
  Final_CV_Kappa <- CV_Kappa_3
}
sink("FinalVars.txt")
cat(Final_Selected)
sink()

# Predict training data
predict_training = predict(Final_Fit, training_data[, Final_Selected], type="prob")
predict_training = cbind(training_data, predict_training)
write.csv(predict_training, file = "R_variableOpt_training.csv")




Independent_Data <- training_data[, 4:ncol(training_data)]
Threshold_Value <- occurrence.threshold(Final_Fit, Independent_Data, class="1", type="delta.ss")
sink("OccurrenceThreshold.txt")
summary(Threshold_Value)
sink()
png(file = "plots\\Threshold_Value.png")
plot(Threshold_Value)
dev.off()

# Export graph of all variable importances.
png(file = "VariableImportance_All.png")
plot(Variables, imp = "all")
dev.off()

# Export scaled variable importance for selected variables.
p <- as.matrix(Final_Fit$importance[,3])
ord <- rev(order(p[,1], decreasing = TRUE)[1:dim(p)[1]])
png(file = "VariableImportance_Selected.png")
dotchart(p[ord,1], main = "Scaled Variable Importance", pch = 19)
dev.off()

# Predict test data
predict_test = predict(Final_Fit, test_data[, Final_Selected], type="prob")
predict_test = cbind(test_data, predict_test)

# Identify threshold for determining positive/negative
threshold = 0.41
thresholded = ifelse(predict_test$`1` >= threshold, 1, 0)
predict_test = cbind(predict_test, thresholded)

# Calculate sensitivity: number of true positives divided by the number of true positives plus the number of false negatives
observed_positive = filter(predict_test, predict_test$present == 1)
sensitivity = mean(observed_positive$thresholded)

# Calculate specificity: number of true negatives divided by the number of true negatives plus the number of false positives
predict_test$thresholded = ifelse(predict_test$thresholded == 1, 0, 1)
observed_negative = filter(predict_test, predict_test$present == 0)
specificity = mean(observed_negative$thresholded)
predict_test$thresholded = ifelse(predict_test$thresholded == 1, 0, 1)

# Calculate the difference in absolute value of sensivity and specificity
delta = abs(sensitivity - specificity)
write.csv(predict_test, file = "R_variableOpt_test.csv")