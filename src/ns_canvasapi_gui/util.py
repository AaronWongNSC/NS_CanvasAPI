"""
Useful code when working with ns_canvasapi_gui
"""
import customtkinter
import datetime as dt

def change_value(button, target):
    """
    Generic function to change the value of a field after clicking a button

    Parameters
        button: The button that was clicked.
        target: The field to be changed.
    
    Returns:
        None
    """

    # Visual feedback
    print(f'Running change value protocol from {button.name} on {target.name}')
    button_name = button.cget('text')
    button.configure(text='Changing...')
    button.after(3000, lambda: button.configure(text=button_name))

    # Dialog Box
    dialog = customtkinter.CTkInputDialog(text="Enter new value:", title="Change Value")
    value = dialog.get_input()
    if value is not None and value.strip() != '':
        target.configure(text=value)

def convert_datetime(date: str, time: str):
    """
    Converts a standardized date string and time string into a datetime object
    """
    month, day, year = [int(number) for number in date.split('/')]
    hour, minute = [int(number) for number in time.split(':')]
    return dt.datetime(month=month, day=day, year=year, hour=hour, minute=minute)

def get_date(prompt: str=None):
    """
    Provides a prompt for a single date
    """
    # Set up prompt
    if prompt is None:
        prompt = 'Date (Month/Day/Year)'

    # Get date
    dialog = customtkinter.CTkInputDialog(text=prompt, title="Date")
    date = standardize_date(dialog.get_input())
    if date is None or date.strip == '':
        return None
    return date

def get_datetime():
    """
    Provides prompts to get a single datetime object
    """
    # Get date and time
    date = get_date()
    time = get_time()
    if date is None or time is None:
        return

    return convert_datetime(date, time)

def get_date_pattern():
    """
    Provides a prompt to create a list of datetime objects in a meeting pattern
    """
    # Get start date
    start_date = get_date(prompt='Start Date (Month/Day/Year)')
    if start_date is None:
        return None
    start_dt = convert_datetime(start_date, '0:00')
    
    # Get stop date
    stop_date = get_date(prompt='Stop Date (Month/Day/Year)')
    if stop_date is None:
        return None
    stop_dt = convert_datetime(stop_date, '0:00')

    # Get meeting pattern
    dialog = customtkinter.CTkInputDialog(text="Define meeting pattern (MTWRF, so MW = Monday/Wednesday):", title="Meeting Pattern")
    dow = dialog.get_input().upper()
    if dow is None or dow.strip == '':
        return None

    pattern = []
    if 'M' in dow:
        pattern.append('Mon')
    if 'T' in dow:
        pattern.append('Tue')
    if 'W' in dow:
        pattern.append('Wed')
    if 'R' in dow:
        pattern.append('Thu')
    if 'F' in dow:
        pattern.append('Fri')

    # Get time
    time = get_time()
    if time is None:
        return

    current_dt = start_dt
    delta_day = dt.timedelta(days=1)

    datetimes = []

    while current_dt <= stop_dt:
        if current_dt.strftime('%a') in pattern:
            datetimes.append(convert_datetime(current_dt.strftime('%m/%d/%Y'), time))
        current_dt += delta_day

    return datetimes

def get_time(prompt: str=None):
    """
    Provides a prompt for a time
    """
    # Set up prompt
    if prompt is None:
        prompt = 'Set the time (use 24-hour time)'

    # Get time
    dialog = customtkinter.CTkInputDialog(text=prompt, title='Time')
    time = standardize_time(dialog.get_input())
    if time is None or time.strip == '':
        return None
    return time

def new_window(parent_window: object, window_name: str):
    """
    Create a new window

    Parameters:
        parent_window: The window that generated the new window.
        window_name: The name of the new window

    Return:
        window: The created NewTopLevel 

    """
    from ns_canvasapi_gui.ctk_extensions import NewTopLevel

    print(f'Attempting to create window {window_name} with parent {parent_window.name}')
    if window_name in parent_window.self_window.windows.keys():
        print('The window already exists')
        parent_window.self_window.windows[window_name].lift()
        parent_window.self_window.windows[window_name].focus()
        return None
    else:
        print('Creating new window')
        parent_window.self_window.windows[window_name] = NewTopLevel(window_name, parent_window.self_window)
    return parent_window.self_window.windows[window_name]

def select_pkl(master: object):
    from customtkinter import filedialog
    import pickle
    import os

    filepath = filedialog.askopenfilename(
        parent=master,
        title="Select the template assignment",
        initialdir=os.getcwd() + 'saved/',
        filetypes=[("Python Pickle File", "*.pkl")]
    )

    if filepath == '':
        return None

    with open(filepath, 'rb') as file:
        contents = pickle.load(file)
    return contents

def standardize_date(date: str):
    """
    Ensure dates are in Month/Day/4-digit Year format. Returns None if it cannot be converted
    """
    try:
        month, day, year = date.split('/')
        month = int(month)
        day = int(day)
        year = int(year)
        if year < 100:
            year += 2000
        return f'{month}/{day}/{year}'
    except:
        return None

def standardize_time(time: str):
    """
    Ensure times are in 24-hour format (HH:MM)
    """
    try:
        hours, minutes = time.split(':')
        hours = int(hours)
        minutes = int(minutes)
        if hours > 24:
            return None
        return f'{hours}:{minutes}'
    except:
        return None