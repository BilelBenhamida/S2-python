import tkinter as tk

def clic(event):
    x, y = event.x, event.y
    if x < 250:
        canvas.create_oval(x-50, y-50, x+50, y+50, fill="blue", outline="blue")
    else:
        canvas.create_oval(x-50, y-50, x+50, y+50, fill="red", outline="red")

root = tk.Tk()
root.title("Clics - Fenêtre 2")
canvas = tk.Canvas(root, width=500, height=500, bg="black")
canvas.pack()
canvas.create_line(250, 0, 250, 500, fill="white", width=2)
canvas.bind("<Button-1>", clic)

root.mainloop()