# Vegetation Cover Modeling
*Author*: Timm Nawrocki, Alaska Center for Conservation Science  
*Created On*: 2018-08-20 
*Last Updated:* 2019-11-18 
*Description*: Scripts and script-tools for quantitative mapping of plant species foliar cover.  

## Getting Started
These instructions will enable you to run the Vegetation Cover Modeling scripts. The scripts integrate multiple systems: MySQL database, Google Earth Engine, python-based ArcGIS Pro toolbox, jupyter notebooks optimized for Google Cloud Compute Engine, and R scripts executable in R or RStudio. The ArcGIS python environment must be set up with python libraries that are not included in the ArcGIS python installation by default. Additional python environments using the Anaconda 3 distribution can be set up on local or virtual machines.

All of the analyses are scripted to be reproducible and abstracted to be applicable beyond this particular project. Because scripts are abstracted, they will not run without being properly parameterized. Inputs and outputs have not therefore been captured in the scripts. Reproducing the results of this study will require proper execution of all scripts. Detailed instructions for each script or tool have been included in this readme file below.

### Prerequisites
1. ArcGIS Pro 2.2.3+  
  a. Python 3.5.3+  
  b. mysql-connecter 2.0.4+  
  c. os  
  d. numpy 1.13.3+  
  e. pandas 0.23.4+  
2. Geomorphometry and Gradient Metrics ArcGIS Toolbox 2.0+  
3. TauDEM 5.3.7+  
4. Access to Google Earth Engine (or create Landsat 8 composites by other means)  
5. Access to Google Cloud Compute (or create virtual machines by other means)  
6. Ubuntu 18.04 LTS  
7. Anaconda 3.7 Build 2019.10  
  a. Python 3.7.4+  
  b. os  
  c. numpy 1.16.5+  
  d. pandas 0.25.1+  
  e. seaborn 0.9.0+  
  f. matplotlib 3.1.1+  
  g. scikit-learn 0.21.3+  
  h. xgboost 0.90+  
  i. GPy 1.9.9+  
  j. GPyOpt 1.2.5+
  k. joblib 0.13.2+  
8. R 3.6.1+  
  a. sp 1.3-2+  
  b. raster 3.0-7+  
  c. rgdal 1.4-7+  
  d. stringr  
9. RStudio Server 1.2.5019+  

### Installing
1. Install ArcGIS Pro, [TauDEM](http://hydrology.usu.edu/taudem/taudem5/index.html), [Geomorphometry and Gradient Metrics Toolbox](https://evansmurphy.wixsite.com/evansspatial/arcgis-gradient-metrics-toolbox), and [R](https://www.r-project.org/) in a local environment according to the documentation provided by the originators.
2. In ArcGIS Pro, select the python management option. Using the conda install option, install the most recent version of mysql-connector.
3. Download or clone this repository to a folder on a drive accessible to your computer. Local drives may perform better than network drives. The structure and names of files and folders within the repository should not be altered.
4. In ArcGIS Pro, open the catalog tab, right click the toolbox folder, select "add toolbox", and navigate to the location of the toolbox in the repository.
5. In order to query vegetation data, set up a mysql server and create an instance of the Alaska Vegetation Plots Database. For more information, see: [https://github.com/accs-uaa/vegetation-plots-database](https://github.com/accs-uaa/vegetation-plots-database).
6. Configure access to Google Earth Engine and Google Cloud Compute Engine.
7. Set up virtual machines in Google Cloud Compute Engine according to instructions provided in the "cloudCompute" folder of this repository.

## Usage

### Earth Engine: Composite Landsat 8 Image Bands and Metrics
The Earth Engine scripts produce cloud-reduced greenest pixel composites (based on maximum NDVI) for Landsat 8 bands 1-7 plus Enhanced Vegetation Index-2 (EVI2), Normalized Burn Ratio (NBR), Normalized Difference Moisture Index (NDMI), Normalized Difference Snow Index (NDSI), Normalized Difference Vegetation Index (NDVI), Normalized Difference Water Index (NDWI) using the Top-Of-Atmosphere (TOA) reflectance image collection filtered to the months of May, June, July, August, and September from 2013 through 2017. See Chander et al. 2009 for a description of the TOA reflectance method.
* In the [Google Earth Engine code editor](https://code.earthengine.google.com/), paste the monthly earth engine script into the javascript window. You can optionally modify and save the script in a git repository within Google Earth Engine.
* Run the script. The results can be inspected in the map window (shows a natural color blue-green-red image), in the inspector, and in the console.
* Once the imagery has been prepared, each image must be exported to a Google Drive by clicking the "run" button. The export requires a large amount of available storage in the Google Drive (over 500 gb) and can take up to several hours to process.
* Download the imagery from the Google Drive to a local directory.

### ArcGIS Pro: Calculation of Topographic Predictor Variables
The following topographic predictor variables were calculated from the National Elevation Dataset (NED) 2-Arc Second Digital Elevation Model (DEM) after reprojecting it to Alaska Albers Equal Area Conic with 60 m cell size (NED 60m DEM). The variables were calculated using the Geomorphometry and Gradient Toolbox 2.0 (Evans et al. 2014). All outputs were converted to integers, some with the modifications indicated in parantheses below.
1. Linear Aspect
2. Slope (multiplied by 10)
3. Roughness
4. Surface Area Ratio
5. Surface Relief Ratio (multiplied by 1000)
6. Compound Topographic Index (multiplied by 100)
7. Heat Load Index (multiplied by 1000)
8. Integrated Moisture Index (divided by 10)
9. Site Exposure Index (multiplied by 100)

### ArcGIS Pro: Calculation of Hydrologic Predictor Variables
The following hydrologic predictor variables were calculated using scripts based partially on the calculation of a stream network from the NED 60m DEM using TauDEM. These script tools are located in the "Predictors" toolset of the Vegetation Cover ArcGIS Pro Toolbox. In addition to the NED 60m DEM used by each of these tools, "Distance to Floodplain" used the Circumboreal Vegetation Map and the Landscape Level Ecological Mapping of Northern Alaska.

#### Distance To Streams (Large and Small)
"Distance to Streams (Large and Small)" processes a Digital Elevation Model into a stream network attributed with stream order and then segregates streams of orders 3-9 (large streams) from streams of orders 1-2 (small streams). The euclidean distance to each type of stream is calculated and output as an integer distance raster. The stream network is also output as a feature class. The hydrographic area of influence must be larger than the study area to account for flow that enters the study area and influences stream order.
* *Input DEM*: Digital elevation model (DEM) that provides full coverage of the hydrographic area of influence. At the time of writing, the National Elevation Dataset or 3D Elevation Program 60 m Digital Elevation Model is the only resolution that provides coverage for the entire state of Alaska.
* *Area of Influence*: Hydrographic area of influence feature class for the study area. Hydrographic area of influence should include the entire study area plus watersheds that contribute flow to watersheds within the study area. This ensures that watersheds outside the study area are accounted for when calculating stream order of streams within the study area.
* *Study Area*: Polygon feature class that defines the region of analysis.
* *Cell Size*: Define the cell size, which should match the desired cell size of analysis and model output.
* *TauDEM*: Location of the TauDEM ArcGIS Toolbox.
* *Number of Processes*: Define the number of processes to run for TauDEM calculations. The default is 12. Less capable machines should be set to run 8 processes.
* *Work Folder*: Folder that can store intermediate files during the processing.
* *Work Geodatabase*: Geodatabase that can store intermediate feature classes during the processing.
* *Stream Network*: Output line feature class of stream network attributed with stream order, as calculated from digital elevation model.
* *Distance to Large Streams*: Output raster dataset with values representing distance in meters to the nearest large stream feature.
* *Distance to Small Streams*: Output raster dataset with values representing distance in meters to the nearest small stream feature.

#### Distance to Floodplain
"Distance to Floodplain" processes a stream network generated from a digital elevation model using TauDEM, the Circumboreal Vegetation Map, and the Landscape Level Ecological Mapping of Northern Alaska to create a coarse floodplain map for Northern Alaska. The euclidean distance to floodplain is calculated and output as an integer distance raster. The floodplain distribution is also output as a feature class. This tool must be executed after the "Distance to Streams (Large and Small)" tool because it requires the stream network feature class as an input.
* *Stream Network*: Stream network feature class that was generated from the "Distance to Streams" tool.
* *Landscape Level Ecological Mapping of Northern Alaska*: Most recent version of the Landscape Level Ecological Mapping of Northern Alaska dataset. As of June 2018, the most recent version was 2014.
* *Circumboreal Vegetation Map - Alaska and Yukon*: Most recent version of the Circumboreal Vegetation Map - Alaska and Yukon.
* *Study Area*: Polygon feature class that defines the region of analysis.
* *Snap Raster*: Define a raster to match the grid alignment of the area of interest. The snap raster should be equivalent to the grid alignment of the desired model output. As of June 2018, the most recent version was 2015.
* *Cell Size*: Define the cell size, which should match the desired cell size of analysis and model output.
* *Work Geodatabase*: Geodatabase that can store intermediate feature classes during the processing.
* *Floodplain Feature*: Output feature class of the unified floodplain surfaces within the study area.
* *Distance to Floodplain*: Output raster dataset with values representing distance in meteres to the nearest floodplain.

### ArcGIS Pro: Calculation of Climate Predictor Variables
All climate variables were downloaded as historic or projected decadal averages from [Scenarios Network for Alaska and Arctic Planning](https://www.snap.uaf.edu/). Projected variables all use the RCP6.0 (for file names and scripts, written as RCP60). Historic data was based on the CRU TS3.1. Decadal averages for all climate variables except summer warmth index were averaged into inter-decadal averages using the "Average Climate Data" tool. Summer warmth index was calculated by summing the inter-decadal monthly average temperatures per day for May through September using the "Summer Warmth Index" tool.

#### Average Climate Data
"Average Climate Data" processes decadal average climate datasets to find the mean for multiple decades. No other formatting is performed by this tool.
* *Input Rasters*: Input decadal climate average rasters of a single climate metric for decades that are to be combined into a single inter-decadal average.
* *Output Raster*: Output inter-decadal climate average of a single climate metric.

#### Summer Warmth Index
"Summer Warmth Index" processes decadal average mean monthly temperature datasets for May through September to sum inter-decadal averages by number of days per month. No other formatting is performed by this tool.
* *Decadal May Average Temperatures*: Input mean decadal average temperature rasters for May.
* *Decadal June Average Temperatures*: Input mean decadal average temperature rasters for June.
* *Decadal July Average Temperatures*: Input mean decadal average temperature rasters for July.
* *Decadal August Average Temperatures*: Input mean decadal average temperature rasters for August.
* *Decadal September Average Temperatures*: Input mean decadal average temperature rasters for September.
* *Workspace Folder*: Folder that can store intermediate files during the processing.
* *Output Raster*: Output raster of inter-decadal average summer warmth index.

### ArcGIS Pro: Query Alaska Vegetation Plots Database
To create model input data, data from the Alaska Vegetation Plots Database must be formatted into feature classes. This workflow assumes that the user has set up a copy of the Alaska Vegetation Plots Database on a local MySQL server or an accessible MySQL server and installed the associated toolbox. To access the project repository for the Alaska Vegetation Plots Database, see: [https://github.com/accs-uaa/vegetation-plots-database](https://github.com/accs-uaa/vegetation-plots-database).

#### Query Taxon Cover:
"Query Taxon Cover" queries the MySQL Alaska Vegetation Plots Database for cover by a taxon. Cover values are aggregated so that multiple values at a single site for a single date are summed.
* *Database User*: Enter the name of the database user with access to the vegplots database.
* *Database Password*: Enter the password for the database user with access to the vegplots database.
* *Database Host*: Leave as 'localhost' if the MySQL Server is running on your local machine or change to the server host location. Otherwise enter the server location for the database to be queried.
* *Database Name*: Leave as 'vegplots' to use the default database name or change to match a custom name for the database.
* *Taxon*: Enter the name of an accepted taxon according to the new Flora of Alaska accessible at [https://floraofalaska.org/comprehensive-checklist/](https://floraofalaska.org/comprehensive-checklist/).
* *Workspace Folder*: Select a folder to which the tool can write temporary files.
* *Output Feature Class*: Enter a geodatabase feature class to store the output.
* *Quantitative Cover*: Selecting 'True' will limit the queried sites to those where the method was quantitative or semi-quantitative visual estimate. Selecting 'False' will include classified cover values, such as Braun-Blanquet.
* *Start Date*: Enter the earliest date to be included in the results.
* *End Date*: Enter the latest date to be included in the results.

#### Query Aggregate Cover:
"Query Aggregate Cover" queries the MySQL Alaska Vegetation Plots Database for cover by an aggregate of taxa. Cover values are aggregated so that multiple values at a single site for a single date are summed.
* *Database User*: Enter the name of the database user with access to the vegplots database.
* *Database Password*: Enter the password for the database user with access to the vegplots database.
* *Database Host*: Leave as 'localhost' if the MySQL Server is running on your local machine or change to the server host location. Otherwise enter the server location for the database to be queried.
* *Database Name*: Leave as 'vegplots' to use the default database name or change to match a custom name for the database.
* *Aggregate*: Enter the names of accepted taxa at the lowest level with each taxon in its own field. Names should be limited to accepted names in the new Flora of Alaska accessible at [https://floraofalaska.org/comprehensive-checklist/](https://floraofalaska.org/comprehensive-checklist/).
* *Workspace Folder*: Select a folder to which the tool can write temporary files.
* *Output Feature Class*: Enter a geodatabase feature class to store the output.
* *Quantitative Cover*: Selecting 'True' will limit the queried sites to those where the method was quantitative or semi-quantitative visual estimate. Selecting 'False' will include classified cover values, such as Braun-Blanquet.
* *Start Date*: Enter the earliest date to be included in the results.
* *End Date*: Enter the latest date to be included in the results.
* *Aggregate Name*: Enter a name for the aggregate.

#### Vegetation Cover Sites:
"Vegetation Cover Sites" queries all sites with associated vegetation cover data and returns the results as a feature class in a file geodatabase.
* *Database User*: Enter the name of the database user with access to the vegplots database.
* *Database Password*: Enter the password for the database user with access to the vegplots database.
* *Database Host*: Leave as 'localhost' if the MySQL Server is running on your local machine or change to the server host location. Otherwise enter the server location for the database to be queried.
* *Database Name*: Leave as 'vegplots' to use the default database name or change to match a custom name for the database.
* *Workspace Folder*: Select a folder to which the tool can write temporary files.
* *Output Feature Class*: Enter a geodatabase feature class to store the output.
* *Type*: Define target life group of survey sites.
* *Quantitative Cover*: Selecting 'True' will limit the queried sites to those where the method was quantitative or semi-quantitative visual estimate. Selecting 'False' will include classified cover values, such as Braun-Blanquet.
* *Start Date*: Enter the earliest date to be included in the results.
* *End Date*: Enter the latest date to be included in the results.

### ArcGIS Pro: Format Model Inputs
Tools 1-5 below prepare model inputs. Tools should be executed in the order listed below.
1. Create Area of Interest
2. Format Environmental Predictors
3. Format Spectral Predictors
4. Format Taxon Data
5. Prepare Watershed Units
6. Convert Predictions to Raster

#### 1. Create Area of Interest:
"Create Area of Interest" creates an area of interest raster from a polygon study area that is matched to the shared extent of the unformatted predictor rasters and a user-specified snap raster and cell size. This tool assumes that the polygon study area and the predictor rasters are in the same projection.
* *Study Area*: Select a polygon study area that defines the modeling area. The area of interest (modeling area) can be different than the prediction area but must entirely include the prediction area. The projection of the study area should be set to the projection of the desired output and must be the same as the projection of all input datasets.
* *Input Rasters*: Select a stack of unformatted predictor rasters that will be used as predictor variables in the model. Unformatted means that the rasters do not need to share the same grid or cell size. The unformatted rasters contribute a shared maximum extent to the area of interest to eliminate the possibility of NoData cells entering the model.
* *Cell Size*: Define the cell size of the area of interest, which should match the desired cell size of analysis and model output.
* *Snap Raster*: Define a raster to match the grid alignment of the area of interest. The snap raster should be equivalent to the grid alignment of the desired model output.
* *Area of Interest Raster*: Provide a name and location for the area of interest raster output.
* *Area of Interest Feature*: Provide a name and location for the area of interest feature class output.

#### 2. Format Environmental Predictors:
"Format Environmental Predictors" processes an input raster stack for use as predictive variables in a classification or regression model by extracting to the area of interest and matching the cell size and grid. The tool will force an integer format on values. This tool assumes that the input rasters are already in the desired projection for analysis.
* *Input Rasters*: Select a stack of unformatted predictor rasters that will be used as predictor variables in the model. Unformatted means that the rasters do not need to share the same grid or cell size. This tool will format rasters so that they do share the same grid and cell size. Stacks of continuous rasters and stacks of discrete rasters must be formatted independently because of differences in output bit depth.
* *Area of Interest*: Select a raster that defines the extent, cell size, grid, and projection for the analysis.
* *Output Folder*: A workspace folder that will store the output rasters must be selected. The folder does not need to be empty but should not have rasters named the same as the input rasters (or those rasters will be overwritten). The output names are the same as the input names.

#### 3. Format Spectral Predictors:
"Format Spectral Predictors" processes an input raster stack for use as predictive variables in a classification or regression model by extracting to the area of interest and matching the cell size and grid. If the cell size of the input raster stack is finer than the cell size of the area of interest then the spectral predictors will be resampled to using a bilinear interpolation. This tool assumes that the input spectral rasters are single band, mosaicked, and in the projection of the desired output.
* *Input Tiles*: Select a stack of image tiles that will be processed into a continuous integer surface. The image tiles should be single band rasters with the band equivalent to the Landsat 8 band or calculated metric of interest. This tool assumes that the input image tiles are in the 4326 GCS WGS 1984 projection, unaltered from Google Earth Engine.
* *Area of Interest*: Select a raster that defines the extent, cell size, grid, and projection for the analysis.
* *Scaling Factor*: Multiplier value to adjust output.
* *Bit Depth*: Bit depth of the output raster.
* *Workspace Folder*: Define a folder that can store intermediate files during the processing.
* *Output Raster*: Define a raster that will store the continuous surface integer mosaic of the spectral data.

#### 4. Format Taxon Data:
"Format Taxon Data" processes the input foliar cover data for a taxon or aggregate and converts values to foliar cover integers or absences. Values from predictor rasters are extracted to the output table and exported as a csv to serve as the input for training a statistical model.
* *Cover Feature*: Select a feature class containing foliar cover values for a taxon or aggregate.
* *Survey Sites*: Select a feature class containing all surveyed sites.
* *Area of Interest*: Select a raster that defines the extent, cell size, grid, and projection for the analysis.
* *Merge Distance*: Distance within which to merge and average nearby survey points.
* *Predictor Rasters*: Select a stack of formatted predictor rasters that will be used as predictor variables in the model. Formatted means that the rasters must share the same grid and cell size.
* *Workspace Geodatabase*: Define a geodatabase that can store intermediate data during the processing.
* *Mean Cover Sites*: Output feature class with the formatted foliar cover values and predictor values.
* *Output csv*: Output csv table with the formatted foliar cover values and predictor values.

#### 5. Prepare Watershed Units:
"Prepare Watershed Units" creates point grids from watersheds within the area of interest based on the cell size and cell centroids.
* *Watersheds*: Feature class containing watersheds (5th level hydrologic units) defined by USGS Watersheds Boundary Dataset. Must have continuous coverage of the area of interest.
* *Area of Interest*: Select a raster that defines the extent, cell size, grid, and projection for the analysis.
* *Workspace Folder*: Define a folder that can store intermediate files during the processing.
* *Watershed Geodatabase*: Define an empty geodatabase that can store intermediate data during the processing.
* *Output Folder*: An empty folder that will store the output tables.



### Configure Virtual Machines on Google Cloud Compute Engine
Virtual machines are highly recommended for the model train, test, and predict steps of the analyses. The train, test, and predict scripts have been formatted as Jupyter notebooks and are optimized for 64 vCPU machines. Running these scripts with fewer than 64 CPUs or vCPUs will result in suboptimal performance or will not run properly. Virtual machines for R and Python have been kept separate in these processes.

### R: Extract Features to Watershed Points

#### 6. Extract Features to Watershed Points
"Extract Features to Points" creates a csv table of features for all points in a regular grid point matrix for each input watershed.
* *List Range*: Range that controls which watersheds are included in the extraction process. Allows splitting the total number of watersheds between multiple virtual machines.
* *Watersheds Folder*: Folder containing the csv tables of watershed point grids.
* *Predictors Folder*: Folder containing the formatted predictor rasters.
* *Output Folder*: Folder where the csv tables of watershed point grids with extracted features will be stored.

### Anaconda: Statistical Modeling of Sample Representativeness
Sample representativeness was calculated as the support vector that bound 95% of samples in feature space. The output prediction is a raster grid where each cell is predicted to have a binary response of being either within or outside the support vector.

#### 7. Create Sample Outlier Detector
"Create Sample Outlier Detector" trains a one-class outlier detection model to determine the landscape coverage of the sampled points.
* *Input File*: A csv of all sample points with features extracted.
* *Output Folder*: Folder in which to store model files.

#### 8. Delineate Sample Representation area
"Delineate Prediction Area" predicts a one-class outlier detection model to watershed data to determine the sample coverage of the watershed.
* *Model Folder*: Folder containing the scaler and outlier detector model files.
* *Watershed Folder*: Folder containing the csv point grid tables for the watersheds with features extracted.
* *Output Folder*: Folder that will store the sample representation prediction tables.
* *Subset*: Range that controls which watersheds are included in the prediction process. Allows splitting the total number of watersheds between multiple virtual machines.

### R: Convert Predictions to Rasters

#### 9. Convert Outlier Predictions to Rasters
"Convert Outlier Predictions to Rasters" converts watershed outlier predictions to rasters in img format so that sample representativeness can be delineated spatially. Raster outputs are in the same coordinate system that watersheds were exported in but will not be associated with that projection.
* *List Range*: Range that controls which watersheds are included in the conversion process. Allows splitting the total number of watersheds between multiple virtual machines.
* *Prediction Folder*: Folder containing the csv tables of predictions by watershed.
* *Raster Folder*: Folder where the output rasters of predictions by watershed will be stored.

### ArcGIS Pro: Process Sample Representation
The study area is calculated as the largest contiguous region where at least 50% of physical space within a 1.5 x 1.5 km moving grid was within the sample representation in feature space. The prediction rasters must first be mosaicked to a single raster, which becomes the sample representation input.

#### 10. Create Study area
"Create Study Area" defines the physical area of valid statistical inference from the sample representation in feature space. The sample representation in feature space must be calculated prior to running this tool.
* *Area of Interest*: Select a raster that defines the extent, cell size, grid, and projection for the analysis.
* *July NDWI*: July Normalized Difference Wetness Index is necessary for approximately defining the extent of standing water without emergent vegetation. These areas are masked out of the calculation of the study area because water is not sampled in surveys of terrestrial vegetation.
* *Sample Representation*: The raster output of the support vector that bounds 95% of input samples in feature space.
* *Threshold*: The threshold value for determining area of valid statistical inference. The default value is 50%.
* *Workspace Geodatabase*: Define a geodatabase that can store intermediate data during the processing.
* *Workspace Folder*: Define a folder that can store intermediate files during the processing.
* *Spatial Certainty*: Output raster with the continuous gradient of spatial certainty relative to sample representativeness.
* *Study Area*: Output study area polygon feature class.

### Anaconda: Statistical Modeling of Foliar cover
The statistical modeling of foliar cover for individual species occurs in a train-test cross validation and train step and a predict step. These processes can take numerous hours or days to complete. Conducting all processes on virtual machines is highly recommended.

#### 11. Distribution-abundance Train and Test by R Squared
"Distribution-Abundance Train and Test" trains a classifier to predict species presence and absence and trains a regressor to predict species abundance within areas of predicted presence. The predictions are composited into a single continuous output that can theoretically range from 0 to 100 representing percent foliar cover. All model performance metrics are calculated on the combined independent test partitions of a single iteration of 10-fold cross-validation. Optimization of hyperparameters and thresholds occurs in nested 10-fold cross-validations that use only the training partitions of the outer cross-validation folds. Models are optimized to maximize R squared.
* *Input File*: CSV table containing the mean foliar cover observations for a particular species with the features extracted.
* *Output Folder*: Folder where the model files, report, and figures will be saved.
* *Output Report Name*: Name (.html file) of the output text report on statistical performance.
* *Taxon Name*: Name of the taxon or aggregate (spaces allowed).

#### 11-alt. Distribution-abundance Train and Test by Negative Mean Squared Error
"Distribution-Abundance Train and Test" trains a classifier to predict species presence and absence and trains a regressor to predict species abundance within areas of predicted presence. The predictions are composited into a single continuous output that can theoretically range from 0 to 100 representing percent foliar cover. All model performance metrics are calculated on the combined independent test partitions of a single iteration of 10-fold cross-validation. Optimization of hyperparameters and thresholds occurs in nested 10-fold cross-validations that use only the training partitions of the outer cross-validation folds. Models are optimized to minimize negative mean squared error.
* *Input File*: CSV table containing the mean foliar cover observations for a particular species with the features extracted.
* *Output Folder*: Folder where the model files, report, and figures will be saved.
* *Output Report Name*: Name (.html file) of the output text report on statistical performance.
* *Taxon Name*: Name of the taxon or aggregate (spaces allowed).

#### 12. Map Performance Discrete NSSI
"Map Performance Discrete NSSI" estimates the amount of observed spatial heterogeneity in species foliar cover predicted by a discrete type vegetation map, the North Slope Land Cover map. All model performance metrics are calculated on the combined independent test partitions of 10-fold cross-validation.
* *Input File*: CSV table containing the mean foliar cover observations for a particular species with the features extracted.
* *Metrics File*: Output csv table containing the mean foliar cover observations and the predictions based on the discrete type map.

#### 13. Map Performance Discrete Random
"Map Performance Discrete Random" estimates the amount of observed spatial heterogeneity in species foliar cover predicted by a random distribution of 25 discrete classes. All model performance metrics are calculated on the combined independent test partitions of 10-fold cross-validation.
* *Input File*: CSV table containing the mean foliar cover observations for a particular species with the features extracted.
* *Metrics File*: Output csv table containing the mean foliar cover observations and the predictions based on the discrete type map.

#### 14. Distribution-abundance Predictor
"Distribution-Abundance Predict" applies the trained classifier and regressor to data in regular point grid format stored in csv files to create a composite prediction representing the distribution and proportional abundance of the target species.
* *Model Folder*: Folder containing the classifier for distribution and regressor for foliar cover of a target species.
* *Watershed Folder*: Folder containing the csv point grid tables for the watersheds with features extracted.
* *Prediction Folder*: Output folder where the csv tables with species foliar cover predictions by watershed will be stored.

### R: Convert Predictions to Rasters

#### 15. Convert Distribution-abundance Predictions to Rasters
"Convert Distribution-abundance Predictions to Raster" processes the composite distribution-adundance predictions in csv tables into rasters in img format. Raster outputs are in the same coordinate system that watersheds were exported in but will not be associated with that projection.
* *List Range*: Range that controls which watersheds are included in the extraction process. Allows splitting the total number of watersheds between multiple virtual machines.
* *Prediction Folder*: Folder containing the csv tables with species foliar cover predictions by watershed.
* *Raster Folder*: Output folder where the rasters with species foliar cover predictions by watershed will be stored.

### ArcGIS Pro: Process Sample Representation
The output foliar cover prediction rasters must be mosaicked into a single continuous surface using the Mosaic to New Raster tool. The raster must then be post-processed to produce a final output.

#### 16. Post-process Distribution-abundance
"Post-process Distribution-abundance" converts predictions to positive integers and extracts to the study area.
* *Area of Interest*: Select a raster that defines the extent, cell size, grid, and projection for the analysis.
* *Study Area*: Select a polygon feature class that defines the area of valid statistical inference.
* *Species Raster*: Composite raster from statistical model predictions for a particular taxon or aggregate.
* *Output Raster*: Output integer raster representing foliar cover prediction for a taxon or aggregate.


## Credits

### Authors
* **Timm Nawrocki** - *Alaska Center for Conservation Science, University of Alaska Anchorage*

### Usage Requirements
Usage of the tools included in this toolbox should cited as follows:

Nawrocki, T.W. 2019. Vegetation Cover Modeling. Git Repository. Available: https://github.com/accs-uaa/vegetation-cover-modeling

#### Geomorphometry and Gradient Toolbox 2.0
1. Evans, J.S., J. Oakleaf, S.A. Cushman, and D. Theobald. 2014. An ArcGIS Toolbox for Surface Gradient and Geomorphometric Modeling, version 2.0-0. Available:  http://evansmurphy.wix.com/evansspatial.
2. Cushman, S.A., K. Gutzweiler, J.S. Evans, and K. McGarigal. 2010. The Gradient Paradigm: A conceptual and analytical framework for landscape ecology [Chapter 5]. In: Cushman, S.A., F. Huettmann (eds.). Spatial complexity, informatics, and wildlife conservation. Springer. New York, New York. 83-108.

#### Geomorphometry and Gradient Toolbox 2.0: Roughness
1. Riley, S.J., S.D. DeGloria, and R. Elliot. 1999. A terrain ruggedness index that quantifies topographic heterogeneity. Intermountain Journal of Sciences. 5. 1-4.
2. Blasczynski, J.S. 1997. Landform characterization with Geographic Information Systems. Photogrammetric Engineering and Remote Sensing. 63. 183-191.

#### Geomorphometry and Gradient Toolbox 2.0: Surface Area Ratio
1. Pike, R.J., and S.E. Wilson. 1971. Elevation relief ratio, hypsometric integral, and geomorphic area altitude analysis. Bulletin of the Geological Society of America. 82. 1079-1084.

#### Geomorphometry and Gradient Toolbox 2.0: Compound Topographic Index
1. Gessler, P.E., I.D. Moore, N.J. McKenzie, and P.J. Ryan. 1995. Soil-landscape modeling and spatial prediction of soil attributes. International Journal of GIS. 9. 421-432.
2. Moore, I.D., P.E. Gessler, G.A. Nielsen, and G.A. Petersen. 1993. Terrain attributes: estimation methods and scale effects. In:  Jakeman, A.J., and M. McAleer (eds.). Modeling Change in Environmental Systems. Wiley. London, United Kingdom. 189-214.

#### Geomorphometry and Gradient Toolbox 2.0: Heat Load Index
1. McCune, B., and D. Keon. 2002. Equations for potential annual direct incident radiation and heat load index. Journal of Vegetation Science. 13. 603-606.

#### Google Earth Engine
1. Gorelick, N. M. Hancher, M. Dixon, S. Ilyushchenko, D. Thau, and R. Moore. Google Earth Engine: Planetary-scale geospatial analysis for everyone. Remote Sensing of Environment. 202: 18-27.

#### R library: sp
1. Pebesma, E.J., and R.S. Bivand. 2005. Classes and methods for spatial data in R. R News. 5: https://cran.r-project.org/doc/Rnews/
2. Bivand, R.S., E.J. Pebesma, and V. Gomez-Rubio. 2013. Applied spatial data analysis with R, second edition. Springer. New York, New York. 405 p.

#### R library: raster
1. Hijmans, R.J. 2017. Raster: Geographic Data Analysis and Modeling. R package version 2.6-7. https://CRAN.R-project.org/package=raster

#### R library: rgdal
1. Bivand, R.S., T. Keitt, and B. Rowlingson. 2018. Rgdal: Bindings for the ‘Geospatial’ Data Abstraction Library. R package version 1.3-4. https://CRAN.R-project.org/package=rgdal

#### Geospatial Data Abstraction Library
1. GDAL/OGR contributors. 2018. GDAL/OGR Geospatial Data Abstraction software Library. Open Source Geospatial Foundation. http://gdal.org

#### Python Package: sklearn
1. Pedregosa, F., G. Varoquaux, A. Gramfort, V. Michel, B. Thirion, O. Grisel, M. Blondel, P. Prettenhofer, R. Weiss, V. Duborg, J. Vanderplas, A. Passos, D. Cournapeau, M. Brucher, M. Perrot, and E. Duchesnay. 2011. Scikit-learn: machine learning in python. Journal of Machine Learning Research. 12: 2825-2830.
2. Buitinck, L., G. Louppe, M. Blondel, F. Pedregosa, A. Mueller, O. Grisel, V. Niculae, P. Prettenhofer, A. Gramfort, J. Grobler, R. Layton, J. Vanderplas, A. Joly, B. Holt, and G. Varaoquaux. 2013. API Design for machine learning software: experiences from the scikit-learn project. European Conference on Machine Learning and Principles and Practices of Knowledge Discovery in Databases: Languages for Data Mining and Machine Learning. 108-122 p. Available: https://arxiv.org/abs/1309.0238

#### Python Package: GPy
1. GPy. 2014. A Gaussian Process Framework in Python. Available: https://github.com/SheffieldML/GPy

#### Python Package GPyOpt
1. González, J., M. Osborne, and N.D. Lawrence. 2016a. GLASSES: Relieving the myopia of bayesian optimization. Proceedings of the 19th Internation Conference on Artificial Intelligence and Statistics (AISTATS). 790-799.
2. González, J., Z. Dai, P. Hennig, and N.D. Lawrence. 2016b. Batch bayesian optimization via local penalization. Proceedings of the 19th International Conference on Artificial Intelligence and Statistics (AISTATS). 648-657.
3. González, J., Z. Dai, P. Hennig, and N.D. Lawrence. 2016c. GPyOpt: A Bayesian Optimization Framework for Python. Available: https://github.com/SheffieldML/GPyOpt

#### XGBoost
1. Chen, T., and C. Guestrin. 2016. XGBoost: A Scalable Tree Boosting System. Proceedings of the 22nd Association for Computing Machinery International Conference. 785-794.

### License
This project is provided under the GNU General Public License v3.0. It is free to use and modify in part or in whole.
