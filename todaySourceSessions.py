from functions import *

def seeTodaySessions():
    timeNow = datetime.now()
    timeStr = timeNow.strftime('%Y-%m-%d')
    weekdayIndex = 3 # timeNow.weekday()

    query = "SELECT arrSessions FROM sources WHERE  ? <= deadline"
    parameters = (timeStr, )

    cursor.execute(query, parameters)
    result = cursor.fetchall()

    sessionsLayout = []
    
    for x in result:
        json = ast.literal_eval(x[0])
        if json[weekdays[weekdayIndex]]['isStudyDay'] and json[weekdays[weekdayIndex]]['areThereSessions']:
            continue                                


    layout = [ 
        [ 
            sg.Text('Your today sessions: ')
        ],
        [] 
    ]
    
    window = sg.Window("Today Sessions", layout=layout, modal=True, finalize=True, keep_on_top=True)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        
        if event is not None:
            continue
    
    window.close()