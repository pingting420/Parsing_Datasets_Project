import pandas as pd
import glob
import os
import numpy as np
from pathlib import Path


reviews_path = r'data/reviews_pre_merge_done' # use your path
review_files = glob.glob(reviews_path + "/*")

review_df_list = []
review_name_list = []
for review_file in review_files:
    try:
        rv = pd.read_csv(review_file)
        review_df_list.append(rv)
        review_name_list.append(review_file)
    except:
        rv = pd.read_excel(review_file)
        review_df_list.append(rv)
        review_name_list.append(review_file)

review_df = pd.DataFrame()
for i in range(0,len(review_df_list)):
    print("Read: "+review_name_list[i]+'\n')
    temp = pd.DataFrame(review_df_list[i],columns = ['software.name','name','job_title','business','employee','business_size','time_used','review_date','heading','detail','pros','cons','other','prob.solved','alternative',
'reason_choosing','switch_reason','switch_from','switch_to','overall.rating','overall_desc','easeofuse','cust.serv','feature','valuemoney','recomm']).dropna(subset=['name','software.name'],how='any')
    temp['valuemoney'] = temp['valuemoney'].fillna(0)
    temp[['overall.rating','feature','valuemoney','cust.serv','recomm','easeofuse']] = temp[['overall.rating','feature','valuemoney','cust.serv','recomm','easeofuse']].astype(float)
    temp = temp.dropna(subset=['software.name'])
    review_df = pd.concat([review_df,temp],axis=0,ignore_index=True)


outPutPath = Path('data/base_data/review_base.csv')
if outPutPath.exists():
    review_df.to_csv(outPutPath, index=False, header=False, mode = 'a')
else:
    review_df.to_csv(outPutPath,index=False)
print('Success!')