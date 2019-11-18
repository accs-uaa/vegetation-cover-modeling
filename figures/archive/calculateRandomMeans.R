# Import required libraries
library(BEST)

# Define input files
carex_file = 'K:/ACCS_Work/Projects/VegetationEcology/Data_Harmonization/Supplemental/discrete_carex_aquatilis_random.csv'
eriophoruma_file = 'K:/ACCS_Work/Projects/VegetationEcology/Data_Harmonization/Supplemental/discrete_eriophorum_angustifolium_random.csv'
eriophorumv_file = 'K:/ACCS_Work/Projects/VegetationEcology/Data_Harmonization/Supplemental/discrete_eriophorum_vaginatum_random.csv'
rhododendron_file = 'K:/ACCS_Work/Projects/VegetationEcology/Data_Harmonization/Supplemental/discrete_rhododendron_tomentosum_random.csv'
salix_file = 'K:/ACCS_Work/Projects/VegetationEcology/Data_Harmonization/Supplemental/discrete_salix_pulchra_random.csv'
vaccinium_file = 'K:/ACCS_Work/Projects/VegetationEcology/Data_Harmonization/Supplemental/discrete_vaccinium_vitisidaea_random.csv'

# Read input data
carex_data = read.csv(carex_file, header=TRUE, stringsAsFactors = TRUE)
eriophoruma_data = read.csv(eriophoruma_file, header=TRUE, stringsAsFactors = TRUE)
eriophorumv_data = read.csv(eriophorumv_file, header=TRUE, stringsAsFactors = TRUE)
rhododendron_data = read.csv(rhododendron_file, header=TRUE, stringsAsFactors = TRUE)
salix_data = read.csv(salix_file, header=TRUE, stringsAsFactors = TRUE)
vaccinium_data = read.csv(vaccinium_file, header=TRUE, stringsAsFactors = TRUE)

# Create vectors from r squared
carex_vector = carex_data$r2
eriophoruma_vector = eriophoruma_data$r2
eriophorumv_vector = eriophorumv_data$r2
rhododendron_vector = rhododendron_data$r2
salix_vector = salix_data$r2
vaccinium_vector = vaccinium_data$r2

# Analyze the mean and standard deviation using Monte Carlo Markov Chain
carex_mean = BESTmcmc(carex_vector, y2 = NULL, priors = NULL, doPriorsOnly = FALSE, numSavedSteps = 1e+06, thinSteps = 1, burnInSteps = 1e+04, verbose = FALSE, rnd.seed = 314, parallel = TRUE)
eriophoruma_mean = BESTmcmc(eriophoruma_vector, y2 = NULL, priors = NULL, doPriorsOnly = FALSE, numSavedSteps = 1e+06, thinSteps = 1, burnInSteps = 1e+04, verbose = FALSE, rnd.seed = 314, parallel = TRUE)
eriophorumv_mean = BESTmcmc(eriophorumv_vector, y2 = NULL, priors = NULL, doPriorsOnly = FALSE, numSavedSteps = 1e+06, thinSteps = 1, burnInSteps = 1e+04, verbose = FALSE, rnd.seed = 314, parallel = TRUE)
rhododendron_mean = BESTmcmc(rhododendron_vector, y2 = NULL, priors = NULL, doPriorsOnly = FALSE, numSavedSteps = 1e+06, thinSteps = 1, burnInSteps = 1e+04, verbose = FALSE, rnd.seed = 314, parallel = TRUE)
salix_mean = BESTmcmc(salix_vector, y2 = NULL, priors = NULL, doPriorsOnly = FALSE, numSavedSteps = 1e+06, thinSteps = 1, burnInSteps = 1e+04, verbose = FALSE, rnd.seed = 314, parallel = TRUE)
vaccinium_mean = BESTmcmc(vaccinium_vector, y2 = NULL, priors = NULL, doPriorsOnly = FALSE, numSavedSteps = 1e+06, thinSteps = 1, burnInSteps = 1e+04, verbose = FALSE, rnd.seed = 314, parallel = TRUE)

# Display the results
carex_mean
eriophoruma_mean
eriophorumv_mean
rhododendron_mean
salix_mean
vaccinium_mean