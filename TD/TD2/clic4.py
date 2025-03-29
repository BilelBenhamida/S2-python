import tkinter as tk

click_count = 0
rectangle_id = None

def clic(event):
    global click_count, rectangle_id
    click_count += 1
    if click_count > 10:
        root.destroy()
        return
    if rectangle_id is None:
        x1, y1 = 200, 200
        x2, y2 = 300, 300
        rectangle_id = canvas.create_rectangle(x1, y1, x2, y2, outline="white", width=3)
    if click_count % 2 == 1:
        canvas.itemconfig(rectangle_id, fill="white")
    else:
        canvas.itemconfig(rectangle_id, fill="black")

root = tk.Tk()
root.title("Clics - Fenêtre 4")
canvas = tk.Canvas(root, width=500, height=500, bg="black")
canvas.pack()
canvas.bind("<Button-1>", clic)

root.mainloop()