from functions import *

'''
    Sessions = [
        {},
        {
            "amount": int,
            "durations": arrInt,    # lenght based on amount value,
            "types": arrStrings,    # ...
            "pages": arrInt         # ...                 

        },...
    ] # based on studyDays

'''

def getStudySlots(type, studyDays, arrAmount, defaults = None, bookID = None):
    minimumDuration = getSettingsValue('minimumDuration')
    rows = []
    for x in range(7):
        if studyDays[x]:
            row = []

            for j in range(arrAmount[x]):
                defaultPages = "10"
                defaultType = "Reading"
                defaultDuration = minimumDuration
                
                if defaults is not None and defaults[weekdays[x]]['areThereSessions']:
                    defaultPages = defaults[weekdays[x]]['pages'][j]
                    defaultType = defaults[weekdays[x]]['types'][j]
                    defaultDuration = defaults[weekdays[x]]['durations'][j]

                lyt =   [
                            sg.Frame(str(f"{j+1}° Session"), [
                                [ sg.Text('Pages: ', size=(12, 1), visible=type), sg.InputText(default_text=defaultPages, key=f'INPUT_TEXT_PAGES_{j}_SESSION_{weekdays[x]}', size=(5, 1), visible=type)],
                                [ sg.Text('Type: ', size=(12, 1)), sg.Combo(["Reading", "Schematization", "Testing", "Notes"], size=(13, 1), default_value=defaultType, key=f'COMBO_TYPE_{j}_SESSION_{weekdays[x]}')],
                                [ sg.Text('Duration: ', size=(12, 1)), sg.Combo([x for x in range(minimumDuration, 60, minimumDuration)], default_value=defaultDuration, tooltip="Minutes", key=f'INPUT_TEXT_DURATION_{j}_SESSION_{weekdays[x]}', size=(3, 1), readonly=True)]
                            ])
                        ]
                
                row.append(lyt)

            frame = [sg.Frame(weekdays_complete[x], row)]
            rows.append(frame)
    
    column = sg.Column(rows, scrollable=True, vertical_scroll_only=True, size=(None, 350))

    layout = [
        [column],
        [sg.Button('Save', key="SAVE_SLOTS")]
    ]

    window = sg.Window("Set study slots", layout=layout, modal=True, finalize=True, keep_on_top=True)
    
    infos = {}

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            infos = defaults
            break

        if event is not None:
            if event == "SAVE_SLOTS":
                infos['totalPages'] = 0
                infos['totalDuration'] = 0

                maxStudyHour = getSettingsValue('maxStudyHour')
                
                condErrorHours = False
                condErrorHoursIndex = False
                condErrorDuration = False
                errorTextHours = f"Max study hours allowed are {maxStudyHour}.\n"
                errorTextDuration = "U cannot have sessions with duration equals to 0.\n"

                for x in range(7):
                    condErrorHoursIndex = False
                    infos[weekdays[x]] = {}
                    if studyDays[x]:
                        infos[weekdays[x]]['isStudyDay'] = True
                        infos[weekdays[x]]['areThereSessions'] = False
                        if arrAmount[x] > 0:
                            infos[weekdays[x]]['areThereSessions'] = True
                        infos[weekdays[x]]['amount'] = arrAmount[x]
                        infos[weekdays[x]]['pages'] = []
                        infos[weekdays[x]]['types'] = []
                        infos[weekdays[x]]['durations'] = []
                        infos[weekdays[x]]['totalPages'] = 0
                        infos[weekdays[x]]['totalDuration'] = 0
                        for j in range(arrAmount[x]):

                            pages = int(values[f'INPUT_TEXT_PAGES_{j}_SESSION_{weekdays[x]}'])
                            duration = int(values[f'INPUT_TEXT_DURATION_{j}_SESSION_{weekdays[x]}'])
                            if duration != 0:
                                infos[weekdays[x]]['pages'].append(pages)
                                infos[weekdays[x]]['types'].append(values[f'COMBO_TYPE_{j}_SESSION_{weekdays[x]}'])
                                infos[weekdays[x]]['durations'].append(duration)
                                infos[weekdays[x]]['totalPages'] += pages
                                infos[weekdays[x]]['totalDuration'] += duration
                                infos['totalPages'] += pages
                                infos['totalDuration'] += duration  

                                oldTotalMinutes = getTotalMinutes(x, exceptID=bookID)
                                newTotalMinutes = oldTotalMinutes + infos[weekdays[x]]['totalDuration']
                                totalHours = newTotalMinutes/60

                                if totalHours > maxStudyHour and not condErrorHoursIndex:
                                    condErrorHours = True
                                    condErrorHoursIndex = True
                                    errorTextHours += "You have to correct " + weekdays_complete[x] + " sessions. Your hour amounts is " + f'{totalHours:.2f}.\n'
                            else:
                                condErrorDuration = True
                                errorTextDuration += f'Correct the {j+1}° Session of {weekdays_complete[x]}\n'
                    else:
                        infos[weekdays[x]]['isStudyDay'] = False

                    
                
                if True in [condErrorHours, condErrorDuration]:
                    if condErrorHours:
                        sg.popup_error(errorTextHours, title="Too much hours", modal=True, keep_on_top=True)
                    else:
                        sg.popup_error(errorTextDuration, title="Duration invalid", modal=True, keep_on_top=True)
                else:
                    break
                    
    
    window.close()

    return infos

