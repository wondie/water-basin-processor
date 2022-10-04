import os
import datetime
from osgeo import ogr
import csv

def create_watershed_average(path):

    for dir_path, sub_dirs, files in os.walk(path):
        watershed = os.path.splitdrive(dir_path)[-1]
        avg_output_csv = os.path.join(dir_path, watershed+'.csv')
        print (avg_output_csv)
        with open(avg_output_csv, 'w', newline='') as avg_in:
            for shp in files:
                if not shp.endswith('.shp'):
                    continue
                data_list = []
                shp_file = os.path.join(dir_path, shp)
                date_str = shp.replace('.shp', '')
                us_date = datetime.datetime.strptime(date_str, '%Y%m%d').strftime('%m/%d/%Y')
                if shp_file.endswith('.shp'):
                    layer = QgsVectorLayer(shp_file, "any_name", "ogr")
                    output_csv = shp_file.replace('.shp', '.csv')
                    QgsVectorFileWriter.writeAsVectorFormat(
                        layer, output_csv, "utf-8", layer.crs(), "CSV", layerOptions = ['GEOMETRY=AS_XYZ']
                    )
                    with open(output_csv, 'r') as fp_in:
                        reader = csv.reader(fp_in, delimiter=" ", skipinitialspace=True,
                                            quoting=csv.QUOTE_NONE)

                        for i, row in enumerate(reader):
                            if i > 0:
                                rows = row[0].split(',')

                                data_list.append(float(rows[-1]))

                        if len(data_list) == 0:
                            average = 0
                        else:
                            average = sum(data_list)/len(data_list)

                        print (average)
                        writer = csv.writer(avg_in)
                        writer.writerow([us_date, average])
                        # avarage_list.append()
                        # float_ppt = [float(n) for n in row[2:26] if n]
                        # avg_ppt = sum(float_ppt) / len(float_ppt) if float_ppt else '0'

path = r'Mississippi_Coastal_watershed'
create_watershed_average(path)