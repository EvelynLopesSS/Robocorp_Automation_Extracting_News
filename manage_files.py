import os
import shutil
import pandas as pd



def exclude_folder(folder):
    if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f'Folder "{folder}" removed successfully.')
    else:
        print(f'Folder "{folder}" does not exist.')

def salve_data_to_excel(df):
    dataframe = pd.DataFrame(df)
    if os.path.exists('news_data.xlsx'):
        os.remove('news_data.xlsx')
    dataframe.to_excel('news_data.xlsx', sheet_name='news', index=False)