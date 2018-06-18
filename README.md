# Vegetation Cover Modeling
Python- and R-based ArcGIS toolbox for semi-quantitative modeling and mapping of vegetation cover.

## Getting Started
These instructions will enable you to run the Vegetation Cover Modeling toolbox in ArcGIS Pro. This toolbox is not compatible with ArcGIS Desktop. The ArcGIS python environment must be set up with python libraries that are not included in the ArcGIS python installation by default.

## Prerequisites
1. ArcGIS Pro 2.1.2 or higher
2. Python 3.5.3 or higher
3. Scikit-learn 0.18.1 or higher
4. mysql-connecter 2.0.4 or higher

## Installing
1. In ArcGIS Pro, select the python management option. Using the conda install option, install the most recent version of scikit-learn and mysql-connector.
2. Download this repository and unzip it to a folder on a drive accessible to your computer. Local drives may perform better than network drives. The structure and names of files and folders within the repository should not be altered.
3. In ArcGIS Pro, open the catalog tab, right click the toolbox folder, select "add toolbox", and navigate to the location of the downloaded/unzipped toolbox.
4. In order to query vegetation data, you will need to set up a mysql server and create an instance of the Alaska VegPlots Database. For more information, see: [https://github.com/accs-uaa/vegetation-plots-database](https://github.com/accs-uaa/vegetation-plots-database).

## Usage

### Earth Engine
The scripts developed for google earth engine create cloud-masked, best-pixel composite images using Landsat 8 for NDVI, NDMI, NDWI, NDSI, NBR, EVI-2, and all raw bands from July imagery between 2013 and 2017 (inclusive). The best pixel selection is based on maximum NDVI for all metrics to ensure uniform pixel selection from all bands.

### Processing Workflow
This workflow assumes that the user has set up a copy of the Alaska VegPlots Database on a local MySQL server or an accessible MySQL server. For instructions related to the database, see the database repository at the link in the installation instructions above.
1. Create Area of Interest
2. Format Environmental Predictors
3. Format Spectral Predictors
4. Query Vegetation Plot Data by Species
5. Merge Presence - Absence Data
6. Prepare Watershed Prediction Units
7. Classify and Extract Input Data
8. Train and test random forest model.
9. Train and predict random forest model.

#### 1. Create Area of Interst:
"Create Area of Interest" creates an area of interest raster from a polygon study area that is matched to the shared extent of the unformatted predictor rasters and a user-specified snap raster and cell size. This tool assumes that the polygon study area and the predictor rasters are in the same projection.
*Study Area*: Select a polygon study area that defines the modeling area. The area of interest (modeling area) can be different than the prediction area but must entirely include the prediction area. The projection of the study area should be set to the projection of the desired output and must be the same as the projection of all input datasets.
*Input Rasters*: Select a stack of unformatted predictor rasters that will be used as predictor variables in the model. Unformatted means that the rasters do not need to share the same grid or cell size. The unformatted rasters contribute a shared maximum extent to the area of interest to eliminate the possibility of NoData cells entering the model.
*Cell Size*: Define the cell size of the area of interest, which should match the desired cell size of analysis and model output.
*Snap Raster*: Define a raster to match the grid alignment of the area of interest. The snap raster should be equivalent to the grid alignment of the desired model output.
*Area of Interest*: Provide a name and location for the area of interest raster output.

#### 2. Format Environmental Predictors:
"Format Environmental Predictors" processes an input raster stack for use as predictive variables in a classification or regression model by extracting to the area of interest and matching the cell size and grid. This tool assumes that the input rasters are already in the desired projection for analysis.
*Input Rasters*: Select a stack of unformatted predictor rasters that will be used as predictor variables in the model. Unformatted means that the rasters do not need to share the same grid or cell size. This tool will format rasters so that they do share the same grid and cell size. Stacks of continuous rasters and stacks of discrete rasters must be formatted independently because of differences in output bit depth.
*Data Type*: Define data type of raster stack as continuous or discrete. The continuous rasters will be output as 32 bit float whereas the discrete rasters will be output as 16 bit signed.
*Output Folder*: An workspace folder that will store the output rasters must be selected. The folder does not need to be empty but should not have rasters named the same as the input rasters (or those rasters will be overwritten). The output names are the same as the input names.

#### 3. Format Spectral Predictors:
"Format Spectral Predictors" processes an input raster stack for use as predictive variables in a classification or regression model by extracting to the area of interest and matching the cell size and grid. If the cell size of the input raster stack is finer than the cell size of the area of interest then the spectral predictors will be resampled to using a bilinear interpolation. This tool assumes that the input spectral rasters are single band, mosaicked, and in the projection of the desired output.

#### 4. Query Vegetation Plot Data by Species:
"Query Vegetation Cover" queries vegetation plot data from a user's copy of the Alaska Vegetation Plots database based on a user-input taxon.
*Database User*: Enter the name of the database user with access to the vegplots database.
*Database Password*: Enter the password for the database user with access to the vegplots database.
*Database Host*: Leave as 'localhost' if the MySQL Server is running on your local machine or change to the server host location.
*Database Name*: Leave as 'vegplots' to use the default database name or change to match a custom name for the database.
*Taxon*: Enter the name of an accepted taxon according to the new Flora of Alaska accessible at [https://floraofalaska.org/vascular-flora/](https://floraofalaska.org/vascular-flora/).
*Workspace*: Select a folder to which the tool can write temporary files.
*Query Output*: Enter a shapefile or geodatabase feature class to store the output.

#### 5. Merge Presence and Absence Data:
"Merge Presence Absence Data" combines the presence cover data from a database query with the survey sites at which the species was not found. The cover values for points closer than a user-specified merge distance are averaged based on the analysis grid with the point closest to grid center retained. Cover values of zero in the presence data will be merged with zero values generated from the absence data. In the resulting dataset, zero and trace cover are indistinguishable.
*Cover Feature*: Define the feature class that contains cover values for the taxon of interest. The cover values were likely obtained via a database query using tool 4. Query Vegetation Plot Data by Species.
*Survey Sites*: Select the feature class containing all possible survey sites relative to the taxon of interest (the selection of possible survey sites should differ between vascular 



## Credits

### Built With
* ArcGIS Pro 2.0
* Notepad ++
* R 3.4.2
* RStudio 1.0.153
* Scikit-learn 0.18.1
* Atom

### Authors
* **Timm Nawrocki** - *Alaska Center for Conservation Science, University of Alaska Anchorage*

### Usage Requirements
* tbd

### License
This project is private and can be used by Alaska Center for Conservation Science and collaborators.
