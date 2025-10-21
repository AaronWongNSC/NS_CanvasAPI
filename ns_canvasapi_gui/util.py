"""
Useful code when working with ns_canvasapi_gui
"""
import customtkinter

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