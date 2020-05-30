
import time
import PySimpleGUI as sg


def get_data(title, possibilities):
    sg.theme('DarkAmber')
    
    answers = [ None for x in possibilities ]
    layout = [
        [sg.Text(row["question"])] + [ sg.Button(y) for y in row["answers"]]
        for row in possibilities
    ]

    window = sg.Window(title, layout, keep_on_top=True)
    window.BringToFront()
    timeout = time.time()
    while True:

        if time.time() - 4 > timeout:
            return ['absent']

        event, values = window.read(timeout=500)
        for i_row, row in enumerate(possibilities):
            for i_column, column in enumerate(row["answers"]):
                if event in (None, column):
                    answers[i_row] = column
        
        if all([x is not None for x in answers]):
            break
        


    return ['present'] + answers