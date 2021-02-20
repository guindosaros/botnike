Il y a quelques conditions à remplir pour faire fonctionner le bot. 

Tout d'abord, vous devez installer Python 3.7 ou supérieur.

Les instructions ci-dessous vous montrent comment le faire dans plusieurs systèmes d'exploitation.



Pour Commencer Téléchargement et installation de python



NB: pendant l'installation ajouter python au path





MacOS



Sur le site officiel de Python https://www.python.org/

Si vous avez installé brew, vous pouvez simplement lancer la commande brew install python3



Linux



Sur le site officiel de Python https://www.python.org/

Utiliser le gestionnaire de paquets pour votre système. Avec Ubuntu, cette commande est sudo apt install python3-dev



Windows



Sur le site officiel de Python https://www.python.org/

Si vous avez le gestionnaire de paquets Chocolatey installé, vous pouvez lancer choco et installer python



Installation des pilotes web:



Nous allons utiliser le webdriver de Google donc avoir Google Chrome installé sur sa machine.



Accéder à ce lien pour télécharger un webdriver. https://chromedriver.chromium.org/downloads



télécharger la version chromium de Chrome inférieur ou égal a la version de votre Google chrome.

decompresser le dossier et copier le fichier dans le dossier de votre choix.





Ensuite l'installation des module Python

dans les fichier recu vous aurez un fichier text nommer requirements.txt 

Ensuite l'installation des modules Python



Dans les fichiers reçus, vous aurez un fichier text nommer requirements.txt 



methode 1

Ouvrir une invite  de commande se mettre au niveau du dossier reçu et lancer la commande



pip install -r requirements.txt



methode 2 



Ouvrir le fichier requirement et installer les modules une par une 



exemple:

pip install pause==0.1.2





Exécution du bot :

Ouvrir le fichier Excel et ensuite renseigner les options de configuration et cliquez sur run



Options de configuration:



- E-mail : l'adresse e-mail du compte snkrs



- password : le mot de pass du compte



- basket-url : le lien du basket a acheté un exemple : (https://www.nike.com/fr/launch/t/womens-lahar-low-black)



- taille-basket : la taille du basket a acheté un exemple : (36)



- cvv : le code cvv de la carte de paiement enregistrer sur le compte



- waitime : le temps d'attente pour chaque action en second (pour plus d'efficacité du robot nous conseillons 30 ou plus)



- driver-path : le chemin vers le webdriver de Google



- python-exe-path : le chemin vers  de python 



- python-script : le chemin du code python a exécuté.


-execute_time : la date et l'heure d'execution du scripts 























