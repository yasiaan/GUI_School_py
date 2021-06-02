from tkinter import *
import  tkinter.messagebox as Mb
from tkinter.ttk import Treeview
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
import filiere_sqlite3

class filiere_window():
    def __init__(self, master):
        filiere_sqlite3.creer_database()
        self.master = master
        self.master.title("Filières")
        self.master.geometry("1110x430")
        self.master.config(bg="white")
        self.master.iconbitmap("images\INSEA_logo.ico")
        self.idFil = StringVar()
        self.etat_stats = 0
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
        self.title = Label(self.master, text="Les informations des filières", font=('sans-serif',20,'bold'), bg='#63c68d').place(x=365, y=110)
        self.listeFil = LabelFrame(self.master, width=520, height=200, bd=10, bg='#63c68d', font=('sans-serif',9), text="Listes des filières")
        self.listeFil.place(x=526, y=199)
        #----------------------------Label & Entry----------------------------
        self.copy = Label(self.master, text="ZOUHRI Yassine", fg="white", bg="green", font=('sans-serif',7,'bold')).place(x=1030, y=415)
        self.id = Label(self.master, text="   Id de la Filière :   ", bg='#63c68d', font=('sans-serif',8,'bold')).place(x=90, y=202)
        self.idInput = Entry(self.master, textvariable=self.idFil, state=DISABLED, width=44)
        self.idInput.place(x=195, y=202)
        self.flrname = Label(self.master, text="Nom de la Filière : ", bg='#63c68d', font=('sans-serif',8,'bold')).place(x=90, y=270)
        self.flrInput = Entry(self.master, width=44)
        self.flrInput.focus()
        self.flrInput.place(x=195, y=270)
        #---------------------------Scrollbar & List--------------------------
        self.trview_fil = Treeview(self.listeFil, columns=('id', 'nom'),show='headings', selectmode=EXTENDED, height=7)
        self.trview_fil.place(x=0, y=0)
        self.trview_fil.heading('id', text='Id filière')
        self.trview_fil.heading('nom', text='Nom filière')
        self.trview_fil.column('id', anchor=CENTER, width=110)
        self.trview_fil.column('nom', anchor=CENTER, width=367)
        self.scroll_fl = Scrollbar(self.listeFil,orient=VERTICAL,command=self.trview_fil.yview)
        self.scroll_fl.place(x=480, y=0, height=167)
        self.trview_fil.bind('<ButtonRelease-1>', self.selection_filiere)
        self.trview_fil.configure(yscrollcommand=self.scroll_fl.set)
        #-------------------------------Button--------------------------------
        self.save = Button(self.master, text="Enregistrer", font=('sans-serif',10,'bold'), fg='white', bg="green", command=self.ajouter)
        self.save.place(x=90, y=370)
        self.reset = Button(self.master, text="Initialiser", font=('sans-serif',10,'bold'), bg="#63c68d", fg="#024f22", command=self.initialiser)
        self.reset.place(x=195, y=370)
        self.edit = Button(self.master, text="Modifier", font=('sans-serif',10,'bold'), fg='green', bg="lightgray", state=DISABLED, command=self.modifier)
        self.edit.place(x=295, y=370)
        self.delete = Button(self.master, text="Supprimer", font=('sans-serif',10,'bold'), fg='red', bg="lightgray", state=DISABLED, command=self.supprimer)
        self.delete.place(x=385, y=370)
        self.afficher()
        self.master.mainloop()
    #----------------------------Function----------------------------
    def afficher(self):
        self.trview_fil.delete(*self.trview_fil.get_children())
        for row in filiere_sqlite3.afficherFil():
            self.trview_fil.insert("", END, values=row)
        self.initialiser()
    def ajouter(self):
        flr = self.flrInput.get()
        if flr == "":
            Mb.showwarning("Error d'insertion","Tous les champs sont obligatoires", parent=self.master)
        else:
            idFil_check = filiere_sqlite3.existFil(flr)
            if idFil_check == 0:
                filiere_sqlite3.ajoutFil(flr)
                self.afficher()
                self.initialiser()
            else:
                self.idFil.set(idFil_check)
                self.basculer(NORMAL)
                Mb.showinfo("Erreur d'insertion","Cette filière existe déjà !", parent=self.master)
                self.flrInput.focus()
    def modifier(self):
        flr = self.flrInput.get()
        if flr == "":
            Mb.showwarning("Error de modification","Tous les champs sont obligatoires", parent=self.master)
        else:
            idFil_check = filiere_sqlite3.existFil(flr)
            if idFil_check == 0:
                filiere_sqlite3.modifFil(self.idFil.get(), flr)
                self.afficher()
                self.initialiser()
            else:
                self.idFil.set(idFil_check)
                self.basculer(NORMAL)
                Mb.showinfo("Erreur de modification","Cette filière existe déjà !", parent=self.master)
                self.flrInput.focus()
    def supprimer(self):
        if Mb.askyesno("Filière","Voulez-vous vraiment supprimer cette filière ?", parent=self.master) > 0:
            if len(filiere_sqlite3.checkEtu(self.idFil.get())):
                Mb.showwarning("Erreur de suppression","Vous ne pouvez pas supprimer cette filière.\nIl y a déjà des étudiants inscrits.", parent=self.master)
            else:
                filiere_sqlite3.supprimFil(self.idFil.get())
                self.afficher()
                self.initialiser()
    def initialiser(self):
        self.flrInput.delete(0, 'end')
        self.idFil.set("")
        self.basculer(DISABLED)
        self.flrInput.focus()
        if self.etat_stats == 1:
            self.stats_destroy()
    def selection_filiere(self, event):
        fil = self.trview_fil.item(self.trview_fil.selection())['values']
        self.idFil.set(fil[0])
        self.flrInput.delete(0, 'end')
        self.flrInput.insert('end', fil[1])
        self.flrInput.focus()
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
                self.stats_canvas.get_tk_widget().place(x=476, y=199)
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