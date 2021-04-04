# essaie prog python 1 de system de cbt basique the orca's IV

# addition modules------------------------
import tkinter as tk
import random as rd
from tkinter import filedialog
#----------------------------------------

# Mise en place du type perso

class Mob:
    def __init__(self,fichier):
        self.fichier = fichier #donne fichier des stat du mob
        self.info()
        self.HP = self.info()['HP']

    def info(self): #recup un dict des stats du mob
        fichier1= self.fichier
        info = {}
        objet_fichier = open(fichier1, 'rt')
        for i in objet_fichier:
            if ':' in i:
                info[i.split(":")[0][:-1]] = i.split(':')[1][:-1]
        objet_fichier.close()
        return info

    def modifier_hp(self,modif):
        a = self.HP
        b = int(a) - int(modif)
        self.HP = str(b)

#Etape n°1 du combat:

def initiative(mob1,mob2,dé1,dé2):
    compare = []
    for i in [0,1]: #mise en place des 2 init
        if i == 0:  #récupération init et cat
            init = int(mob1.info()['Init'])
            cat = int(mob1.info()['Catégorie']) - int(mob1.info()['Catégorie'])
        else:
            init = int(mob2.info()['Init'])
            cat = int(mob1.info()['Catégorie']) - int(mob1.info()['Catégorie'])
        if cat < 0:
            cat = 0
        if i == 0:      #mose en place des 2 dés
            dés = dé1
        else:
            dés = dé2
        init_tot = init + dés + cat
        compare.append(init_tot)    #liste des 2 init tot
    diff = abs(compare[0] - compare[1]) - 5
    pas = 0
    while diff >= 0:   #mise en place des bonus de diff d'init
        pas += 1
        diff += -5
    if compare[0] > compare[1]:
        return [mob1,mob2,pas,compare]
    else:
        return [mob2,mob1,pas,compare]

#Etape n°2 : calcul dégats appliqués (sans les types)

def dgt_applique(mob1,dé1,mob2,dé2,bonus):
    #calcul catégorie libre
    cat1 = int(mob1.info()['Catégorie'])
    cat2 = int(mob2.info()['Catégorie'])
    diff = cat1 - cat2 
    if diff > 0:
        catlibr1 , catlibr2 = diff , 0
    else:
        catlibr1 , catlibr2 = 0, diff
    #phase dégats
    atk = int(mob1.info()['Atk'])
    att_tot = dé1 + atk + catlibr1 + bonus
    #phase défence
    Def= int(mob2.info()['Def'])
    def_tot = dé2 + Def + catlibr2
    retour = att_tot - def_tot
    if retour > 0:
        return [retour,att_tot,def_tot]
    else:
        return [0,att_tot,def_tot]

#Etape n°3 : model Graphique
class Interface():
    def __init__(self):
        #création window de base
        self.root = tk.Tk()
        self.root.geometry("900x600")
        self.root.title("Gestion de combat : The Orca's IV")
        self.root.config(background='#CE85F0')
        self.mobs_fichier = ['','']
        self.mobs_objets = ['','']
        self.etape = 0

        #création page 1
        self.page1 = tk.Frame(self.root, bg='#CE85F0')
        self.gestion_grille(1)
        self.creation_page1()
        self.page1.pack(expand=True)


    def creation_page1(self):
        self.texte_page1()
        self.tout_bouton_page1()

    def gestion_grille(self,number):
        for row_index in range(4):
            if number == 1:
                self.page1.rowconfigure(row_index,minsize=100,pad=40)
            else:
                self.page2.rowconfigure(row_index,minsize=100,pad=40)
            for col_index in range(3):
                if number ==1:
                    self.page1.columnconfigure(col_index,minsize=100,
                        pad=40)
                else:
                    self.page2.columnconfigure(col_index,minsize=100,
                        pad=40)

    def texte_page1(self):
        titre = tk.Label(self.page1,
                text="Gestion de combats the Orca's IV",bg='#CE85F0',
                font=('Arial',30))
        titre.grid(column=1,row=0,sticky='ns')

    def tout_bouton_page1(self):
        self.boutton_mob_gauche = tk.Button(self.page1,text='Mob_1',
                fg='#000000',font=('Arial',12),
                command=self.chercher_fichier(0))
        self.boutton_mob_gauche.grid(column=0,row=1)

        self.boutton_mob_droit = tk.Button(self.page1,text='Mob_2',
                fg='#000000',font=('Arial',12),
                command=self.chercher_fichier(1))
        self.boutton_mob_droit.grid(column=2,row=1)

        boutton_next =tk.Button(self.page1,text='Next',fg='#DC1616',
                font=('Arial',12),command=self.next_page2)
        boutton_next.grid(column=1,row=4)

    #overture gestionnaire fichier, return chmin absolut fichier
    def chercher_fichier(self,number):
        def sous_fonc():
            resultat = filedialog.askopenfilename(
                    initialdir='C:\\',
               title='selctionner fiche mob',
               filetypes=(('fiches','.txt'),('all','*,*')))
            self.mobs_fichier[number] = resultat
            if number == 0:
                self.boutton_mob_gauche.configure(bg='green')
            else:
                self.boutton_mob_droit.configure(bg='green')
        return sous_fonc

    def next_page2(self):
        self.page1.destroy()
        self.mise_en_place_page2()
        
    #Mise en place de la page n°2

    def hp_mob(self):
        self.hp = ['','']
        for i in range(len(self.mobs_objets)):
            tmp = self.mobs_objets[i].HP
            self.hp[i] = tmp

    def mise_en_place_page2(self):
        #forme de la frame
        self.page2 = tk.Frame(self.root, bg='#CE85F0')
        self.gestion_grille(2)

        #création objets mob
        self.creation_mob()
        self.hp_mob()

        #constantes utiles
        self.resultats = ['','','']
        self.dé = ['','']

        #création de la mise en page
        self.text_page2()
        self.boutton_page2()
        self.suivant()
        self.page2.pack(expand=True)

    def creation_mob(self): #mise en place des objets mobs
        for i in range(len(self.mobs_fichier)):
            tmp = Mob(self.mobs_fichier[i])
            self.mobs_objets[i] = tmp

    def text_page2(self):

        #informaton mob
        txt_m1 = tk.Frame(self.page2,bg='#CE85F0')
        txt_m1.grid(column=0,row=0)
        txt_m2 = tk.Frame(self.page2,bg='#CE85F0')
        txt_m2.grid(column=3,row=0)

        text1_nom = tk.Label(txt_m1,
                text=self.mobs_objets[0].info()['Nom'],
                font=('Arial',15),bg='#CE85F0')
        text2_nom = tk.Label(txt_m2,
                text=self.mobs_objets[1].info()['Nom'],
                font=('Arial',15),bg='#CE85F0')
        text1_nom.pack()
        text2_nom.pack()

        self.hp1 = tk.StringVar()
        self.hp2 = tk.StringVar()
        text1_hp = tk.Label(txt_m1,
                textvariable=self.hp1,
                font=('Arial',15),bg='#CE85F0')
        text2_hp = tk.Label(txt_m2,
                textvariable=self.hp2,
                font=('Arial',15),bg='#CE85F0')
        self.hp1.set('HP ='+self.mobs_objets[0].HP)
        self.hp2.set('HP ='+self.mobs_objets[1].HP)
        text1_hp.pack()
        text2_hp.pack()

        #resultats action
        self.resultats0 = tk.StringVar()
        self.resultats1 = tk.StringVar()
        self.resultats2 = tk.StringVar()
        info_mob1 = tk.Label(self.page2,
                textvariable=self.resultats0,
                font=('Arial',15),bg='#CE85F0')
        info_mob2 = tk.Label(self.page2,
                textvariable=self.resultats1,
                font=('Arial',15),bg='#CE85F0')
        info_tot = tk.Label(self.page2,
                textvariable=self.resultats2,
                font=('Arial',15),bg='#CE85F0')
        self.resultats0.set('')
        self.resultats1.set('')
        self.resultats2.set('')

        info_mob1.grid(column=0,row=3)
        info_mob2.grid(column=3,row=3)
        info_tot.grid(column=1,row=3,columnspan=2)


    def boutton_page2(self):
        self.tb1 = tk.StringVar()
        self.tb2 = tk.StringVar()
        dé_mob1 = tk.Button(self.page2,textvariable=self.tb1,
                font=('Arial',15), command=self.alea(1))
        dé_mob2 = tk.Button(self.page2,textvariable=self.tb2,
                font=('Arial',15), command=self.alea(2))

        self.tb1.set('Dé')
        self.tb2.set('Dé')

        dé_mob1.grid(column=0,row=1)
        dé_mob2.grid(column=3,row=1)

        dé_next = tk.Button(self.page2,text='Next',
                font=('Arial',15), command=self.suivant)
        dé_next.grid(column=1,row=4,columnspan=2)

    #dé_suite
    def alea(self,number):
        def rand():
            a = rd.randint(1,6)
            if number == 1:
                self.dé[0]=a
                self.tb1.set(str(self.dé[0]))
            else:
                self.dé[1]=a
                self.tb2.set(str(self.dé[1]))
        return rand

    def suivant(self):
        mob1 = self.mobs_objets[0]
        mob2 = self.mobs_objets[1]

        #Début de tour
        if self.etape == 0:
            self.resultats0.set('')
            self.resultats1.set('')
            self.resultats2.set('Début du tour')
            a = int(mob1.HP) ; b = int(mob2.HP)
            if a < 0 or b < 0:
                self.reboot()

        #Affichae du resultat de l'init
        if self.etape == 1:
            init = initiative(mob1,mob2,self.dé[0],self.dé[1])
            ini_mb = init[3]
            gagnant = init[0]

            self.resultats0.set('Init = '+str(ini_mb[0]))
            self.resultats1.set('Init = '+str(ini_mb[1]))
            self.resultats2.set('Gagnant = '+gagnant.info()['Nom'])

        #Afficher le resultat atk/def
        if self.etape == 2:
            init = initiative(mob1,mob2,self.dé[0],self.dé[1])

            if init[0] == self.mobs_objets[1]: #vérif ordre mob
                self.dé[0],self.dé[1] = self.dé[1],self.dé[0]

            dgt = dgt_applique(init[0],self.dé[0],init[1],self.dé[1],init[2])
            if init[0] == self.mobs_objets[0]:
                self.resultats0.set('Atk ='+str(dgt[1]))
                self.resultats1.set('Def ='+str(dgt[2]))
                self.resultats2.set('Total ='+str(dgt[0]))

            else:
                self.resultats0.set('Def ='+str(dgt[2]))
                self.resultats1.set('Atk ='+str(dgt[1]))
                self.resultats2.set('Total ='+str(dgt[0]))

        #update des hp puis boucle
        if self.etape == 3:
            init = initiative(mob1,mob2,self.dé[0],self.dé[1])

            if init[0] == self.mobs_objets[1]: #vérif ordre mob
                self.dé[0],self.dé[1] = self.dé[1],self.dé[0]
            dgt = dgt_applique(init[0],self.dé[0],init[1],self.dé[1],init[2])
            init[1].modifier_hp(dgt[0])
            self.resultats0.set('')
            self.resultats1.set('')
            if init[0] == mob1:
                self.resultats1.set('-'+str(dgt[0])+'HP')
                self.hp2.set('HP ='+str(self.mobs_objets[1].HP))
            else:
                self.resultats0.set('-'+str(dgt[0])+'HP')
                self.hp1.set('HP ='+str(self.mobs_objets[0].HP))
            self.resultats2.set('Tour suivant')

        self.etape = (self.etape + 1)%4

    def reboot(self):
        #config popup
        self.popup = tk.Tk()
        self.popup.geometry('200x70')
        self.popup.config(background='#CE85F0')
        self.popup.title("Nouveau Combat")
        
        #gestion des objets dans popup
        self.coco = tk.Frame(self.popup,bg='#CE85F0')
        m1 = int(self.mobs_objets[0].HP)
        m2 = int(self.mobs_objets[1].HP)
        if m1 <= 0:
            qui_gagne = tk.Label(self.coco,
                text='Gagnant ='+self.mob_objets[1].info()['Nom'],
                font=('Arial',15),bg='#CE85F0')
        if m2 <= 0:
            qui_gagne = tk.Label(self.coco,
                text='Gagnant ='+self.mobs_objets[0].info()['Nom'],
                font=('Arial',15),bg='#CE85F0')

        boutton_fin = tk.Button(self.coco,text='Nouveau combat',
                font=('Arial',15),bg='#CE85F0',
                command=self.fin_combat)

        #affichage popup
        self.coco.pack(expand=True)
        qui_gagne.pack()
        boutton_fin.pack()

    #Remise a 0 pour un nouveau combat
    def fin_combat(self):
        self.page2.destroy()
        self.coco.destroy()
        self.popup.destroy()
        self.page1 = tk.Frame(self.root, bg='#CE85F0')
        self.gestion_grille(1)
        self.creation_page1()
        self.page1.pack(expand=True)

a = Interface()
a.root.mainloop()
