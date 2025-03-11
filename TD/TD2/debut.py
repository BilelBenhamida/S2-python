import tkinter as tk

CANVAS_WIDTH, CANVAS_HEIGHT = 600, 400

root = tk.Tk()
canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
canvas.grid(row=0, column=0)

y0 = 100
y1 = CANVAS_HEIGHT - 100
x = CANVAS_WIDTH / 2
canvas.create_line(x, y0, x, y1)
canvas.create_oval(x - 50, y0 - 50, x + 50, y0 + 50)
canvas.create_oval(x - 50, y1 - 50, x + 50, y1 + 50)
canvas.create_oval(x - 50, (y0 + y1) / 2 - 50, x + 50, (y0 + y1) / 2 + 50)

root.mainloop()