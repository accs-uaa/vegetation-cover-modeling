# Vegetation Cover Modeling
Python- and R-based ArcGIS toolbox for semi-quantitative modeling and mapping of vegetation cover.

## Getting Started
These instructions will enable you to run the Vegetation Cover Random Forest toolbox in ArcGIS Pro. This toolbox is not compatible with ArcGIS Desktop.

## Prerequisites
1. ArcGIS Pro 2.1.2 or higher
2. Python 3.5.3 or higher
3. Scikit-learn 0.18.1 or higher
4. mysql-connecter 2.0.4 or higher

## Installing
1. In ArcGIS Pro, select the python management option. Using the conda install option, install the most recent version of scikit-learn and mysql-connector.
2. Download this repository and unzip it to a folder on a drive accessible to your computer. Local drives may perform better than network drives. The structure and names of files and folders within the repository should not be altered.
3. In ArcGIS Pro, open the catalog tab, right click the toolbox folder, select "add toolbox", and navigate to the location of the downloaded/unzipped toolbox.
4. In order to query vegetation data, you will need to set up a mysql server and create an instance of the Alaska VegPlots Database. For more information, see: https://github.com/accs-uaa/vegetation-plots-database

## Usage

### Workflow
*This section is a work in progress and does not reflect the current toolset.*
A suggested workflow is to create an area of interest, a set of species cover points, and a suite of predictor rasters. Use the tools in this toolbox to do the following:

#### 1. Query vegetation plot data by species:
This tool queries vegetation plot data from a user's copy of the Alaska Vegetation Plots database. The tool can either query a single taxon or a list of taxa at the species or infraspecies level.


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
