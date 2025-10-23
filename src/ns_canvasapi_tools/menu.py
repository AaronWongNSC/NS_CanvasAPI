from ns_canvasapi_gui.ctk_extensions import NewButton, NewFrame, NewLabel
from ns_canvasapi_gui.general_style import DEFAULT_GRID_OPTIONS, LARGEFONT
from ns_canvasapi_gui.util import new_window

from ns_canvasapi_tools.assignment_generator import make_TopAssignmentGenerator
from ns_canvasapi_tools.date_adjuster import make_DateAdjuster
from ns_canvasapi_tools.course_navigator import make_TopCourseNavigator

class MainMenu(NewFrame):
    def __init__(self, name: str, master: object, *args, **kwargs):
        # General setup
        super().__init__(name=name, master=master, *args, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Widgets
        # Header
        header = NewLabel(name='header', master=self)
        header.configure(text='NSU Canvas Tools -- Main Menu', font=LARGEFONT)
        header.grid(row=0, column=0, **DEFAULT_GRID_OPTIONS)

        # Assignment Generator
        assign_gen = NewButton(name='Assignment Generator', master=self)
        assign_gen.configure(command=lambda master=self: make_TopAssignmentGenerator(master))
        assign_gen.grid(row=self.grid_size()[1], column=0, **DEFAULT_GRID_OPTIONS)

        # Date Adjuster
        date_adjust = NewButton(name='Date Adjuster', master=self)
        date_adjust.configure(command=lambda master=self: make_DateAdjuster(master))
        date_adjust.grid(row=self.grid_size()[1], column=0, **DEFAULT_GRID_OPTIONS)

        '''
        # Course Navigator
        course_nav = NewButton(name='Course Navigator', master=self)
        course_nav.configure(command=lambda master=self: make_TopCourseNavigator(master))
        course_nav.grid(row=self.grid_size()[1], column=0, **DEFAULT_GRID_OPTIONS)
        '''

def make_TopMainMenu(parent_window: object):
    # Visual feedback
    print(f'Creating TopMainMenu as child of {parent_window.name}')

    # Create or locate the window
    window = new_window(parent_window=parent_window, window_name='TopMainMenu')
    if window is None:
        return
    window.title('NSU Canvas Tools -- Main Menu')

    main_menu = MainMenu(name='FrameMainMenu', master=window)
    main_menu.grid(row=0, column=0, **DEFAULT_GRID_OPTIONS)