#!/usr/bin/env python
# -*- coding: cp1252 -*-


from selenium.webdriver.common.keys import Keys
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, uuid
from selenium.webdriver.common.action_chains import ActionChains
from distutils.version import StrictVersion
from numbers import Number
from configparser import ConfigParser
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support import expected_conditions as EC
from openpyxl.workbook import Workbook
import ast

from datetime import date
import time
import datetime
import sys
import os
import random
import glob
import re
import shutil
import traceback, wx
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding("cp1252")




class MainApp(wx.App):
    def OnInit(self):
        frame = menu()
        return True

class menu:
    def __init__(self,commande='',matricule=4546):
        if os.path.exists("main.lock")==False:
            try:
                lock=open("main.lock", "a")
                lock.close()
                k = 0

                #04 04 2018 python27
                trace = open("trace.txt", "w")
                trace.close()
                date_jour1 = str(date.today())
                date_jour=self.date2fr(date_jour1,"/")

                nom_parametre = r"" + "parametres.ini"
                if (os.access(nom_parametre, os.F_OK) == False):
                    trace = open("trace.txt", "a")
                    trace.write("Le fichier parametres.ini est introuvable !\n")
                    trace.close()
                    # print("Le fichier parametres.ini est introuvable !")
                    sys.exit(0)

                config = ConfigParser()
                config.read(nom_parametre)

                login = u""+str(config.get('parametre', 'login'))
                password = u""+str(config.get('parametre', 'password'))

                liste_url=[]
                with open(r"liste_url.txt", "r") as f :
                    fichier_entier = f.read()
                    if fichier_entier!="":
                        lignes = fichier_entier.split("\n")
                        liste_url=lignes
                if len(liste_url)==0:
                    print("La liste a traiter est vide !")
                    trace = open("trace.txt", "a")
                    trace.write("La liste a traiter est vide" + "\n")
                    trace.close()

                    sys.exit(0)
                nom_fichier="resultats.txt"
                rep="resultats"
                sans_entete=False

                if(os.access(rep,os.F_OK)==False):
                    os.makedirs(rep,777)

                chromeOptions = webdriver.ChromeOptions()
                chromeOptions.add_argument("--start-maximized")

                prefs = {"profile.default_content_settings.popups": 0,
                         "download.default_directory": "", # IMPORTANT - ENDING SLASH V IMPORTANT
                         "directory_upgrade": True, "extensions_to_open": "", "plugins.plugins_disabled": ["Chrome PDF Viewer"], "plugins.plugins_list": [{"enabled":False,"name":"Chrome PDF Viewer"}]}

                chromeOptions.add_experimental_option("prefs",prefs)
                chromeOptions.add_argument("--disable-print-preview")
                chromedriver = r"chromedriver.exe"
                driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions)

                driver.implicitly_wait(60)

                wait = ui.WebDriverWait(driver,60)

                driver.get("https://www.linkedin.com/uas/login?trk=hb_signin")

                driver.maximize_window()

                s_script= "document.getElementById('session_key-login').setAttribute('value', '%s')"%(login)
                trace = open("trace.txt", "a")
                trace.write("entree login"+"\n")
                trace.close()
                print("entree login")
                driver.execute_script(s_script)
                s_script= "document.getElementById('session_password-login').setAttribute('value', '%s')"%(password)
                trace = open("trace.txt", "a")
                trace.write("entree mdp"+"\n")
                trace.close()
                print("entree mdp")
                driver.execute_script(s_script)

                driver.find_element_by_id("btn-primary").click()
                trace = open("trace.txt", "a")
                trace.write("clic sur authentification"+"\n")
                trace.close()
                print("clic sur authentification")
                time.sleep(10)

                precedent_url = "https://www.linkedin.com/"
                entete = ["url_a_traiter", "nom", "titre", "lien linkedln"]
                existe_fichier_resultat=False
                if os.path.exists(r""+rep + "\\" + nom_fichier)==True:
                    existe_fichier_resultat=True
                ligne = 0
                for x in range(len(liste_url)):
                    url=liste_url[x]
                    driver.get(u""+url)
                    driver.maximize_window()
                    time.sleep(2)
                    trace = open("trace.txt", "a")
                    trace.write("*********************** url a traiter: "+u""+url+"\n")
                    trace.close()
                    #Clic sur commentaire suivant
                    n=0
                    while n<2:
                        try:
                            commentaire_suivant=driver.find_element_by_xpath("//button[@id='show_prev']")
                            commentaire_suivant.click()
                            time.sleep(3)
                            n=n+1
                            trace = open("trace.txt", "a")
                            trace.write("clic sur commentaire suivant "+str(n)+"\n")
                            trace.close()
                        except:
                            break

                    s_script="return $('.feed-shared-update__comments-container').html()"
                    html=driver.execute_script(s_script)
                    # soup=BeautifulSoup(html,"html5lib")
                    soup=BeautifulSoup(html,"html.parser")

                    #ouvrir repli
                    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
                    time.sleep(3)
                    liste_buttons=driver.find_elements_by_xpath("//div[@class='feed-shared-comment-social-bar__social-counts']/button")
                    for y in range(len(liste_buttons)):
                        reply_count=liste_buttons[y].get_attribute("data-control-name")
                        if reply_count=="reply_count":
                            try:
                                liste_buttons[y].click()
                                time.sleep(2)
                            except:
                                pass
                    #ouvrir reponses precedentes
                    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
                    while True:
                        time.sleep(2)
                        try:
                            liste_precedentes=driver.find_elements_by_xpath("//div[@class='feed-shared-comment-item__replies-list replies-list comments-list ember-view']/button")
                            if len(liste_precedentes)==0:
                                break
                        except:
                            break
                        for w in range(len(liste_precedentes)):
                            retour=liste_precedentes[w].get_attribute("data-control-name")
                            if retour=="more_replies":
                                try:
                                    liste_precedentes[w].click()
                                    time.sleep(3)
                                except:
                                    pass

                    #traiter like
                    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)

                    time.sleep(2)
                    liste_likes=driver.find_elements_by_xpath("//div[@class='feed-shared-comment-social-bar__social-counts']/button")
                    for ww in range(len(liste_likes)):
                        retour=liste_likes[ww].get_attribute("data-control-name")
                        if retour=="reply_like_count" or retour=="comment_like_count":
                            try:
                                liste_likes[ww].click()
                                time.sleep(3)
                                #reperer infos like
                                ul=driver.find_element_by_xpath("//ul[@class='feed-shared-likers-modal__actor-list actor-list ember-view']")
                                li_s=ul.find_elements_by_tag_name("li")
                                for l in range(len(li_s)):
                                    a=li_s[l].find_element_by_xpath("./a")
                                    href=a.get_attribute("href")
                                    h3=li_s[l].find_element_by_xpath("./a/div/h3")
                                    commentaire_nom = h3.text
                                    p=li_s[l].find_element_by_xpath("./a/div/p")
                                    commentaire_titre = p.text
                                    #Ajout infos
                                    ligne = ligne + 1
                                    fichier = open(rep + "\\" + str(nom_fichier), "a")
                                    if ligne==1:
                                        if existe_fichier_resultat==False:
                                            fichier.write("\t".join(entete)+"\n")
                                    contenu=u""+url+"\t"+u""+self.nettoye(commentaire_nom.encode("cp1252", "ignore"))+"\t"+u""+self.nettoye(commentaire_titre.encode("cp1252", "ignore"))+"\t"+u""+href
                                    fichier.write(contenu+"\n")
                                    fichier.close()

                                    trace = open("trace.txt", "a")
                                    trace.write(str(x+1)+"/"+str(len(liste_url))+" - "+str(ligne) + " - " + str(u""+url) + "\n")
                                    trace.close()

                                # driver.find_element_by_xpath("//button[@class='feed-fe-modal__close-button close']/span/li-icon/svg/path").click()
                                driver.find_element_by_xpath("//button[@class='feed-fe-modal__close-button close']/span").click()
                                time.sleep(1)
                            except:
                                pass

                    #Recuperer les enregistrements
                    s_script0="return $('.feed-shared-comments-list').html()"
                    html0=driver.execute_script(s_script0)
                    soup0=BeautifulSoup(html0,"html.parser")
                    article_s=soup0.find_all('article')
                    for article in article_s:
                        cas1 = False
                        try:
                            commentaire_nom = article.find("span", {"aria-expanded": "true"}).text
                            cas1=True
                        except:
                            commentaire_nom = article.find("span", {"class": "hoverable-link-text"}).text
                        if cas1:
                            href = article.find("a", {"data-control-name": "mention"})["href"]
                        else:
                            try:
                                href = article.find("a", {"data-control-name": "comment_actor"})["href"]
                            except:
                                href = article.find("a", {"data-control-name": "reply_actor"})["href"]

                        commentaire_titre = article.find("span", {"class": "feed-shared-post-meta__headline Sans-13px-black-55%"}).text
                        #Ajout infos
                        ligne = ligne + 1
                        fichier = open(rep + "\\" + str(nom_fichier), "a")
                        if ligne==1:
                            if existe_fichier_resultat==False:
                                fichier.write("\t".join(entete)+"\n")
                        contenu=u""+url+"\t"+u""+self.nettoye(commentaire_nom.encode("cp1252", "ignore"))+"\t"+u""+self.nettoye(commentaire_titre.encode("cp1252", "ignore"))+"\t"+u""+precedent_url+href
                        fichier.write(contenu+"\n")
                        fichier.close()

                        trace = open("trace.txt", "a")
                        trace.write(str(x+1)+"/"+str(len(liste_url))+" - "+str(ligne) + " - " + str(u""+url) + "\n")
                        trace.close()





                    try:
                        driver.close()
                    except:
                        pass

                    trace = open("trace.txt", "a")
                    trace.write("FIN Traitement decompte mentions linkedin !"+"\n")
                    trace.close()

                    #Suppression du fichier .lock
                    if os.path.exists('main.lock')==True:
                        os.remove('main.lock')

                    sys.exit(0)
                    # print("FIN Traitement recuperation donnees !")

            except Exception as inst:
                log=open(date_jour.replace("/", "-")+".txt", "a")
                traceback.print_exc(file=log)
                log.close()
                try:
                    driver.close()
                except:
                    pass
                if os.path.exists('main.lock')==True:
                    os.remove('main.lock')

                sys.exit(0)


    def retour_valeur(self, tchamp, tvaleur, lib_champ):
        for l in range(len(lib_champ)):
            chp=lib_champ[l]
            for c in range(len(tchamp)):
                if tchamp[c].strip()==chp:
                    return u""+tvaleur[c].strip()
        return ""

    def nettoye(self, chaine):
        chaine=chaine.replace("\t"," ").replace("\n"," ").replace("  "," ").strip().strip("\t").strip("\n")
        return chaine

    def nz(self, valeur_o,valeur_pardefaut=''):
        if valeur_o=='' or valeur_o==None or valeur_o=='None':
            return valeur_pardefaut
        else:
            return valeur_o

    def date2fr(self, sdateEn,sep="-"):
        a1=sdateEn[0:4]
        m1=sdateEn[5:7]
        d1=sdateEn[8:10]
        return d1+sep+m1+sep+a1

    def retour_lignes_fichier(self, sfichier):
        if os.path.exists(r""+sfichier)==False:
            return ""
        with open(r""+sfichier, "r") as f :
            fichier_entier = f.read()
            if fichier_entier!="":
                lignes = fichier_entier.split("\n")
                return lignes
            else:
                return ""

if __name__ == "__main__":
    app = MainApp()
    app.MainLoop()