/* -*- coding: utf-8 -*-
---------------------------------------------------------------------------
Cloud-reduced Greenest Pixel Composite Landsat 8 Imagery for July 2013-2017
Author: Timm Nawrocki, Alaska Center for Conservation Science
Created on: 2018-08-20
Usage: Must be executed from the Google Earth Engine code editor.
Description: This script produces a cloud-reduced greenest pixel composite (based on maximum NDVI) for bands 1-7 plus Enhanced Vegetation Index-2 (EVI2), Normalized Burn Ratio (NBR), Normalized Difference Moisture Index (NDMI), Normalized Difference Snow Index (NDSI), Normalized Difference Vegetation Index (NDVI), Normalized Difference Water Index (NDWI) using the Landsat8 Top-Of-Atmosphere (TOA) reflectance image collection filtered to the month of July from 2013 through 2017. See Chander et al. 2009 for a description of the TOA reflectance method. from July imagery between 2013 and 2017 (inclusive). The best pixel selection is based on maximum NDVI for all metrics to ensure uniform pixel selection from all bands.
- EVI-2 was calculated as (Red - Green) / (Red + [2.4 x Green] + 1), where Red is Landsat 8 Band 4 and Green is Landsat 8 Band 3.
- NBR was calculated as (NIR - SWIR2) / (NIR + SWIR2), where NIR (near infrared) is Landsat 8 Band 5 and SWIR2 (short-wave infrared 2) is Landsat 8 Band 7, using the Google Earth Engine normalized difference algorithm.
- NDMI was calculated as (NIR - SWIR1)/(NIR + SWIR1), where NIR (near infrared) is Landsat 8 Band 5 and SWIR1 (short-wave infrared 1) is Landsat 8 Band 6, using the Google Earth Engine normalized difference algorithm.
- NDSI was calculated as (Green - SWIR1) / (Green + SWIR1), where Green is Landsat 8 Band 3 and SWIR1 (short-wave infrared 1) is Landsat 8 Band 6, using the Google Earth Engine normalized difference algorithm.
- NDVI was calculated as (NIR - Red)/(NIR + Red), where NIR (near infrared) is Landsat 8 Band 5 and Red is Landsat 8 Band 4, using the Google Earth Engine normalized difference algorithm.
- NDWI was calculated as (Green - NIR)/(Green + NIR), where Green is Landsat 8 Band 3 and NIR (near infrared) is Landsat 8 Band 5, using the Google Earth Engine normalized difference algorithm.
---------------------------------------------------------------------------*/

// Define an area of interest geometry.
var areaOfInterest = /* color: #ffc82d */ee.Geometry.Polygon(
        [[[-152.0102247571382, 70.9252290904927],
          [-154.4452730349626, 71.1543982293018],
          [-156.56617293317774, 71.50869963922115],
          [-162.5265409716858, 70.28273292609235],
          [-163.23075239147093, 69.89000776807097],
          [-163.58292620615333, 69.31639221665581],
          [-164.44410004139095, 69.02572331396982],
          [-166.42545877972526, 68.94545437962545],
          [-167.22535685338616, 68.21295084098831],
          [-165.43508973443917, 67.8544054239737],
          [-164.1807462457679, 67.35800364037813],
          [-164.0840990860454, 66.96186838828613],
          [-162.93032898267933, 66.81005062732052],
          [-161.69041836906888, 65.72034838653647],
          [-161.13091239684894, 65.68933638425219],
          [-160.81908235553885, 65.87350842233059],
          [-159.76881701669282, 65.88040430995149],
          [-159.2996153731802, 65.60144269239325],
          [-156.83325158776913, 65.53955564938177],
          [-157.73773899207274, 64.7740231776961],
          [-157.4941279405618, 64.51965594214724],
          [-156.90002868737903, 64.36250171897812],
          [-156.01842037346285, 64.45565788023332],
          [-155.2148138001279, 64.65602424650854],
          [-154.55437892677577, 64.60334011615699],
          [-154.02801664768302, 64.75110474060759],
          [-153.8952458627111, 64.87529210945537],
          [-152.83454410582127, 64.81450638686385],
          [-151.85713995816437, 64.75894412324766],
          [-150.8448051660892, 64.57216198916382],
          [-150.23555665036614, 64.400247041077],
          [-149.90094523207958, 64.17687502849152],
          [-148.7996579833648, 64.51680319858733],
          [-146.62775046571747, 65.37122561493678],
          [-144.44771671648448, 65.12869245276251],
          [-143.21492525374188, 64.73942263309328],
          [-141.31126213285955, 64.43296979942667],
          [-140.6801583753294, 64.41347917470533],
          [-140.6067436416567, 69.78630891489286],
          [-143.1132841021565, 70.30054561014617],
          [-144.83517301345924, 70.14831789601057],
          [-149.36291532748905, 70.64878808985637],
          [-151.2289852785363, 70.68476838804165],
          [-152.0102247571382, 70.9252290904927]]]);

// Define a function to create a cloud-reduction mask and calculate NDVI.
var ndviCloudlessAdd = function(image) {
  //Get a cloud score in the range [0, 100].
  var cloudScore = ee.Algorithms.Landsat.simpleCloudScore(image).select('cloud');
  //Create a mask of cloudy pixels from an arbitrary threshold.
  var cloudMask = cloudScore.lte(20);
    //Compute the Normalized Difference Vegetation Index (NDVI).
  var ndviCalc = image.normalizedDifference(['B5', 'B4']).rename('NDVI');
  // Return the masked image with an NDVI band.
  return image.addBands(ndviCalc).updateMask(cloudMask);
};

// Define a function for EVI-2 calculation.
var addEVI2 = function(image) {
  // Assign variables to the red and green Landsat 8 bands.
  var red = image.select('B4');
  var green = image.select('B3');
  //Compute the Enhanced Vegetation Index-2 (EVI2).
  var evi2Calc = red.subtract(green).divide(red.add(green.multiply(2.4)).add(1)).rename('EVI2');
  // Return the masked image with an EVI-2 band.
  return image.addBands(evi2Calc);
};

// Define a function for NDSI calculation.
var addNBR = function(image) {
  //Compute the Normalized Burn Ratio (NBR).
  var nbrCalc = image.normalizedDifference(['B5', 'B7']).rename('NBR');
  // Return the masked image with an NBR band.
  return image.addBands(nbrCalc);
};

// Define a function for NDMI calculation.
var addNDMI = function(image) {
  //Compute the Normalized Difference Moisture Index (NDMI).
  var ndmiCalc = image.normalizedDifference(['B3', 'B5']).rename('NDMI');
  // Return the masked image with an NDMI band.
  return image.addBands(ndmiCalc);
};

// Define a function for NDSI calculation.
var addNDSI = function(image) {
  //Compute the Normalized Difference Snow Index (NDSI).
  var ndsiCalc = image.normalizedDifference(['B3', 'B6']).rename('NDSI');
  // Return the masked image with an NDSI band.
  return image.addBands(ndsiCalc);
};

// Define a function for NDWI calculation.
var addNDWI = function(image) {
  //Compute the Normalized Difference Water Index (NDWI).
  var ndwiCalc = image.normalizedDifference(['B3', 'B5']).rename('NDWI');
  // Return the masked image with an NDWI band.
  return image.addBands(ndwiCalc);
};

// Import Landsat 8 TOA Reflectance (ortho-rectified).
var landsat8TOA = ee.ImageCollection('LANDSAT/LC8_L1T_TOA');

// Filter the image collection by intersection with the area of interest from 2013 to 2017 for the month of July.
var landsatFiltered = landsat8TOA.filterBounds(areaOfInterest).filter(ee.Filter.calendarRange(2013, 2017, 'year')).filter(ee.Filter.calendarRange(7, 7, 'month'));
print('Filtered Collection:', landsatFiltered);

// Calculate NDVI for image collection and add as new band.
var ndviCollection = landsatFiltered.map(ndviCloudlessAdd);

// Make a greenest pixel composite from the image collection.
var compositeGreenest = ndviCollection.qualityMosaic('NDVI');

// Add bands to the greenest pixel composite for EVI-2, NBR, NDMI, NDSI, NDWI.
var compositeGreenest = addEVI2(compositeGreenest);
var compositeGreenest = addNBR(compositeGreenest);
var compositeGreenest = addNDMI(compositeGreenest);
var compositeGreenest = addNDSI(compositeGreenest);
var compositeGreenest = addNDWI(compositeGreenest);
print('Greenest Pixel NDVI:', compositeGreenest)

// Define parameters for NDVI.
var ndviParams = {
  bands: ['NDVI'],
  min: -1,
  max: 1,
  palette: ['blue', 'white', 'green']
};

// Add image to the map.
Map.setCenter(-154.43408203125, 67.4845662217412, 5);
var visParams = {bands: ['B4', 'B3', 'B2'], max: 0.3};
Map.addLayer(compositeGreenest, visParams, 'Greenest pixel composite');

// Create a single band image for Landsat 8 bands 1-7 and the additional bands calculated above.
var band_1_ultraBlue = ee.Image(compositeGreenest).select(['B1']);
var band_2_blue = ee.Image(compositeGreenest).select(['B2']);
var band_3_green = ee.Image(compositeGreenest).select(['B3']);
var band_4_red = ee.Image(compositeGreenest).select(['B4']);
var band_5_nearInfrared = ee.Image(compositeGreenest).select(['B5']);
var band_6_shortInfrared1 = ee.Image(compositeGreenest).select(['B6']);
var band_7_shortInfrared2 = ee.Image(compositeGreenest).select(['B7']);
var evi2 = ee.Image(compositeGreenest).select(['EVI2']);
var nbr = ee.Image(compositeGreenest).select(['NBR']);
var ndmi = ee.Image(compositeGreenest).select(['NDMI']);
var ndsi = ee.Image(compositeGreenest).select(['NDSI']);
var ndvi = ee.Image(compositeGreenest).select(['NDVI']);
var ndwi = ee.Image(compositeGreenest).select(['NDWI']);

// Export images to Google Drive.
Export.image.toDrive({
  image: band_1_ultraBlue,
  description: '07July_1_ultraBlue',
  scale: 30,
  region: areaOfInterest,
  maxPixels: 30000000000
});
Export.image.toDrive({
  image: band_2_blue,
  description: '07July_2_blue',
  scale: 30,
  region: areaOfInterest,
  maxPixels: 30000000000
});
Export.image.toDrive({
  image: band_3_green,
  description: '07July_3_green',
  scale: 30,
  region: areaOfInterest,
  maxPixels: 30000000000
});
Export.image.toDrive({
  image: band_4_red,
  description: '07July_4_red',
  scale: 30,
  region: areaOfInterest,
  maxPixels: 30000000000
});
Export.image.toDrive({
  image: band_5_nearInfrared,
  description: '07July_5_nearInfrared',
  scale: 30,
  region: areaOfInterest,
  maxPixels: 30000000000
});
Export.image.toDrive({
  image: band_6_shortInfrared1,
  description: '07July_6_shortInfrared1',
  scale: 30,
  region: areaOfInterest,
  maxPixels: 30000000000
});
Export.image.toDrive({
  image: band_7_shortInfrared2,
  description: '07July_7_shortInfrared2',
  scale: 30,
  region: areaOfInterest,
  maxPixels: 30000000000
});
Export.image.toDrive({
  image: evi2,
  description: '07July_evi2',
  scale: 30,
  region: areaOfInterest,
  maxPixels: 30000000000
});
Export.image.toDrive({
  image: nbr,
  description: '07July_nbr',
  scale: 30,
  region: areaOfInterest,
  maxPixels: 30000000000
});
Export.image.toDrive({
  image: ndmi,
  description: '07July_ndmi',
  scale: 30,
  region: areaOfInterest,
  maxPixels: 30000000000
});
Export.image.toDrive({
  image: ndsi,
  description: '07July_ndsi',
  scale: 30,
  region: areaOfInterest,
  maxPixels: 30000000000
});
Export.image.toDrive({
  image: ndvi,
  description: '07July_ndvi',
  scale: 30,
  region: areaOfInterest,
  maxPixels: 30000000000
});
Export.image.toDrive({
  image: ndwi,
  description: '07July_ndwi',
  scale: 30,
  region: areaOfInterest,
  maxPixels: 30000000000
});