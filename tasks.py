from robocorp.tasks import task
from main import main

@task
def news_scrapper():
    main("brazil", "economy", 2)