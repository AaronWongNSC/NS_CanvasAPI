"""
Creates classes with custom code that creates the structures I want.
"""

import customtkinter

class NewObject:
    def short_display(self):
        """
        Use this to provide short feedback about an object
        """
        if self.type == 'NewScrollFrame':
            print(f'{self.type} {self.name} in {self.master.master.master.name} in window {self.self_window.name}')
        else:
            print(f'{self.type} {self.name} in {self.master.name} in window {self.self_window.name}')

    def long_display(self):
        """
        Use this to display some of the key information about objects to help with debugging
        """
        from pprint import pprint

        print('----- BEGIN DISPLAY -----')
        attributes = sorted(self.__dict__.keys())
        new_attributes = ['type', 'name', 'connection', 'api_key', 'api_url', 'master', 'parent_window', 'self_window', 'root', 'widgets', 'windows']
        pprint_attributes = ['widgets', 'windows']
        for attribute in new_attributes:
            if attribute in attributes:
                if attribute in pprint_attributes:
                    print(f'{attribute}:')
                    pprint(self.__dict__[attribute])
                else:
                    print(f'{attribute}: {self.__dict__[attribute]}')
        attributes = [attribute for attribute in attributes if attribute not in new_attributes]
        for attribute in attributes:
            print(f'{attribute}: {self.__dict__[attribute]}')
        print('----- END DISPLAY -----')

    def get_self_window(self):
        """
        Get the window (root or TopLevel) that the object resides in.

        Parameters:
            NewObject: An extended ctk object whose window you want

        Return:
            NewObject: The root or TopLevel that contains the original NewObject
        """
        found = False
        current = self
        while not found:
            if 'type' in current.__dict__.keys():
                if current.type not in ['NewRoot', 'NewTopLevel']:
                    current = current.master
                else:
                    found = True
                if current is None:
                    return None
            else:
                current = current.master
        return current

    def wipe(self):
        if self.type not in ['NewFrame', 'NewScrollFrame']:
            return

        for _, widget in self.widgets.items():
            widget.destroy()
        self.widgets = {}
        

class NewButton(customtkinter.CTkButton, NewObject):
    """
    Button object with tracking information
    """
    def __init__(self, name: str, master: object):
        # General setup
        super().__init__(master=master, text=name)

        # Set tracking parameters
        self.name = name
        self.root = master.root
        self.self_window = self.get_self_window()
        self.type = 'NewButton'

        # Establish connection to master
        master.widgets[name] = self

        # Set up feedback
        self.configure(command=self.click)

        # Command Window Feedback
        self.short_display()
    
    def click(self):
        """
        Generic button click feedback
        """
        if 'name' in self.master.__dict__.keys():
            print(f'Button Click: {self.name} in {self.master.name} in {self.self_window}')
        else:
            print(f'Button Click: {self.name} in ??? in {self.self_window}')
        button_text = self.cget('text')
        self.configure(text='Clicked!', state='disabled')
        self.after(3000, lambda: self.configure(text=button_text, state='normal'))

class NewCheckBox(customtkinter.CTkCheckBox, NewObject):
    """
    CheckBox object with tracking information
    """
    def __init__(self, name: str, master: object, onvalue: int|str = 'on', offvalue: int|str = 'off', variable=object):
        # General setup
        super().__init__(master=master, text=name, onvalue=onvalue, offvalue=offvalue, variable=variable)

        # Set tracking parameters
        self.name = name
        self.root = master.root
        self.self_window = self.get_self_window()
        self.type = 'NewCheckBox'

        # Set general parameters
        self.offvalue = offvalue
        self.onvalue = onvalue
        self.variable = variable

        # Establish connection to master
        master.widgets[name] = self

        # Set up feedback
        self.configure(command=self.checkbox_event)

        # Command Window Feedback
        self.short_display()
    
    def checkbox_event(self):
        """
        Generic checkbox click feedback
        """
        if 'name' in self.master.__dict__.keys():
            print(f'Checkbox Toggle: {self.name} in {self.master.name} in {self.self_window} set to {self.variable.get()}')
        else:
            print(f'Checkbox Toggle: {self.name} in ??? in {self.self_window} set to {self.variable.get()}')

class NewFrame(customtkinter.CTkFrame, NewObject):
    """
    Frame object with tracking information
    """
    def __init__(self, name: str, master: object, *args, **kwargs):
        # General setup
        super().__init__(master=master, *args, **kwargs)

        # Set tracking parameters
        self.name = name
        self.root = master.root
        self.self_window = self.get_self_window()
        self.type = 'NewFrame'

        # Containers
        self.widgets = {}

        # Establish connection to master
        master.widgets[name] = self

        # Command Window Feedback
        self.short_display()

class NewLabel(customtkinter.CTkLabel, NewObject):
    def __init__(self, name: str, master: object):
        # General setup
        super().__init__(master=master, text=name)

        # Set tracking parameters
        self.name = name
        self.root = master.root
        self.self_window = self.get_self_window()
        self.type = 'NewLabel'

        # Establish connection to master
        master.widgets[name] = self

        # Command Window Feedback
        self.short_display()

class NewRadio(customtkinter.CTkRadioButton, NewObject):
    def __init__(self, name: str, master: object, value: int|str, variable=object):
        # General setup
        super().__init__(master=master, text=name, value=value, variable=variable)

        # Set tracking parameters
        self.name = name
        self.root = master.root
        self.self_window = self.get_self_window()
        self.type = 'NewRadio'

        # Set general parameters
        self.value = value
        self.variable = variable

        # Establish connection to master
        master.widgets[name] = self

        # Command Window Feedback
        self.short_display()

class NewRoot(customtkinter.CTk, NewObject):
    """
    Root object with tracking information
    """
    def __init__(self, name: str):
        # General setup
        super().__init__()

        # Set tracking parameters
        self.name = name
        self.parent_window = None
        self.root = self
        self.self_window = self
        self.type = 'NewRoot'

        # Create containers
        self.widgets = {}
        self.windows = {}

class NewScrollFrame(customtkinter.CTkScrollableFrame, NewObject):
    def __init__(self, name: str, master: object):
        # General setup
        super().__init__(master=master)
        self.bind("<MouseWheel>", lambda event: self.on_mousewheel(event))

        # Set tracking parameters
        self.name = name
        self.root = master.root
        self.self_window = self.get_self_window()
        self.type = 'NewScrollFrame'

        # Containers
        self.widgets = {}

        # Establish connection to master
        master.widgets[name] = self

        # Command Window Feedback
        self.short_display()

    def on_mousewheel(self, event):
        # Determine the widget under the mouse pointer
        widget = event.widget

        while widget and not hasattr(widget, '_parent_canvas'): # Find the first scrollable parent
            widget = widget.master

        if widget:
            canvas = widget._parent_canvas
            # Adjust scrolling based on delta value
            if event.num == 4 or event.delta > 0:  # Scroll up
                canvas.yview("scroll", -100, "units")
            elif event.num == 5 or event.delta < 0: # Scroll down
                canvas.yview("scroll", 100, "units")


class NewTabView(customtkinter.CTkTabview, NewObject):
    """
    TabView object with tracking information
    """
    def __init__(self, name: str, master: object, **kwargs):
        # General setup
        super().__init__(master=master, **kwargs)

        # Set tracking parameters
        self.name = name
        self.root = master.root
        self.self_window = self.get_self_window()
        self.type = 'NewTabview'

        # Containers
        self.tabs = {}

        # Establish connection to master
        master.widgets[name] = self

        # Command Window Feedback
        self.short_display()

    def add(self, name: str):
        # General setup
        super().add(name = name)

        # Set tracking parameters
        self.tab(name).name = name
        self.tab(name).root = self.root
        self.tab(name).self_window = self.self_window
        self.tab(name).type = 'NewTab'

        # Containers
        self.tab(name).widgets = {}

        # Establish connection to master (TabView)
        self.tabs[name] = self.tab(name)

class NewTextbox(customtkinter.CTkTextbox, NewObject):
    """
    Textbox object with tracking information
    """
    def __init__(self, name: str, master: object):
        # General setup
        super().__init__(master=master)

        # Set tracking parameters
        self.name = name
        self.root = master.root
        self.self_window = self.get_self_window()
        self.type = 'NewTextbox'

        # Establish connection to master
        master.widgets[name] = self

        # Command Window Feedback
        self.short_display()

class NewTopLevel(customtkinter.CTkToplevel, NewObject):
    """
    TopLevel object with tracking information
    """
    def __init__(self, name: str, master: object, *args, **kwargs):
        # General setup
        super().__init__(*args, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        # Set tracking parameters
        self.name = name
        self.parent_window = master.self_window
        self.root = master.root
        self.self_window = self
        self.type = 'NewTopLevel'

        # Containers
        self.widgets = {}
        self.windows = {}

        # Establish connection to master
        master.windows[name] = self

        # Command Window Feedback
        self.short_display()

        # Capture Window Closing
        self.protocol("WM_DELETE_WINDOW", self.close_window)

        # Lift self
        self.after(250, self.lift)

    
    def close_window(self):
        for key in list(self.windows.keys()):
            self.windows[key].close_window()
        self.parent_window.windows.pop(self.name)
        self.parent_window.deiconify()
        self.destroy()
