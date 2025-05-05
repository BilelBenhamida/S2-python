import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog


LIGNES = 6
COLONNES = 7
ALIGNEMENT = 4
MANCHES_GAGNANTES = 3
MODE_IA = False
TAILLE_CASE = 80
COULEUR_VIDE = "white"
COULEUR_JOUEUR1 = "red"
COULEUR_JOUEUR2 = "yellow"

def afficher_menu_principal():
    global menu_frame, jeu_frame
    if 'jeu_frame' in globals():
        jeu_frame.pack_forget()
    menu_frame = tk.Frame(root, bg="#2C3E50")
    menu_frame.pack(expand=True, fill="both")
    titre_frame = tk.Frame(menu_frame, bg="#2C3E50")
    titre_frame.pack(pady=50)
    tk.Label(titre_frame, text="PUISSANCE 4", font=("Arial", 36, "bold"), fg="white", bg="#2C3E50").pack(pady=10)
    boutons_frame = tk.Frame(menu_frame, bg="#2C3E50")
    boutons_frame.pack(pady=20)
    button_style = {"font": ("Arial", 16), "width": 20, "height": 2, "bg": "#3498DB", "fg": "white", "activebackground": "#2980B9", "relief": tk.RAISED, "borderwidth": 3}
    tk.Button(boutons_frame, text="Nouvelle Partie", command=commencer_partie, **button_style).pack(pady=10)
    tk.Button(boutons_frame, text="Charger Partie", command=charger_partie, **button_style).pack(pady=10)
    tk.Button(boutons_frame, text="Quitter", command=root.quit, **button_style).pack(pady=10)


def dessiner_jeton(ligne, colonne):
    centre_x = colonne * TAILLE_CASE + TAILLE_CASE // 2
    centre_y = ligne * TAILLE_CASE + TAILLE_CASE // 2
    rayon = TAILLE_CASE // 2 - 6
   
    if plateau[ligne][colonne] == 1:
        couleurs = {'base': "#FF3333", 'sombre': "#CC0000", 'clair': "#FF6666", 'reflet': "#FF9999", 'bordure': "#880000"}
    else:
        couleurs = {'base': "#FFD700", 'sombre': "#FFA500", 'clair': "#FFEE99", 'reflet': "#FFFFCC", 'bordure': "#DDAA00"}
   
    canvas.create_oval(centre_x - rayon + 2, centre_y - rayon + 2, centre_x + rayon + 2, centre_y + rayon + 2, fill="#333333", outline="", tags="jeton")
   
    etapes = min(rayon, 10)
    for i in range(etapes, 0, -1):
        ratio = i / etapes
        r = rayon * ratio
        couleur = interpoler_couleur(couleurs['sombre'], couleurs['base'], ratio)
        canvas.create_oval(centre_x - r, centre_y - r, centre_x + r, centre_y + r, fill=couleur, outline="", tags="jeton")
   
    for i in range(etapes//2, 0, -1):
        ratio = i / (etapes//2)
        r = (rayon//2) * ratio
        decalage_x = -rayon//4 * (1 - ratio)
        decalage_y = -rayon//4 * (1 - ratio)
        couleur = interpoler_couleur(couleurs['reflet'], couleurs['clair'], ratio)
        canvas.create_oval(centre_x - r + decalage_x, centre_y - r + decalage_y, centre_x + r + decalage_x, centre_y + r + decalage_y, fill=couleur, outline="", tags="jeton")
   
    rayon_reflet = rayon // 3
    canvas.create_oval(centre_x - rayon_reflet, centre_y - rayon_reflet, centre_x + rayon_reflet, centre_y + rayon_reflet, fill=couleurs['reflet'], outline="", tags="jeton")
   
    canvas.create_oval(centre_x - rayon - 1, centre_y - rayon - 1,centre_x + rayon + 1, centre_y + rayon + 1, outline=couleurs['bordure'], width=2, tags="jeton")

def dessiner_plateau():
    canvas.delete("all")
    for ligne in range(LIGNES):
        for colonne in range(COLONNES):
            x1 = colonne * TAILLE_CASE
            y1 = ligne * TAILLE_CASE
            x2 = x1 + TAILLE_CASE
            y2 = y1 + TAILLE_CASE
            intensite_bleu = 200 + (ligne * 5) + (colonne * 2)
            intensite_bleu = min(255, intensite_bleu)
            couleur = f"#1E{intensite_bleu:02x}FF"
            canvas.create_rectangle(x1, y1, x2, y2, fill=couleur, outline="#104E8B", width=2, tags="plateau")
    for ligne in range(LIGNES):
        for colonne in range(COLONNES):
            if plateau[ligne][colonne] != 0:
                dessiner_jeton(ligne, colonne)
    for ligne in range(LIGNES):
        for colonne in range(COLONNES):
            centre_x = colonne * TAILLE_CASE + TAILLE_CASE // 2
            centre_y = ligne * TAILLE_CASE + TAILLE_CASE // 2
            rayon_trou = TAILLE_CASE // 10
            canvas.create_oval(centre_x - rayon_trou, centre_y - rayon_trou, centre_x + rayon_trou, centre_y + rayon_trou, fill="#000000", outline="", tags="plateau")

def afficher_menu_principal():
    global menu_frame, jeu_frame
    if 'jeu_frame' in globals():
        jeu_frame.pack_forget()
    menu_frame = tk.Frame(root, bg="#2C3E50")
    menu_frame.pack(expand=True, fill="both")
    titre_frame = tk.Frame(menu_frame, bg="#2C3E50")
    titre_frame.pack(pady=50)
    tk.Label(titre_frame, text="PUISSANCE 4", font=("Arial", 36, "bold"), fg="white", bg="#2C3E50").pack(pady=10)
    boutons_frame = tk.Frame(menu_frame, bg="#2C3E50")
    boutons_frame.pack(pady=20)
    button_style = {"font": ("Arial", 16), "width": 20, "height": 2, "bg": "#3498DB", "fg": "white", "activebackground": "#2980B9", "relief": tk.RAISED, "borderwidth": 3}
    tk.Button(boutons_frame, text="Nouvelle Partie", command=commencer_partie, **button_style).pack(pady=10)
    tk.Button(boutons_frame, text="Charger Partie", command=charger_partie, **button_style).pack(pady=10)
    tk.Button(boutons_frame, text="Quitter", command=root.quit, **button_style).pack(pady=10)

def clic(event):
    colonne = event.x // TAILLE_CASE
    poser_jeton(colonne)
def commencer_partie():
    '''
    Lance une nouvelle partie.
    '''
    global menu_frame, jeu_frame, canvas, label_scores, ia_button
    global plateau, joueur_actuel, partie_en_cours, historique_coups, premier_joueur_manche
   
    premier_joueur_manche = random.randint(1, 2)
    joueur_actuel = premier_joueur_manche
    menu_frame.pack_forget()
   
    jeu_frame = tk.Frame(root, bg="#2C3E50")
    jeu_frame.pack(expand=True, fill="both")
   
    frame_score = tk.Frame(jeu_frame, bg="#34495E", height=50)
    frame_score.pack(fill=tk.X, pady=5)
   
    label_scores = tk.Label(frame_score, text=f"Joueur 1: {scores[0]}  |  Joueur 2: {scores[1]}  |  Manche: {sum(scores)+1}", font=("Arial", 14, "bold"), fg="white", bg="#34495E")
    label_scores.pack(pady=10)
   
    game_frame = tk.Frame(jeu_frame, bg="#2C3E50")
    game_frame.pack(expand=True)
   
    canvas = tk.Canvas(game_frame, width=COLONNES * TAILLE_CASE, height=LIGNES * TAILLE_CASE, bg="#2C3E50", highlightthickness=0)
    canvas.pack(pady=10)
    canvas.bind("<Button-1>", clic)
   
    button_frame = tk.Frame(jeu_frame, bg="#2C3E50", height=50)
    button_frame.pack(fill=tk.X, pady=5)
   
    button_style = {"font": ("Arial", 12), "width": 15, "bg": "#3498DB", "fg": "white", "activebackground": "#2980B9"}
   
    tk.Button(button_frame, text="Annuler", command=annuler_dernier_coup, **button_style).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Sauvegarder", command=sauvegarder_partie, **button_style).pack(side=tk.LEFT, padx=10)
   
    ia_button = tk.Button(button_frame, text="IA: " + ("ON" if MODE_IA else "OFF"), font=("Arial", 12), width=15, bg="#3498DB" if MODE_IA else "#E74C3C", fg="white", activebackground="#2980B9", command=basculer_mode_ia)
    ia_button.pack(side=tk.LEFT, padx=10)
   
    tk.Button(button_frame, text="Menu", command=retour_au_menu, **button_style).pack(side=tk.RIGHT, padx=10)
   
    initialiser_plateau()
    dessiner_plateau()
   
    if MODE_IA and joueur_actuel == 2:
        root.after(500, jouer_coup_ia)

root = tk.Tk()
root.title("Puissance 4 - Jeu avec jetons 3D")
root.geometry(f"{COLONNES * TAILLE_CASE + 100}x{LIGNES * TAILLE_CASE + 250}")
root.minsize(600, 600)
root.configure(bg="#2C3E50")

import json
import random
import math

plateau = [[0] * COLONNES for _ in range(LIGNES)]
joueur_actuel = 1
partie_en_cours = True
historique_coups = []
scores = [0, 0]
manche_terminee = False
premier_joueur_manche = 1

def interpoler_couleur(couleur1, couleur2, ratio):
    '''
    Crée une couleur intermédiaire entre deux couleurs selon un ratio.
    '''
    r1, g1, b1 = int(couleur1[1:3], 16), int(couleur1[3:5], 16), int(couleur1[5:7], 16)
    r2, g2, b2 = int(couleur2[1:3], 16), int(couleur2[3:5], 16), int(couleur2[5:7], 16)
    r = int(r1 + (r2 - r1) * ratio)
    g = int(g1 + (g2 - g1) * ratio)
    b = int(b1 + (b2 - b1) * ratio)
    return f"#{r:02x}{g:02x}{b:02x}"

def initialiser_plateau():
    '''
    Initialise le plateau de jeu.
    '''
    global plateau, joueur_actuel, partie_en_cours, historique_coups
    plateau = [[0] * COLONNES for _ in range(LIGNES)]
    partie_en_cours = True
    historique_coups = []

def poser_jeton(colonne):
    '''
    Place un jeton dans la colonne spécifiée.
    '''
    global joueur_actuel, partie_en_cours, historique_coups, scores, manche_terminee
   
    if not partie_en_cours or colonne < 0 or colonne >= COLONNES or plateau[0][colonne] != 0:
        return
   
    for ligne in range(LIGNES - 1, -1, -1):
        if plateau[ligne][colonne] == 0:
            plateau[ligne][colonne] = joueur_actuel
            historique_coups.append((ligne, colonne))
           
            if verifier_victoire(ligne, colonne):
                scores[joueur_actuel-1] += 1
                if scores[joueur_actuel-1] >= MANCHES_GAGNANTES:
                    partie_en_cours = False
                    manche_terminee = True
                else:
                    partie_en_cours = False
                    manche_terminee = True
                return
               
            if verifier_match_nul():
                partie_en_cours = False
                manche_terminee = True
                return
               
            joueur_actuel = 3 - joueur_actuel
            return

def verifier_victoire(ligne, colonne):
    '''
    Vérifie si le joueur a gagné.
    '''
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
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
        if compteur >= ALIGNEMENT:
            return True
    return False

def verifier_match_nul():
    '''
    Vérifie s'il y a match nul.
    '''
    return all(plateau[0][colonne] != 0 for colonne in range(COLONNES))

def jouer_coup_ia():
    '''
    Fait jouer l'IA.
    '''
    if not partie_en_cours or joueur_actuel != 2:
        return
    colonnes_valides = [col for col in range(COLONNES) if plateau[0][col] == 0]
    if colonnes_valides:
        colonnes_prioritaires = sorted(colonnes_valides, key=lambda x: abs(x - COLONNES//2))
        colonne = random.choice(colonnes_prioritaires[:max(3, len(colonnes_prioritaires)//2)])
        poser_jeton(colonne)

def sauvegarder_partie():
    '''
    Sauvegarde la partie en cours.
    '''
    etat_partie = {
        "plateau": plateau,
        "joueur_actuel": joueur_actuel,
        "historique_coups": historique_coups,
        "scores": scores,
        "premier_joueur_manche": premier_joueur_manche,
        "lignes": LIGNES,
        "colonnes": COLONNES,
        "alignement": ALIGNEMENT,
        "manches_gagnantes": MANCHES_GAGNANTES,
        "mode_ia": MODE_IA,
        "partie_en_cours": partie_en_cours,
        "manche_terminee": manche_terminee
    }
    with open(fichier, "w") as f:
        json.dump(etat_partie, f)

def charger_partie():
    '''
    Charge une partie sauvegardée.
    '''
    global plateau, joueur_actuel, historique_coups, scores, premier_joueur_manche
    global LIGNES, COLONNES, ALIGNEMENT, MANCHES_GAGNANTES, MODE_IA, partie_en_cours, manche_terminee
   
    with open(fichier, "r") as f:
        etat_partie = json.load(f)
    LIGNES = etat_partie["lignes"]
    COLONNES = etat_partie["colonnes"]
    ALIGNEMENT = etat_partie["alignement"]
    MANCHES_GAGNANTES = etat_partie["manches_gagnantes"]
    MODE_IA = etat_partie.get("mode_ia", False)
    plateau = etat_partie["plateau"]
    joueur_actuel = etat_partie["joueur_actuel"]
    historique_coups = etat_partie["historique_coups"]
    scores = etat_partie["scores"]
    premier_joueur_manche = etat_partie["premier_joueur_manche"]
    partie_en_cours = etat_partie["partie_en_cours"]
    manche_terminee = etat_partie["manche_terminee"]

afficher_menu_principal()
root.mainloop()