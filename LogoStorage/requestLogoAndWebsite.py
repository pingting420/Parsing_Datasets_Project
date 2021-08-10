import clearbit
import requests
from pathlib import Path
import pandas as pd

clearbit.key = 'sk_8fb2fb29349e22e9ecd07ee93ea03c31'
inPutResult = Path("../data/base_data/result_base.csv")
if inPutResult.exists():
    result_df = pd.read_csv(inPutResult,low_memory=False) 
else:
    print("Make Sure you have result_base.csv")
    exit()

result_dict = result_df.to_dict('records')
for row in result_dict:
    if str(row['Website']).find(".")==-1:
        r = clearbit.NameToDomain.find(name=str(row['software.name']))
        if r is None:
            print(row['software.name'] + " Not Available")
            continue
        if r['logo'] is not None and r['domain'] is not None:
            row['Website'] = r['domain']
            with open('logo/'+str(row['software.name'])+'.png','wb') as f:
                f.write(requests.get(r['logo']).content)
result_df = pd.DataFrame.from_dict(result_dict)
result_df.to_csv(inPutResult,index=False)
