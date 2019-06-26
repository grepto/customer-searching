import datetime


def get_filtered_list(list, key, timedelta):
    now = datetime.datetime.now()
    min_date = now - timedelta
    filtered_list = [item for item in list if item[key] > int(min_date.timestamp())]
    return filtered_list
