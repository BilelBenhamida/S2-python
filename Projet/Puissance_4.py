import tkinter as tk
from tkinter import messagebox

LIGNES = 6
COLONNES = 7
TAILLE_CASE = 80
COULEUR_VIDE = "white"
COULEUR_JOUEUR1 = "red"
COULEUR_JOUEUR2 = "yellow"
plateau = [[0] * COLONNES for _ in range(LIGNES)]
joueur_actuel = 1
partie_en_cours = True
historique_coups = []

def afficher_menu_principal():
    global menu_frame, jeu_frame
    if 'jeu_frame' in globals():
        jeu_frame.pack_forget()
    menu_frame = tk.Frame(root, width=COLONNES * TAILLE_CASE, height=LIGNES * TAILLE_CASE + 100)
    menu_frame.pack(pady=50)
    titre = tk.Label(menu_frame, text="PUISSANCE 4", font=("Arial", 24, "bold"))
    titre.pack(pady=20)
    bouton_start = tk.Button(menu_frame, text="Start", font=("Arial", 16), command=commencer_partie)
    bouton_start.pack(pady=10)

def commencer_partie():
    global menu_frame, jeu_frame, canvas, bouton_annuler, bouton_sauvegarder, bouton_retour_menu
    menu_frame.pack_forget()
    jeu_frame = tk.Frame(root)
    jeu_frame.pack()
    canvas = tk.Canvas(jeu_frame, width=COLONNES * TAILLE_CASE, height=LIGNES * TAILLE_CASE, bg="blue")
    canvas.pack()
    canvas.bind("<Button-1>", clic)
    bouton_annuler = tk.Button(jeu_frame, text="Annuler", font=("Arial", 14), command=annuler_dernier_coup)
    bouton_annuler.pack(pady=5)
    #bouton_sauvegarder = tk.Button(jeu_frame, text="Sauvegarder", font=("Arial", 14), command=sauvegarder_partie)
    #bouton_sauvegarder.pack(pady=5)
    bouton_retour_menu = tk.Button(jeu_frame, text="Retour au menu", font=("Arial", 14), command=retour_au_menu)
    bouton_retour_menu.pack(pady=5)
    if not hasattr(commencer_partie, 'partie_chargee'):
        initialiser_plateau()
    commencer_partie.partie_chargee = False

def retour_au_menu():
    global jeu_frame
    jeu_frame.pack_forget()
    afficher_menu_principal()

def initialiser_plateau():
    global plateau, joueur_actuel, partie_en_cours, historique_coups
    plateau = [[0] * COLONNES for _ in range(LIGNES)]
    joueur_actuel = 1
    partie_en_cours = True
    historique_coups = []
    dessiner_plateau()

def dessiner_plateau():
    canvas.delete("all")
    for ligne in range(LIGNES):
        for colonne in range(COLONNES):
            x1 = colonne * TAILLE_CASE
            y1 = ligne * TAILLE_CASE
            x2 = x1 + TAILLE_CASE
            y2 = y1 + TAILLE_CASE
            couleur = COULEUR_VIDE
            if plateau[ligne][colonne] == 1:
                couleur = COULEUR_JOUEUR1
            elif plateau[ligne][colonne] == 2:
                couleur = COULEUR_JOUEUR2
            canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill=couleur, outline="black")

def poser_jeton(colonne):
    global joueur_actuel, partie_en_cours, historique_coups
    if not partie_en_cours:
        return
    for ligne in range(LIGNES - 1, -1, -1):
        if plateau[ligne][colonne] == 0:
            plateau[ligne][colonne] = joueur_actuel
            historique_coups.append((ligne, colonne))
            dessiner_plateau()
            if verifier_victoire(ligne, colonne):
                messagebox.showinfo("Fin de partie", f"Le joueur {joueur_actuel} a gagné !")
                partie_en_cours = False
                return
            joueur_actuel = 3 - joueur_actuel
            return

def annuler_dernier_coup():
    global joueur_actuel, historique_coups
    if not historique_coups:
        return
    dernier_coup = historique_coups.pop()
    ligne, colonne = dernier_coup
    plateau[ligne][colonne] = 0
    joueur_actuel = 3 - joueur_actuel
    dessiner_plateau()

def verifier_victoire(ligne, colonne):
    directions = [
        (1, 0),
        (0, 1),
        (1, 1),
        (1, -1)]
    for dx, dy in directions:
        compteur = 1
        x, y = ligne + dx, colonne + dy
        while 0 <= x < LIGNES and 0 <= y < COLONNES and plateau[x][y] == plateau[ligne][colonne]:
            compteur += 1
            x += dx
            y += dy
        x, y = ligne - dx, colonne - dy
        while 0 <= x < LIGNES and 0 <= y < COLONNES and plateau[x][y] == plateau[ligne][colonne]:
            compteur += 1
            x -= dx
            y -= dy
        if compteur >= 4:
            return True
    return False

def clic(event):
    colonne = event.x // TAILLE_CASE
    poser_jeton(colonne)

root = tk.Tk()
root.title("Puissance 4")
root.geometry(f"{COLONNES * TAILLE_CASE}x{LIGNES * TAILLE_CASE + 150}")

afficher_menu_principal()

root.mainloop()