# Import required libraries
library(BEST)

# Import data
input_file = 'K:/ACCS_Work/Projects/VegetationEcology/Data_Harmonization/Supplemental/r2_eriophorum_angustifolium.csv'
input_data = read.csv(input_file, header=TRUE, stringsAsFactors = TRUE)
continuous = input_data[input_data$type == 'continuous','r_score']
nssi = input_data[input_data$type == 'nssi','r_score']

# Analyze the difference in means using Monte Carlo Markov Chain
bayesian_difference = BESTmcmc(continuous, nssi, priors = NULL, doPriorsOnly = FALSE, numSavedSteps = 1e+06, thinSteps = 1, burnInSteps = 1e+04, verbose = FALSE, rnd.seed = 314, parallel = TRUE)

# Display the result
bayesian_difference

# Plot the difference in means
plot(bayesian_difference, which = "mean", credMass = 0.95, ROPE = NULL)