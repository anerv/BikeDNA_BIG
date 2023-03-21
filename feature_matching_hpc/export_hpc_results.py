
import os
import yaml
import shutil

with open(r"config.yml") as file:

    parsed_yaml_file = yaml.load(file, Loader=yaml.FullLoader)

    study_area = parsed_yaml_file["study_area"]

source = f'{study_area}/processed/'
destination = f'../data/COMPARE/{study_area}/processed/'

files = os.listdir(source)

for f in files:
    shutil.move(source+f, destination)

source = f'{study_area}/results/'
destination = f'../results/COMPARE/{study_area}/data/'

files = os.listdir(source)

for f in files:
    shutil.move(source+f, destination)

