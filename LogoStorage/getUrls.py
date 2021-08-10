import pyrebase
import glob
import os
import pandas as pd
from pathlib import Path
import authentication

def getUrls(firebase, user):
    inPutResult = Path("../data/base_data/result_base.csv")
    if inPutResult.exists():
        result_df = pd.read_csv(inPutResult,low_memory=False).set_index('software.name',drop=False)
    else:
        print("Make Sure you have result_base.csv")
        exit()
    result_dict = result_df.to_dict("index")

    storage = firebase.storage()
    logos = glob.glob('logo/*')
    for logo in logos:
        software_name = logo[logo.find('/')+1:logo.find('.png')]
        if software_name in result_dict:
            result_dict[software_name]['logo'] = storage.child(logo).get_url(user['idToken'])
    result_df = pd.DataFrame.from_dict(result_dict,orient='index')
    result_df.to_csv(inPutResult,index=False)

def clearLocalStorage():
    logos = glob.glob('logo/*')
    for logo in logos:
        os.remove(logo)

def main():
    firebase,user = authentication.authentication()
    getUrls(firebase, user)
    clearLocalStorage()

if __name__ == "__main__":
    main()