import datetime


def get_filtered_list(list_to_filter, key, timedelta):
    now = datetime.datetime.now()
    min_date = now - timedelta
    filtered_list = [item for item in list_to_filter if item[key] > int(min_date.timestamp())]
    return filtered_list
