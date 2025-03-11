import tkinter as tk
import random

root = tk.Tk()
root.title("Mon dessin")

btn_style = {"font": ("Arial", 12, "bold"),"bg": "blue","fg": "pink","relief": "raised"}

couleur = "blue"

def changer_couleur():
    global couleur
    couleur = input("Entrez une couleur : ")

def cercle():
    diameter = 100
    x = random.randint(0, 400 - diameter)
    y = random.randint(0, 400 - diameter)
    canvas.create_oval(x, y, x + diameter, y + diameter, fill=couleur, outline=couleur)

def carre():
    side = 100
    x = random.randint(0, 400 - side)
    y = random.randint(0, 400 - side)
    canvas.create_rectangle(x, y, x + side, y + side, fill=couleur, outline=couleur)

def croix():
    side = 100
    x = random.randint(0, 400 - side)
    y = random.randint(0, 400 - side)
    canvas.create_line(x, y, x + side, y + side, fill=couleur, width=5)
    canvas.create_line(x + side, y, x, y + side, fill=couleur, width=5)

btn_top = tk.Button(root, text="Choisir une couleur", command = changer_Acouleur, **btn_style)
btn_left1 = tk.Button(root, text="Cercle", command = cercle, **btn_style)
btn_left2 = tk.Button(root, text="Carré", command = carre, **btn_style)
btn_left3 = tk.Button(root, text="Croix", command = croix, **btn_style)

canvas = tk.Canvas(root, width=400, height=400, bg="black", borderwidth=5, relief="sunken")

btn_top.grid(row=0, column=1, columnspan=2, pady=10)
btn_left1.grid(row=1, column=0, padx=10, pady=5)
btn_left2.grid(row=2, column=0, padx=10, pady=5)
btn_left3.grid(row=3, column=0, padx=10, pady=5)
canvas.grid(row=1, column=1, rowspan=3, columnspan=2, padx=10, pady=10)

root.mainloop()