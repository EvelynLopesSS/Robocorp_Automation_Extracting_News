from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def calculate_time_interval(months: int):
    current_date = datetime.now()
    end_date = current_date  
    start_date = current_date - relativedelta(months=months) 

    start_date_str = start_date.strftime('%d %b %Y')
    end_date_str = end_date.strftime('%d %b %Y')
    
    return start_date_str, end_date_str