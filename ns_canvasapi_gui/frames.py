"""
ButtonFrame for a frame with a title text and a series of buttons with different commands
ChangeFrame for a frame with a title text and a series of text entries that can be changed
NewWindowFrame for a single-button frame that opens something in a new window

"""
import customtkinter

from ns_canvasapi_gui.ctk_extensions import NewButton, NewFrame, NewLabel, NewScrollFrame, NewTextbox
from ns_canvasapi_gui.general_style import REGULARFONT, DEFAULT_GRID_OPTIONS
from ns_canvasapi_gui.util import standardize_date, standardize_time

import datetime as dt

class DateTimeFrame(NewFrame):
    """
    Creates a frame for producing a list of dates. 
    """
    def __init__(self, name: str, master: object):
        # General setup
        super().__init__(name=name, master=master)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Store parameters
        self.datetimes = []

        # Set up buttons
        button_frame = NewFrame('button_frame', master=self)
        button_frame.grid(row=0, column=0, **DEFAULT_GRID_OPTIONS)

        pattern = NewButton(name='Add Pattern', master=button_frame)
        pattern.configure(command=self.add_pattern)
        pattern.grid(row=0, column=0, **DEFAULT_GRID_OPTIONS)
        
        add = NewButton(name='Add Date/Time', master=button_frame)
        add.configure(command=self.add_datetime)
        add.grid(row=0, column=1, **DEFAULT_GRID_OPTIONS)

        remove = NewButton(name='Remove Date/Time', master=button_frame)
        remove.configure(command=self.remove_datetime)
        remove.grid(row=0, column=2, **DEFAULT_GRID_OPTIONS)

        # Set up display area
        display_frame = NewScrollFrame('display_frame', master=self)
        display_frame.grid(row=1, column=0, **DEFAULT_GRID_OPTIONS)

    def add_datetime(self):
        """
        Adds a single datetime object to the list
        """
        # Get date and time
        date = self.get_date()
        time = self.get_time()
        if date is None or time is None:
            return

        # Add the datetime object to the list
        add = self.convert_datetime(date, time)
        self.datetimes.append(add)
        self.fill_dates()

    def add_pattern(self):
        # Get start date
        start_date = self.get_date(prompt='Start Date (Month/Day/Year)')
        if start_date is None:
            return None
        start_dt = self.convert_datetime(start_date, '0:00')
        
        # Get stop date
        stop_date = self.get_date(prompt='Stop Date (Month/Day/Year)')
        if stop_date is None:
            return None
        stop_dt = self.convert_datetime(stop_date, '0:00')

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
        time = self.get_time()
        if time is None:
            return
    
        current_dt = start_dt
        delta_day = dt.timedelta(days=1)

        while current_dt <= stop_dt:
            if current_dt.strftime('%a') in pattern:
                self.datetimes.append(self.convert_datetime(current_dt.strftime('%m/%d/%Y'), time))
            current_dt += delta_day
        
        self.fill_dates()

    def convert_datetime(self, date: str, time: str):
        """
        Converts a standardized date string and time string into a datetime object
        """
        month, day, year = [int(number) for number in date.split('/')]
        hour, minute = [int(number) for number in time.split(':')]
        return dt.datetime(month=month, day=day, year=year, hour=hour, minute=minute)

    def fill_dates(self):
        # Clear old data
        subframe = self.widgets['display_frame']
        self.widgets['display_frame'].wipe()

        # Fill new data
        self.datetimes = sorted(list(set(self.datetimes)))

        for count, date in enumerate(self.datetimes):
            count_label = NewLabel(name=f'count {count+1}', master=subframe)
            count_label.configure(text=f'{count+1}')
            count_label.grid(row=count, column=0, **DEFAULT_GRID_OPTIONS)
            name_label = NewLabel(name=f'name {count+1}', master=subframe)
            name_label.configure(text=date.strftime('%a, %m/%d/%Y at %H:%M'))
            name_label.grid(row=count, column=1, **DEFAULT_GRID_OPTIONS)

    def get_date(self, prompt: str=None):
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

    def get_time(self, prompt: str=None):
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

    def remove_datetime(self):
        # Get date and time
        date = self.get_date()
        time = self.get_time()
        if date is None or time is None:
            return

        # Remove the datetime object from the list
        eliminate = self.convert_datetime(date, time)
        self.datetimes = [datetime for datetime in self.datetimes if datetime != eliminate]
        self.fill_dates()


class GridFrame(NewFrame):
    """
    Creates a frame contianing a grid of objects (buttons, labels, and textboxes)

    Parameters
        name (str): Name of the NewFrame.
        master (object): Master object.
        row_names (list): Names of the rows. Used for referencing.
        col_names (list): Names of the columns. Used for referencing.
        pattern (list): Pattern of objects in each row. Selected from 'button', 'label', and 'textbox'.
    """
    def __init__(self, name: str, master: object, row_names: list, col_names: list, pattern: list):
        # General setup
        super().__init__(name=name, master=master)

        # Store parameters
        self.col_names = col_names
        self.row_names = row_names

        # Generate Grid of NewObjects
        for row_count, row_name in enumerate(row_names):
            self.widgets[row_name] = {}
            for col_count, col_name in enumerate(col_names):
                match pattern[col_count]:
                    case 'button':
                        NewObject = NewButton
                    case 'label':
                        NewObject = NewLabel
                    case 'textbox':
                        NewObject = NewTextbox
                    case _:
                        NewObject = NewLabel
                content = NewObject(name=f'{row_name}_{col_name}', master=self)
                content.configure(font=REGULARFONT)
                content.grid(row=row_count, column=col_count, **DEFAULT_GRID_OPTIONS)
                self.widgets[row_name][col_name] = content

    def get_values(self):
        """
        Returns a dictionary of all of the values in the grid
        """
        return {(row_name, col_name): self.widgets[row_name][col_name].cget('text')
                for row_name in self.row_names
                for col_name in self.col_names}
        
