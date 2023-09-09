from functions import *
import textwrap
import base64

def fromTextToElements(text):
    elements = []

    startLatex = False
    stringLatex = ""
    normalString = ""

    x = 0
    while x < len(text):

        if x + 6 < len(text) and text[x:x+7] == '[latex]':
            if len(normalString)> 0 :
                elements.append([sg.Text(text=textwrap.fill(normalString), expand_x=True)])
            normalString = ""
            startLatex = True
            x += 7

        if x + 7 < len(text) and text[x:x+8] == '[/latex]':

            if len(stringLatex)> 0 : 
                image_bytes = render_latex(stringLatex)
                image_base64 = base64.b64encode(image_bytes)
                elements.append([sg.Column([[sg.Image(source=image_base64)]])])
            startLatex = False
            stringLatex = ""
            x += 8

        if x < len(text):
            if startLatex:
                stringLatex += text[x]
            else:
                normalString += text[x]
            x += 1

    if len(normalString)> 0:
        elements.append([sg.Text(textwrap.fill(normalString), expand_x=True)])
    
    return elements

def previewCard(textFront, textBack):

    elementsFront = fromTextToElements(copy.deepcopy(textFront))
    elementsBack = fromTextToElements(copy.deepcopy(textBack))

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