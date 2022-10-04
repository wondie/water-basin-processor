import os
import glob

import processing
from qgis.core import QgsVectorLayer, QgsVectorFileWriter


def convert_csv_to_point_layer(path, shp_path, x, y):
    """
    Converts csv file to point shapefile using lat long in the csv file.
    :param path: csv file path
    :type path: String
    :param shp_path: output shapefile path
    :type shp_path: String
    :param x: Longitude column name
    :type x: String
    :param y: Latitude column name
    :type y: String
    :return:
    :rtype:
    """
    if os.path.isfile(shp_path):
        return shp_path

    uri = 'file:///{}?delimiter={}&type=csv&spatialIndex=no&' \
          'subsetIndex=no&watchFile=no&crs=epsg:4326&xField={}&yField={}'.format(
        path, ',', x, y )

    uri = uri.replace('\\', '/')

    layer_csv = QgsVectorLayer(uri, os.path.basename(path),
                               'delimitedtext')

    _writer = QgsVectorFileWriter.writeAsVectorFormat(layer_csv,
                                                      shp_path,
                                                      "utf-8", layer_csv.crs(),
                                                      "ESRI Shapefile")
    return shp_path

def clip_point_by_poygon(input_layer, clip_layer, output_layer):
    try:
        processing.run('gdal:clipvectorbypolygon', {'INPUT':input_layer, 'MASK':clip_layer, 'OPTIONS' : '','OUTPUT':output_layer})
    except Exception as ex:
        print (ex)

def clip_csv_point(csv_file_path, polygon_file_path):
    shp_point = convert_csv_to_point_layer(csv_file_path, csv_file_path.replace('.csv', '.shp'), x='lon', y='lat')
    output_path = os.path.dirname(polygon_file_path)
    output_name = os.path.basename(csv_file_path).replace('Sankar_prcp_', '')
    sub_folder = os.path.basename(polygon_file_path).replace('.shp', '')
    output_path = os.path.join(output_path, sub_folder)
    if not os.path.isdir(output_path):
        os.mkdir(output_path)

    output_clipped_point = os.path.join(output_path, output_name.replace('.csv', '.shp'))
    print (output_clipped_point)
    clip_point_by_poygon(shp_point, polygon_file_path, output_clipped_point)

def clip_csv_path(csv_path, polygon_path):
    shp_files = glob.glob('{}/*.shp'.format(polygon_path))
    csv_files = glob.glob('{}/*.csv'.format(csv_path))
    for shp in shp_files:
        for csv in csv_files:
            clip_csv_point(csv, shp)

root_path = os.path.realpath(__file__)

csv_path = r'data\MPE_prcp\csv_avg'
polygon_path = r'data\WMS watersheds'
clip_csv_path(csv_path, polygon_path)
