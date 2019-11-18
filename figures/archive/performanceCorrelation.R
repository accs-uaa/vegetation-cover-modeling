# Import data
ca_file = 'E:/VegetationEcology/Data_Harmonization/Project_GIS/Data_Output/modelResults/carex_aquatilis/metrics.csv'
ea_file = 'E:/VegetationEcology/Data_Harmonization/Project_GIS/Data_Output/modelResults/eriophorum_angustifolium/metrics.csv'
ev_file = 'E:/VegetationEcology/Data_Harmonization/Project_GIS/Data_Output/modelResults/eriophorum_vaginatum/metrics.csv'
rt_file = 'E:/VegetationEcology/Data_Harmonization/Project_GIS/Data_Output/modelResults/rhododendron_tomentosum/metrics.csv'
sp_file = 'E:/VegetationEcology/Data_Harmonization/Project_GIS/Data_Output/modelResults/salix_pulchra/metrics.csv'
vv_file = 'E:/VegetationEcology/Data_Harmonization/Project_GIS/Data_Output/modelResults/vaccinium_vitisidaea/metrics.csv'
ca_performance = read.csv(ca_file, header=TRUE, stringsAsFactors = FALSE)
ea_performance = read.csv(ea_file, header=TRUE, stringsAsFactors = FALSE)
ev_performance = read.csv(ev_file, header=TRUE, stringsAsFactors = FALSE)
rt_performance = read.csv(rt_file, header=TRUE, stringsAsFactors = FALSE)
sp_performance = read.csv(sp_file, header=TRUE, stringsAsFactors = FALSE)
vv_performance = read.csv(vv_file, header=TRUE, stringsAsFactors = FALSE)

# Test correlation per species
ca_cor = cor.test(ca_performance$overall_r_score, ca_performance$auc, alternative='two.sided', method='pearson')
ea_cor = cor.test(ea_performance$overall_r_score, ea_performance$auc, alternative='two.sided', method='pearson')
ev_cor = cor.test(ev_performance$overall_r_score, ev_performance$auc, alternative='two.sided', method='pearson')
rt_cor = cor.test(rt_performance$overall_r_score, rt_performance$auc, alternative='two.sided', method='pearson')
sp_cor = cor.test(sp_performance$overall_r_score, sp_performance$auc, alternative='two.sided', method='pearson')
vv_cor = cor.test(vv_performance$overall_r_score, vv_performance$auc, alternative='two.sided', method='pearson')

# Display correlation test results
ca_cor
ea_cor
ev_cor
rt_cor
sp_cor
vv_cor