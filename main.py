from SeleniumClass import SeleniumBrowser
from manage_files import salve_data_to_excel, exclude_folder

def main(search_phrase:str, category:str, month:int):
    query = [search_phrase, category ]
    exclude_folder('Img')
    drive = SeleniumBrowser()
    drive.navigate()
    drive.search(query)
    news_data = drive.extract_news_data(search_phrase, month)
    salve_data_to_excel(news_data)
    drive.close_browser()


main("brazil", "economy", 2)