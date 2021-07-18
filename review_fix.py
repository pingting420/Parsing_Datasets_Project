import pandas as pd 
import glob
import os
import numpy as np

review_path = r'data/reviews_pre_merge_done'
review_files = glob.glob(review_path + "/*")

review_df_list = []

def updateColumns(df):
    if 'pros' not in df:
        df = df.assign(pros = '')
    if 'cons' not in df:
        df = df.assign(cons = '')
    if 'alternative' not in df:
        df = df.assign(alternative = '')
    if 'reason_switching' not in df:
        df = df.assign(reason_switching = '')
    if 'reason_choosing' not in df:
        df = df.assign(reason_choosing = '')
    if 'switch_from' not in df:
        df = df.assign(switch_from = '')
    return df

def moveContent(df):
    dict = df.to_dict('records')
    for row in dict:
        
        wrong_segment_dict = {}
        
        if str(row['pros']).find('Cons:')!=-1:
            wrong_segment_dict['cons'] = str(row['pros'])
            row['pros'] = ''
        elif str(row['pros']).find('Alternative')!=-1:
            wrong_segment_dict['alternative'] = str(row['pros'])
            row['pros'] = ''
        elif str(row['pros']).find('Switching')!=-1:
            wrong_segment_dict['reason_switching'] = str(row['pros'])
            row['pros'] = ''
        elif str(row['pros']).find('Choosing')!=-1:
            wrong_segment_dict['reason_choosing'] = str(row['pros'])
            row['pros'] = ''
        elif str(row['pros']).find('Switched')!=-1:
            wrong_segment_dict['switch_from'] = str(row['pros'])
            row['pros'] = ''
        
        
        if str(row['cons']).find('Pros:')!=-1:
            wrong_segment_dict['pros'] = str(row['cons'])
            row['cons'] = ''
        elif str(row['cons']).find('Alternative')!=-1:
            wrong_segment_dict['alternative'] = str(row['cons'])
            row['cons'] = ''
        elif str(row['cons']).find('Switching')!=-1:
            wrong_segment_dict['reason_switching'] = str(row['cons'])
            row['cons'] = ''
        elif str(row['cons']).find('Choosing')!=-1:
            wrong_segment_dict['reason_choosing'] = str(row['cons'])
            row['cons'] = ''
        elif str(row['cons']).find('Switched')!=-1:
            wrong_segment_dict['switch_from'] = str(row['cons'])
            row['cons'] = ''
        
        if str(row['alternative']).find('Pros:')!=-1:
            wrong_segment_dict['pros'] = str(row['alternative'])
            row['alternative'] = ''
        elif str(row['alternative']).find('Cons:')!=-1:
            wrong_segment_dict['cons'] = str(row['alternative'])
            row['alternative'] = ''
        elif str(row['alternative']).find('Switching')!=-1:
            wrong_segment_dict['reason_switching'] = str(row['alternative'])
            row['alternative'] = ''
        elif str(row['alternative']).find('Choosing')!=-1:
            wrong_segment_dict['reason_choosing'] = str(row['alternative'])
            row['alternative'] = ''
        elif str(row['alternative']).find('Switched')!=-1:
            wrong_segment_dict['switch_from'] = str(row['alternative'])
            row['alternative'] = ''
        
        
        if str(row['reason_switching']).find('Pros:')!=-1:
            wrong_segment_dict['pros'] = str(row['reason_switching'])
            row['reason_switching'] = ''
        elif str(row['reason_switching']).find('Cons:')!=-1:
            wrong_segment_dict['alternative'] = str(row['reason_switching'])
            row['reason_switching'] = ''
        elif str(row['reason_switching']).find('Alternative')!=-1:
            wrong_segment_dict['alternative'] = str(row['reason_switching'])
            row['reason_switching'] = ''
        elif str(row['reason_switching']).find('Choosing')!=-1:
            wrong_segment_dict['reason_choosing'] = str(row['reason_switching'])
            row['reason_switching'] = ''
        elif str(row['reason_switching']).find('Switched')!=-1:
            wrong_segment_dict['switch_from'] = str(row['reason_switching'])
            row['reason_switching'] = ''
        

    
        if str(row['reason_choosing']).find('Pros:')!=-1:
            wrong_segment_dict['pros'] = str(row['reason_choosing'])
            row['reason_choosing'] = ''
        elif str(row['reason_choosing']).find('Cons:')!=-1:
            wrong_segment_dict['cons'] = str(row['reason_choosing'])
            row['reason_choosing'] = ''
        elif str(row['reason_choosing']).find('Alternative')!=-1:
            wrong_segment_dict['alternative'] = str(row['reason_choosing'])
            row['reason_choosing'] = ''
        elif str(row['reason_choosing']).find('Switching')!=-1:
            wrong_segment_dict['reason_choosing'] = str(row['reason_choosing'])
            row['reason_choosing'] = ''
        elif str(row['reason_choosing']).find('Switched')!=-1:
            wrong_segment_dict['switch_from'] = str(row['reason_choosing'])
            row['reason_choosing'] = ''
        
        
        
        if str(row['switch_from']).find('Pros:')!=-1:
            wrong_segment_dict['pros'] = str(row['switch_from'])
            row['switch_from'] = ''
        elif str(row['switch_from']).find('Cons:')!=-1:
            wrong_segment_dict['cons'] = str(row['switch_from'])
            row['switch_from'] = ''
        elif str(row['switch_from']).find('Alternative')!=-1:
            wrong_segment_dict['alternative'] = str(row['switch_from'])
            row['switch_from'] = ''
        elif str(row['switch_from']).find('Choosing')!=-1:
            wrong_segment_dict['reason_choosing'] = str(row['switch_from'])
            row['switch_from'] = ''
        elif str(row['switch_from']).find('Switching')!=-1:
            wrong_segment_dict['reason_switching'] = str(row['switch_from'])
            row['switch_from'] = ''
        
        if 'switch_reason' in row:
            if str(row['switch_reason']).find('Pros:')!=-1:
                wrong_segment_dict['pros'] = str(row['switch_reason'])
                row['switch_reason'] = ''
            elif str(row['switch_reason']).find('Cons:')!=-1:
                wrong_segment_dict['cons'] = str(row['switch_reason'])
                row['switch_reason'] = ''
            elif str(row['switch_reason']).find('Alternative')!=-1:
                wrong_segment_dict['alternative'] = str(row['switch_reason'])
                row['switch_reason'] = ''
            elif str(row['switch_reason']).find('Choosing')!=-1:
                wrong_segment_dict['reason_choosing'] = str(row['switch_reason'])
                row['switch_reason'] = ''
            elif str(row['switch_reason']).find('Switching')!=-1:
                wrong_segment_dict['reason_switching'] = str(row['switch_reason'])
                row['switch_reason'] = ''
            elif str(row['switch_reason']).find('Switched')!=-1:
                wrong_segment_dict['switch_from'] = str(row['switch_reason'])
                row['switch_reason'] = ''
            
        if 'detail' in row:
            if str(row['detail']).find('Pros:')!=-1:
                wrong_segment_dict['pros'] = str(row['detail'])
                row['detail'] = ''
            elif str(row['detail']).find('Cons:')!=-1:
                wrong_segment_dict['cons'] = str(row['detail'])
                row['detail'] = ''
            elif str(row['detail']).find('Alternative')!=-1:
                wrong_segment_dict['alternative'] = str(row['detail'])
                row['detail'] = ''
            elif str(row['detail']).find('Choosing')!=-1:
                wrong_segment_dict['reason_choosing'] = str(row['detail'])
                row['detail'] = ''
            elif str(row['detail']).find('Switching')!=-1:
                wrong_segment_dict['reason_switching'] = str(row['detail'])
                row['detail'] = ''
            elif str(row['detail']).find('Switched')!=-1:
                wrong_segment_dict['detail'] = str(row['detail'])
                row['detail'] = ''
            
            
        for col,content in wrong_segment_dict.items():
            row[col] = content
        
        #----------Cell contents clean------------
        if 'time_used' in row.keys() and str(row['time_used']).find('Used the software for:')!=-1:
            row['time_used'] = str(row['time_used']).replace('Used the software for:','')
        if 'detail' in row.keys() and str(row['detail']).find('Overall:')!=-1:
            row['detail'] = str(row['detail']).replace('Overall: ','')
        if 'pros' in row.keys() and str(row['pros']).find('Pros')!=-1:
            row['pros'] = str(row['pros']).replace('Pros: ','')
        if 'pros' in row.keys() and str(row['pros']).find('-')!=-1:
            row['pros'] = str(row['pros']).replace('-','')
        if 'cons' in row.keys() and str(row['cons']).find('Cons')!=-1:
            row['cons'] = str(row['cons']).replace('Cons: ','')
        if 'cons' in row.keys() and str(row['cons']).find('-')!=-1:
            row['cons'] = str(row['cons']).replace('-','')
        if 'switch_from' in row.keys() and str(row['switch_from']).find('Switched From')!=-1:
            row['switch_from'] = str(row['switch_from']).replace('Switched From: ','')
        if 'heading' in row.keys() and str(row['heading']).find('“')!=-1:
            row['heading'] = str(row['heading']).replace('“','')
        if 'heading' in row.keys() and str(row['heading']).find('”')!=-1:
            row['heading'] = str(row['heading']).replace('”','')
        if 'software.name' in row.keys() and str(row['software.name']).find('reviews')!=-1:
            row['software.name'] = str(row['software.name']).replace('reviews','')
        if 'alternative' in row.keys() and str(row['alternative']).find('Alternative')!=-1:
            row['alternative'] = str(row['alternative']).replace('Alternatives Considered: ','')
        if 'reason_choosing' in row.keys() and str(row['reason_choosing']).find('Reasons')!=-1:
            index = row['reason_choosing'].find(':')
            row['reason_choosing'] = str(row['reason_choosing'])[index::]
        if 'reason_choosing' in row.keys() and str(row['reason_choosing']).find(':')!=-1:
            row['reason_choosing'] = str(row['reason_choosing']).replace(': ','')
        if 'reason_switching' in row.keys() and str(row['reason_switching']).find('Reasons')!=-1:
            index = row['reason_switching'].find(':')
            row['reason_switching'] = str(row['reason_switching'])[index::]
        if 'reason_switching' in row.keys() and str(row['reason_switching']).find(':')!=-1:
            row['reason_switching'] = str(row['reason_switching']).replace(': ','')
        
        #---------------Update Score: Remove '/'----------------
        if 'overall.rating' in row.keys() and str(row['overall.rating']).find('/')!=-1:
            position = str(row['overall.rating']).index('/')
            row['overall.rating'] = float(str(row['overall.rating']).replace(str(row['overall.rating'])[position:],''))
        if 'feature' in row.keys() and str(row['feature']).find('/')!=-1:
            position = str(row['feature']).index('/')
            row['feature'] = float(str(row['feature']).replace(str(row['feature'])[position:],''))
        if 'valuemoney' in row.keys() and str(row['valuemoney']).find('/')!=-1:
            position = str(row['valuemoney']).index('/')
            row['valuemoney'] = float(str(row['valuemoney']).replace(str(row['valuemoney'])[position:],''))
        if 'cust.serv' in row.keys() and str(row['cust.serv']).find('/')!=-1:
            position = str(row['cust.serv']).index('/')
            row['cust.serv'] = float(str(row['cust.serv']).replace(str(row['cust.serv'])[position:],''))
        if 'recomm' in row.keys() and str(row['recomm']).find('/')!=-1:
            position = str(row['recomm']).index('/')
            row['recomm'] = float(str(row['recomm']).replace(str(row['recomm'])[position:],''))
        if 'easeofuse' in row.keys() and str(row['easeofuse']).find('/')!=-1:
            position = str(row['easeofuse']).index('/')
            row['easeofuse'] = float(str(row['easeofuse']).replace(str(row['easeofuse'])[position:],''))
        #---------------Update Score: Remove ','----------------
        if 'overall.rating' in row.keys() and str(row['overall.rating']).find(',')!=-1:
            position = str(row['overall.rating']).index(',')
            row['overall.rating'] = float(str(row['overall.rating']).replace(str(row['overall.rating'])[position:],''))
        if 'feature' in row.keys() and str(row['feature']).find(',')!=-1:
            position = str(row['feature']).index(',')
            row['feature'] = float(str(row['feature']).replace(str(row['feature'])[position:],''))
        if 'valuemoney' in row.keys() and str(row['valuemoney']).find(',')!=-1:
            position = str(row['valuemoney']).index(',')
            row['valuemoney'] = float(str(row['valuemoney']).replace(str(row['valuemoney'])[position:],''))
        if 'cust.serv' in row.keys() and str(row['cust.serv']).find(',')!=-1:
            position = str(row['cust.serv']).index(',')
            row['cust.serv'] = float(str(row['cust.serv']).replace(str(row['cust.serv'])[position:],''))
        if 'recomm' in row.keys() and str(row['recomm']).find(',')!=-1:
            position = str(row['recomm']).index(',')
            row['recomm'] = float(str(row['recomm']).replace(str(row['recomm'])[position:],''))
        if 'easeofuse' in row.keys() and str(row['easeofuse']).find(',')!=-1:
            position = str(row['easeofuse']).index(',')
            row['easeofuse'] = float(str(row['easeofuse']).replace(str(row['easeofuse'])[position:],''))


    df = pd.DataFrame.from_dict(dict)
    return df
        
            

count = 0
for review_file in review_files:
    count +=1
    print("Read:" + review_file + '\n')
    try:
        df = pd.read_csv(review_file)
        df = updateColumns(df)
        df = moveContent(df)
        df.to_csv(review_file,index=False)
        review_df_list.append(df)
    except:
        df = pd.read_excel(review_file)
        df = updateColumns(df)
        df = moveContent(df)
        df.to_excel(review_file,index=False)
        review_df_list.append(df)







        


    




