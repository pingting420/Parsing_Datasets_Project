import pandas as pd
import glob
import os
import numpy as np
from pathlib import Path

inPutReview= Path("data/base_data/review_base.csv")
review_df = pd.DataFrame()
if inPutReview.exists():
    review_df = pd.read_csv(inPutReview,low_memory=False) 
else:
    print("Make Sure you have review_base.csv")
    exit()

inPutResult = Path("data/base_data/result_base.csv")
result_df = pd.DataFrame()
if inPutReview.exists():
    result_df = pd.read_csv(inPutResult,low_memory=False) 
else:
    print("Make Sure you have result_base.csv")
    exit()

review_calculation = pd.DataFrame(review_df,columns = ['software.name','overall.rating','feature','pros','cons','recomm','cust.serv','easeofuse','valuemoney','total.reviews'])
review_calculation['total.reviews'] = 0

overall_rating_1 = review_calculation.pivot_table(index = ["software.name"], values=['overall.rating'],aggfunc={'overall.rating':lambda x: (x<=1).sum()}).reset_index('software.name',drop=False).to_dict('index')
overall_rating_2 = review_calculation.pivot_table(index = ["software.name"], values=['overall.rating'],aggfunc={'overall.rating':lambda x: ((x>1).sum()-(x>2).sum())}).reset_index('software.name',drop=False).to_dict('index')
overall_rating_3 = review_calculation.pivot_table(index = ["software.name"], values=['overall.rating'],aggfunc={'overall.rating':lambda x: ((x>2).sum()-(x>3).sum())}).reset_index('software.name',drop=False).to_dict('index')
overall_rating_4 = review_calculation.pivot_table(index = ["software.name"], values=['overall.rating'],aggfunc={'overall.rating':lambda x: ((x>3).sum()-(x>4).sum())}).reset_index('software.name',drop=False).to_dict('index')
overall_rating_5 = review_calculation.pivot_table(index = ["software.name"], values=['overall.rating'],aggfunc={'overall.rating':lambda x: (x>4).sum()}).reset_index('software.name',drop=False).to_dict('index')



review_rating = review_calculation.pivot_table(index = ["software.name"],values=["overall.rating","recomm","feature","easeofuse","cust.serv",'valuemoney'],
            aggfunc={"overall.rating":"mean","recomm":"mean","feature":"mean","easeofuse":"mean","cust.serv":"mean","valuemoney":"mean"})
review_rating = review_rating.rename(columns={"recomm": "recomm.rating","feature":"feature.rating",
    "easeofuse":"easeofuse.rating","cust.serv":"cust.serv.rating","valuemoney":"valuemoney.rating"}).reset_index().round(
    {'overall.rating':1,'recomm.rating':1,'feature.rating':1,'easeofuse.rating':1,'cust.serv.rating':1,'valuemoney.rating':1})

review_count = review_calculation.pivot_table(index = ["software.name"],values=["recomm","feature","easeofuse","total.reviews","cust.serv","pros","cons","valuemoney"],
               aggfunc={"recomm":"count","feature":"count","easeofuse":"count","total.reviews":"count","cust.serv":"count","pros":"count","cons":"count","valuemoney":"count"})
review_count = review_count.rename(columns={"recomm": "recomm.count","feature":"feature.count","easeofuse":"easeofuse.count","cust.serv":"cust.serv.count",
    "pros":"pros.count","cons":"cons.count","valuemoney":"valuemoney.count"}).reset_index()

calculation = pd.merge(review_rating,review_count,how = "inner", on="software.name").set_index('software.name',drop=False).to_dict('index')
result_dict = result_df.to_dict("records")
for row in result_dict:
    software_name = str(row['software.name'])
    if software_name in calculation:
        for col,val in calculation[software_name].items():
            row[col] = val
    if software_name in overall_rating_1:
        row['overall.1rating'] = overall_rating_1[software_name]['overall.rating']
    if software_name in overall_rating_2:
        row['overall.2rating'] = overall_rating_2[software_name]['overall.rating']
    if software_name in overall_rating_3:
        row['overall.3rating'] = overall_rating_3[software_name]['overall.rating']
    if software_name in overall_rating_4:
        row['overall.4rating'] = overall_rating_4[software_name]['overall.rating']
    if software_name in overall_rating_5:
        row['overall.5rating'] = overall_rating_5[software_name]['overall.rating']
result_df = pd.DataFrame.from_dict(result_dict)


outPutPath = Path('data/base_data/result_base.csv')
result_df.to_csv(outPutPath,index=False)
