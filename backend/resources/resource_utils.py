from datetime import datetime

def validate_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")                             
    except:
        raise ValueError("datetime needs to be in format %Y-%m-%d %H:%M:%S")

