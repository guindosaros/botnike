########### Importation des packages ###########
import selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import argparse

########### Fonctions ###########
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
        connexion=driver.find_element_by_xpath(connexion_xpath)
        connexion.click()
        ## Completion du mdp et du pass
        # Identiifcation des Text box
        mail_xpath = '/html/body/div[2]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/form/div[2]/input'
        pass_xpath = '/html/body/div[2]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/form/div[3]/input'
        mail = driver.find_element_by_xpath(mail_xpath)
        passw = driver.find_element_by_xpath(pass_xpath)
        # Completion des champs
        mail.send_keys(usermail)
        passw.send_keys(userpass)
        ## Connexion sur la page
        bttn_connex_xpath = '/html/body/div[2]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/form/div[6]/input'
        bttn_connex = driver.find_element_by_xpath(bttn_connex_xpath)
        bttn_connex.click()
        status = True
    except:
        status = False
    wait = WebDriverWait(driver, wait_time).until(EC.visibility_of_element_located((By.XPATH,connexion_xpath)))
    return driver, status

    ### E2 : Sélection de la pointure
### Fonction pour vérifier si la pointure existe
def check_size_available(size_dispo,size):
    st_size = "EU " + str(size)
    available = False
    for t in size_dispo:
        if st_size == t.text:
            available=True
            break
    return available
### Fonction principale
def add_shoe_basket(driver, shoe_url, size,wait_time=10):
    driver.get(shoe_url)
    sizes_xpath = "//li[@class='size va-sm-m d-sm-ib va-sm-t ta-sm-c  ']"
    wait = WebDriverWait(driver, wait_time).until(EC.visibility_of_element_located((By.XPATH,sizes_xpath)))
    size_dispo = driver.find_elements_by_xpath(sizes_xpath)
    available = check_size_available(size_dispo,size)
    if available == True:
        try: 
            driver.find_element_by_xpath("//li[@data-qa='size-available']").find_element_by_xpath(f"//button[text()='EU {size}']").click()
            xpath_basket = "/html/body/div[2]/div/div/div[1]/div/div[2]/div[2]/div/section/div[2]/aside/div/div[2]/div/div[2]/div/button"
            add_basket_btn = driver.find_elements_by_xpath(xpath_basket)
            add_basket_btn[0].click()
        except : 
            driver.find_element_by_xpath("//li[@data-qa='size-available']").find_element_by_xpath(f"//button[text()='EU {size}']").click()
            xpath_basket = "/html/body/div[2]/div/div/div[1]/div/div[2]/div[2]/div/section/div[2]/aside/div/div[2]/div/div[2]/div/button"
            add_basket_btn = driver.find_elements_by_xpath(xpath_basket)
            add_basket_btn[0].click()
    
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
            # Sélection de frame
            iframe = driver.find_element_by_xpath(iframe_xpath)
            # Switch sur le frame
            driver.switch_to.frame(iframe)
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
        payment_btn = driver.find_element_by_xpath(btnxpath)
        payment_btn.click()
    return driver, status

### E5 : Valider paiement
def validate_checkout(driver, wait_time=10):
    #time.sleep(min(3,wait_time))
    validate_xpath = "/html/body/div[1]/div/div[3]/div/div[2]/div/div/main/section[4]/div/div/div/div/section[2]/div/button"
    wait = WebDriverWait(driver, wait_time).until(EC.visibility_of_element_located((By.XPATH,validate_xpath)))
    try:
        btn_validate = driver.find_element_by_xpath(validate_xpath)
        btn_validate.click()
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

### Fonction principale pour l'exécution des calculs
def Shop_Basket_SNKRS(usermail, userpass, shoe_url,shoe_size,secure,exec_date_time,path_driver,wait_time, wait_bf_exec= True,quit_driver = False):
    ### E0 : Attente avant exécution
    if wait_bf_exec==True : 
        sec_wait = Seconds_Wait_Before_Execute(exec_date_time)
        print("Wait time : {0}".format(sec_wait))
        time.sleep(max(0, sec_wait-2))
        
    ### E1 :  Accès et connexion au site
    driver, status_connex = user_connexion(usermail, userpass, path_driver,wait_time)
    if status_connex==False:
        print("Connexion impossible")
        return None
    time.sleep(3)
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
    if quit_driver:
        driver.quit()
    else:
        time.sleep(1600)
        driver.quit()

### python main.py --usermail mohamedsaros@gmail.com --password Momo2020 --shoe_url https://www.nike.com/fr/launch/t/womens-lahar-low-wheat --shoe_size 42 --secure 333 --exec_time "2021-02-17 00:46:00" --waitTime 10 --path_driver /Users/Solo/PythonDriver/chromedriver

######## Main function to execute
# format exec time :  %Y-%m-%d %H:%M:%S -> "2021-02-16 23:54:00"
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