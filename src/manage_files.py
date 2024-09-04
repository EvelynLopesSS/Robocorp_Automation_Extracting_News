import os
import shutil
import pandas as pd
import glob
import xlsxwriter 


     
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
    #excel_path_output = os.path.join('output', 'news_data.xlsx')
    excel_path = os.path.join(excel_dir, 'news_data.xlsx')

    dataframe = pd.DataFrame(df)
    dataframe.to_excel(excel_path, sheet_name='news', index=False)
    #dataframe.to_excel(excel_path_output, sheet_name='news', index=False)
    
def zip_folder(folder_path:str, zip_file_name:str):
    zip_path = os.path.join('output', zip_file_name)

    if os.path.exists(folder_path):
        shutil.make_archive(zip_path, 'zip', folder_path)
        print(f"Pasta 'Img' zipada com sucesso em: {zip_path}.zip")
    else:
        print(f"A pasta '{folder_path}' não foi encontrada.")

def exclude_zip_files():
    zip_files = glob.glob('output/*.zip')
    for zip_file in zip_files:
        os.remove(zip_file)

def excel():
    excel_path = 'output/teste.xlsx' 
    dataframe = pd.read_excel('output/Excel/news_data.xlsx')
    dataframe = dataframe[['title', 'description', 'publication_date',
                           'search_phrase_count', 'contains_money', 'image_name',
                           'image_url', 'news_url']]

    workbook = xlsxwriter.Workbook(excel_path)
    worksheet = workbook.add_worksheet('news')
    header_format = workbook.add_format({'bold': True, 'bg_color': '#C6EFCE', 'border': 1})

    for col_num, header in enumerate(dataframe.columns):
        worksheet.write(0, col_num, header, header_format)

    for row_num, row_data in enumerate(dataframe.values, start=1):
        for col_num, value in enumerate(row_data):
            worksheet.write(row_num, col_num, value)

    options = {'name': 'Data',
               'columns': [{'header': col} for col in dataframe.columns]}
    worksheet.add_table(0, 0, len(dataframe), len(dataframe.columns) - 1, options)

    worksheet.freeze_panes(1, 0)
    workbook.close()

    print(f"Data saved: {excel_path} - successfully!")

