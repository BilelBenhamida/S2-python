import tkinter as tk

def dessiner_cible(taille_image, nb_cercles):
    couleurs = ['blue', 'green', 'black', 'yellow', 'magenta', 'red']
    root = tk.Tk()
    root.title("Cible en Couleur")
    canvas = tk.Canvas(root, width=taille_image, height=taille_image)
    canvas.pack()
    centre_x = taille_image // 2
    centre_y = taille_image // 2
    rayon = taille_image // 2
    for i in range(nb_cercles):
        couleur = couleurs[i % len(couleurs)]
        canvas.create_oval(centre_x - rayon, centre_y - rayon, 
                           centre_x + rayon, centre_y + rayon, 
                           fill=couleur, outline=couleur)
        rayon -= taille_image // (2 * nb_cercles)
    root.mainloop()

taille_image = 400
nb_cercles = 6
dessiner_cible(taille_image, nb_cercles)