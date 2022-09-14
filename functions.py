import numpy as np
import pandas as pd

def get_df_by_types(df,process_step="current step",detailed=False):
    '''
    INPUT:
        df - pandas dataframe
        process_step - for display only
        detailed - Bool for detailed display
    
    OUTPUT:
        num_cols  :labels of numerical columns
        bool_cols :labels of boolean columns
        date_cols :labels of datetime columns
        cat_cols  :labels of categorical (string and object) columns
           
    '''
        
    num_cols = df.select_dtypes(include=[np.number]).columns 
    cat_cols = df.select_dtypes(include=["object","string"]).columns
    bool_cols = df.select_dtypes(include="bool").columns
    date_cols= df.select_dtypes(include="datetime64").columns
    print(process_step+":")
    print("\t- {} numeric columns".format(len(num_cols)))
    if detailed and len(num_cols)>0:
        print(num_cols)
    
    print("\t- {} boolean columns".format(len(bool_cols)))
    if detailed and len(bool_cols)>0:
        print(bool_cols)
        
    print("\t- {} date columns".format(len(date_cols)))
    if detailed and len(date_cols)>0:
        print(date_cols)
        
    print("\t- {} categorical columns".format(len(cat_cols)))
    if detailed and len(cat_cols)>0:
        print(cat_cols)
    
    return num_cols,bool_cols,date_cols,cat_cols

def convert_price_cols(df,price_cols):
    '''
    INPUT:
        df - pandas dataframe
        price_cols - column labels
    
    OUTPUT:
        modified df with e.g. $1,230.50 converted to 1230.50 in one of the price_cols 
           
    '''
    for col in price_cols:
        try:
            df[col] = pd.to_numeric((df[col].str.replace(',','',regex=False)).str.replace('$','',regex=False))
        except:
            continue

def convert_percent(df,percent_cols):
    '''
    INPUT:
        df - pandas dataframe
        percent_cols - column labels
    
    OUTPUT:
        modified df with e.g. 95% converted to 0.95 in one of the percent_cols 
           
    '''
    for col in percent_cols:
        try:
            df[col] = df[col].str.rstrip('%').astype('float') / 100.0
        except:
            continue

def convert_bool_cols(df,bool_cols,bool_dict= {'t': 1, 'f': 0}):
    '''
    INPUT:
        df - pandas dataframe
        bool_cols - column labels
    
    OUTPUT:
        modified df with boolean columns
           
    '''
    for col in bool_cols:    
        try:
            df.replace({col: bool_dict},inplace=True)
            df[col]=df[col].astype(pd.Int64Dtype())
        except:
            print("Could not infer boolean for column {}".format(col))
            continue
    
def convert_date_cols(df,date_cols):
    '''
    INPUT:
        df - pandas dataframe
        date_cols - column labels
    
    OUTPUT:
        modified df with datetime columns
           
    '''
    for col in date_cols:
        try:
            df[col] = pd.to_datetime(df[col], infer_datetime_format=True)
        except:
            print("Could not infer date for column {}".format(col))
            continue
        
def convert_scores (df,rate_dict):
    '''
    INPUT:
        df - pandas dataframe
        rate_dict - a map column name to max_value
    
    OUTPUT:
        modified df, if value = 9 and rate_dict = 10, returned 0.9
           
    '''
    for col,max_val in rate_dict.items():
        try:
            df[col] = df[col].astype('float') / float(max_val)
        except:
            print("Could not infer rate for column {}".format(col))
            continue
    
    
def create_dummy_df(df, cat_cols, dummy_na):
    '''
    INPUT:
    df - pandas dataframe with categorical variables you want to dummy
    cat_cols - list of strings that are associated with names of the categorical columns
    dummy_na - Bool holding whether you want to dummy NA vals of categorical columns or not
    
    OUTPUT:
    df - a new dataframe that has the following characteristics:
            1. contains all columns that were not specified as categorical
            2. convert boolean columns to 0-1 encoding. NaN values remain NaN
            3. for non boolean categorical columns removes all the original columns in cat_cols
                3.1 dummy columns for each of the categorical columns in cat_cols
                3.2 if dummy_na is True - it also contains dummy columns for the NaN values
                3.3 Use a prefix of the column name with an underscore (_) for separating 
    '''
    for col in  cat_cols:
        try:
            has_na = df[col].isna().sum()>0
            if has_na:
                new_df = df[col].dropna()
                new_df.infer_types()
                print(new_df.dtypes)
            if df[col].dtype=='bool':
                df[col].astype('int')
            else:             
              
                # for each cat add dummy var, drop original column
                df = pd.concat([df.drop(col, axis=1), pd.get_dummies(df[col], prefix=col, prefix_sep='_', drop_first=True, dummy_na=(dummy_na and has_na))], axis=1)
        except:
            print("Error when concatening column {}".format(col))
            continue
    return df