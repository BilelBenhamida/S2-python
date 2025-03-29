import tkinter as tk

clicks = []

def clic(event):
    clicks.append((event.x, event.y))
    if len(clicks) == 2:
        x1, y1 = clicks[0]
        x2, y2 = clicks[1]
        color = "blue" if (x1 < 250 and x2 < 250) or (x1 >= 250 and x2 >= 250) else "red"
        canvas.create_line(x1, y1, x2, y2, fill=color, width=2)
        clicks.clear()

root = tk.Tk()
root.title("Clics - Fenêtre 3")
canvas = tk.Canvas(root, width=500, height=500, bg="black")
canvas.pack()
canvas.create_line(250, 0, 250, 500, fill="white", width=2)
canvas.bind("<Button-1>", clic)

root.mainloop()