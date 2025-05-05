import tkinter as tk
from tkinter import messagebox

LIGNES = 6
COLONNES = 7
ALIGNEMENT = 4
TAILLE_CASE = 80
COULEUR_VIDE = "white"
COULEUR_JOUEUR1 = "red"
COULEUR_JOUEUR2 = "yellow"
MANCHES_GAGNANTES = 3
MODE_IA = False

plateau = [[0] * COLONNES for _ in range(LIGNES)]
joueur_actuel = 1
partie_en_cours = True
historique_coups = []
scores = [0, 0]
manche_terminee = False
premier_joueur_manche = 1

def interpoler_couleur(couleur1, couleur2, ratio):
    r1, g1, b1 = int(couleur1[1:3], 16), int(couleur1[3:5], 16), int(couleur1[5:7], 16)
    r2, g2, b2 = int(couleur2[1:3], 16), int(couleur2[3:5], 16), int(couleur2[5:7], 16)
    r = int(r1 + (r2 - r1) * ratio)
    g = int(g1 + (g2 - g1) * ratio)
    b = int(b1 + (b2 - b1) * ratio)
    return f"#{r:02x}{g:02x}{b:02x}"

def animer_victoire_manche(joueur):
    couleur = COULEUR_JOUEUR1 if joueur == 1 else COULEUR_JOUEUR2
    barre_victoire = tk.Canvas(jeu_frame, width=0, height=10, bg=couleur, highlightthickness=0)
    barre_victoire.place(relx=0.5, rely=0.92, anchor=tk.CENTER)
    
    def animer():
        width = barre_victoire.winfo_width()
        if width < COLONNES * TAILLE_CASE:
            barre_victoire.config(width=width + 20)
            barre_victoire.after(20, animer)
        else:
            barre_victoire.after(1000, lambda: barre_victoire.destroy())
    animer()

def animer_jetons_gagnants(ligne, colonne):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    jetons_gagnants = []
    for dx, dy in directions:
        jetons = [(ligne, colonne)]
        x, y = ligne + dx, colonne + dy
        while 0 <= x < LIGNES and 0 <= y < COLONNES and plateau[x][y] == plateau[ligne][colonne]:
            jetons.append((x, y))
            x += dx
            y += dy
        x, y = ligne - dx, colonne - dy
        while 0 <= x < LIGNES and 0 <= y < COLONNES and plateau[x][y] == plateau[ligne][colonne]:
            jetons.append((x, y))
            x -= dx
            y -= dy
        if len(jetons) >= ALIGNEMENT:
            jetons_gagnants = jetons[:ALIGNEMENT]
            break
    if not jetons_gagnants:
        return False
    def clignoter(compteur):
        if compteur < 6:
            for l, c in jetons_gagnants:
                x1 = c * TAILLE_CASE + 5
                y1 = l * TAILLE_CASE + 5
                x2 = x1 + TAILLE_CASE - 10
                y2 = y1 + TAILLE_CASE - 10
                if compteur % 2 == 0:
                    canvas.create_oval(x1, y1, x2, y2, fill="white", outline="gold", width=3, tags="clignote")
                else:
                    dessiner_jeton(l, c)
            canvas.after(300, lambda: clignoter(compteur + 1))
        else:
            canvas.delete("clignote")
            dessiner_plateau()
            commencer_nouvelle_manche()
    clignoter(0)
    return True
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
def basculer_mode_ia():
    global MODE_IA
    MODE_IA = not MODE_IA
    for widget in jeu_frame.winfo_children():
        if isinstance(widget, tk.Frame):
            for btn in widget.winfo_children():
                if isinstance(btn, tk.Button) and "IA: " in btn.cget("text"):
                    btn.config(text="IA: " + ("ON" if MODE_IA else "OFF"),
                             bg="#3498DB" if MODE_IA else "#E74C3C")
    if MODE_IA and joueur_actuel == 2 and partie_en_cours:
        jouer_coup_ia()
def afficher_parametres():
    fenetre_parametres = tk.Toplevel(root)
    fenetre_parametres.title("Paramètres du jeu")
    fenetre_parametres.resizable(False, False)
    style_label = {"font": ("Arial", 12), "padx": 10, "pady": 5}
    style_entry = {"font": ("Arial", 12), "width": 5}
    tk.Label(fenetre_parametres, text="Nombre de lignes:", **style_label).grid(row=0, column=0)
    entry_lignes = tk.Entry(fenetre_parametres, **style_entry)
    entry_lignes.insert(0, str(LIGNES))
    entry_lignes.grid(row=0, column=1)
    tk.Label(fenetre_parametres, text="Nombre de colonnes:", **style_label).grid(row=1, column=0)
    entry_colonnes = tk.Entry(fenetre_parametres, **style_entry)
    entry_colonnes.insert(0, str(COLONNES))
    entry_colonnes.grid(row=1, column=1)
    tk.Label(fenetre_parametres, text="Jetons à aligner:", **style_label).grid(row=2, column=0)
    entry_alignement = tk.Entry(fenetre_parametres, **style_entry)
    entry_alignement.insert(0, str(ALIGNEMENT))
    entry_alignement.grid(row=2, column=1)
    tk.Label(fenetre_parametres, text="Manches à gagner:", **style_label).grid(row=3, column=0)
    entry_manches = tk.Entry(fenetre_parametres, **style_entry)
    entry_manches.insert(0, str(MANCHES_GAGNANTES))
    entry_manches.grid(row=3, column=1)
    var_mode_ia = tk.BooleanVar(value=MODE_IA)
    tk.Checkbutton(fenetre_parametres, text="Jouer contre IA", variable=var_mode_ia, font=("Arial", 12)).grid(row=4, column=0, columnspan=2, pady=5)
    def appliquer_parametres():
        global LIGNES, COLONNES, ALIGNEMENT, MANCHES_GAGNANTES, MODE_IA
        try:
            new_lignes = int(entry_lignes.get())
            new_colonnes = int(entry_colonnes.get())
            new_alignement = int(entry_alignement.get())
            new_manches = int(entry_manches.get())
            if new_lignes < 4 or new_colonnes < 4 or new_alignement < 2:
                raise ValueError("Les valeurs doivent être supérieures à 3 (2 pour l'alignement)")
            LIGNES = new_lignes
            COLONNES = new_colonnes
            ALIGNEMENT = new_alignement
            MANCHES_GAGNANTES = new_manches
            MODE_IA = var_mode_ia.get()
            messagebox.showinfo("Succès", "Paramètres enregistrés avec succès !")
            fenetre_parametres.destroy()
        except ValueError as e:
            messagebox.showerror("Erreur", f"Valeurs invalides: {str(e)}")
    tk.Button(fenetre_parametres, text="Appliquer", command=appliquer_parametres, font=("Arial", 12), bg="#27AE60", fg="white").grid(row=5, columnspan=2, pady=10)
def commencer_partie():
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
    tk.Button(button_frame, text="Charger", command=charger_partie, **button_style).pack(side=tk.LEFT, padx=10)
    ia_button = tk.Button(button_frame, text="IA: " + ("ON" if MODE_IA else "OFF"), font=("Arial", 12), width=15, bg="#3498DB" if MODE_IA else "#E74C3C", fg="white", activebackground="#2980B9", command=basculer_mode_ia)
    ia_button.pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Menu", command=retour_au_menu, **button_style).pack(side=tk.RIGHT, padx=10)
    initialiser_plateau()
    dessiner_plateau()
    if MODE_IA and joueur_actuel == 2:
        root.after(500, jouer_coup_ia)
def initialiser_plateau():
    global plateau, joueur_actuel, partie_en_cours, historique_coups
    plateau = [[0] * COLONNES for _ in range(LIGNES)]
    partie_en_cours = True
    historique_coups = []
    dessiner_plateau()
def poser_jeton(colonne):
    global joueur_actuel, partie_en_cours, historique_coups, scores, manche_terminee
    if not partie_en_cours or colonne < 0 or colonne >= COLONNES or plateau[0][colonne] != 0:
        return
    for ligne in range(LIGNES - 1, -1, -1):
        if plateau[ligne][colonne] == 0:
            plateau[ligne][colonne] = joueur_actuel
            historique_coups.append((ligne, colonne))
            dessiner_plateau()
            if verifier_victoire(ligne, colonne):
                scores[joueur_actuel-1] += 1
                label_scores.config(text=f"Joueur 1: {scores[0]}  |  Joueur 2: {scores[1]}  |  Manche: {sum(scores)+1}")
                animer_victoire_manche(joueur_actuel)
                if scores[joueur_actuel-1] >= MANCHES_GAGNANTES:
                    messagebox.showinfo("Fin de partie", f"Le joueur {joueur_actuel} a gagné la partie !")
                    partie_en_cours = False
                    manche_terminee = True
                else:
                    messagebox.showinfo("Manche terminée", f"Le joueur {joueur_actuel} a gagné la manche !")
                    partie_en_cours = False
                    manche_terminee = True
                    if not animer_jetons_gagnants(ligne, colonne):
                        root.after(2000, commencer_nouvelle_manche)
                return

            if verifier_match_nul():
                messagebox.showinfo("Match nul", "La manche se termine par un match nul !")
                partie_en_cours = False
                manche_terminee = True
                root.after(2000, commencer_nouvelle_manche)
                return
            joueur_actuel = 3 - joueur_actuel
            
            if MODE_IA and joueur_actuel == 2 and partie_en_cours and not manche_terminee:
                root.after(500, jouer_coup_ia)
            return


def commencer_nouvelle_manche():
    global joueur_actuel, premier_joueur_manche, manche_terminee, scores
    
    manche_terminee = False
    premier_joueur_manche = 3 - premier_joueur_manche
    joueur_actuel = premier_joueur_manche
    
    if max(scores) < MANCHES_GAGNANTES:
        initialiser_plateau()
    else:
        retour_au_menu()


def verifier_victoire(ligne, colonne):
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

def clic(event):
    colonne = event.x // TAILLE_CASE
    poser_jeton(colonne)

def retour_au_menu():
    global jeu_frame, scores, manche_terminee
    jeu_frame.pack_forget()
    if not manche_terminee:
        scores = [0, 0]
    manche_terminee = False
    afficher_menu_principal()
root = tk.Tk()
root.title("Puissance 4 - Jeu avec jetons 3D")
root.geometry(f"{COLONNES * TAILLE_CASE + 100}x{LIGNES * TAILLE_CASE + 250}")
root.minsize(600, 600)
root.configure(bg="#2C3E50")

afficher_menu_principal()
root.mainloop()