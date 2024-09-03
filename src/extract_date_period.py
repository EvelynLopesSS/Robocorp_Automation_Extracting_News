from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def calculate_time_interval(months: int):
    current_date  = datetime.now()
    start_date  = datetime(current_date.year, current_date.month, 1)
    end_date  = start_date + relativedelta(months=months+1) - timedelta(days=1)

    start_date =start_date.strftime('%d %b %Y')
    end_date =end_date.strftime('%d %b %Y')
    return start_date, end_date

# months = 2
# start_date, end_date = calculate_time_interval(months)

# print(start_date, end_date)