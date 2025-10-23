import customtkinter

from ns_canvasapi_tools.util import z_time_str_to_dt

from ns_canvasapi_gui.ctk_extensions import NewButton, NewCheckBox, NewFrame, NewLabel, NewScrollFrame
from ns_canvasapi_gui.frames import DateTimeFrame
from ns_canvasapi_gui.general_style import DEFAULT_GRID_OPTIONS, LARGEFONT
from ns_canvasapi_gui.util import get_datetime, get_date_pattern, new_window

class DateAdjuster(NewFrame):
    def __init__(self, name: str, master: object, *args, **kwargs):
        # General setup
        super().__init__(name=name, master=master, *args, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Set parameters
        self.assignments = None
        self.course = None
        self.incoming_checkboxes = []
        self.incoming_datetimes = []
        self.outgoing_checkboxes = []
        self.outgoing_datetimes = []

        # Main header
        header = NewLabel(name='header', master=self)
        header.configure(text='Date Adjuster', font=LARGEFONT)
        header.grid(row=0, column=0, **DEFAULT_GRID_OPTIONS)

        # Course Selection
        course_select = NewButton(name='Select Course', master=self)
        course_select.configure(command=self.select_course)
        course_select.grid(row=1, column=0, **DEFAULT_GRID_OPTIONS)

        # Button Container
        button_container = NewFrame(name='button_container', master=self)
        button_container.grid(row=2, column=0, **DEFAULT_GRID_OPTIONS)
        button_container.grid_columnconfigure((0, 1, 2, 3), weight=1)
        button_container.grid_rowconfigure(1, weight=1)

        remove_incoming = NewButton(name='Remove Incoming', master=button_container)
        remove_incoming.configure(command=self.remove_incoming_datetimes)
        remove_incoming.grid(row=0, column=0, **DEFAULT_GRID_OPTIONS)

        add_outgoing_pattern = NewButton(name='Add Outgoing Pattern', master=button_container)
        add_outgoing_pattern.configure(command=self.add_outgoing_datetimes)
        add_outgoing_pattern.grid(row=0, column=1, **DEFAULT_GRID_OPTIONS)

        add_outgoing = NewButton(name='Add Outgoing', master=button_container)
        add_outgoing.configure(command=self.add_outgoing_datetime)
        add_outgoing.grid(row=0, column=2, **DEFAULT_GRID_OPTIONS)

        remove_outgoing = NewButton(name='Remove Outgoing', master=button_container)
        remove_outgoing.configure(command=self.remove_outgoing_datetimes)
        remove_outgoing.grid(row=0, column=3, **DEFAULT_GRID_OPTIONS)

        # Date Container
        date_container = NewScrollFrame(name='date_container', master=self)
        date_container.grid(row=3, column=0, **DEFAULT_GRID_OPTIONS)

        # Check Assignments
        verify = NewButton(name='Verify Date Mapping', master=self)
        verify.configure(command=self.verify_mapping)
        verify.grid(row=4, column=0, **DEFAULT_GRID_OPTIONS)

    def add_outgoing_datetime(self):
        new_datetime = get_datetime()
        if new_datetime is None:
            return
        self.outgoing_datetimes += [new_datetime]
        self.outgoing_datetimes = sorted(list(set(self.outgoing_datetimes)))
        self.display_datetimes()

    def add_outgoing_datetimes(self):
        new_pattern = get_date_pattern()
        if new_pattern is None:
            return
        self.outgoing_datetimes += new_pattern
        self.outgoing_datetimes = sorted(list(set(self.outgoing_datetimes)))

        import pprint
        pprint.pprint(self.outgoing_datetimes)

        self.display_datetimes()

    def adjust_dates(self):
        self.self_window.windows['Mapping Verification'].long_display()
        self.self_window.windows['Mapping Verification'].widgets['Adjust the Dates'].configure(
            text='--- Adjusting the Dates ---',
            state='disabled'
        )
        self.update()
        for count, datetime in enumerate(self.incoming_datetimes):
            assignments_to_map = []
            for assignment in self.assignments:
                due_at = z_time_str_to_dt(assignment.due_at).astimezone(self.root.tz).replace(second=0)
                if due_at.strftime('%a, %m/%d/%Y at %H:%M') == datetime.strftime('%a, %m/%d/%Y at %H:%M'):
                    assignments_to_map.append(assignment)
            for assignment in assignments_to_map:
                due_at = self.root.tz.localize(self.outgoing_datetimes[count]).isoformat()
                assignment.edit(assignment={'due_at': due_at})
                print(assignment)
        self.self_window.windows['Mapping Verification'].widgets['Adjust the Dates'].configure(
            text='Dates Adjusted'
        )
        self.update()

    def display_datetimes(self):
        container = self.widgets['date_container']
        container.wipe()
        self.incoming_checkboxes = []
        self.outgoing_checkboxes = []

        for count, datetime in enumerate(self.incoming_datetimes):
            checkbox = NewCheckBox(name=f'in_{count}', master=container, variable=customtkinter.StringVar(master=self, value='off'))
            checkbox.configure(text=f'{datetime.strftime('%a, %m/%d/%Y at %H:%M')}')
            checkbox.grid(row=count, column=0, **DEFAULT_GRID_OPTIONS)
            self.incoming_checkboxes.append(checkbox)

        for count, datetime in enumerate(self.outgoing_datetimes):
            filler = NewLabel(name=f'fill_{count}', master=container)
            filler.configure(text='will become')
            filler.grid(row=count, column=1)

            checkbox = NewCheckBox(name=f'out_{count}', master=container, variable=customtkinter.StringVar(master=self, value='off'))
            checkbox.configure(text=f'{datetime.strftime('%a, %m/%d/%Y at %H:%M')}')
            checkbox.grid(row=count, column=2, **DEFAULT_GRID_OPTIONS)
            self.outgoing_checkboxes.append(checkbox)

    def remove_incoming_datetimes(self):
        remove_list = []
        for checkbox in self.incoming_checkboxes:
            if checkbox.variable.get() == 'on':
                remove_list.append(int(checkbox.name[3:]))

        self.incoming_datetimes = [datetime for count, datetime in enumerate(self.incoming_datetimes) if count not in remove_list]
        self.display_datetimes()

    def remove_outgoing_datetimes(self):
        remove_list = []
        for checkbox in self.outgoing_checkboxes:
            if checkbox.variable.get() == 'on':
                remove_list.append(int(checkbox.name[4:]))

        self.outgoing_datetimes = [datetime for count, datetime in enumerate(self.outgoing_datetimes) if count not in remove_list]
        self.display_datetimes()

    def select_course(self):
        dialog = customtkinter.CTkInputDialog(text="Enter  course ID", title="Select Course")
        course_id = dialog.get_input()
        if not(course_id.isdigit()):
            return None
        
        try:
            course = self.root.connection.get_course(course_id)
            self.course = course
            if 'name' in course.__dict__.keys():
                self.widgets['Select Course'].configure(text=f'{course.name} ({course.id})')
            else:
                self.widgets['Select Course'].configure(text=f'Course ID: {course.id}')

        except:
            print('Course does not exist')
            self.widgets['Select Course'].configure(text='Course Does Not Exist')
            self.after(3000, lambda: self.widgets['Select Course'].configure(text='Select Course'))
            self.course = None
            return None

        self.update()

        assignments = self.course.get_assignments()
        assignments = [assignment for assignment in assignments if assignment.due_at is not None]
        self.assignments = assignments

        incoming_datetimes = []
        
        for assignment in assignments:
            incoming_datetimes.append(z_time_str_to_dt(assignment.due_at).astimezone(self.root.tz).replace(second=0))

        self.incoming_datetimes = sorted(list(set(incoming_datetimes)))

        import pprint
        pprint.pprint(self.incoming_datetimes)

        self.display_datetimes()
    
    def verify_mapping(self):
        if len(self.outgoing_datetimes) != len(self.incoming_datetimes):
            self.widgets['Verify Date Mapping'].configure(text='Incoming and outgoing dates mismatched!')
            self.after(3000, lambda: self.widgets['Verify Date Mapping'].configure(text='Verify Date Mapping'))
            return
        
        window = new_window(parent_window=self.self_window, window_name='Mapping Verification')
        window.title('Date Adjuster -- Verify Mapping')
        window.grid_columnconfigure(0, weight=1)
        window.grid_rowconfigure(1, weight=1)
        window.geometry('1200x600')

        # Main header
        header = NewLabel(name='header', master=window)
        header.configure(text='Verify the date mapping', font=LARGEFONT)
        header.grid(row=0, column=0, **DEFAULT_GRID_OPTIONS)

        # Container
        container = NewScrollFrame(name='contents', master=window)
        container.grid(row=1, column=0, **DEFAULT_GRID_OPTIONS)

        for count, datetime in enumerate(self.incoming_datetimes):
            assignments_to_map = []
            for assignment in self.assignments:
                due_at = z_time_str_to_dt(assignment.due_at).astimezone(self.root.tz).replace(second=0)
                if due_at.strftime('%a, %m/%d/%Y at %H:%M') == datetime.strftime('%a, %m/%d/%Y at %H:%M'):
                    assignments_to_map.append(assignment)
            if len(assignments_to_map) > 0:
                last_row = container.grid_size()[1]
                label = NewLabel(name=f'label_{count}', master=container)
                label.configure(text=f'{self.incoming_datetimes[count].strftime('%a, %m/%d/%Y at %H:%M')} will become {self.outgoing_datetimes[count].strftime('%a, %m/%d/%Y at %H:%M')}')
                label.grid(row=last_row, column=0, **DEFAULT_GRID_OPTIONS)

                for assignment in assignments_to_map:
                    content = NewLabel(name=f'{count}_{assignment.id}', master=container)
                    if 'name' not in assignment.__dict__.keys():
                        content.configure(text=f'Unnamed Assignment ({assignment.id})')
                    else:
                        content.configure(text=f'{assignment.name} ({assignment.id})')
                    content.grid(row=last_row, column=1, **DEFAULT_GRID_OPTIONS)
                    last_row += 1

        # Adjust Dates
        adjust = NewButton(name='Adjust the Dates', master=window)
        adjust.configure(command=self.adjust_dates)
        adjust.grid(row=2, column=0, **DEFAULT_GRID_OPTIONS)


def make_DateAdjuster(parent_window: object):
    window = new_window(parent_window=parent_window, window_name='DateAdjuster')
    window.title('NSU Canvas Tools -- Date Adjuster')
    window.grid_rowconfigure(0, weight=1)
    window.geometry('1200x600')

    course_nav = DateAdjuster(name='FrameAssignmentGenerator', master=window)
    course_nav.grid(row=0, column=0, **DEFAULT_GRID_OPTIONS)