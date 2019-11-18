# Import data
ca_file = 'E:/VegetationEcology/Data_Harmonization/Project_GIS/Data_Output/modelResults/carex_aquatilis/prediction.csv'
ea_file = 'E:/VegetationEcology/Data_Harmonization/Project_GIS/Data_Output/modelResults/eriophorum_angustifolium/prediction.csv'
ev_file = 'E:/VegetationEcology/Data_Harmonization/Project_GIS/Data_Output/modelResults/eriophorum_vaginatum/prediction.csv'
rt_file = 'E:/VegetationEcology/Data_Harmonization/Project_GIS/Data_Output/modelResults/rhododendron_tomentosum/prediction.csv'
sp_file = 'E:/VegetationEcology/Data_Harmonization/Project_GIS/Data_Output/modelResults/salix_pulchra/prediction.csv'
vv_file = 'E:/VegetationEcology/Data_Harmonization/Project_GIS/Data_Output/modelResults/vaccinium_vitisidaea/prediction.csv'
ca_predictions = read.csv(ca_file, header=TRUE, stringsAsFactors = FALSE)
ea_predictions = read.csv(ea_file, header=TRUE, stringsAsFactors = FALSE)
ev_predictions = read.csv(ev_file, header=TRUE, stringsAsFactors = FALSE)
rt_predictions = read.csv(rt_file, header=TRUE, stringsAsFactors = FALSE)
sp_predictions = read.csv(sp_file, header=TRUE, stringsAsFactors = FALSE)
vv_predictions = read.csv(vv_file, header=TRUE, stringsAsFactors = FALSE)

# Subset the data to AIM NPR-A
ca_predictions = subset(ca_predictions, ca_predictions$project=='AIM NPR-A')
ea_predictions = subset(ea_predictions, ea_predictions$project=='AIM NPR-A')
ev_predictions = subset(ev_predictions, ev_predictions$project=='AIM NPR-A')
rt_predictions = subset(rt_predictions, rt_predictions$project=='AIM NPR-A')
sp_predictions = subset(sp_predictions, sp_predictions$project=='AIM NPR-A')
vv_predictions = subset(vv_predictions, vv_predictions$project=='AIM NPR-A')

# Subset the data to presences
ca_predictions = subset(ca_predictions, ca_predictions$cover!=0)
ea_predictions = subset(ea_predictions, ea_predictions$cover!=0)
ev_predictions = subset(ev_predictions, ev_predictions$cover!=0)
rt_predictions = subset(rt_predictions, rt_predictions$cover!=0)
sp_predictions = subset(sp_predictions, sp_predictions$cover!=0)
vv_predictions = subset(vv_predictions, vv_predictions$cover!=0)

# Test correlation per species
ca_cor = lm(ca_predictions$prediction~ca_predictions$presence)
ea_cor = lm(ea_predictions$prediction~ea_predictions$presence)
ev_cor = lm(ev_predictions$prediction~ev_predictions$presence)
rt_cor = lm(rt_predictions$prediction~rt_predictions$presence)
sp_cor = lm(sp_predictions$prediction~sp_predictions$presence)
vv_cor = lm(vv_predictions$prediction~vv_predictions$presence)

# Display correlation test results
summary(ca_cor)
summary(ea_cor)
summary(ev_cor)
summary(rt_cor)
summary(sp_cor)
summary(vv_cor)