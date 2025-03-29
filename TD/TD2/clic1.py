import tkinter as tk

def clic(event):
    x, y = event.x, event.y
    canvas.create_rectangle(x, y, x+1, y+1, fill="red", outline="red")

root = tk.Tk()
root.title("Clics - Fenêtre 1")
canvas = tk.Canvas(root, width=500, height=500, bg="black")
canvas.pack()
canvas.bind("<Button-1>", clic)
root.mainloop()