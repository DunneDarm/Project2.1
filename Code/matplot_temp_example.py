from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")

root = tk.Tk()

figure = Figure(figsize=(8, 5), dpi=100)
plot = figure.add_subplot(1, 1, 1)

# Lijsten van x en y coördinaten
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
y = [21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 22, 22, 23, 24, 24, 19]
x = x[0:20]  # Pak alleen 20 waarden
y = y[0:20]

# Bereken het gemiddelde van alle gemeten temperaturen
avg = round(sum(y) / len(y))
print(avg)

# Pak 20 keer de gemiddelde waarde (anders gaat hij zeuren)
avg_list = []
for i in range(20):
    avg_list.append(avg-0.025)

# Teken de lijnen
plot.plot(x, y, color="blue",  linestyle="-")
plot.plot(x, avg_list, color="red", linestyle="-")

# Canvas
canvas = FigureCanvasTkAgg(figure, root)
canvas.get_tk_widget().grid(row=0, column=0)

# Labels
title = tk.Label(text="Gemeten temperatuur", font=(
    None, 18, 'bold'), bg = "white")
title.place(x=400, y=20, anchor="center")

blue_line = tk.Label(text="Gemeten temperatuur", fg="blue", bg = "white")
blue_line.place(x=725, y=15, anchor="e")

red_line = tk.Label(text="Gemiddelde temperatuur", fg="red", bg = "white")
red_line.place(x=725, y=40, anchor="e")

y_label = tk.Label(text="Temperatuur", bg = "white")
y_label.place(x=15, y=15)

x_label = tk.Label(text="Meetmoment", bg = "white")
x_label.place(x=725, y=485, anchor="e")

root.mainloop()
