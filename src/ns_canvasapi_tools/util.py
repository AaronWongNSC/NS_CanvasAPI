"""
Things I find useful to have when working with ns_canvasapi.

functions:
    
"""

from datetime import datetime

def z_time_str_to_dt(z_time_str: str) -> datetime:
    """
    Convert a Z-time string to a datetime object.
    
    Args:
        z_time_str: A Z-time string. Note that this does not error-check, so 
        z_time_str_test() should be run on the string before this happens.
    
    Returns:
        datetime: A datetime object matching the Z-time.
    """
    return datetime.fromisoformat(z_time_str.replace('Z', '+00:00'))

def dt_to_local_str(dt: datetime, tz = 'pytz.timezone') -> str:
    """
    Convert a datetime object into a local time string.
    
    Args:
        dt (datetime): The datetime object being converted to a string.
        tz (pytz.timezone): The local timezone. This is typically the tz attribute
            of the object. This is set at the Canvas CanvasObject level. 
    
    Returns:
        str: The local time string of the original datetime object.
    """
    return dt.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")
