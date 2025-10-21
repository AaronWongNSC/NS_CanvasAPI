"""
Main connection hub for NSCanvasAPI
"""

from canvasapi import Canvas
import customtkinter
import pytz

from ns_canvasapi_gui.ctk_extensions import NewButton, NewLabel, NewRoot
from ns_canvasapi_gui.frames import GridFrame
from ns_canvasapi_gui.general_style import DEFAULT_GRID_OPTIONS, LARGEFONT

from ns_canvasapi_tools.menu import make_TopMainMenu

class CanvasConnection(NewRoot):
    """
    Checks for API_KEY and successful connection to the Canvas API
    """
    def __init__(self, name):
        # General setup
        super().__init__(name)
        self.grid_columnconfigure(0, weight=1)
        self.title('NSU Canvas Tools -- Connection Page')

        # Set parameters (Note: In the future, this can be a JSON)
        self.api_key = None
        self.api_url = 'https://nsc.test.instructure.com'
        self.connection = None
        self.tz = pytz.timezone('America/Los_Angeles')

        # Widgets
        # Connection Parameters
        header = NewLabel(name='header', master=self)
        header.configure(text='Connection Parameters', font=LARGEFONT)
        header.grid(row=0, column=0, **DEFAULT_GRID_OPTIONS)
        connection_params = GridFrame(name='connect', master=self, row_names=['api_url', 'api_key'], col_names=['button', 'content'], pattern=['button', 'label'])
        connection_params.grid_columnconfigure(1, weight=1)
        connection_params.grid(row=1, column=0, **DEFAULT_GRID_OPTIONS)

        for row_name in connection_params.row_names:
            connection_params.widgets[row_name]['button'].configure(text='Change')

        connection_params.widgets['api_url']['button'].configure(
            command=lambda button=connection_params.widgets['api_url']['button'],
            target=connection_params.widgets['api_url']['content']:
            connection_params.change_value(button, target))
        connection_params.widgets['api_url']['content'].configure(text=self.api_url)

        connection_params.widgets['api_key']['button'].configure(command=self.get_api_key)

        # Check for existing api_key
        try: 
            with open('key.txt', 'r') as file:
                self.api_key = file.read()
            if self.api_key == '':
                raise Exception()
            connection_params.widgets['api_key']['content'].configure(text='API key found')
        except:
            self.API_KEY = None
            connection_params.widgets['api_key']['content'].configure(text='No API key found')
        
        # Connect Button
        button = NewButton(name='Connect', master=self)
        button.configure(command=self.connect)
        button.grid(row=2, column=0, **DEFAULT_GRID_OPTIONS)
        self.widgets['button'] = button

    def connect(self):
        # Button Feedback
        print(f'Running connection protocol...')
        self.widgets['Connect'].configure(text='Connecting...')
        self.after(3000, lambda: self.widgets['Connect'].configure(text='Connect'))

        # Check if main_menu is already open
        if 'main_menu' in self.widgets.keys():
            self.windows['main_menu'].lift()
            return

        # Get data from connect frame
        values = self.widgets['connect'].get_values()

        # Check for api_key
        if values['api_key','content'] != 'API key found':
            error = NewLabel(name='error', master=self)
            error.configure(text='Missing API key!', font=LARGEFONT)
            error.grid(row=3, column=0, **DEFAULT_GRID_OPTIONS)
            return False
        
        # Attempt connection
        self.api_url = values['api_url','content']
        with open('key.txt', 'r') as file:
            self.api_key = file.read()
        
        try:
            canvas = Canvas(self.api_url, self.api_key)
            user = canvas.get_current_user()
        except:
            error = NewLabel('error', master=self)
            error.configure(text='Could not connect! Check URL and key.', font=LARGEFONT)
            error.grid(row=3, column=0, **DEFAULT_GRID_OPTIONS)
            return False

        # Connection Successful -- Provide feedback
        if 'error' in self.widgets.keys():
            self.widgets['error'].grid_forget()
            self.widgets.pop('error')
        welcome = NewLabel(name='welcome', master=self)
        welcome.configure(text=f'Connected as {user.name}', font=LARGEFONT)
        welcome.grid(row=3, column=0, **DEFAULT_GRID_OPTIONS)

        # Create connection
        self.connection = canvas

        # Create main_menu
        make_TopMainMenu(parent_window=self)

    def get_api_key(self):
        # Button Feedback
        print(f'Running get_api_key protocol...')
        new_master = self.widgets['connect']        
        new_master.widgets['api_key']['button'].configure(text='Getting key...')
        self.after(3000, lambda: new_master.widgets['api_key']['button'].configure(text='Connect'))

        # Attempt Connection
        try:
            dialog = customtkinter.CTkInputDialog(text='Provide a new API Key (Access Token): ', title='Store New Key')
            key = dialog.get_input()
            if key is not None and key.strip() != '':
                with open('key.txt', 'w') as file:
                    file.write(key)
                    new_master.widgets['api_key']['content'].configure(text='API key found')
        except:
            new_master.widgets['api_key']['content'].configure(text='No API key found')

app = CanvasConnection('canvas')

app.mainloop()
