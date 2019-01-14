import json
import pandas as pd
import os
import time

configPath = os.path.join(os.getcwd(), 'config.json')
with open(configPath, 'r') as f:
    config = json.load(f)


files = []
for (dirpath, dirnames, filenames) in os.walk(config['csvFolder']):
    for f in filenames:
        if f.lower().endswith(('.csv')):
            files.append({ 'uri': os.path.join(dirpath, f), 'filename': f })

resultFile = None

baseCSV = pd.read_csv("/home/kelvin/Desktop/WCC-1.csv", skip_blank_lines=True)
baseCSV['Date'] = baseCSV['Date'] + ' ' + baseCSV['Time']
baseCSV['Date'] = pd.to_datetime(baseCSV['Date'])
baseCSV = baseCSV.set_index('Date')

# print(baseCSV)
resultFile = baseCSV
for csv in files:
    print(csv)
    csvConfig = config['defaultSettings']
    if csv['filename'] in config['csvFiles']:
        csvConfig = config['csvFiles'][csv['filename']]
    df = pd.read_csv(csv['uri'], skip_blank_lines=True)
    df['Date'] = df['Report Timings:'] + ' ' + df['All Hours']
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y %H:%M:%S')
    df = df.set_index('Date')
    df.index = df.index.map(lambda x: x.replace(second=0))
    # print(df)
    # if resultFile is None:
    #     resultFile = df
    # else:
    #     resultFile = resultFile.append(df, ignore_index=True, sort=False)
    baseCSV[csv['filename']] = df['Unnamed: 2']

# print(resultFile)
resultFile.to_csv(os.path.join(config['exportFolder'], "exported-"+str(int(time.time())) +".csv"), index=True, na_rep='')
print('file exported ' + os.path.join(config['exportFolder'], "exported-"+str(int(time.time())) +".csv"))