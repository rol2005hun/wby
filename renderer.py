import re
from tkinter import ttk, Label, Button, Entry, Radiobutton, IntVar, Listbox, Scrollbar, Scale, Message, Menubutton, Text
from tkinter.ttk import Progressbar

def parse_style(style_str):
    style = {}
    for item in style_str.split(','):
        key, value = item.split('=')
        style[key.strip()] = value.strip().strip('"')
    return style

def apply_style(widget, style):
    background_color = style.get('background-color', 'white')

    if isinstance(widget, (Label, Message, Button, Text, Radiobutton)):
        widget.config(bg=background_color)
    
    if 'color' in style:
        widget.config(fg=style['color'])
    if 'font-size' in style:
        widget.config(font=("Arial", int(style['font-size'])))
    if 'width' in style:
        widget.config(width=int(style['width']))
    if 'height' in style:
        widget.config(height=int(style['height']))
    if 'padding' in style:
        padding = tuple(map(int, style['padding'].split()))
        if len(padding) == 1:
            padding = (padding[0], padding[0])
        widget.config(padx=padding[0], pady=padding[1])

class WBYRenderer:
    def __init__(self, display_area):
        self.display_area = display_area
        self.widgets = []

    def render_line(self, line):
        match = re.match(r'(\w+): text="([^"]+)", style=\[(.+?)\](?:, options=\[(.+)\])?', line)
        if match:
            widget_type, text, style_str, options_str = match.groups()
            style = parse_style(style_str)
            options = parse_style(options_str) if options_str else {}

            if widget_type == 'text':
                label = Label(self.display_area, text=text)
                apply_style(label, style)
                label.pack()
                self.widgets.append(label)

            elif widget_type == 'button':
                button = Button(self.display_area, text=text)
                apply_style(button, style)
                button.pack()
                self.widgets.append(button)

            elif widget_type == 'entry':
                entry = Entry(self.display_area)
                entry.insert(0, text)
                apply_style(entry, style)
                entry.pack()
                self.widgets.append(entry)

            elif widget_type == 'radiobutton':
                var = IntVar()
                radiobutton = Radiobutton(self.display_area, text=text, variable=var, value=int(options.get('value', 0)))
                apply_style(radiobutton, style)
                radiobutton.pack()
                self.widgets.append(radiobutton)

            elif widget_type == 'combobox':
                values = options.get('values', '').split('|')
                combobox = ttk.Combobox(self.display_area, values=values)
                combobox.set(text)
                apply_style(combobox, style)
                combobox.pack()
                self.widgets.append(combobox)

            elif widget_type == 'listbox':
                listbox = Listbox(self.display_area)
                for item in text.split('|'):
                    listbox.insert('end', item)
                apply_style(listbox, style)
                listbox.pack()
                self.widgets.append(listbox)

            elif widget_type == 'scrollbar':
                scrollbar = Scrollbar(self.display_area)
                apply_style(scrollbar, style)
                scrollbar.pack(side='right', fill='y')
                self.widgets.append(scrollbar)

            elif widget_type == 'scale':
                scale = Scale(self.display_area, from_=int(options.get('from', 0)), to=int(options.get('to', 100)), orient=options.get('orient', 'horizontal'))
                apply_style(scale, style)
                scale.pack()
                self.widgets.append(scale)

            elif widget_type == 'message':
                message = Message(self.display_area, text=text)
                apply_style(message, style)
                message.pack()
                self.widgets.append(message)

            elif widget_type == 'menubutton':
                menubutton = Menubutton(self.display_area, text=text)
                apply_style(menubutton, style)
                menubutton.pack()
                self.widgets.append(menubutton)

            elif widget_type == 'progressbar':
                progressbar = Progressbar(self.display_area, value=int(options.get('value', 0)))
                progressbar.pack()
                self.widgets.append(progressbar)

    def render(self, content):
        lines = content.split("\n")
        for line in lines:
            if not line.startswith('\\W/'):
                self.render_line(line.strip())

    def clear_widgets(self):
        for widget in self.widgets:
            widget.destroy()
        self.widgets = []