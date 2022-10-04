import csv
import os

from glob import glob


def create_average_ppt_csv(infilename, outfilename):
    with open(infilename, 'r') as fp_in, open(outfilename, "wb") as outfile:
        reader = csv.reader(fp_in, delimiter=" ", skipinitialspace=True,
                            quoting=csv.QUOTE_NONE)
        writer = csv.writer(outfile)
        writer.writerow(['lon', 'lat', 'ave_ppt_mm'])
        for row in reader:
            float_ppt = [float(n) for n in row[2:26] if n]
            avg_ppt = sum(float_ppt) / len(float_ppt) if float_ppt else '0'
            writer.writerow([row[0], row[1], avg_ppt])

def batch_create_avg_ppt(path):
    dat_files = glob('{}/*.dat'.format(path))
    for dat in dat_files:
        dat_dir = os.path.dirname(dat)
        csv_dir = os.path.join(dat_dir, 'csv_avg')
        dat_file = os.path.basename(dat)
        if not os.path.isdir(csv_dir):
            os.mkdir(csv_dir)
        csv_file = dat_file.replace('.dat', '.csv')
        outfilename = os.path.join(csv_dir, csv_file)
        create_average_ppt_csv(dat, outfilename)

path = r'data\MPE_prcp'
output = r'data\MPE_prcp\csv_avg'
batch_create_avg_ppt(path)


