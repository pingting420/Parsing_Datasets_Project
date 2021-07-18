import pandas as pd
import glob
import os
import numpy as np
from collections import OrderedDict

#-------------------------------- Read first type of files (features already splited) --------------------------#
# get data file names
feature_path = r'data/features' # use your path
feature_files = glob.glob(feature_path + "/*")

feature_df_list = []
for feature_file in feature_files:
    print("Read:" + feature_file + '\n')
    try:
        df = pd.read_csv(feature_file)
        feature_df_list.append(df)
    except:
        df = pd.read_excel(feature_file)
        feature_df_list.append(df)

feature_df = pd.DataFrame()

for df in feature_df_list:
    feature_df = pd.concat([feature_df,df], axis = 0, ignore_index = True)

Feature_dict = feature_df.to_dict('records',into=OrderedDict)

for row in Feature_dict:
    for key in list(row.keys()):
        if key=='software.name' or key=='feature.cat':
            continue
        if any(str.isdigit(c) for c in key) and key.find('feat')!=-1:
            continue
        row.pop(key)
Features = pd.DataFrame.from_dict(Feature_dict)
Features.insert(loc=2,column='overall.feat.rating',value=np.nan)
Features.insert(loc=2,column='entry.price',value=np.nan)
Features = Features.dropna(subset=['feat1'])

Feature_dict = Features.to_dict('records',into=OrderedDict)
for row in Feature_dict:
    count, sum= 0, 0.0
    for key in list(row.keys()):
        if key.find('.rating')!=-1 and str(row[key]).find('%')!=-1:
            sum += float(str(row[key])[:-1])
            count += 1
    if count > 0:
        row['overall.feat.rating'] = str(sum/count)+'%'

Features = pd.DataFrame.from_dict(Feature_dict)

#------------------------------ Read second type of files (features combined together) ------------------------------------------

features_base = pd.DataFrame(feature_df, columns = ['software.name','Description','feature.rating','feature.count','features'])
features_base_dict = features_base.to_dict('records')

for row in features_base_dict:
    text = str(row['features'])
    if len(text)==0: 
        continue
    index = max(text.rfind('Summary'),text.rfind('summary'))
    text = text[index+len('Summary'):]

    left, count=0, 1
    for right in range(1,len(text)):

        def spilter(): #May update in future
            a = text[right].isupper() and text[right-1].islower()
            b = text[right].isupper() and text[right-1] == '.'
            return a or b
        
        if spilter():
            row['feat' + str(count)] = text[left:right]
            count += 1
            left = right
    row.pop('features')

features_base = pd.DataFrame.from_dict(features_base_dict)
features_base = features_base.dropna(subset=['Description','feature.rating','feature.count'], how='all')

result = Features.append(features_base)
result = result.sort_index(axis=0)
result.to_csv(r'data/base_data/feature_base.csv',index=False)












