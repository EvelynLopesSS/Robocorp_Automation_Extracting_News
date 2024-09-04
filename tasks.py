from robocorp.tasks import task
from RPA.Robocorp.WorkItems import WorkItems

from main import main


@task
def news_scrapper():
    wi = WorkItems()
    work_item = wi.get_input_work_item()
    
    country = work_item.payload.get("country")
    category = work_item.payload.get("category")
    months = work_item.payload.get("months")
    print(f"Country: {country}, Category: {category}, Months: {months}")
    main(country, category, months)
    #main("brazil", "economy", 2)

