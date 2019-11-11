import random
import tkinter as tk
from matplotlib import style
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use("TkAgg")

# Moet bovenaan de classes, is voor het plotten van de grafiek!
# Tot de animate functie
# Ook onderaan classes nieuwe regel toegevoegd
style.use("ggplot")

f = Figure(figsize=(5, 5), dpi=100, facecolor="Azure")
a = f.add_subplot(111)


x_axis = [0]
y_axis = [0]


def add_y(y):
    """Voeg nieuwe y toe"""
    x_axis.append(x_axis[-1] + 1)
    y_axis.append(y)


def animate(_i):
    """Schets de grafiek"""
    add_y(random.randint(15, 25))  # Random data simuleren
    x = x_axis[-10:]
    y = y_axis[-10:]
    a.clear()
    a.plot(x, y, '-o')


class App(tk.Tk):
    # Dit is dezelfde class App als in de GUI
    pass

class Temperature(tk.Frame):
    '''Bevat een grafiek van de gemeten temperatuur data'''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        title_label = tk.Label(self, text="Gemeten temperatuur",
                               font=controller.tfont, bg="white smoke")
        title_label.pack(side="top", fill="x")

        divider = tk.Frame(self, height=1, bg="black")
        divider.pack(side="top", fill="x")

        button = tk.Button(self, text="Terug naar bekijk data",
                           command=lambda: controller.show_frame(ViewData))
        button.pack(pady=20)
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        y_label = tk.Label(self, text="Gemeten temperatuur", bg="Azure")
        y_label.place(x=15, y=90)

        x_label = tk.Label(self, text="Meetmoment", bg="Azure")
        x_label.place(x=700, y=475)

if __name__ == "__main__":
    APP = App()
    APP.title("Zonnescherm Applicatie")
    APP.resizable(0, 0)
    APP.geometry("800x500")
    ani = animation.FuncAnimation(f, animate, interval=1000) # NIEUWE REGEL!
    APP.mainloop()