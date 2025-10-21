import customtkinter
import pytz

from ns_canvasapi_gui.ctk_extensions import NewFrame, NewLabel, NewTabView
from ns_canvasapi_gui.display import display_object
from ns_canvasapi_gui.frames import GridFrame, NewScrollFrame
from ns_canvasapi_gui.general_style import DEFAULT_GRID_OPTIONS, LARGEFONT
from ns_canvasapi_gui.util import new_window

from ns_canvasapi_tools.util import dt_to_local_str

class CourseNavigator(NewFrame):
    def __init__(self, name: str, master: object, *args, **kwargs):
        # General setup
        super().__init__(name=name, master=master, *args, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Set parameters
        self.courses = None

        # Main header
        header = NewLabel(name='header', master=self)
        header.configure(text='Course Navigator', font=LARGEFONT)
        header.grid(row=0, column=0, **DEFAULT_GRID_OPTIONS)

        # Get course data, if needed
        if self.courses is None:
            self.courses = self.root.connection.get_courses()

        # Build the display
        scroll_frame = NewScrollFrame(name='course_list', master=self)
        scroll_frame.grid_columnconfigure(0, weight=1)
        scroll_frame.grid(row=1, column=0, sticky='news')
        course_ids = [course.id for course in self.courses]
        col_names = ['button', 'name']
        course_display = GridFrame(name='course_selection', master=scroll_frame, row_names=course_ids, col_names=col_names, pattern=['button', 'label'])
        course_display.grid_columnconfigure(1, weight=1)
        course_display.grid(row=1, column=0, **DEFAULT_GRID_OPTIONS)

        for course in self.courses:
            course_display.widgets[course.id]['button'].configure(text=str(course.id))
            course_display.widgets[course.id]['button'].configure(command=lambda id=course.id: self.select_course(id))
            if 'name' not in course.__dict__.keys():
                course.name = 'N/A'
            course_display.widgets[course.id]['name'].configure(text=course.name)

    def select_course(self, id):
        # Create new window
        window = new_window(parent_window=self.self_window, window_name=f'Course {id}')
        if window is None:
            return
        window.title(f'Course Navigator -- Course {id}')
        window.geometry('1200x600')
        window.grid_columnconfigure(0, weight=1)
        window.grid_rowconfigure(1, weight=1)

        # Get the course information
        course = self.root.connection.get_course(id)

        # Header
        header = NewLabel(name='header', master=window)
        header.configure(text=f'{course.name} ({course.id})', font=LARGEFONT)
        header.grid(row=0, column=0, **DEFAULT_GRID_OPTIONS)

        # Create Tabs
        tabs = NewTabView('course_data', window)
        tabs.grid(row=1, column=0, **DEFAULT_GRID_OPTIONS)

        # Assignments Tab
        tabs.add('Assignments')
        tabs.tab('Assignments').columnconfigure(0, weight=1)
        tabs.tab('Assignments').rowconfigure(0, weight=1)

        assignment_groups = course.get_assignment_groups()
        assignments = course.get_assignments()
        assignment_ids = [assignment.id for assignment in assignments]
        col_names = ['button', 'group', 'name', 'due_at_date']

        assignment_scroll = NewScrollFrame(name='assignment_scroll', master=tabs.tab('Assignments'))
        assignment_scroll.grid_columnconfigure(0, weight=1)
        assignment_scroll.grid(row=0, column=0, sticky='news')

        data = GridFrame(name='assignments', master=assignment_scroll, row_names=assignment_ids, col_names=col_names, pattern=['button', 'label', 'label', 'label'])
        data.grid_rowconfigure(0, weight=1)
        data.grid_columnconfigure((1, 2, 3), weight=1)
        data.grid(row=0, column=0, **DEFAULT_GRID_OPTIONS)

        for assignment in assignments:
            data.widgets[assignment.id]['button'].configure(text=str(assignment.id))
            data.widgets[assignment.id]['button'].configure(command=lambda id=assignment.id: self.show_assignment_details(course, id))
            
            assignment_group_name = [assignment_group.name for assignment_group in assignment_groups if assignment_group.id == assignment.assignment_group_id][0]

            data.widgets[assignment.id]['group'].configure(text=assignment_group_name)
            data.widgets[assignment.id]['name'].configure(text=assignment.name)
            if not hasattr(assignment, 'due_at_date'):
                data.widgets[assignment.id]['due_at_date'].configure(text='N/A')
            else:
                data.widgets[assignment.id]['due_at_date'].configure(text=dt_to_local_str(assignment.due_at_date, tz=pytz.timezone('US/Pacific')))

        tabs.add('Discussions')
        tabs.add('Modules')
        tabs.add('Pages')
        tabs.add('Students')

    def show_assignment_details(self, course, id):
        assignment = course.get_assignment(id)
        display_object(name=f'{assignment.id}-{assignment.name}', parent_window=self.self_window.windows[f'Course {assignment.course_id}'], contents=assignment.__dict__)

def make_TopCourseNavigator(parent_window: object):
    window = new_window(parent_window=parent_window, window_name='TopCourseNavigator')
    if window is None:
        return
    window.title('NSU Canvas Tools -- Course Navigator')
    window.grid_rowconfigure(0, weight=1)
    window.geometry('1200x600')

    course_nav = CourseNavigator(name='FrameCourseNavigator', master=window)
    course_nav.grid(row=0, column=0, **DEFAULT_GRID_OPTIONS)