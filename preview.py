from functions import *

def previewCard(textFront, textBack):

    elementsFront = fromTextToElements(textFront)
    elementsBack = fromTextToElements(textBack)

    layout = [
        [sg.Text(text='Front: ')],
        [sg.Column(elementsFront, scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, size=(None, 150), justification='center')],
        [sg.Text(text='Back: ')],
        [sg.Column(elementsBack, scrollable=True, vertical_scroll_only=True, expand_x=True, size=(None, 150), justification='center')],
    ]

    window = sg.Window('PreviewCard', size=(500, 400), layout=layout, keep_on_top=True, modal=True, finalize=True, resizable=True)

    while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Exit'):
                break

    window.close()