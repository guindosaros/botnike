import os
import sys
import six
import pause
import argparse
import logging.config
import re
import time
import random
import json
from selenium.webdriver import ActionChains
from selenium import webdriver
from dateutil import parser as date_parser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC

# usermail = "mohamedsaros@gmail.com"
# userpass = "Momo2020"
# python main.py --username mohamedsaros@gmail.com --password Momo2020 --url https://www.nike.com/fr/launch/t/womens-lahar-low-black --secure 333 --shoe-size EU 38 --driver-type chrome

logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s [PID %(process)d] [Thread %(thread)d] [%(levelname)s] [%(name)s] %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
            "stream": "ext://sys.stdout"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": [
            "console"
        ]
    }
})


NIKE_HOME_URL = "https://www.nike.com/fr/launch"
SUBMIT_BUTTON_XPATH = "/html/body/div[2]/div/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div/div/div[6]/button"
LOGGER = logging.getLogger()


def run(driver,username,password,url,secure,shoe_size,login_time=None,release_time=None,page_load_timeout=None,num_retries=None,dont_quit=True):
    
    driver.maximize_window()
    WebDriverWait(driver,3)
    driver.implicitly_wait(3)
    driver.set_page_load_timeout(page_load_timeout)
    purchase = False

    if login_time:
        LOGGER.info("Attendre le temps de connexion : " + login_time)
        pause.until(date_parser.parse(login_time))

    skip_retry_login = True
    try:
       is_login =  login(driver=driver, username=username, password=password)
    except TimeoutException:
        LOGGER.info("Impossible de se connecter en raison d'un délai d'attente. Réessayer...")
        skip_retry_login = False
    except Exception as e:
        LOGGER.exception("Failed to login: " + str(e))
        six.reraise(Exception, e, sys.exc_info()[2])
    
     
    if release_time:
        LOGGER.info("Waiting until release time: " + release_time)
        pause.until(date_parser.parse(release_time))
    
    num_retries_attempted = 0
    if is_login :
        while True:
            try:
                try:
                    LOGGER.info("Page de demande : " + url)
                    driver.get(url)
                except TimeoutException:
                    LOGGER.info("Le chargement des pages a été interrompu, mais se poursuit quand même")
                    
                try:
                    select_size = select_shoe_size(driver=driver, shoe_size=shoe_size)
                except Exception as e:
                    select_size = False
                    # Try refreshing page since you can't click Buy button without selecting size (except if size parameter passed in)
                    LOGGER.exception("Erreur choix de la pointure" + str(e))
                    # continue
                    
                if select_size :
                    try:
                        add_panier_status = click_add_panier_button(driver=driver)
                    except Exception as e:
                        add_panier_status = False
                        LOGGER.exception("Erreur d'Ajout dans panier: " + str(e))                                
                        six.reraise(Exception, e, sys.exc_info()[2])
                        
                    if add_panier_status :
                        try: 
                            LOGGER.info("initialisation du  panier")
                            # time.sleep(6)
                            panier_url = "https://www.nike.com/fr/cart"
                            LOGGER.info("Page de demande : " + panier_url)
                            driver.get(panier_url)
                        except TimeoutException:
                            LOGGER.info("temps d'attente terminer mais continue")

                        try: 
                            LOGGER.info("Verification du panier")
                            verif_panier = check_panier(driver) 
                        except TimeoutException:
                            verif_panier = False
                            LOGGER.exception("verif_panier" + str(e))
                            
                        # Quand panier contient au moins un element a son sein
                        if verif_panier :
                            try:
                                try:
                                    check_url = 'https://www.nike.com/fr/fr/checkout'
                                    LOGGER.info("Attendre le Boutton de payement")
                                    wait_until_visible(driver, xpath="//div[@class='ncss-col-sm-12 css-gajhq5']/button[1]", duration=10)
                                    driver.get(check_url)
                                    LOGGER.info("Page de demande : " + check_url)
                                    # time.sleep(3)
                                    status_check_adresse = check_livraison_adresse(driver=driver)
                                    carte_paiement_status = check_carte_paiement(driver)
                                except TimeoutException:
                                    LOGGER.info("Le chargement des pages a été interrompu, mais se poursuit quand même")
                            except Exception as e:
                                LOGGER.exception("Impossible d'acceder a la page de payement" + str(e))
                            
                            if status_check_adresse :
                                LOGGER.info("Adresse de livraison ok verification carte paiement")
                                if carte_paiement_status :
                                    LOGGER.info("carte de paiment present saisir votre cvv")
                                    try: 
                                        check_and_validate_cvv = add_cvv(driver,secure) 
                                    except TimeoutException:
                                        check_and_validate_cvv = False
                                        LOGGER.info("Erreur d'ajout du cvv")   
                                        
                                    if check_and_validate_cvv :
                                        LOGGER.info("cvv valide ok passe to paiement")
                                        try: 
                                            purchase = validate_commande(driver) 
                                        except TimeoutException:
                                            LOGGER.info("La validation de la commande a échoué")
                                    else:
                                        LOGGER.info("validation cvv echouer ")
                                else:
                                    LOGGER.info("votre compte manque de carte de paiement")
                            else:
                                LOGGER.info("votre compte manque d'adresse de livraison")
                        else:
                            LOGGER.info("votre panier est vide")
                    else:
                        LOGGER.info("Erreur d'Ajout du basket au panier")
                else:
                    LOGGER.info("n'a pas réussi à sélectionner la pointure car elle est indisponible:")

            except Exception as e:
                print('exeception',str(e))
                if num_retries and num_retries_attempted < num_retries:
                    num_retries_attempted += 1
                    continue
                else:
                    LOGGER.info("L'achat a échoué")
                    break
            if purchase:
                 LOGGER.info("vous avez passer la commande de votre basket avec success")
            break
    else:       
        LOGGER.info("Echec de connexion verifier vos information de connexion")
          
    
      
    if dont_quit:
            LOGGER.info("Prévenir le départ d'un conducteur...")
            input("Appuyez sur la touche Entrée pour quitter...")
        
    driver.quit()

def check_panier(driver):
    time.sleep(10)
    status = False
    
    xpath = "//p[@class='css-1lavku9 e181ly3q6']/span[1]"
    valeur = "0,00 €"
    try:
        panier = driver.find_element_by_xpath("//p[@class='css-1lavku9 e181ly3q6']/span[1]")
        print('panier element ===>', panier.text)
        if panier.text == valeur :
            LOGGER.info("panier vide")
            status = False
        else:
            status = True
            LOGGER.info(f"la somme total du panier est : {panier.text}")
    except Exception as e:
        LOGGER.exception("Impossible d'acceder a la page de payement" + str(e))
    
    return status
    
def select_shoe_size(driver, shoe_size):
    time.sleep(10)
    LOGGER.info("Action pour voir si on peut payer l'element")
    wait_until_visible(driver, xpath="//button[@class='ncss-btn-primary-dark btn-lg']", duration=10)
    size_dispo = driver.find_elements_by_xpath("//li[@class='size va-sm-m d-sm-ib va-sm-t ta-sm-c  ']")
    taille_list = []
    disponible = False
    status = False
    
    for tailles in size_dispo:
        taille = tailles.text
        x = taille.split()
        taille_list.append(x[1])
        
    LOGGER.info(f"Pointure choisir : EU {shoe_size} ")   
    if shoe_size in taille_list:
        LOGGER.info(f"La pointure {shoe_size}  est disponible") 
        disponible = True
    else:
        LOGGER.info(f"La pointure {shoe_size}  est indisponible")
        
    if disponible:
        driver.find_element_by_xpath("//li[@data-qa='size-available']").find_element_by_xpath(f"//button[text()='EU {shoe_size}']").click()
        LOGGER.info("Pointure chosir avec success")
        status = True
    
    return status

       
def click_add_panier_button(driver):
    time.sleep(7)
    status = False
    try:
        xpath = "//button[@class='ncss-btn-primary-dark btn-lg']"
        LOGGER.info("En attendant  que le bouton ajouter dans panier  soit présent")
        element = wait_until_present(driver, xpath=xpath, duration=10) 
        LOGGER.info("Ajouter au panier")
        driver.execute_script("arguments[0].click();", element)
        LOGGER.info("Basket Ajouter au Panier avec Success")
        status = True
    except Exception as e:
        LOGGER.exception("Erreur Ajout du basket dans le panier" + str(e))
    return status
    
def check_livraison_adresse(driver):
    # time.sleep(4)
    status = False
    try:
        LOGGER.info("Verification de l'adresse de livraison")
        xpath = "//i[@class='g72-check text-color-success mr4-sm']"
        wait_until_present(driver, xpath=xpath, duration=10)
        LOGGER.info("Adresse de livraison disponible")
        status = True
    except Exception as e:
        LOGGER.exception("Adresse de livraison non enregistre " + str(e))
        status = False
    return status

def check_carte_paiement(driver):
    time.sleep(4)
    status = False
    try:
        LOGGER.info("verification de presence de carte de paiement")
        xpath = "//label[@class='ncss-label pl4-sm pt3-sm pb3-sm pr4-sm pt2-lg pb2-lg u-full-width']"
        wait_until_present(driver, xpath=xpath, duration=10)
        LOGGER.info("carte paiement disponible")
        
        
        # # LOGGER.info("Waiting for cvv to become visible")
        # LOGGER.info("Insertion du code secure")
        # WebDriverWait(driver, 10, 0.01).until(EC.frame_to_be_available_and_switch_to_it(driver.find_element_by_css_selector("iframe[class='credit-card-iframe-cvv mt1 u-full-width']")))
        # idName = "cvNumber"
        # wait_until_visible(driver, el_id=idName)
        # secure_input = driver.find_element_by_id("cvNumber")
        # secure_input.clear()
        # secure_input.send_keys(secure)
        # driver.switch_to.parent_frame()
        
        # time.sleep(4)
        # LOGGER.info("validation de la carte")
        # btnxpath = "////*[@class='ncss-brand pt2-sm pr5-sm pb2-sm pl5-sm ncss-btn-accent continueOrderReviewBtn mod-button-width ncss-brand pt3-sm prl5-sm pb3-sm pt2-lg pb2-lg d-sm-b d-md-ib u-uppercase u-rounded fs14-sm']"
        # element = wait_until_present(driver, xpath=btnxpath, duration=10)
        # driver.execute_script("arguments[0].click();", element)
        # LOGGER.info("mode de paiement valider")

        status = True
    except Exception as e:
        LOGGER.exception("carte de livraison non enregistre " + str(e))
        status = False
    return status

def add_cvv(driver,secure):
    time.sleep(3)
    status = False
    try:
        # LOGGER.info("Waiting for cvv to become visible")
        LOGGER.info("Insertion du code secure")
        WebDriverWait(driver, 10, 0.01).until(EC.frame_to_be_available_and_switch_to_it(driver.find_element_by_css_selector("iframe[class='credit-card-iframe-cvv mt1 u-full-width']")))
        idName = "cvNumber"
        wait_until_visible(driver, el_id=idName)
        secure_input = driver.find_element_by_id("cvNumber")
        secure_input.clear()
        secure_input.send_keys(secure)
        driver.switch_to.parent_frame()
        
        # time.sleep(1)
        LOGGER.info("validation de la carte")
        btnxpath = "/html/body/div[1]/div/div[3]/div/div[2]/div/div/main/section[3]/div/div[1]/div[2]/div[5]/button"
        element = wait_until_present(driver, xpath=btnxpath, duration=10)
        driver.execute_script("arguments[0].click();", element)
        LOGGER.info("mode de paiement valider")
        status = True
    except Exception as e:
        LOGGER.exception("Erreur D'ajout de la cvv " + str(e))
        status = False
    return status

def validate_commande(driver):
    time.sleep(2)
    status = False
    try:
        LOGGER.info("Verification si paiement valide")
        xpath = "/html/body/div[1]/div/div[3]/div/div[2]/div/div/main/section[3]/header/h2/i"
        wait_until_present(driver, xpath=xpath, duration=10)
        LOGGER.info("paiement valider ")
        
        LOGGER.info("Validation de la commande")
        btnxpath = "/html/body/div[1]/div/div[3]/div/div[2]/div/div/main/section[4]/div/div/section/div/button"
        element = wait_until_present(driver, xpath=btnxpath, duration=10)
        driver.execute_script("arguments[0].click();", element)
        LOGGER.info("validation commande en cours ...... ")
        wait_until_visible(driver=driver, xpath="/html/body/div[1]/div/div[3]/div/div[2]/div/div/div[2]/div/div/div/div/div", duration=20)
        LOGGER.info("validation commande terminer")
        status = True
    except Exception as e:
        LOGGER.exception("Erreur validation commande " + str(e))
        status = False
        
    return status

# fonction de connexion au Site 
def login(driver, username, password):
    status = False
    try:
        LOGGER.info("Page de demande : " + NIKE_HOME_URL)
        driver.get(NIKE_HOME_URL)
    except TimeoutException:
        LOGGER.info("Le chargement des pages a été interrompu, mais se poursuit quand même")
        
    LOGGER.info("modal de connexion ")    
    ## Aller sur la page de connexion
    connexion_xpath = '//button[@class="join-log-in text-color-grey prl3-sm pt2-sm pb2-sm fs12-sm d-sm-b"]'
    connexion=driver.find_element_by_xpath(connexion_xpath)
    connexion.click()
    ## Completion du mdp et du pass
    # Identiifcation des Text box
    
    mail_xpath = '/html/body/div[2]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/form/div[2]/input'
    pass_xpath = '/html/body/div[2]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/form/div[3]/input'
    mail = driver.find_element_by_xpath(mail_xpath)
    passw = driver.find_element_by_xpath(pass_xpath)
    
    LOGGER.info("Entrez password et email")
    # Completion des champs
    mail.send_keys(username)
    passw.send_keys(password)
    
    LOGGER.info("clique boutton de connexion")
    ## Connexion sur la page
    bttn_connex_xpath = '/html/body/div[2]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/form/div[6]/input'
    bttn_connex = driver.find_element_by_xpath(bttn_connex_xpath)
    bttn_connex.click()
    try :
        wait_until_visible(driver=driver, xpath="//*[@data-qa='user-name']/*[@data-qa='user-name']", duration=15)
        LOGGER.info("Connexion réussie")
        status = True
    except Exception as e:
        status = False
        LOGGER.exception("Erreur de connexion")
        
    return status

def wait_until_visible(driver, xpath=None, class_name=None, el_id=None, duration=10000, frequency=0.01):
    if xpath:
        WebDriverWait(driver, duration, frequency).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    elif class_name:
        WebDriverWait(driver, duration, frequency).until(EC.visibility_of_element_located((By.CLASS_NAME, class_name)))
    elif el_id:
        WebDriverWait(driver, duration, frequency).until(EC.visibility_of_element_located((By.ID, el_id)))


# fonction de verification de la disponibilite d'un champs de saisir 
def wait_until_present(driver, xpath=None, class_name=None, el_id=None, duration=10000, frequency=0.01):
    if xpath:
        return WebDriverWait(driver, duration, frequency).until(EC.presence_of_element_located((By.XPATH, xpath)))
    elif class_name:
        return WebDriverWait(driver, duration, frequency).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
    elif el_id:
        return WebDriverWait(driver, duration, frequency).until(EC.presence_of_element_located((By.ID, el_id)))   

def wait_until_clickable(driver, xpath=None, class_name=None, el_id=None, duration=10000, frequency=0.01):
    if xpath:
        WebDriverWait(driver, duration, frequency).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    elif class_name:
        WebDriverWait(driver, duration, frequency).until(EC.element_to_be_clickable((By.CLASS_NAME, class_name)))
    elif el_id:
        WebDriverWait(driver, duration, frequency).until(EC.element_to_be_clickable((By.ID, el_id)))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--url", required=True)
    parser.add_argument("--secure", required=True)
    parser.add_argument("--shoe-size", required=True)
    parser.add_argument("--driver-type", default="firefox", choices=("firefox", "chrome"))
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--webdriver-path", required=False, default=None)
    parser.add_argument("--login-time", default=None)
    parser.add_argument("--release-time", default=None)
    parser.add_argument("--page-load-timeout", type=int, default=30)
    parser.add_argument("--dont-quit", action="store_true")
    parser.add_argument("--num-retries", type=int, default=1)
    
    args = parser.parse_args()
    
    driver = None
    if args.driver_type == "firefox":
        options = webdriver.FirefoxOptions()
        if args.headless:
            options.add_argument("--headless")
        if args.webdriver_path != None:
            executable_path = args.webdriver_path
        elif sys.platform == "darwin":
            executable_path = "./bin/geckodriver_mac"
        elif "linux" in sys.platform:
            executable_path = "./bin/geckodriver_linux"
        elif "win32" in sys.platform:
            executable_path = "./bin/geckodriver_win32.exe"
        else:
            raise Exception("Drivers for installed operating system not found. Try specifying the path to the drivers with the --webdriver-path option")
        driver = webdriver.Firefox(executable_path=executable_path, firefox_options=options, log_path=os.devnull)
    elif args.driver_type == "chrome":
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        if args.headless:
            options.add_argument("headless")
        if args.webdriver_path != None:
            executable_path = args.webdriver_path
        elif sys.platform == "darwin":
            executable_path = "./bin/chromedriver_mac"
        elif "linux" in sys.platform:
            executable_path = "./bin/chromedriver_linux"
        elif "win32" in sys.platform:
            executable_path = "./bin/chromedriver.exe"
        else:
            raise Exception("Drivers for installed operating system not found. Try specifying the path to the drivers with the --webdriver-path option")
        driver = webdriver.Chrome(executable_path=executable_path, chrome_options=options)
    else:
        raise Exception("Specified web browser not supported, only Firefox and Chrome are supported at this point")
    
    run(driver=driver,username=args.username, password=args.password, url=args.url, secure=args.secure,shoe_size=args.shoe_size,login_time=args.login_time,release_time=args.release_time,page_load_timeout=args.page_load_timeout,num_retries=args.num_retries,dont_quit=args.dont_quit)