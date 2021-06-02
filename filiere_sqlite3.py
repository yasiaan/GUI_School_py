import sqlite3

def connexion():
    con = sqlite3.connect('projet.db')
    return con
def creer_database():
    con = connexion()
    req = con.cursor()
    req.execute("CREATE TABLE IF NOT EXISTS `filiere` (\
                        `idFiliere` integer PRIMARY KEY AUTOINCREMENT,\
                        `nomFiliere` text\
                        )")
    con.commit()
    con.close()
def afficherFil():
    con = connexion()
    req = con.cursor()
    req.execute("SELECT * FROM filiere ORDER BY idFiliere DESC")
    con.commit()
    rows = req.fetchall()
    con.close()
    return rows
def ajoutFil(nom):
    con = connexion()
    req = con.cursor()
    sql = "INSERT INTO filiere(nomFiliere) VALUES(?)"
    req.execute(sql, (nom,))
    con.commit()
    con.close()
def modifFil(idFil, nom):
    con = connexion()
    req = con.cursor()
    sql = "UPDATE filiere SET nomFiliere=? WHERE idFiliere=?"
    req.execute(sql, (nom, idFil))
    con.commit()
    con.close()
def checkEtu(idFil):
    con = connexion()
    req = con.cursor()
    sql = "SELECT nom FROM etudiant WHERE idFiliereFK=?"
    req.execute(sql, (idFil,))
    con.commit()
    rows = req.fetchall()
    con.close()
    return rows
def supprimFil(idFil):
    con = connexion()
    req = con.cursor()
    sql = "DELETE FROM filiere WHERE idFiliere=?"
    req.execute(sql, (idFil,))
    con.commit()
    con.close()
def getFilId(nom):
    con = connexion()
    req = con.cursor()
    req.execute("SELECT idFiliere FROM filiere WHERE nomFiliere=?",(nom,))
    con.commit()
    row = req.fetchall()
    con.close()
    return row
def getFilNom():
    con = connexion()
    req = con.cursor()
    req.execute("SELECT nomFiliere FROM filiere")
    con.commit()
    rows = req.fetchall()
    con.close()
    nomList = [row[0] for row in rows]
    if len(nomList) == 0:
        nomList = ['sélectionnez']
    return nomList
def existFil(nom):
    con = connexion()
    req = con.cursor()
    sql = "SELECT * FROM filiere"
    req.execute(sql)
    con.commit()
    rows = req.fetchall()
    con.close()
    idFil = 0
    for row in rows:
        if row[1] == nom:
            idFil = row[0]
            break
    return idFil
def stats_donnees():
    con = connexion()
    req = con.cursor()
    sql = "SELECT f.nomFiliere, count(e.nom) \
            FROM etudiant e\
            JOIN filiere f\
            ON e.idFiliereFK=f.idFiliere\
            GROUP BY e.idFiliereFK"
    req.execute(sql)
    con.commit()
    rows = req.fetchall()
    return rows