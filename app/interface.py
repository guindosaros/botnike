import PySimpleGUI as sg
from json import (load as jsonload, dump as jsondump)
from os import path


SETTINGS_FILE = path.join(path.dirname(__file__), r'settings_file.cfg')
DEFAULT_SETTINGS = {'email': '',  'theme': sg.theme(), 'password' : '','cvv': '', 'webdriver': ''}
SETTINGS_KEYS_TO_ELEMENT_KEYS = {'email': '-EMAIL-' , 'theme': '-THEME-', 'password' : '-PASSWORD-','cvv' : '-CVV-','webdriver' : '-WEBDRIVER-'}

def load_settings(settings_file, default_settings):
    try:
        with open(settings_file, 'r') as f:
            settings = jsonload(f)
    except Exception as e:
        sg.popup_quick_message(f'exception {e}', "Aucun fichier de configuration n'a été trouvé.", keep_on_top=True, background_color='red', text_color='white')
        settings = default_settings
        save_settings(settings_file, settings, None)
    return settings


def save_settings(settings_file, settings, values):
    if values:      # if there are stuff specified by another window, fill in those values
        for key in SETTINGS_KEYS_TO_ELEMENT_KEYS:  # update window with the values read from settings file
            try:
                settings[key] = values[SETTINGS_KEYS_TO_ELEMENT_KEYS[key]]
            except Exception as e:
                print(f"Problème de mise à jour des paramètres à partir des valeurs des fenêtres. Clé =  {key} ")

    with open(settings_file, 'w') as f:
        jsondump(settings, f)

    sg.popup('Paramètres sauvegardés')

    

def create_settings_window(settings):
    
    sg.theme(settings['theme'])

    def TextLabel(text): return sg.Text(text+':', justification='r', size=(15,1))

    layout = [  [sg.Text('Settings', font='Any 15')],
                [TextLabel('Email'), sg.Input(key='-EMAIL-')],
                [TextLabel('Password'), sg.Input(key='-PASSWORD-')],
                [TextLabel('Cvv'), sg.Input(key='-CVV-')],
                [TextLabel('Webdriver'), sg.Input(key='-WEBDRIVER-')],
                [TextLabel('Theme'),sg.Combo(sg.theme_list(), size=(20, 20), key='-THEME-')],
                [sg.Button('Save'), sg.Button('Exit')]  ]

    window = sg.Window('Settings', layout, keep_on_top=True, finalize=True)

    for key in SETTINGS_KEYS_TO_ELEMENT_KEYS:   # update window with the values read from settings file
        try:
            window[SETTINGS_KEYS_TO_ELEMENT_KEYS[key]].update(value=settings[key])
        except Exception as e:
            print(f'Problem updating PySimpleGUI window from settings. Key = {key}')

    return window



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
        if event == sg.WIN_CLOSED or event == 'Quitter':     # If user closed window with X or if user clicked "Exit" button then exit
            break
        if event == 'A-propos':
            # window.disappear()
            sg.popup('About this program','Version 1.0', 'PySimpleGUI rocks...', grab_anywhere=True,icon= 'skrs.ico',
             location = (0,50))
            # window.reappear()

        if event == 'Commander':
            print('You pressed the button')
    window.close()



if __name__ == '__main__':      
        app()