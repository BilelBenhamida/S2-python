import tkinter as tk
import random

objets = []
current_color = "blue"

def draw_cercle():
    x1 = random.randint(50, 200)
    y1 = random.randint(50, 200)
    x2 = x1 + 100
    y2 = y1 + 100
    cercle = canvas.create_oval(x1, y1, x2, y2, fill=current_color)
    objets.append(cercle)

def draw_carre():
    x1 = random.randint(50, 200)
    y1 = random.randint(50, 200)
    x2 = x1 + 100
    y2 = y1 + 100
    carre = canvas.create_rectangle(x1, y1, x2, y2, fill=current_color)
    objets.append(carre)

def draw_croix():
    x1 = random.randint(50, 200)
    y1 = random.randint(50, 200)
    x2 = x1 + 100
    y2 = y1 + 100
    ligne1 = canvas.create_line(x1, y1, x2, y2, fill=current_color)
    ligne2 = canvas.create_line(x1, y2, x2, y1, fill=current_color)
    objets.append(ligne1)
    objets.append(ligne2)

def choisir_couleur():
    global current_color
    current_color = input("Entrez une couleur (par exemple, 'red', 'blue'): ")

def undo():
    if objets:
        dernier_objet = objets.pop()
        canvas.delete(dernier_objet)

root = tk.Tk()
root.title("Dessin avec Undo")
canvas = tk.Canvas(root, width=400, height=400, bg="black")
canvas.grid(row=0, column=0, columnspan=4)
button_cercle = tk.Button(root, text="Cercle", command=draw_cercle)
button_cercle.grid(row=1, column=0)
button_carre = tk.Button(root, text="Carré", command=draw_carre)
button_carre.grid(row=1, column=1)
button_croix = tk.Button(root, text="Croix", command=draw_croix)
button_croix.grid(row=1, column=2)
button_couleur = tk.Button(root, text="Choisir une couleur", command=choisir_couleur)
button_couleur.grid(row=1, column=3)
button_undo = tk.Button(root, text="Undo", command=undo)
button_undo.grid(row=2, column=0, columnspan=4)

root.mainloop()