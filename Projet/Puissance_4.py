import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import json
import random
import math

LIGNES = 6
COLONNES = 7
ALIGNEMENT = 4
TAILLE_CASE = 80
COULEUR_VIDE = "white"
COULEUR_JOUEUR1 = "red"
COULEUR_JOUEUR2 = "yellow"

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
    tk.Button(boutons_frame, text="Paramètres", command=afficher_parametres, **button_style).pack(pady=10)
    tk.Button(boutons_frame, text="Charger Partie", command=charger_partie, **button_style).pack(pady=10)
    tk.Button(boutons_frame, text="Quitter", command=root.quit, **button_style).pack(pady=10)

def clic(event):
    '''
    Gère le clic de souris.
    '''
    colonne = event.x // TAILLE_CASE
    poser_jeton(colonne)

root = tk.Tk()
root.title("Puissance 4 - Jeu avec jetons 3D")
root.geometry(f"{COLONNES * TAILLE_CASE + 100}x{LIGNES * TAILLE_CASE + 250}")
root.minsize(600, 600)
root.configure(bg="#2C3E50")

afficher_menu_principal()

root.mainloop()