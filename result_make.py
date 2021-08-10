import pandas as pd
import glob
import os
import numpy as np
from pathlib import Path

# get data file names
software_path = r'data/softwares' # use your path
software_files = glob.glob(software_path + "/*")

#----------Check result_base.csv exist -----------
outPutPath = Path('data/base_data/result_base.csv')
software_old_base_dict = pd.read_csv(outPutPath).set_index('software.name',drop=False).to_dict("index") if outPutPath.exists() else {}

#------------End -----------------------

#----------Check need update------------------
updatePath = r'data/update'
update_files = glob.glob(updatePath + "/*")
update_df_list = []
for update_file in update_files:
    try:
        df = pd.read_csv(update_file)
        update_df_list.append(df)
    except:
        df = pd.read_excel(update_file)
        update_df_list.append(df)

#------------End -----------------------


software_df_list = []
software_name_dict = {}

for software_file in software_files:
    print("Read:" + software_file + '\n')
    sub_cat, main_cat= "",""
    try:
        df = pd.read_csv(software_file)
    except:
        df = pd.read_excel(software_file)
    df = df.dropna(subset=['software.name'])
    df = df.drop_duplicates(subset=['software.name'])
    software_df_list.append(df)
    dict = df.to_dict('records')
    try:
        sub_cat, main_cat = software_file.split('/')[-1].split(', ')
        main_cat = main_cat.split('.')[0]
        for row in dict:
            try:
                software_name_dict[str(row['software.name']).rstrip()] = [sub_cat,main_cat]
            except:
                continue
    except:
        for row in dict:
            try:
                software_name_dict[str(row['software.name']).rstrip()] = [str(row['sub.category']),str(row['main.category'])]
            except:
                continue
software_new_df = pd.DataFrame()
for df in software_df_list:
    software_new_df = pd.concat([software_new_df,df], axis = 0, ignore_index = True)

software_new_df = pd.DataFrame(software_new_df,columns = ['software.name','logo','Company','Description','Website','main.category','Sub.cat1','Sub.cat2','Pricing','entry.price','liked','match.score','x2.rating','overall.rating','total.reviews','recomm.rating','recomm.count','easeofuse.rating','easeofuse.count','cust.serv.rating','cust.serv.count','feature.rating','feature.count','valuemoney.rating','valuemoney.count','pros.count','cons.count','overall.1rating','overall.2rating','overall.3rating','overall.4rating','overall.5rating',
'free.trial','subscription','free.version','free.demo','open.source','train.inperson','train.online','train.webinar','train.liverep','train.doc','support.hours','support.online','support.liverep','feature_list','location','industry','sector','employee','tel','email','contact','demo','freetrial','getstarted','download','document','tutorial','community','feature','github','claim','support.url','pricing.url'])
software_new_df = software_new_df.drop_duplicates(subset=['software.name']).set_index("software.name",drop=False)

unmodified_columns = {'software.name','logo','Company','Description','Website','main.category','Sub.cat1','Sub.cat2','Pricing','entry.price','subscription','free.version','free.demo','open.source','train.inperson','train.online','train.webinar','train.liverep','train.doc','support.hours','support.online','support.liverep','feature_list','location','industry','sector','employee','tel','email','contact','demo','freetrial','getstarted','download','document','tutorial','community','feature','github'}
software_new_dict = software_new_df.to_dict('records')
for row in software_new_dict:
    row['software.name'] = str(row['software.name']).rstrip()
    if str(row['Company']).find('By ')!=-1:
        row['Company'] = str(row['Company']).replace('By ','')
    if str(row['software.name']) in software_name_dict.keys():
        row['Sub.cat1'] = software_name_dict[str(row['software.name'])][0]
        row['main.category'] = software_name_dict[str(row['software.name'])][1]

    if row['software.name'] not in software_old_base_dict.keys():
        software_old_base_dict[row['software.name']] = row
    else:
        for col,val in row.items():
            if col in unmodified_columns and str(software_old_base_dict[row['software.name']][col])!='nan':
                continue
            if str(val)!='nan':
                software_old_base_dict[row['software.name']][col] = val
    
#--------Check update folder files -------------------------
for update_df in update_df_list:
    update_df_dict = update_df.set_index('software.name',drop=False).to_dict("records") if 'software.name' in set(update_df.columns) else {}
    for row in update_df_dict:
        row['software.name'] = str(row['software.name']).rstrip()
        if str(row['software.name']) not in software_old_base_dict.keys():
            software_old_base_dict[str(row['software.name'])] = {}
        for col,val in row.items():
            if str(col) in set(software_new_df.columns):
                if str(row['software.name']) in software_old_base_dict:
                    software_old_base_dict[row['software.name']][col] = val
#------------End-------------------------------------
software_base = pd.DataFrame.from_dict(software_old_base_dict,orient='index')
software_base.replace(r'^\s*$', np.nan, regex=True)
outPutPath = Path('data/base_data/result_base.csv')
software_base.to_csv(outPutPath,index=False)


  
    
    


    