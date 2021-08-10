import pandas as pd
import glob
import os
import numpy as np
from pathlib import Path

inPutReview= Path("data/base_data/result_base.csv")
result_df = pd.DataFrame()
if inPutReview.exists():
    result_df = pd.read_csv(inPutReview,low_memory=False) 
else:
    print("Make Sure you have result_base.csv")
    exit()

result_df = result_df.rename(columns={'software.name':'softwareName','Company':'company','Description':'description','Website':'website',
'main.category':'mainCategory','Sub.cat1':'subCat1','Sub.cat2':'subCat1','Pricing':'pricing','entry.price':'entryPrice','match.score':'matchScore',
'x2.rating':'x2Rating','overall.rating':'overallRating','total.reviews':'totalReviews','recomm.rating':'recommRating','recomm.count':'recommCount','easeofuse.rating':'easeofuseRating',
'easeofuse.count':'easeofuseCount','cust.serv.rating':'custservRating','cust.serv.count':'custservCount','feature.rating':'featureRating','feature.count':'featureCount',
'valuemoney.rating':'valuemoneyRating','valuemoney.count':'valuemoneyCount','pros.count':'prosCount','cons.count':'consCount','overall.1rating':'overall1rating','overall.2rating':'overall2rating',
'overall.3rating':'overall3rating','overall.4rating':'overall4rating','overall.5rating':'overall5rating','free.trial':'freeTrial','free.version':'freeVersion','free.demo':'freeDemo','open.source':'openSource',
'train.inperson':'trainInperson','train.online':'trainOnline','train.webinar':'trainWebinar','train.liverep':'trainLiverep','train.doc':'trainDoc','support.hours':'supportHours','support.online':'supportOnline',
'support.liverep':'supportLiverep','support.url':'supportUrl','pricing.url':'pricingUrl'})

outPutPath = Path('data/base_data/result_base_for_firebase.csv')
result_df.to_csv(outPutPath,index=False)
