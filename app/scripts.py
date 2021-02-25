import selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import argparse

### E1 : Connexion
def user_connexion(usermail, userpass, path_driver,wait_time =10):
    url = "https://www.nike.com/fr/launch"
    ### Création de l'objet driver
    #Chemin jusqu'au driver
    path_to_web_driver = path_driver
    #On charge le driver
    driver=webdriver.Chrome(path_to_web_driver)
    driver.implicitly_wait(0) #Seconde d'attente avant quelconque opération
    ### Accès au site
    driver.get(url)
    ### Wait pour exécuter code
    connexion_xpath = '//button[@class="join-log-in text-color-grey prl3-sm pt2-sm pb2-sm fs12-sm d-sm-b"]'
    wait = WebDriverWait(driver, wait_time).until(EC.visibility_of_element_located((By.XPATH,connexion_xpath)))
    try: 
        ###Navigation
        ## Aller sur la page de connexion
        driver.find_element_by_xpath(connexion_xpath).click()
        ## Completion du mdp et du pass
        # Identiifcation des Text box et exécution des commandes
        mail_xpath = '/html/body/div[2]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/form/div[2]/input'
        pass_xpath = '/html/body/div[2]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/form/div[3]/input'
        driver.find_element_by_xpath(mail_xpath).send_keys(usermail)
        driver.find_element_by_xpath(pass_xpath).send_keys(userpass)
        ## Connexion sur la page
        bttn_connex_xpath = '/html/body/div[2]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/form/div[6]/input'
        driver.find_element_by_xpath(bttn_connex_xpath).click()
        status = True
    except:
        status = False
    #wait = WebDriverWait(driver, wait_time).until(EC.visibility_of_element_located((By.XPATH,connexion_xpath)))
    return driver, status

### E2 : Sélection de la pointure
def add_shoe_basket(driver, shoe_url, size,wait_time=10, freq=0.1):
    # Pour les essais
    status= False
    itermax=int(wait_time/freq)
    available=False
    ### E0 : Accès à la page
    driver.get(shoe_url)
    ### E1 : Trouver la taille
    cpt=0
    while available == False and cpt<=itermax:
        try:
            find_size = driver.find_element_by_xpath('//button[contains(text(), "EU {}")]'.format(size))
            driver.execute_script("arguments[0].scrollIntoView(true);", find_size)
            find_size.click()
            #Check classroot for validate the class has been chosen
            getElementClassRoot = find_size.find_element_by_xpath('..')
            if "selected" in getElementClassRoot.get_attribute('class'):
                available=True
                print(f"Iterations pour trouver la taille : {cpt}/{itermax} ")
        except:
            time.sleep(freq)
            cpt+=1
    ### E2 : Ajouter la carte
    if available ==True:
        xpath_add_cart = '//*[@data-qa="add-to-cart"]'
        status = False
        wait = WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((By.XPATH,xpath_add_cart)))
        cpt = 0
        while status == False and cpt<=itermax:
            try: 
                add_card_btn = driver.find_element_by_xpath(xpath_add_cart)
                add_card_btn.click()
                status=True
                print(f"Iterations pour ajouter à la carte : {cpt}/{itermax} ")
            except:
                time.sleep(freq)
                cpt+=1
    print("Chaussure ajoutée au panier")
    return driver, available

### E3 : Aller au panier
def go_checkout(driver):
    url_checkout = "https://www.nike.com/fr/checkout"
    driver.get(url_checkout)
    return driver



### E4 : Exécuter le paiement
def execute_payment(driver, secure_code, wait_time=10):
    #time.sleep(min(10,wait_time))
    ### Param
    status= False
    itermax =2
    cpt =1
    iframe_xpath = "//iframe[@class='credit-card-iframe-cvv mt1 u-full-width']"
    ### Wait till element visible
    wait = WebDriverWait(driver, wait_time).until(EC.visibility_of_element_located((By.XPATH,iframe_xpath)))
    ### Ajout du cvv
    while status == False and cpt <=itermax:
        try:
            # Sélection & Switch sur le frame
            driver.switch_to.frame(driver.find_element_by_xpath(iframe_xpath))
            status = True
        except:
            status=False
            cpt+=1
            pass
    if status ==True:   
        # Sélection du cvv
        idName = "cvNumber"
        secure_input = driver.find_element_by_id(idName)
        secure_input.clear()
        secure_input.send_keys(secure_code)
        driver.switch_to.parent_frame()
        ## Exécuter le paiement
        btnxpath = "/html/body/div[1]/div/div[3]/div/div[2]/div/div/main/section[3]/div/div[1]/div[2]/div[5]/button"
        wait = WebDriverWait(driver, wait_time).until(EC.visibility_of_element_located((By.XPATH,btnxpath)))
        #time.sleep(min(3,wait_time))
        driver.find_element_by_xpath(btnxpath).click()
    return driver, status



### E5 : Valider paiement
def validate_checkout(driver, wait_time=10):
    #time.sleep(min(3,wait_time))
    validate_xpath = "/html/body/div[1]/div/div[3]/div/div[2]/div/div/main/section[4]/div/div/div/div/section[2]/div/button"
    wait = WebDriverWait(driver, wait_time).until(EC.visibility_of_element_located((By.XPATH,validate_xpath)))
    try:
        driver.find_element_by_xpath(validate_xpath).click()
        status = True
    except:
        status = False
    return driver, status


### Fonction pour définir le temps à attendre avant l'exécution du script
# Format du temps à attendre : %Y-%m-%d %H:%M:%S -> 2021-02-16 23:54:00
def Seconds_Wait_Before_Execute(string_date):
    time_exec = time.strptime(string_date,'%Y-%m-%d %H:%M:%S')
    time_exec_sec = time.mktime(time_exec)
    return max(0, time_exec_sec-time.time())


def Shop_Basket_SNKRS(usermail, userpass, shoe_url,shoe_size,secure,exec_date_time,path_driver,wait_time, wait_bf_exec= True,quit_driver = False):
    ### E1 :  Accès et connexion au site
    driver, status_connex = user_connexion(usermail, userpass, path_driver,wait_time)
    if status_connex==False:
        print("Connexion impossible")
        return None
    else:
        print("Connexion reussie")
    ### Ewait : Attente avant exécution
    if wait_bf_exec==True : 
        sec_wait = Seconds_Wait_Before_Execute(exec_date_time)
        print("Wait time : {0}".format(sec_wait))
        time.sleep(max(2, sec_wait))
    else:
        time.sleep(3)
    time_start = time.time()
    ### E2 :  Ajout chaussures au panier
    driver, available = add_shoe_basket(driver,shoe_url,shoe_size,wait_time)
    if available==False:
        print("Impossible d'ajouter la chaussure au panier")
        return None
    ### E3 : Accès à la page de paiement
    driver = go_checkout(driver)
    ### E4 : Exécuter paiement
    driver, status_pay = execute_payment(driver, secure,wait_time)
    if status_pay==False:
        print("Paiement Non execute")
        return None
    ### E5 : Valider paiement
    driver, status_val = validate_checkout(driver, wait_time)
    if status_val==False:
        print("Paiment non valide")
        return None
    print("Script bien execute !")
    time_exec = time.time() - time_start
    print(f"Temps d'execution : {time_exec}")
    if quit_driver:
        driver.quit()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--usermail", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--shoe_url", required=True)
    parser.add_argument("--shoe_size", type=int,required=True)
    parser.add_argument("--secure", required=True)
    parser.add_argument("--exec_time", required=True)
    parser.add_argument("--waitTime",  type=int,required=True)
    parser.add_argument("--path_driver", required=True)
    args = parser.parse_args()
       
    #### Execute computation

    Shop_Basket_SNKRS(usermail=args.usermail, userpass=args.password, shoe_url=args.shoe_url, shoe_size=args.shoe_size,secure=args.secure , exec_date_time =args.exec_time, path_driver = args.path_driver,wait_time=args.waitTime)