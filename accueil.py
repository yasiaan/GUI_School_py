from tkinter import *
import  tkinter.messagebox as Mb
import mysql.connector as mysql
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from etudiant_window import *
from filiere_window import *
import etudiant_sqlite3
import filiere_sqlite3

class accueil():
    def __init__(self, master):
        self.master = master
        self.master.config(bg="white")
        self.master.title("Listes des étudiants et leurs filières")
        self.master.geometry("1110x430")
        self.master.iconbitmap("images\INSEA_logo.ico")
        self.etat_stats = 0
        #---------------------------Icon&Image-----------------------------
        self.background = Frame(self.master, width=1110, height=330, bg="white").place(x=0, y=100)
        self.hide_stat_icon = Frame(self.master, width=100, height=60, bg="white").place(x=240, y=16)
        self.imageLabel = Label(self.master)
        img = PhotoImage(file="images\INSEA_logo.png")
        self.imageLabel.config(bg="white", image=img)
        self.imageLabel.image = img
        self.imageLabel.place(x=520, y=10) 

        self.img_accueil = PhotoImage(file="images\Redirect_accueil.png")
        self.btnAccueil = Button(self.master, image = self.img_accueil, bd=0, bg = 'white', command=self.acc_window)
        self.btnAccueil.place(x=90, y=19)

        self.img_fil = PhotoImage(file="images\Redirect_fil.png")
        self.btnFil = Button(self.master, image = self.img_fil, bd=0, bg = 'white', command=self.fili_window)
        self.btnFil.place(x=140, y=16)

        self.img_etu = PhotoImage(file="images\Redirect_etu.png")
        self.btnEtu = Button(self.master, image = self.img_etu, bd=0, bg = 'white', command=self.etud_window)
        self.btnEtu.place(x=190, y=16)

        self.imageFilLabel = Label(self.master)
        imgFil = PhotoImage(file="images\Filiere.png")
        self.imageFilLabel.config(bg="white", image=imgFil)
        self.imageFilLabel.image = imgFil
        self.imageFilLabel.place(x=700, y=150) 

        self.imageEtuLabel = Label(self.master)
        imgEtu = PhotoImage(file="images\Etudiant.png")
        self.imageEtuLabel.config(bg="white", image=imgEtu)
        self.imageEtuLabel.image = imgEtu
        self.imageEtuLabel.place(x=300, y=150)

        img_sortir = PhotoImage(file="images\sortir.png")
        self.btnSortir = Button(self.master, image = img_sortir, bd=0, bg = 'white', command=self.sortir).place(x=1010, y=14)
        #-----------------------------Button&Label----------------------------
        self.project = Label(self.master, text="ZOUHRI Yassine", fg="white", bg="green", font=('sans-serif',7,'bold'))
        self.project.place(x=1030, y=415)
        self.btnEtudiant = Button(self.master, width=16, height=2, text="Liste des étudiants", bg="#63c68d", fg="#024f22", font=('sans-serif',8,'bold'), command=self.etud_window)
        self.btnEtudiant.place(x=300, y=320)
        self.btnFiliere = Button(self.master, width=16, height=2, text="Liste des filières", bg="#63c68d", fg="#024f22", font=('sans-serif',8,'bold'), command=self.fili_window)
        self.btnFiliere.place(x=700, y=320)
        self.statistics()
        self.master.mainloop()
    #-----------------------------------Function------------------------------
    def etud_window(self):
        self.stats_destroy()
        self.master = etudiant_window(self.master)
    def fili_window(self):
        self.stats_destroy()
        self.master = filiere_window(self.master)
    def acc_window(self):
        self.stats_destroy()
        self.master = accueil(self.master)
    def statistics(self):
        donnees = filiere_sqlite3.stats_donnees()
        if len(donnees) > 0:
            self.etat_stats = 1
            fig = plt.figure(figsize=(5,2))
            ax = fig.add_subplot(111)
            self.stats_canvas = FigureCanvasTkAgg(fig, self.master)
            self.btnEtudiant.place(x=150, y=320)
            self.imageEtuLabel.place(x=150, y=150) 
            self.btnFiliere.place(x=850, y=320)
            self.imageFilLabel.place(x=850, y=150) 
            self.stats_canvas.get_tk_widget().place(x=310, y=150)
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
    def stats_destroy(self):
        try:
            if self.etat_stats == 1:
                self.stats_canvas.get_tk_widget().destroy()
        except:
            pass
    def sortir(self):
        self.isortir = Mb.askyesno("Listes des étudiants et leurs filières","Voulez-vous vraiment sortir ?")
        if self.isortir > 0:
            self.master.destroy()
            return
    

if __name__ == '__main__':
    etudiant_sqlite3.creer_database()
    filiere_sqlite3.creer_database()
    root = Tk()
    app = accueil(root)
