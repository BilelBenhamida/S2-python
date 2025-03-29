import tkinter as tk
import random

def get_color(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def draw_pixel(i, j, color):
    canvas.create_rectangle(i, j, i+1, j+1, fill=color, width=0)

def ecran_aleatoire():
    for i in range(256):
        for j in range(256):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            color = get_color(r, g, b)
            draw_pixel(i, j, color)

def degrade_gris():
    for i in range(256):
        gray_value = i
        color = get_color(gray_value, gray_value, gray_value)
        for j in range(256):
            draw_pixel(i, j, color)

def degrade_2D():

    for i in range(256):
        r = i
        b = 255 - i
        color = get_color(r, 0, b)
        for j in range(256):
            draw_pixel(i, j, color)

root = tk.Tk()
root.title("Couleurs")
canvas = tk.Canvas(root, width=256, height=256)
canvas.grid(row=0, column=0, columnspan=4)
button_aleatoire = tk.Button(root, text="Aléatoire", command=ecran_aleatoire)
button_aleatoire.grid(row=1, column=0)
button_gris = tk.Button(root, text="Dégradé Gris", command=degrade_gris)
button_gris.grid(row=1, column=1)
button_rouge_bleu = tk.Button(root, text="Dégradé Rouge-Bleu", command=degrade_2D)
button_rouge_bleu.grid(row=1, column=2)

root.mainloop()