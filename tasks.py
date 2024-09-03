from robocorp.tasks import task
from RPA.Robocorp.WorkItems import WorkItems
from main import main


@task
def news_scrapper():
    """
    This function is the main entry point for the Robocorp Task.
    It retrieves the country and category from the Work Item variables,
    and then calls the main function with these values and the number of pages to scrape (2).
    """
    # Get the Work Item variables
    wi = WorkItems()
    work_item = wi.get_input_work_item()
    
    # Recupera os valores do payload
    country = work_item.payload.get("country")
    category = work_item.payload.get("category")
    months = work_item.payload.get("months")
    print(f"Country: {country}, Category: {category}, Months: {months}")
    main(country, category, months)
    #main("brazil", "economy", 2)

