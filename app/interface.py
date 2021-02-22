import PySimpleGUI as sg



def app():

    sg.theme('SandyBeach')  # No gray windows please!
    # sg.set_options(element_padding=(0, 0))

     # ------ Menu Definition ------ #
    menu_def = [
                    ['&Accueil'],
                    ['&Configuration'],
                    ['&Aide', '&A-propos', '&Guide'],
                    ['&Quitter'],
                ]

    col1 = sg.Column([
    # Categories frame
    [ sg.Frame(' SNKRS : ', [[ sg.Text('Acheter Automatiquement vos baskets sur SNKRS ',font=("Verdana", "10", "bold")),]],)],
    # Information frame
    [ sg.Frame(' Information basket :', [[ sg.Text(),  sg.Column([
                                    [sg.Text('basket-url :', justification='right',size =( 10, 1)), sg.InputText(key='-URL-')],
                                    [sg.Text('taille-basket :' , justification='right',size =(10, 1)), sg.InputText(key='-TAILLE-')],
                                    [sg.Text('waitime :' , justification='right',size =(10, 1)), sg.InputText(key='-WAITIME-')],
                                    [sg.Text("date: " , justification='right',size =(10, 1)), sg.InputText(key='-DATE-')],
                                    ], size=(400, 200), pad=(50, 50))]])], 

    [ sg.Frame('Actions:', [[ sg.Column([[ sg.Button('Commander'),  sg.Button(
    'Annuler'),]], size=(400, 50), pad=(0, 0))]])]], pad=(50, 50))

    
                                    
    col3 =  sg.Column([[sg.Output(size=(75, 12))],], pad=(50, 50))
    
    # STEP 1 define the layout
    layout = [ 
                [sg.Menu(menu_def, tearoff=False, pad=(20,1))],
                [col1],
                [col3],
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
        if event == sg.WIN_CLOSED or event == 'Help':     # If user closed window with X or if user clicked "Exit" button then exit
            break
        if event == 'Commander':
            print('You pressed the button')
    window.close()



if __name__ == '__main__':      
        app()