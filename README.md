# Vegetation Cover Modeling
Python- and R-based ArcGIS toolbox for semi-quantitative modeling and mapping of vegetation cover.

## Getting Started
These instructions will enable you to run the Vegetation Cover Modeling toolbox in ArcGIS Pro. This toolbox is not compatible with ArcGIS Desktop.

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

### Workflow
This workflow assumes that the user has set up a copy of the Alaska VegPlots Database on a local MySQL server or an accessible MySQL server. For instructions related to the database, see the database repository at the link in the installation instructions above.
1. Query the vegetation plot data by species
2. Remove values less than a user-specified threshold (default is 1) from cover dataset.
3. If necessary, merge cover values of related taxa.
3. Average the cover values of points that are closer to each other than a user-specified threshold (default is 60 m).
4. Classify data
5. Extract predictor variables to csv
6. Set up training and test partitions at user-defined proportion (default is 70% training) with proportional numbers of points per class in each partition.
7. 

#### 1. Query vegetation plot data by species:
"Query Vegetation Cover" queries vegetation plot data from a user's copy of the Alaska Vegetation Plots database based on a user-input taxon.
*Database User*: Enter the name of the database user with access to the vegplots database.
*Database Password*: Enter the password for the database user with access to the vegplots database.
*Database Host*: Leave as 'localhost' if the MySQL Server is running on your local machine or change to the server host location.
*Database Name*: Leave as 'vegplots' to use the default database name or change to match a custom name for the database.
*Taxon*: Enter the name of an accepted taxon according to the new Flora of Alaska accessible at [https://floraofalaska.org/vascular-flora/](https://floraofalaska.org/vascular-flora/).
*Workspace*: Select a folder to which the tool can write temporary files.
*Query Output*: Enter a shapefile or geodatabase feature class to store the output.

#### 2. Average and merge proximal cover:
"Average Proximal Covers" finds points that are within a user-specified distance of each other, takes the mean of the cover values, and retains one of the proximal points at random.


#### 3. Create summed species assemblage cover:
"Create Assemblage Cover" combines the point outputs from multiple taxa queries into a single output where the cover value of the output is the sum of the cover values of the input.


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
