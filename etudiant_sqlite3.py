import sqlite3

def connexion():
    con = sqlite3.connect('projet.db')
    return con
def creer_database():
    con = connexion()
    req = con.cursor()
    req.execute("CREATE TABLE IF NOT EXISTS `etudiant` (\
                        `idEtudiant` integer PRIMARY KEY AUTOINCREMENT,\
                        `nom` text ,\
                        `prenom` text,\
                        `age` integer ,\
                        `idFiliereFK` integer ,\
                        FOREIGN KEY (`idFiliereFK`) REFERENCES `filiere` (`idFiliere`)\
                        )")
    con.commit()
    con.close()
def afficherEtu():
    con = connexion()
    req = con.cursor()
    sql = "SELECT e.idEtudiant, e.nom, e.prenom, e.age, f.nomFiliere FROM etudiant e JOIN filiere f ON e.idFiliereFK=f.idFiliere ORDER BY e.idEtudiant DESC"
    req.execute(sql)
    con.commit()
    rows = req.fetchall()
    con.close()
    return rows
def ajoutEtu(nom, prenom, age, idFiliereFK):
    con = connexion()
    req = con.cursor()
    sql = "INSERT INTO etudiant(idEtudiant, nom, prenom, age, idFiliereFK) VALUES(?,?,?,?,?)"
    values = (req.lastrowid, nom, prenom, age, idFiliereFK)
    req.execute(sql, values)
    con.commit()
    con.close()
def modifEtu(idEtu, nom, prenom, age, idFK):
    con = connexion()
    req = con.cursor()
    sql = "UPDATE etudiant SET nom=?, prenom=?, age=?, idFiliereFK=? WHERE idEtudiant=?"
    req.execute(sql, (nom, prenom, age, idFK, idEtu))
    con.commit()
    con.close()
def supprimEtu(idEtu):
    con = connexion()
    req = con.cursor()
    sql = "DELETE FROM etudiant WHERE idEtudiant=?"
    req.execute(sql, (idEtu,))
    con.commit()
    con.close()
def existEtu(nom, prenom, age, idflr):
    con = connexion()
    req = con.cursor()
    sql = "SELECT idEtudiant, nom, prenom, age, idFiliereFK FROM etudiant"
    req.execute(sql)
    con.commit()
    rows = req.fetchall()
    con.close()
    idEtu = 0
    for row in rows:
        if row[1] == nom and row[2] == prenom and row[3] == age and row[4] == idflr:
            idEtu = row[0]
            break
    return idEtu

