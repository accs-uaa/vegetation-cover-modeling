# Vegetation Cover Modeling
Python-based ArcGIS toolbox for semi-quantitative modeling and mapping of vegetation cover.

## Getting Started
These instructions will enable you to run the Vegetation Cover Modeling toolbox in ArcGIS Pro. This toolbox is not compatible with ArcGIS Desktop. The ArcGIS python environment must be set up with python libraries that are not included in the ArcGIS python installation by default.

### Prerequisites
1. ArcGIS Pro 2.2.0 or higher
2. Python 3.5.3 or higher
3. Scikit-learn 0.18.1 or higher
4. mysql-connecter 2.0.4 or higher
5. Access to Google Earth Engine
6. TauDEM 5.3.7 or higher

### Installing
1. In ArcGIS Pro, select the python management option. Using the conda install option, install the most recent version of scikit-learn and mysql-connector.
2. Download or clone this repository to a folder on a drive accessible to your computer. Local drives may perform better than network drives. The structure and names of files and folders within the repository should not be altered.
3. In ArcGIS Pro, open the catalog tab, right click the toolbox folder, select "add toolbox", and navigate to the location of the toolbox in the repository.
4. In order to query vegetation data, you will need to set up a mysql server and create an instance of the Alaska VegPlots Database. For more information, see: [https://github.com/accs-uaa/vegetation-plots-database](https://github.com/accs-uaa/vegetation-plots-database).
5. Install [TauDEM](http://hydrology.usu.edu/taudem/taudem5/index.html) 5.3.7+ according to the documentation provided by TauDEM.

## Usage

### Earth Engine
The Earth Engine script produces a cloud-reduced greenest pixel composite (based on maximum NDVI) for Landsat 8 bands 1-7 plus Enhanced Vegetation Index-2 (EVI2), Normalized Burn Ratio (NBR), Normalized Difference Moisture Index (NDMI), Normalized Difference Snow Index (NDSI), Normalized Difference Vegetation Index (NDVI), Normalized Difference Water Index (NDWI) using the Top-Of-Atmosphere (TOA) reflectance image collection filtered to the month of July from 2013 through 2017. See Chander et al. 2009 for a description of the TOA reflectance method.
* In [Google Earth Engine code editor](https://code.earthengine.google.com/), paste this script into the javascript window. You can save modify and save the script in a git repository within Google Earth Engine.
* Run the script. The results can be inspected on the map (shows NDVI), in the inspector, and in the console.
* Once the imagery has been prepared, each image must be exported to a Google Drive by clicking the "run" button. The export requires a large amount of available storage in the Google Drive (over 100 gb) and can take up to several hours to process.

### Calculation of Topographic Predictor Variables
The following topographic predictor variables were calculated from the National Elevation Dataset 2-Arc Second Digital Elevation Model after reprojecting it to Alaska Albers Equal Area Conic with 60 m cell size. The variables were calculated using the Geomorphometry and Gradient Toolbox 2.0 (Evans et al. 2014). All outputs were converted to integers, some with the modifications indicated in parantheses below.
1. Linear Aspect
2. Slope (multiplied by 10)
3. Roughness
4. Surface Area Ratio
5. Surface Relief Ratio (multiplied by 1000)
6. Compound Topographic Index (multiplied by 100)
7. Heat Load Index (multiplied by 1000)
8. Integrated Moisture Index (divided by 10)
9. Site Exposure Index (multiplied by 100)

### Calculation of Hydrologic Predictor Variables
The following hydrologic predictor variables were calculated using scripts based partially on the calculation of a stream network from a digital elevation model using TauDEM. These script tools are located in the "Predictors" toolset of the Vegetation Cover Toolbox. In addition to the National Elevation Dataset 60 m Second Digital Elevation Model used by each of these tools, "Distance to Floodplain" used the Circumboreal Vegetation Map and the Landscape Level Ecological Mapping of Northern Alaska.

#### Distance To Streams (Large and Small)
"Distance to Streams (Large and Small)" processes a Digital Elevation Model into a stream network attributed with stream order and then segregates streams of orders 3-9 (large streams) from streams of orders 1-2 (small streams). The euclidean distance to each type of stream is calculated and output as an integer distance raster. The stream network is also output as a feature class. The hydrographic area of influence must be larger than the study area to account for flow that enters the study area and influences stream order.
* *Input Digital Elevation Model for Alaska*: Select a digital elevation model that provides full coverage of the study area. The National Elevation Dataset or 3D Elevation Program 60 m Digital Elevation Model provides coverage for the entire state of Alaska.
* *Area of Influence*: Select the hydrographic area of influence feature class for the study area. Hydrographic area of influence should include the entire study area plus watersheds that contribute flow to watersheds within the study area. This ensures that watersheds outside the study area are accounted for when calculating stream order of streams within the study area.
* *Study Area*: Select the study area feature class. This is the polygon that defines the region of analysis.
* *Cell Size*: Define the cell size, which should match the desired cell size of analysis and model output.
* *TauDEM*: Select location of the TauDEM ArcGIS Toolbox.
* *Number of Processes*: Define the number of processes to run for TauDEM calculations. The default is 12. Less capable machines should be set to run 8 processes.
* *Work Folder*: Define a folder that can store intermediate files during the processing.
* *Work Geodatabase*: Define a geodatabase that can store intermediate feature classes during the processing.
* *Stream Network*: Line feature class of stream network attributed with stream order, as calculated from digital elevation model.
* *Distance to Large Streams*: Raster dataset with values representing distance in meters to the nearest large stream feature.
* *Distance to Small Streams*: Raster dataset with values representing distance in meters to the nearest small stream feature.

#### Distance to Floodplain
"Distance to Floodplain" processes a Digital Elevation Model, the Circumboreal Vegetation Map, and the Landscape Level Ecological Mapping of Northern Alaska to create a coarse floodplain map for Northern Alaska. The euclidean distance to floodplain is calculated and output as an integer distance raster. The floodplain distribution is also output as a feature class. This tool must be executed after the "Distance to Streams (Large and Small)" tool because it requires the stream network feature class as an input.


### Calculation of Climate Predictor Variables
All climate variables were downloaded as historic or projected decadal averages from [Scenarios Network for Alaska and Arctic Planning](https://www.snap.uaf.edu/). Projected variables all use the RCP6.0 (for file names and scripts, written as RCP60). Historic data was based on the CRU TS3.1. Decadal averages for all climate variables except summer warmth index were averaged into inter-decadal averages using the "Average Climate Data" tool. Summer warmth index was calculated by summing the inter-decadal monthly average temperatures per day for May through September using the "Summer Warmth Index" tool.

#### Average Climate Data
"Average Climate Data" processes decadal average climate datasets to find the mean for multiple decades. No other formatting is performed by this tool.

#### Summer Warmth Index
"Summer Warmth Index" processes decadal average mean monthly temperature datasets for May through September to sum inter-decadal averages by number of days per month. No other formatting is performed by this tool.
* *Input Decadal May Average Temperatures*: Define a set of mean decadal average temperature rasters for May.
* *Input Decadal June Average Temperatures*: Define a set of mean decadal average temperature rasters for June.
* *Input Decadal July Average Temperatures*: Define a set of mean decadal average temperature rasters for July.
* *Input Decadal August Average Temperatures*: Define a set of mean decadal average temperature rasters for August.
* *Input Decadal September Average Temperatures*: Define a set of mean decadal average temperature rasters for September.
* *Work Folder*: Define a folder that can store intermediate files during the processing.
* *Output Raster*: Define a raster that will store the summer warmth index output.

### Predictor Variable Names
The names of the predictor variables were shortened according to the scheme shown in the table below for simplicity during modeling:


### Processing Workflow
This workflow assumes that the user has set up a copy of the Alaska VegPlots Database on a local MySQL server or an accessible MySQL server. For instructions related to the database, see the database repository at the link in the installation instructions above.
1. Create Area of Interest
2. Format Environmental Predictors
3. Format Spectral Predictors
4. Query Vegetation Plot Data by Species (Vegplots Database Tools)
5. Vegetation Cover Sites (Vegplots Database Tools)
6. Merge Presence - Absence Data
7. Prepare Watershed Prediction Units
8. Classify and Extract Input Data
9. Train and test random forest model.
10. Train and predict random forest model.

#### 1. Create Area of Interst:
"Create Area of Interest" creates an area of interest raster from a polygon study area that is matched to the shared extent of the unformatted predictor rasters and a user-specified snap raster and cell size. This tool assumes that the polygon study area and the predictor rasters are in the same projection.
* *Study Area*: Select a polygon study area that defines the modeling area. The area of interest (modeling area) can be different than the prediction area but must entirely include the prediction area. The projection of the study area should be set to the projection of the desired output and must be the same as the projection of all input datasets.
* *Input Rasters*: Select a stack of unformatted predictor rasters that will be used as predictor variables in the model. Unformatted means that the rasters do not need to share the same grid or cell size. The unformatted rasters contribute a shared maximum extent to the area of interest to eliminate the possibility of NoData cells entering the model.
* *Cell Size*: Define the cell size of the area of interest, which should match the desired cell size of analysis and model output.
* *Snap Raster*: Define a raster to match the grid alignment of the area of interest. The snap raster should be equivalent to the grid alignment of the desired model output.
* *Area of Interest*: Provide a name and location for the area of interest raster output.

#### 2. Format Environmental Predictors:
"Format Environmental Predictors" processes an input raster stack for use as predictive variables in a classification or regression model by extracting to the area of interest and matching the cell size and grid. The tool will force an integer format on values. This tool assumes that the input rasters are already in the desired projection for analysis.
* *Input Rasters*: Select a stack of unformatted predictor rasters that will be used as predictor variables in the model. Unformatted means that the rasters do not need to share the same grid or cell size. This tool will format rasters so that they do share the same grid and cell size. Stacks of continuous rasters and stacks of discrete rasters must be formatted independently because of differences in output bit depth.
* *Area of Interest*: Select a raster that defines the study area extent, cell size, grid, and projection for the analysis.
* *Output Folder*: An workspace folder that will store the output rasters must be selected. The folder does not need to be empty but should not have rasters named the same as the input rasters (or those rasters will be overwritten). The output names are the same as the input names.

#### 3. Format Spectral Predictors:
"Format Spectral Predictors" processes an input raster stack for use as predictive variables in a classification or regression model by extracting to the area of interest and matching the cell size and grid. If the cell size of the input raster stack is finer than the cell size of the area of interest then the spectral predictors will be resampled to using a bilinear interpolation. This tool assumes that the input spectral rasters are single band, mosaicked, and in the projection of the desired output.
* *Input Tiles*: Select a stack of image tiles that will be processed into a continuous integer surface. The image tiles should be single band rasters with the band equivalent to the Landsat 8 band or calculated metric of interest. This tool assumes that the input image tiles are in the 4326 GCS WGS 1984 projection, unaltered from Google Earth Engine.
* *Area of Interest*: Select a raster that defines the study area extent, cell size, grid, and projection for the analysis.
* *Work Folder*: Define a folder that can store intermediate files during the processing.
* *Output Raster*: Define a raster that will store the continuous surface integer mosaic of the spectral data.

#### 4. Query Vegetation Plot Data by Species:
This tool is found in the Vegplots Database Tools toolbox. For the toolbox and documentation on its use, see the Alaska Vegetation Plots Database repository at [https://github.com/accs-uaa/vegetation-plots-database](https://github.com/accs-uaa/vegetation-plots-database).

#### 5. Vegetation Cover Sites:
This tool is found in the Vegplots Database Tools toolbox. For the toolbox and documentation on its use, see the Alaska Vegetation Plots Database repository at [https://github.com/accs-uaa/vegetation-plots-database](https://github.com/accs-uaa/vegetation-plots-database).

#### 6. Merge Presence and Absence Data:
"Merge Presence Absence Data" combines the presence cover data from a database query with the survey sites at which the species was not found. The cover values for points closer than a user-specified merge distance are averaged based on the analysis grid with the point closest to grid center retained. Cover values of zero in the presence data will be merged with zero values generated from the absence data. In the resulting dataset, zero and trace cover are indistinguishable.
* *Cover Feature*: Define the feature class that contains cover values for the taxon of interest. The cover values were likely obtained via a database query using tool 4. Query Vegetation Plot Data by Species.
* *Survey Sites*: Select the feature class containing all possible survey sites relative to the taxon of interest (the selection of possible survey sites should differ between vascular 



## Credits

### Built With
* ArcGIS Pro 2.2
* Notepad ++
* R 3.4.2
* RStudio 1.0.153
* Scikit-learn 0.18.1
* mysql-connecter 2.0.4

### Authors
* **Timm Nawrocki** - *Alaska Center for Conservation Science, University of Alaska Anchorage*

### Usage Requirements
Usage of the tools included in this toolbox should include citations of the following papers:

Nawrocki, T., ... tbd

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
McCune, B., and D. Keon. 2002. Equations for potential annual direct incident radiation and heat load index. Journal of Vegetation Science. 13. 603-606.

### License
This project is private and can be used by Alaska Center for Conservation Science and collaborators.
