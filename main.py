import PySimpleGUI as sg
import sys
from datetime import date
import os


# Defining main window content
layout = [[sg.Button('Add new book', key='add_button'),
           sg.Button('Print library', key='print_button'),
           sg.Button('Exit', key='exit_button')],
          [sg.T('')],
          [sg.T('Library contains following books:')],
          [sg.MLine(size=(45,34), key='output', autoscroll=True, auto_size_text=True)]]


# create list with lines from the file
def convert_file_content_into_list(file):
    file_content = []
    with open(file, 'r', encoding='utf-8') as fh:
        for line in fh:
            if line != '':
                file_content.append(line.strip())
    return file_content


# validation of the input fields
def validation(title, author, isbn, year):
    message_error = ''

    if not title or not author or not isbn or not year:
        # check if all fields are filled
        message_error = 'Please fill missing fields'
    elif len(title) > 30 or len(author) > 30 or len(isbn) > 30:
        message_error = 'Max length of the field is 30'
    elif not isbn.isdigit():
        # check if ISBN contains only numbers
        message_error = 'ISBN should contain only numbers'
    elif not year.isdigit() or int(year) not in range(0, date.today().year + 1):
        # check if year contains numbers from 0 to current year
        message_error = 'Year is not valid'

    return message_error


# sort library file by publishing year
def sorting_library_file(file, new_entry):

    file_content = convert_file_content_into_list(file)

    # check the year of new book and insert data in proper index of the list
    if int(new_entry.split('/')[3]) >= int(file_content[len(file_content)-1].split('/')[3]):
        file_content.append(new_entry)
    else:
        for i in file_content.copy():
            if int(new_entry.split('/')[3]) <= int(i.split('/')[3]):
                file_content.insert(file_content.index(i), new_entry)
                break

    # save data into the file
    with open(file, 'w', encoding='utf-8') as fh:
        for line in file_content:
            fh.write(line + '\n')


# creating UI window for adding new book
def add_book_window(file_to_update):

    # Defining popup window content
    layout_popup = [
                [sg.Text('Please fill necessary information')],
                [sg.T('')],
                [sg.Text('Name of the book'), sg.InputText(key='title')],
                [sg.Text('Author'), sg.InputText(key='author')],
                [sg.Text('ISBN'), sg.InputText(key='isbn')],
                [sg.Text('Year'), sg.InputText(key='year')],
                [sg.T('')],
                [sg.Button('Add', key='save'),
                 sg.Button('Cancel', key='cancel')]]

    window = sg.Window("Add new book", layout_popup, modal=True, size=(300, 250))

    while True:
        event, values = window.read()
        print('e=', event, 'v=', values)
        if event == 'cancel' or event == sg.WIN_CLOSED:
            break

        title = values['title']
        author = values['author']
        isbn = values['isbn']
        book_year = values['year']

        if event == 'save':

            if validation(title=title, author=author, isbn=isbn, year=book_year):
                sg.popup_ok(validation(title=title, author=author, isbn=isbn, year=book_year))
                continue

            new_data = '{}/{}/{}/{}'.format(title, author, isbn, book_year)

            # check if file exists or if it's' empty
            if not os.path.isfile(os.path.join('.', file_to_update)) or os.path.getsize(file_to_update) == 0:
                with open(file_to_update, 'w', encoding='utf-8') as fh:
                    fh.write(new_data + '\n')
            else:
                sorting_library_file(file_to_update, new_data)

            window.close()

    window.close()


# print file content in the UI
def show_result(file):
    file_content = convert_file_content_into_list(file)
    library_output = ''

    # create list of books from the file, than convert it to string separated with ','
    for book in file_content:
        library_output = library_output + ', '.join(book.split('/')) + '\n'
    return library_output


if __name__ == '__main__':
    library_file = sys.argv[1]
    # library_file = "test.txt"

    # creating main UI window
    window = sg.Window('Python library', layout, size=(400, 500), grab_anywhere=True, resizable=False,
                       margins=(10, 10))

    # interacting with window
    while True:
        event, values = window.read()
        print('e=', event, 'v=', values)

        if event == 'exit_button' or event == sg.WIN_CLOSED:
            break

        if event == 'add_button':
            add_book_window(library_file)

        if event == 'print_button':
            if not os.path.isfile(os.path.join('.', library_file)) or os.path.getsize(library_file) == 0:
                output = "Library is empty"
            else:
                output = show_result(library_file)
            window['output'].update(output)

    window.close()
