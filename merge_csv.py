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

for csv in files:
    print(csv)
    csvConfig = config['defaultSettings']
    if csv['filename'] in config['csvFiles']:
        csvConfig = config['csvFiles'][csv['filename']]
    df = pd.read_csv(csv['uri'], skiprows=csvConfig['skiprows'], skipfooter=csvConfig['skipfooter'], skip_blank_lines=True)
    if resultFile is None:
        resultFile = df
    else:
        resultFile = resultFile.append(df, ignore_index=True, sort=False)

# print(resultFile)
resultFile.to_csv(os.path.join(config['exportFolder'], "exported-"+str(int(time.time())) +".csv"), index=False, na_rep='')
print('file exported ' + os.path.join(config['exportFolder'], "exported-"+str(int(time.time())) +".csv"))