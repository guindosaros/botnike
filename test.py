import PySimpleGUI as sg

sg.change_look_and_feel('GreenTan') # give our window a spiffy set of colors

layout = [[sg.Text('Your output will go here', size=(40, 1))],
          [sg.Output(size=(110, 30), font=('Helvetica 10'))],
          [sg.MLine(size=(60, 5), enter_submits=True, key='-QUERY-', do_not_clear=False),
           sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),
           sg.Button('EXIT', button_color=(sg.YELLOWS[0], sg.GREENS[0]))]]

window = sg.Window('Chat window', layout, font=('Helvetica', ' 13'), default_button_element_size=(8, 2))

while True:     # The Event Loop
    event, value = window.read()
    if event in (None, 'EXIT'):            # quit if exit button or X
        break
    if event == 'SEND':
        query = value['-QUERY-'].rstrip()
        # EXECUTE YOUR COMMAND HERE
        print('The command you entered was {}'.format(query))
        