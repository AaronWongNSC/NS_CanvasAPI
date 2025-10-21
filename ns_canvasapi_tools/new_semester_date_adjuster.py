import customtkinter
import pytz

from ns_canvasapi_gui.ctk_extensions import NewFrame, NewScrollFrame, NewTabView
from ns_canvasapi_gui.frames import DataDisplayFrame, LeadingButtonFrame, LeadingButtonScrollFrame
from ns_canvasapi_gui.general_style import LARGEFONT, REGULARFONT, PADS
from ns_canvasapi_gui.util import display_contents, new_window

from ns_canvasapi_tools.util import dt_to_local_str

class NewSemesterDateAdjuster(NewFrame):
    def __init__(self, name: str, master: object, *args, **kwargs):
        # General setup
        super().__init__(name=name, master=master, *args, **kwargs)
        self.grid_columnconfigure((0,1), weight=1)
