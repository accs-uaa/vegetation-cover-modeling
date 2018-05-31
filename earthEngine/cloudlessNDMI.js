/* -*- coding: utf-8 -*-
---------------------------------------------------------------------------
Cloud-reduced Best Pixel Composite NDMI
Author: Timm Nawrocki, Alaska Center for Conservation Science
Created on: 2018-05-30
Usage: Must be executed from the Google Earth Engine code editor.
Description: This script produces a cloud-reduced best pixel composite Normalized Difference Moisture Index (NDMI) using Top-Of-Atmosphere (TOA) reflectance. See Chander et al. 2009 for a description of the TOA reflectance method. NDMI was calculated as (NIR - SWIR1)/(NIR + SWIR1), where NIR (near infrared) is Landsat 8 Band 5 and SWIR1 (short-wave infrared 1) is Landsat 8 Band 6, using the Google Earth Engine normalized difference algorithm.
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

// Define a function for NDMI calculation with cloud-reduction mask.
var ndmiCloudless = function(image) {
  //Get a cloud score in the range [0, 100].
  var cloudScore = ee.Algorithms.Landsat.simpleCloudScore(image).select('cloud');
  //Create a mask of cloudy pixels from an arbitrary threshold.
  var cloudMask = cloudScore.lte(20);
  //Compute the Normalized Difference Moisture Index (NDMI).
  var ndmi = image.normalizedDifference(['B3', 'B5']).rename('NDMI');
  // Return the masked image with an NDMI band.
  return image.addBands(ndmi).updateMask(cloudMask);
};

// Import Landsat 8 TOA Reflectance (ortho-rectified).
var landsat8TOA = ee.ImageCollection('LANDSAT/LC8_L1T_TOA');

// Filter the image collection by intersection with the area of interest from 2013 to 2017 for the month of July.
var landsatFiltered = landsat8TOA.filterBounds(areaOfInterest).filter(ee.Filter.calendarRange(2013, 2017, 'year')).filter(ee.Filter.calendarRange(7, 7, 'month'));
print('Filtered Collection:', landsatFiltered);

// Calculate NDWI for image collection and add as new band.
var ndmiCollection = landsatFiltered.map(ndmiCloudless);

// Make a best pixel composite from the image collection.
var compositeBest = ndmiCollection.qualityMosaic('NDMI');
print('Best Pixel NDMI:', compositeBest)

// Define parameters for NDMI.
var ndmiParams = {
  bands: ['NDMI'],
  min: -1,
  max: 1,
  palette: ['blue', 'white', 'green']
};

// Add image to the map.
Map.setCenter(-157.43408203125, 70.4845662217412, 7);
Map.addLayer(compositeBest, ndmiParams, 'NDMI Composite');

// Create a single band image with NDMI.
var ndmiBest = ee.Image(compositeBest).select(['NDMI']);

// Export image to Google Drive.
Export.image.toDrive({
  image: ndmiBest,
  description: 'cloudlessLandsat8NDMI',
  scale: 30,
  region: areaOfInterest
});