from tkinter import *
import  tkinter.messagebox as Mb
from tkinter.ttk import Treeview
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
import etudiant_sqlite3
import filiere_sqlite3

class etudiant_window():
    def __init__(self, master):
        etudiant_sqlite3.creer_database()
        self.master = master
        self.master.title("Etudiant")
        self.master.geometry("1110x430")
        self.master.config(bg="white")
        self.idEtu = StringVar()
        self.etat_stats = 0
        self.master.iconbitmap("images\INSEA_logo.ico")
        #---------------------------Icon&Image-----------------------------
        self.background = Frame(self.master, width=1110, height=330, bg="white").place(x=0, y=100)
        self.hide_stat_icon = Frame(self.master, width=100, height=60, bg="white").place(x=240, y=16)
        
        self.img_stat_hide = PhotoImage(file="images\stats_hide.png")
        self.img_stat_show = PhotoImage(file="images\stats_show.png")
        self.btnStats = Button(self.master, image = self.img_stat_hide, bd=0, bg = 'white', command=self.statistics)
        self.btnStats.place(x=240, y=16)
        #---------------------------Frame & Title-----------------------------
        self.cadreTitle = Frame(self.master, width=955, height=60, bd=10, bg='#63c68d')
        self.cadreTitle.place(x=90, y=100)
        self.title = Label(self.master, text="Les informations des étudiants", font=('sans-serif',20,'bold'), bg='#63c68d').place(x=365, y=110)
        self.listeEtu = LabelFrame(self.master, width=590, height=200, bd=10, bg='#63c68d', font=('sans-serif',9), text="Listes des étudiants")
        self.listeEtu.place(x=456, y=199)
        #----------------------------Label & Entry----------------------------
        self.copy = Label(self.master, text="ZOUHRI Yassine", fg="white", bg="green", font=('sans-serif',7,'bold')).place(x=1030, y=415)
        self.idLabel = Label(self.master, text="       Id :      ", bg='#63c68d', font=('sans-serif',8,'bold')).place(x=90, y=200)
        self.idInput = Entry(self.master, textvariable=self.idEtu, bg='#63c68d', state=DISABLED, width=45)
        self.idInput.place(x=150, y=200)
        self.lastname = Label(self.master, text="    Nom :    ", bg='#63c68d', font=('sans-serif',8,'bold')).place(x=90, y=230)
        self.lNInput = Entry(self.master, width=45)
        self.lNInput.focus()
        self.lNInput.place(x=150, y=230)
        self.firstname = Label(self.master, text=" Prénom : ", bg='#63c68d', font=('sans-serif',8,'bold')).place(x=90, y=260)
        self.fNInput = Entry(self.master, width=45)
        self.fNInput.place(x=150, y=260)
        self.age = Label(self.master, text="     Âge :     ", bg='#63c68d', font=('sans-serif',8,'bold')).place(x=90, y=290)
        self.ageInput = Entry(self.master, width=45)
        self.ageInput.place(x=150, y=290)
        self.default = StringVar()
        self.default.set("sélectionnez")
        self.filiere = Label(self.master, text="   Filière :  ", bg='#63c68d', font=('sans-serif',8,'bold')).place(x=90, y=320)
        self.filInput = OptionMenu(self.master, self.default, *filiere_sqlite3.getFilNom())
        self.filInput.config(width=39)
        self.filInput.place(x=150, y=320)
        #---------------------------Scrollbar & List--------------------------
        self.trview_etu = Treeview(self.listeEtu, columns=('id', 'nom', 'prenom', 'age', 'filiere'),show='headings', selectmode=EXTENDED, height=7)
        self.trview_etu.place(x=0, y=0)
        self.trview_etu.heading('id', text='Id étudiant')
        self.trview_etu.heading('nom', text='Nom')
        self.trview_etu.heading('prenom', text='Prénom')
        self.trview_etu.heading('age', text='Âge')
        self.trview_etu.heading('filiere', text='Filière')
        self.trview_etu.column('id', anchor=CENTER, width=70)
        self.trview_etu.column('nom', anchor=CENTER, width=75)
        self.trview_etu.column('prenom', anchor=CENTER, width=75)
        self.trview_etu.column('age', anchor=CENTER, width=60)
        self.trview_etu.column('filiere', anchor=CENTER, width=267)
        self.scroll_etu = Scrollbar(self.listeEtu,orient=VERTICAL,command=self.trview_etu.yview)
        self.scroll_etu.place(x=550, y=0, height=167)
        self.trview_etu.bind('<ButtonRelease-1>', self.selection_etudiant)
        self.trview_etu.configure(yscrollcommand=self.scroll_etu.set)
        #-------------------------------Button--------------------------------
        self.save = Button(self.master, text="Enregistrer", font=('sans-serif',10,'bold'), fg='white', bg="green", command=self.ajouter)
        self.save.place(x=90, y=370)
        self.reset = Button(self.master, text="Initialiser", font=('sans-serif',10,'bold'), bg="#63c68d", fg="#024f22", command=self.initialiser)
        self.reset.place(x=185, y=370)
        self.edit = Button(self.master, text="Modifier", font=('sans-serif',10,'bold'), fg='green', bg="lightgray", state=DISABLED, command=self.modifier)
        self.edit.place(x=270, y=370)
        self.delete = Button(self.master, text="Supprimer", font=('sans-serif',10,'bold'), fg='red', bg="lightgray", state=DISABLED, command=self.supprimer)
        self.delete.place(x=350, y=370)
        self.afficher()
        self.background = Frame(self.master, width=1010, height=430)
        self.master.mainloop()
    #-----------------------------------Function------------------------------
    def afficher(self):
        self.trview_etu.delete(*self.trview_etu.get_children())
        for row in etudiant_sqlite3.afficherEtu():
            self.trview_etu.insert("", END, values=row)
        self.initialiser()   
    def ajouter(self):
        ln = self.lNInput.get()
        fn = self.fNInput.get()
        try:
            age = float(self.ageInput.get())
        except:
            self.ageInput.delete(0, END)
            self.ageInput.focus()
            Mb.showwarning("Erreur de modification","Le champ âge doit être numérique !", parent=self.master)
        flr = self.default.get()
        if ln == "" or fn == "" or age == "" or flr == "sélectionnez":
            Mb.showwarning("Erreur d'insertion","Tous les champs sont obligatoires", parent=self.master)
        else:
            idfil = filiere_sqlite3.getFilId(flr)[0][0]
            idEtu_check = etudiant_sqlite3.existEtu(ln, fn, int(age), int(idfil))
            if idEtu_check == 0 :
                etudiant_sqlite3.ajoutEtu(ln, fn, age, idfil)
                self.afficher()
                self.initialiser()
            else:
                self.idEtu.set(idEtu_check)
                self.basculer(NORMAL)
                Mb.showinfo("Erreur d'insertion","Cet étudiant existe déjà !", parent=self.master)
                self.lNInput.focus()
    def modifier(self):
        ln = self.lNInput.get()
        fn = self.fNInput.get()
        try:
            age = float(self.ageInput.get())
        except:
            self.ageInput.delete(0, END)
            self.ageInput.focus()
            Mb.showwarning("Erreur de modification","Le champ âge doit être numérique !", parent=self.master)
        flr = self.default.get()
        if ln == "" or fn == "" or age == "" or flr == "sélectionnez":
            Mb.showwarning("Erreur de modification","Tous les champs sont obligatoires", parent=self.master)
        else:
            idfil = filiere_sqlite3.getFilId(flr)[0][0]
            idEtu_check = etudiant_sqlite3.existEtu(ln, fn, age, int(idfil))
            if idEtu_check == 0 :
                etudiant_sqlite3.modifEtu(self.idEtu.get(), ln, fn, age, idfil)
                self.afficher()
                self.initialiser()
            else:
                self.idEtu.set(idEtu_check)
                self.basculer(NORMAL)
                Mb.showinfo("Erreur de modification","Cet étudiant existe déjà !", parent=self.master)
                self.lNInput.focus()
    def supprimer(self):
        if Mb.askyesno("Etudiant","Voulez-vous vraiment supprimer cet étudiant ?", parent=self.master) > 0:
            etudiant_sqlite3.supprimEtu(self.idEtu.get())
            self.afficher()
            self.initialiser()
    def initialiser(self):
        self.lNInput.delete(0, 'end')
        self.fNInput.delete(0, 'end')
        self.ageInput.delete(0, 'end')
        self.default.set("sélectionnez")
        self.idEtu.set("")
        self.basculer(DISABLED)
        self.lNInput.focus()
        if self.etat_stats == 1:
            self.stats_destroy()
    def selection_etudiant(self, event):
        etu = self.trview_etu.item(self.trview_etu.selection())['values']
        self.idEtu.set(etu[0])
        self.lNInput.delete(0, 'end')
        self.lNInput.insert('end', etu[1])
        self.lNInput.focus()
        self.fNInput.delete(0, 'end')
        self.fNInput.insert('end', etu[2])
        self.ageInput.delete(0, 'end')
        self.ageInput.insert('end', etu[3])
        self.default.set("sélectionnez")
        self.default.set(etu[4])
        self.basculer(NORMAL)
    def basculer(self, action):
        if action == NORMAL:
            color = ['#c3f8da', '#f7dadf']
            self.save.config(state=DISABLED, bg='lightgray')
        else:
            self.save.config(state=NORMAL, bg='green')
            color = ['lightgray', 'lightgray']
        self.edit.config(state=action, bg=color[0])
        self.delete.config(state=action, bg=color[1])
    def statistics(self):
        donnees = filiere_sqlite3.stats_donnees()
        if len(donnees) > 0:
            if self.etat_stats == 0: 
                self.etat_stats = 1  
                self.btnStats.config(image=self.img_stat_show) 
                fig = plt.figure(figsize=(6,2))
                ax = fig.add_subplot(111)
                self.stats_canvas = FigureCanvasTkAgg(fig, self.master)
                self.stats_canvas.get_tk_widget().place(x=456, y=199)
                fil_abs = []
                for donnee in donnees:
                    nom_abs = ''
                    for fil_nom in donnee[0].split():
                        if len(fil_nom) > 2 :
                            for word1 in fil_nom.split('-'):
                                for word2 in word1.split('&'):
                                    if len(word2) == 3:
                                        nom_abs += word2[0]
                                    else:
                                        nom_abs += word2[0].upper()
                    if nom_abs != '':
                        fil_abs.append(nom_abs) 
                countEtu = [donnee[1] for donnee in donnees]
                ax.bar(fil_abs, countEtu, color='g')
                ax.set_title('Nombre des étudiants par filière')
            else:
                self.stats_destroy()
        else:
            Mb.showinfo('Étudiant et filières','Personne n\'est encore inscrit !')
    def stats_destroy(self):
        self.etat_stats = 0
        self.btnStats.config(image=self.img_stat_hide) 
        self.stats_canvas.get_tk_widget().destroy()
    def sortir(self):
        self.isortir = Mb.askyesno("Listes des étudiants et leurs filières","Voulez-vous vraiment sortir ?", parent=self.master)
        if self.isortir > 0:
            self.master.destroy()
            return