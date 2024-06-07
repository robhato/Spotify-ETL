import extract_spo as ex
import pandas as pd


def Data_Quality(load_df):
    if load_df.empty:
        print('No data in DataFrame')
        return False
    
    if pd.Series(load_df['Timestamp']).is_unique:
        pass
    else:
        raise Exception("Primary Key Exception, may contain numerous of the same entries")
    
    if load_df.isnull().values.any():
        raise Exception("Null Values within DataFrame")
    
if __name__ == "__main__":
    load_df = ex.create_recently_played_df()
    Data_Quality(load_df)
    print(load_df)