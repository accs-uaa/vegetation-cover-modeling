# Import required libraries
library(BEST)

# Define input files
metric_file = 'K:/ACCS_Work/Projects/VegetationEcology/Data_Harmonization/Supplemental/continuous_vaccinium_vitisidaea_metrics.csv'

# Read input data
metric_data = read.csv(metric_file, header=TRUE, stringsAsFactors = TRUE)

# Create vectors for performance metrics
vector_mae = metric_data$overall_mae
vector_rmse = metric_data$overall_rmse
vector_auc = metric_data$auc
vector_acc = metric_data$accuracy


# Analyze the mean and standard deviation using Monte Carlo Markov Chain
mean_mae = BESTmcmc(vector_mae, y2 = NULL, priors = NULL, doPriorsOnly = FALSE, numSavedSteps = 1e+06, thinSteps = 1, burnInSteps = 1e+04, verbose = FALSE, rnd.seed = 314, parallel = TRUE)
mean_rmse = BESTmcmc(vector_rmse, y2 = NULL, priors = NULL, doPriorsOnly = FALSE, numSavedSteps = 1e+06, thinSteps = 1, burnInSteps = 1e+04, verbose = FALSE, rnd.seed = 314, parallel = TRUE)
mean_auc = BESTmcmc(vector_auc, y2 = NULL, priors = NULL, doPriorsOnly = FALSE, numSavedSteps = 1e+06, thinSteps = 1, burnInSteps = 1e+04, verbose = FALSE, rnd.seed = 314, parallel = TRUE)
mean_acc = BESTmcmc(vector_acc, y2 = NULL, priors = NULL, doPriorsOnly = FALSE, numSavedSteps = 1e+06, thinSteps = 1, burnInSteps = 1e+04, verbose = FALSE, rnd.seed = 314, parallel = TRUE)

# Display the results
mean_mae
mean_rmse
mean_auc
mean_acc