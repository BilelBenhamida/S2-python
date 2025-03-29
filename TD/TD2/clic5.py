import tkinter as tk

click_count = 0
circles = []

def clic(event):
    global click_count
    click_count += 1
    x, y = event.x, event.y
    if click_count <= 8:
        circle = canvas.create_oval(x-50, y-50, x+50, y+50, fill="red", outline="red")
    elif click_count == 9:
        for circle in circles:
            canvas.itemconfig(circle, fill="yellow")
        return
    elif click_count == 10:
        for circle in circles:
            canvas.delete(circle)
        circles.clear()
        click_count = 0
        return
    circles.append(circle)

root = tk.Tk()
root.title("Clics - Fenêtre 5")
canvas = tk.Canvas(root, width=500, height=500, bg="black")
canvas.pack()
canvas.bind("<Button-1>", clic)

root.mainloop()