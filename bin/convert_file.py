import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
from sys import argv
from pathlib import Path
import datetime

def read_header(file_name):
    with open(file_name, 'r') as f:
        raw_file = f.readlines()
    raw_file = [x.strip() for x in raw_file] 
    header_dict = {}
    for line in range(0,len(raw_file),2):
        if raw_file[line][0] == '%':
            header_dict[raw_file[line][1:]] = raw_file[line+1][1:]
        else:
            break
    return header_dict
n_args = len(argv)

if ((n_args == 1) or (n_args > 3)):
    print('Incorrect number of parameters')
    print('Usage file_conversion.py input_file_path [output_file_path]')
    sys.exit(1)

input_file_path = Path(argv[1])
if not input_file_path.exists():
    print('Input file does not exist')
    sys.exit(1)

header = read_header(input_file_path)

input_file_start_time = header['Started writing at:']

if ('Info:' in header.keys()):
    input_file_custom_header = header['Info:'][1:]

    if len(input_file_custom_header.split(' ')) > 1:
        input_file_custom_header = input_file_custom_header.split(' ')[1].rjust(4,'_')
    input_file_custom_header = input_file_custom_header.rjust(5,'_')
else:
    input_file_custom_header = ''

if (n_args == 3):
    output_file_path = Path(argv[2])
    if (not output_file_path.exists()):
        print('Output file path does not exist')
        print('Saving data in input file location')
        output_file_path = input_file_path.parent
        print(output_file_path)
else:
    print('Output file not specified')
    print('Saving data in input file location')
    output_file_path = input_file_path.parent
    print(output_file_path)

output_file_name = output_file_path / (input_file_start_time + input_file_custom_header + '.csv')
print(output_file_name)

data = pd.read_csv(input_file_path, 
                    header=0, 
                    names=['Packet Counter','Cap 1','Cap 2','Cap 3','Cap 4',
                            'Capdac 1','Capdac 2','Capdac 3','Capdac 4','Temperature','Humidity'],
                            dtype=str,
                    skiprows=len(header.keys())*2-1)
# Drop footer
data = data.dropna(axis=0, how='any')
print(data)
# Convert capacitance values
cap_columns = ['Cap 1','Cap 2','Cap 3','Cap 4']
capdac_columns = ['Capdac 1','Capdac 2','Capdac 3','Capdac 4']
for col in cap_columns:
    data[col] = data[col].apply(lambda x: int(x, 16))

for col in capdac_columns:
    data[col] = data[col].apply(lambda x: int(x, 16))

for col in zip(cap_columns, capdac_columns):
    data[col[0]] = data[col[0]].apply(lambda x: x / (2<<18))
    data[col[0]] = data[col[0]] + data[col[1]] * 3.125


# Temperature and Humidity
data['Temperature'] = data['Temperature'].apply(lambda x: int(x, 16))
data['Temperature'] = data['Temperature'].apply(lambda x: -45 + 175 * x / ((2 << 15) - 1))

data['Humidity'] = data['Humidity'].apply(lambda x: int(x, 16))
data['Humidity'] = data['Humidity'].apply(lambda x: 100 * x / ((2 << 15) - 1))

data.loc[data.Temperature == -45,'Humidity'] = np.nan
data.loc[data.Temperature == -45,'Temperature'] = np.nan

data['Temperature'] = data['Temperature'].fillna(method='ffill')
data['Humidity'] = data['Humidity'].fillna(method='ffill')

start_time = datetime.datetime.strptime(input_file_start_time, "%Y%m%d_%H%M%S")

sample_rate_dict = {
    '001': 1000,
    '010': 100,
    '025': 40,
    '050': 20,
    '100': 10
} 

sample_rate = header['Sample rate:']

t = []
for i in range(len(data)):
    t.append(start_time + i*datetime.timedelta(milliseconds=sample_rate_dict[sample_rate]))

data['Time'] = t

print(output_file_name)
data.to_csv(output_file_name, index=False)

plt.subplots(2,4)
plt.subplot(2,4,1)
plt.plot(data['Cap 1'])
plt.subplot(2,4,2)
plt.plot(data['Cap 2'])
plt.subplot(2,4,3)
plt.plot(data['Cap 3'])
plt.subplot(2,4,4)
plt.plot(data['Cap 4'])
plt.subplot(2,4,5)
plt.plot(data['Temperature'])
plt.subplot(2,4,6)
plt.plot(data['Humidity'])
plt.show()