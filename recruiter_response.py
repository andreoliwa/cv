#!/usr/bin/env python3
"""A GUI helper build with appJar, to build responses to recruiters (LinkedIn, e-mail, etc.).

Install appJar reading their docs:
https://github.com/jarvisteach/appJar
"""
import os
import sys

import pyperclip

from appJar import gui

SENTENCES_FILE = os.environ.get('SENTENCES_FILE')
if not SENTENCES_FILE:
    print('Set the environment variable SENTENCES_FILE with the full path to a .txt file containing your sentences.')
    sys.exit(1)

SENTENCES = ''


def load_grid():
    """Load the grid with the sentences from the .txt file."""
    global SENTENCES

    with open(os.path.expanduser(SENTENCES_FILE)) as file:
        content = file.readlines()

    SENTENCES = [line.strip() for line in content if line.strip()]

    return [[line.strip()] for line in SENTENCES]


def on_row_click(row):
    """Add the sentence to the text area."""
    app.setTextArea('Response', SENTENCES[row] + '\n')


def clear_button():
    """Clear the text area."""
    app.clearTextArea('Response')


def copy_button():
    """Copy the content of the text area to the clipboard."""
    response = app.getTextArea('Response')
    pyperclip.copy(response.replace('{recruiter}', app.getEntry('Recruiter')))
    print('Text area content copied to the clipboard:')
    print(pyperclip.paste())


def edit_button():
    """Open the sentences file on Visual Studio Code."""
    os.system(f'code {SENTENCES_FILE}')


BUTTONS = {
    'Clear response': clear_button,
    'Copy response': copy_button,
    'Edit sentences': edit_button,
}


def on_button_click(button):
    """Call the corresponding function when a button is clicked."""
    func = BUTTONS.get(button)
    if func:
        func()


with gui() as app:
    app.setTitle('LinkedIn Response Builder')
    app.setSize(1200, 800)

    app.addGrid('sentences', [['Sentence'], *load_grid()], action=on_row_click, row=0, column=0, colspan=2, rowspan=10,
                actionButton='Use', showMenu=True)
    app.setGridWidth('sentences', 300)
    app.setGridHeight('sentences', 800)

    app.addLabelEntry('Recruiter', row=0, column=2)
    app.addTextArea('Response', row=app.getRow() + 1, column=2)

    index = app.getRow() + 3
    for button in BUTTONS.keys():
        index += 1
        app.addButton(button, on_button_click, row=index, column=2)

    app.go()
