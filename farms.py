import sqlite3
import numpy as np
from osgeo import gdal, gdalconst, gdalnumeric, ogr
import sys
import os


def import_farms(file_name, band, seive):
	gdal.UseExceptions()

	#create a folder for the band output
	folder = "output/band_" + str(band)
	if not os.path.exists(folder):
		os.makedirs(folder)

    #open file
	file1 = gdal.Open(file_name)
	band1 = file1.GetRasterBand(1)
	data1 = gdalnumeric.BandReadAsArray(band1)

	#limit band to the data i care about
	rastercalc = np.vectorize(lambda x: 1 if x==band else np.nan)
	data2 = rastercalc(data1)

	#create a new geotiff
	driver1 = gdal.GetDriverByName("GTiff")
	file2 = driver1.Create(folder + "/band_" + str(band) + ".tiff", file1.RasterXSize, file1.RasterYSize, 1, band1.DataType)
	gdalnumeric.CopyDatasetInfo(file1,file2)
	band2 = file2.GetRasterBand(1)
	band2.SetNoDataValue(0)
	gdalnumeric.BandWriteArray(band2, data2)

	#close original data
	file1 = None
	band1 = None

	#then polygonize
	driver2 = ogr.GetDriverByName("ESRI Shapefile")
	file3 = driver2.CreateDataSource(folder + "/band_" + str(band) + ".shp" )
	data3 = file3.CreateLayer( "band_" + str(band) , srs = None )
	gdal.Polygonize( band2, band2, data3, -1, [], callback=None )

	#then sieve the data

	#then calculate fields

	#then move fields to db

	#close dataset
	return

if __name__ == "__main__":
	import_farms('input/test.tif',36,10000)