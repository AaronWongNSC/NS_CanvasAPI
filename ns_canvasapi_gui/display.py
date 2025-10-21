"""
"""

from ns_canvasapi_gui.ctk_extensions import NewButton, NewFrame, NewScrollFrame, NewTabView
from ns_canvasapi_gui.frames import GridFrame
from ns_canvasapi_gui.general_style import DEFAULT_GRID_OPTIONS
from ns_canvasapi_gui.util import new_window


def button_command(window: object, name: str, contents: dict):
    print('Button!')
    text = dict_to_file(name=name, contents=contents)
    print(text)
    window.widgets['Save'].configure(text='Saved!!!')
    window.after(3000, lambda: window.widgets['Save'].configure(text='Save'))

def display_object(name: str, parent_window: object, contents: dict):
    window = new_window(parent_window=parent_window, window_name=name)
    window.grid_rowconfigure(1, weight=1)
    window.geometry('1200x600')
    window.title(name)

    save_button = NewButton(name='Save', master=window)
    save_button.configure(command=lambda: button_command(window=window, name=name, contents=contents))
    save_button.grid(row=0, column=0, **DEFAULT_GRID_OPTIONS)

    scroll_frame = NewScrollFrame(name='course_data_scroll', master=window)
    scroll_frame.grid_rowconfigure(0, weight=1)
    scroll_frame.grid_columnconfigure(0, weight=1)
    scroll_frame.grid(row=1, column=0, sticky='news')

    row_names = sorted(contents.keys())
    data_display = GridFrame(name=name, master=scroll_frame, row_names=row_names, col_names=['key', 'value'], pattern=['textbox', 'textbox'])
    data_display.grid_columnconfigure(1, weight=1)
    data_display.grid_rowconfigure(1, weight=1)
    data_display.grid(row=0, column=0, **DEFAULT_GRID_OPTIONS)

    for key in contents.keys():
        data_display.widgets[key]['key'].insert('0.0', key)
        data_display.widgets[key]['key'].configure(state='disabled', height=30)
        data_display.widgets[key]['value'].insert('0.0', contents[key].__str__())
        data_display.widgets[key]['value'].configure(state='disabled', height=30)
    
    data_display.widgets['description']['value'].configure(height=100)

def dict_to_file(name: str, contents: dict):
    import os
    import pprint
    import pickle

    try:
        os.makedirs('saved')
    except:
        pass

    with open(f'saved/{name}.txt', 'w') as file:
        content_string = pprint.pformat(contents, indent=4, sort_dicts=True)
        file.write(content_string)
    
    with open(f'saved/{name}.pkl', 'wb') as file:
        pickle.dump(contents, file)

    return content_string