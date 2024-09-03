import os
import shutil
import pandas as pd

     
def create_output_folder():
    parent_dir = 'output'
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)

def create_folder_in_output(folder_name):
    create_output_folder()
    folder_path = os.path.join('output', folder_name)
    if not os.path.exists(folder_path):
         os.makedirs(folder_path)
         print(f"Folder '{folder_name}' created successfully.")
    return folder_path

def create_image_path(image_name):
    img_dir = create_folder_in_output('Img')
    image_path = os.path.join(img_dir, image_name)

    return image_path



def exclude_folder_in_output(folder_name):
    folder_path = os.path.join('output', folder_name)

    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_name}' sucessfully deleted.")
    else:
        print(f"Folder '{folder_name}' not found.")

def salve_data_to_excel(df):
    excel_dir = create_folder_in_output('Excel')
    excel_path = os.path.join(excel_dir, 'news_data.xlsx')


    dataframe = pd.DataFrame(df)
    dataframe.to_excel(excel_path, sheet_name='news', index=False)
    
    