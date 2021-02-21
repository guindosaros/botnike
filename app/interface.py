import PySimpleGUI as sg



def app():

    sg.theme('DarkAmber')  # No gray windows please!
    # sg.set_options(element_padding=(0, 0))

     # ------ Menu Definition ------ #
    menu_def = [['&Accueil'],
                ['&Configuration'],
                ['&Aide'],
                ['&Quitter'],]

    col1 = sg.Column([
    # Categories frame
    [ sg.Frame('SNKRS : ', [[ sg.Text('Acheter Automatiquement vos Basket sur SNKRS '),]],)],
    # Information frame
    [ sg.Frame('Information Basket:', [[ sg.Text(),  sg.Column([
                                    [sg.Text('Basket-url :', size=(10, 1)), sg.InputText(key='-NAME-')],
                                    [sg.Text('Taille-Basket :', size=(10, 1)), sg.InputText(key='-ADDRESS-')],
                                    [sg.Text('Waitime :', size=(10, 1)), sg.InputText(key='-PHONE-')],
                                    [sg.Text("Date:", size=(10, 1)), sg.InputText(key='-Date-')],
                                    ], size=(235, 150), pad=(50, 50))]])], ], pad=(50, 50))
                                    
    col3 =  sg.Column([[ sg.Frame('Actions:', [[ sg.Column([[ sg.Button('Commander'),  sg.Button(
    'Annuler'),]], size=(450, 60), pad=(0, 0))]])]], pad=(0, 0))
    
    # STEP 1 define the layout
    layout = [ 
                [sg.Menu(menu_def, tearoff=False, pad=(20,1))],
                [col1],
                [col3]
            ]

    #STEP 2 - create the window
    window = sg.Window('SNKRS Boot Application', 
    layout, grab_anywhere=True,
    icon= 'skrs.ico',
    location = (50,50)
    )

    # STEP3 - the event loop
    while True:
        event, values = window.read()   # Read the event that happened and the values dictionary
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':     # If user closed window with X or if user clicked "Exit" button then exit
            break
        if event == 'Button':
            print('You pressed the button')
    window.close()



if __name__ == '__main__':      
        app()