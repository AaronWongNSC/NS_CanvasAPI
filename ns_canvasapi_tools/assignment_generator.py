import customtkinter

from ns_canvasapi_gui.ctk_extensions import NewButton, NewFrame, NewLabel, NewRadio, NewScrollFrame, NewTextbox
from ns_canvasapi_gui.frames import DateTimeFrame
from ns_canvasapi_gui.general_style import DEFAULT_GRID_OPTIONS, LARGEFONT, PADS, TOP_ALIGN
from ns_canvasapi_gui.util import new_window, select_pkl

class AssignmentGenerator(NewFrame):
    def __init__(self, name: str, master: object, *args, **kwargs):
        # General setup
        super().__init__(name=name, master=master, *args, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Set parameters
        self.assignment_group = None
        self.assignment_names = []
        self.datetimes = []
        self.naming_pattern = None
        self.relevant_template_attributes = [
            'allowed_extensions',
            'description',
            'id',
            'name',
            'points_possible',
            'submission_types'
        ]
        self.target_course = None
        self.template = None

        # Main header
        header = NewLabel(name='header', master=self)
        header.configure(text='Assignment Generator', font=LARGEFONT)
        header.grid(row=0, column=0, **DEFAULT_GRID_OPTIONS)

        # Main content area
        container = NewScrollFrame(name='contents', master=self)
        container.grid(row=1, column=0, **DEFAULT_GRID_OPTIONS)
        container.grid_columnconfigure(1, weight=1)

        # Template Selection
        template_label = NewLabel(name='Template Selection', master=container)
        template_label.grid(row=0, column=0, **TOP_ALIGN)

        template_button_frame = NewFrame(name='template_button_frame', master=container)
        template_button_frame.grid(row=0, column=1, **DEFAULT_GRID_OPTIONS)
        select_template = NewButton(name='Select Template', master=template_button_frame)
        select_template.configure(command=lambda: self.get_template())
        select_template.grid(row=0, column=0, **DEFAULT_GRID_OPTIONS)
        template_status = NewLabel(master=template_button_frame, name='template_status')
        template_status.configure(text='No Template Selected')
        template_status.grid(row=0, column=1, **DEFAULT_GRID_OPTIONS)

        template_info = NewScrollFrame(name='template_info', master=container)
        template_info.grid(row=1, column=1, **DEFAULT_GRID_OPTIONS)

        # Naming Pattern
        naming_label = NewLabel(name='Naming Pattern', master=container)
        naming_label.grid(row=2, column=0, **TOP_ALIGN)

        naming_button_frame = NewFrame(name='naming_button_frame', master=container)
        naming_button_frame.grid(row=2, column=1, **DEFAULT_GRID_OPTIONS)
        set_naming = NewButton(name='Naming Pattern', master=naming_button_frame)
        set_naming.configure(command=lambda: self.get_naming())
        set_naming.grid(row=0, column=0, **DEFAULT_GRID_OPTIONS)
        naming_pattern = NewLabel(master=naming_button_frame, name='naming_pattern')
        naming_pattern.configure(text='No pattern defined')
        naming_pattern.grid(row=0, column=1, **DEFAULT_GRID_OPTIONS)

        naming_info = NewScrollFrame(name='naming_info', master=container)
        naming_info.grid(row=3, column=1, **DEFAULT_GRID_OPTIONS)

        # Dates
        date_label = NewLabel(name='Set Due Dates', master=container)
        date_label.grid(row=4, column=0, **TOP_ALIGN)

        date_button_frame = DateTimeFrame(name='date_button_frame', master=container)
        date_button_frame.grid(row=4, column=1, **DEFAULT_GRID_OPTIONS)

        # Target
        target_label = NewLabel(name='Target Course', master=container)
        target_label.grid(row=6, column=0, **TOP_ALIGN)

        target_button_frame = NewFrame(name='target_button_frame', master=container)
        target_button_frame.grid(row=6, column=1, **DEFAULT_GRID_OPTIONS)

        select_target = NewButton(name='select_target_course', master=target_button_frame)
        select_target.configure(text='Select Target Course', command=self.get_target_course)
        select_target.grid(row=0, column=0, **DEFAULT_GRID_OPTIONS)
        target_id = NewLabel(name='target_course_id', master=target_button_frame)
        target_id.configure(text='No Course Selected')
        target_id.grid(row=0, column=1, **DEFAULT_GRID_OPTIONS)
        target_name = NewLabel(name='target_course_name', master=target_button_frame)
        target_name.configure(text='')
        target_name.grid(row=0, column=2, **DEFAULT_GRID_OPTIONS)

        ag_label = NewLabel(name='Assignment Group', master=container)
        ag_label.grid(row=7, column=0, **TOP_ALIGN)

        target_assignment_group = NewScrollFrame(name='target_group', master=container)
        target_assignment_group.grid(row=7, column=1, **DEFAULT_GRID_OPTIONS)

        # Go Button
        go_button = NewButton(name='go', master=self)
        go_button.configure(text='Check Assignments', command=self.check_assignments)
        go_button.grid(row=2, column=0)

    def check_assignments(self):
        # Transfer datetime data
        self.datetimes = self.widgets['contents'].widgets['date_button_frame'].datetimes
        # Check if necessary data has been generated
        data_check = True
        if len(self.datetimes) == 0:
            data_check = False
        if self.naming_pattern is None:
            data_check = False
        if self.target_course is None:
            data_check = False
        if self.template is None:
            data_check = False

        if not(data_check):
            self.widgets['go'].configure(text='Missing Data!!')
            self.after(3000, lambda: self.widgets['go'].configure(text='Check Assignments'))
            return

        window = new_window(parent_window=self.self_window, window_name='check_assignments')
        window.title('Assignment Generator -- Check Assignments')
        window.grid_rowconfigure(1, weight=1)
        window.geometry('1200x600')

        # Main header
        header = NewLabel(name='header', master=window)
        header.configure(text='Verify the information before committing', font=LARGEFONT)
        header.grid(row=0, column=0, **DEFAULT_GRID_OPTIONS)

        # Main content area
        container = NewScrollFrame(name='contents', master=window)
        container.grid(row=1, column=0, **DEFAULT_GRID_OPTIONS)
        container.grid_columnconfigure(1, weight=1)

        # Show Template
        template_label = NewLabel(name='Template', master=container)
        template_label.grid(row=0, column=0, **DEFAULT_GRID_OPTIONS)
        template_frame = NewScrollFrame(name='template_contents', master=container)
        template_frame.grid(row=0, column=1, **DEFAULT_GRID_OPTIONS)
        template_frame.grid_columnconfigure(1, weight=1)

        final_template = {
            key: value for key, value in self.template.items()
            if key not in ['name', 'id']
        }
        sorted_keys = sorted(final_template.keys())
        for key in sorted_keys:
            new_row = template_frame.grid_size()[1]
            key_label = NewTextbox(name=f'{key}_key', master=template_frame)
            key_label.insert('0.0', f'{key}')
            key_label.configure(state='disabled', height=30)
            key_label.grid(row=new_row, column=0, **DEFAULT_GRID_OPTIONS)

            content = NewTextbox(name=f'{key}_content', master=template_frame)
            content.insert('0.0', self.template[key].__str__())
            content.configure(state='disabled', height=30)
            content.grid(row=new_row, column=1, **DEFAULT_GRID_OPTIONS)

        # Target Course
        target_course_label = NewLabel(name='Target Course', master=container)
        target_course_label.grid(row=1, column=0, **DEFAULT_GRID_OPTIONS)

        target_course = NewLabel(name='course', master=container)
        target_course.configure(text=f'{self.target_course.name} ({self.target_course.id})')
        target_course.grid(row=1, column=1, **DEFAULT_GRID_OPTIONS)

        # Target Assignment Group
        target_ag_label = NewLabel(name='Target Assignment Group', master=container)
        target_ag_label.grid(row=2, column=0, **DEFAULT_GRID_OPTIONS)

        target_course = NewLabel(name='ag', master=container)
        target_course.configure(text=f'{self.assignment_group.name} ({self.assignment_group.id})')
        target_course.grid(row=2, column=1, **DEFAULT_GRID_OPTIONS)

        # Assignments
        assignments_label = NewLabel(name='Assignments', master=container)
        assignments_label.grid(row=3, column=0, **TOP_ALIGN)
        assignments_frame = NewFrame(name='assignments_contents', master=container)
        assignments_frame.grid(row=3, column=1, **DEFAULT_GRID_OPTIONS)

        for count, datetime in enumerate(self.datetimes):
            assignment_name = self.naming_pattern.replace('#NUM#', str(count + 1)).replace('#LNUM#', str(count + 1).zfill(2))
            assignment_label = NewLabel(f'name_{count}', master=assignments_frame)
            assignment_label.configure(text=assignment_name)
            assignment_label.grid(row=count, column=0)
            due_at = NewLabel(name=f'due_at_{count}', master=assignments_frame)
            due_at.configure(text=datetime.strftime('Due on %a, %m/%d/%Y at %H:%M'))
            due_at.grid(row=count, column=1, **DEFAULT_GRID_OPTIONS)


        # Go Button
        go_button = NewButton(name='go', master=window)
        go_button.configure(text='Generate Assignments', command=self.generate_assignments)
        go_button.grid(row=2, column=0, **DEFAULT_GRID_OPTIONS)
        
    def generate_assignments(self):
        button = self.self_window.windows['check_assignments'].widgets['go']
        button.configure(text='--- Working ---', state='disabled')
        final_template = {
            key: value for key, value in self.template.items()
            if key not in ['name', 'id']
        }
        for count, datetime in enumerate(self.datetimes):
            assignment_name = self.naming_pattern.replace('#NUM#', str(count + 1)).replace('#LNUM#', str(count + 1).zfill(2))
            time_adjusted_dt = self.root.tz.localize(datetime)
            assignment = final_template
            assignment['name'] = assignment_name
            assignment['assignment_group_id'] = self.assignment_group.id
            assignment['due_at'] = time_adjusted_dt.isoformat()
            assignment['published'] = False
            print(assignment)

            self.target_course.create_assignment(assignment=assignment)

        button.configure(text='--- DONE! ---')

    def get_assignment_group(self, radio_ag_value: object):
        self.assignment_group = self.target_course.get_assignment_group(radio_ag_value.get())

    def get_naming(self):
        dialog = customtkinter.CTkInputDialog(text="Enter naming pattern. Use #NUM# for numbering. Use #LNUM# to have leading zeros:", title="Set naming pattern")
        value = dialog.get_input()
        if value is None or value.strip == '':
            return None
        value = value.strip()
        self.naming_pattern = value
        new_master = self.widgets['contents'].widgets['naming_button_frame']
        new_master.widgets['naming_pattern'].configure(text=value)

        new_master = self.widgets['contents'].widgets['naming_info']
        if 'name_subframe' in new_master.widgets.keys():
            subframe = new_master.widgets.pop('name_subframe')
            subframe.destroy()
        new_master.update()
        subframe = NewFrame(name='name_subframe', master=new_master)
        subframe.grid(row=0, column=0, sticky='news')

        for test_value in range(1, 16):
            test_string = value.replace('#NUM#', str(test_value)).replace('#LNUM#', str(test_value).zfill(2))
            test_label = NewLabel(f'test_{test_value}', master=subframe)
            test_label.configure(text=test_string)
            test_label.grid(row=test_value-1, column=0)

    def get_target_course(self):
        dialog = customtkinter.CTkInputDialog(text="Enter target course ID:", title="Set Target Course")
        course_id = dialog.get_input()
        if not(course_id.isdigit()):
            return None
        
        try:
            course = self.root.connection.get_course(course_id)
            self.target_course = course
            new_master = self.widgets['contents'].widgets['target_button_frame']
            new_master.widgets['target_course_id'].configure(text=f'{course.id}')
            if 'name' in course.__dict__.keys():
                new_master.widgets['target_course_name'].configure(text=f'{course.name}')
            else:
                new_master.widgets['target_course_name'].configure(text='N/A')

        except:
            new_master = self.widgets['contents'].widgets['target_button_frame']
            new_master.widgets['target_course_id'].configure(text='Invalid course ID')
            self.target_course = None
            return None
        
        new_master = self.widgets['contents'].widgets['target_group']
        assignment_groups = course.get_assignment_groups()
        radio_ag_value = customtkinter.IntVar(value=assignment_groups[0].id)
        self.get_assignment_group(radio_ag_value)

        for assignment_group in assignment_groups:
            button = NewRadio(name=assignment_group.name, master=new_master, value=assignment_group.id, variable=radio_ag_value)
            button.configure(text=f'{assignment_group.name} ({assignment_group.id})')
            button.configure(command=lambda: self.get_assignment_group(radio_ag_value))

            last_row = new_master.grid_size()[1]
            button.grid(row=last_row, column=0, **DEFAULT_GRID_OPTIONS)
            
    def get_template(self):
        from bs4 import BeautifulSoup

        contents = select_pkl(master=self)
        if contents is None:
            return
        contents = {key: content for key, content in contents.items()
                    if key in self.relevant_template_attributes}
        self.template = contents

        new_master = self.widgets['contents'].widgets['template_button_frame']
        new_master.widgets['template_status'].configure(text='Template Selected')

        new_master = self.widgets['contents'].widgets['template_info']
        if 'template_subframe' in new_master.widgets.keys():
            subframe = new_master.widgets.pop('template_subframe')
            subframe.destroy()
        subframe = NewFrame(name='template_subframe', master=new_master)
        subframe.grid(row=0, column=0, sticky='news')
        new_master.grid_columnconfigure(0, weight=1)

        subframe.grid_columnconfigure(1, weight=1)
        row_names = self.template.keys()
        col_names = ['key', 'value']

        for row_count, row_name in enumerate(row_names):
            new_master.widgets[row_name] = {}
            for col_count, col_name in enumerate(col_names):
                content = NewTextbox(name='content', master=subframe)
                content.configure(height=30)
                content.configure(wrap='word')
                content.grid(row=row_count, column=col_count, **DEFAULT_GRID_OPTIONS)
                new_master.widgets[row_name][col_name] = content
            
        new_master.widgets['description']['value'].configure(height=100)

        for row_name in row_names:
            new_master.widgets[row_name]['key'].insert('0.0', row_name)
            new_master.widgets[row_name]['key'].configure(state='disabled')
            new_master.widgets[row_name]['value'].insert('0.0', f'{contents[row_name]}')

        #soup = BeautifulSoup(contents['description'], "html.parser")
        #new_master.widgets['Description']['value'].insert('0.0', soup.get_text())

        for row_name in row_names:
            new_master.widgets[row_name]['value'].configure(state='disabled')

def make_TopAssignmentGenerator(parent_window: object):
    window = new_window(parent_window=parent_window, window_name='TopAssignmentGenerator')
    window.title('NSU Canvas Tools -- Assignment Generator')
    window.grid_rowconfigure(0, weight=1)
    window.geometry('1200x600')

    course_nav = AssignmentGenerator(name='FrameAssignmentGenerator', master=window)
    course_nav.grid(row=0, column=0, **DEFAULT_GRID_OPTIONS)