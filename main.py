from src.manage_files import (exclude_folder_in_output, exclude_zip_files,
                              salve_data_to_excel, zip_folder)
from src.rpa_framework_browser import SeleniumBrowser


def main(search_phrase: str, category: str, month: int):
    query = [search_phrase, category]
    exclude_folder_in_output("Img")
    exclude_folder_in_output("Excel")
    drive = SeleniumBrowser()
    drive.navigate()
    drive.search(query)
    news_data = drive.extract_news_data(search_phrase, month)
    salve_data_to_excel(news_data)
    exclude_zip_files()
    zip_folder("output/Img", "Images")
    zip_folder("output/Excel", "Excel")
    drive.close_browser()
