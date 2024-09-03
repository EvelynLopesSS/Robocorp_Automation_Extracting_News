from robocorp.tasks import task
from robocorp.workitems import WorkItems

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
    country = wi.get_variable("country")
    category = wi.get_variable("category")
    months = wi.get_variable("months")

    main(country, category, months)
    #main("brazil", "economy", 2)