'''Python GUI voor het uitlezen en bekijken van data van zonnescherm'''
import tkinter as tk
from tkinter import font as tfont
from tkinter.messagebox import showinfo, showerror
import platform
from serialportconnection import *
from tempRead import *
import threading
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plotting
import matplotlib
matplotlib.use("TkAgg")

global ser
global TempList

class App(tk.Tk):
    '''App initialisatie'''

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Setup frame
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Title font
        if platform.system() == "Darwin":
            self.tfont = tfont.Font(size=14, weight='bold')
            self.tempfont = tfont.Font(size=14)
        else:
            self.tfont = tfont.Font(size=11, weight='bold')
            self.tempfont = tfont.Font(size=11)

        # Settings
        self.temp_rollout = 20
        self.temp_pullup = 20
        self.light_rollout = 18
        self.light_pullup = 2
        self.max_rollout = 140
        self.cur_temp = "unknown"

        self.frames = {}
        for frame_class in (Login, Home, ControlPanel, Settings, ViewData, Temperature,
                            Distance, Lightintensity, ConnectedUnits):
            frame = frame_class(container, self)
            self.frames[frame_class] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            frame.config(bg="Azure")

        self.show_frame(Login)

    def show_frame(self, page):
        '''Verander van frame in de GUI'''
        frame = self.frames[page]
        frame.tkraise()

class Login(tk.Frame):
    '''Bevat het (dummy) login scherm'''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Titel
        title_label = tk.Label(
            self, text="Welkom bij de officiële zonnescherm applicatie van Zeng ltd. " +
            "Log alstublieft in of maak een account aan.",
            font=controller.tfont, bg="white smoke")
        title_label.pack(side="top", fill="x")

        divider = tk.Frame(self, height=1, bg="black")
        divider.pack(side="top", fill="x")

        # Login entries
        username_label = tk.Label(self, text="Gebruikersnaam", bg="Azure")
        username_label.place(x=230, y=80)

        password_label = tk.Label(self, text="Wachtwoord", bg="Azure")
        password_label.place(x=230, y=110)

        entry_username = tk.Entry(self)
        entry_password = tk.Entry(self, show="•")
        entry_username.place(x=350, y=80)
        entry_password.place(x=350, y=110)

        # Wachtwoord vergeten
        forgot_label = tk.Label(
            self, text="Wachtwoord vergeten?", bg="Azure", fg="Blue", font=(None, 12, "italic"))
        forgot_label.place(x=400, y=150, anchor="center")

        def show_msg(_label):
            showinfo("Wachtwoord vergeten (dummy)",
                     "Username = Groep3\nPassword = 1234")

        forgot_label.bind("<Button-1>", show_msg)

        # Login / registreer button
        def login():
            '''Bepaal of de opgegeven inlog correct is of niet (zonder DB)'''
            if entry_username.get().lower() == "groep3" and entry_password.get() == "1234":
                controller.show_frame(Home)
            else:
                showerror("Onjuist wachtwoord",
                          "Probeer opnieuw in te loggen of druk op wachtwoord vergeten.")

        if platform.system() == "Darwin":
            # Login
            login_button = tk.Button(
                self, text="Login", highlightbackground="white smoke", font=(None, 18, 'bold'),
                command=login)
            login_button.config(height=3, width=25)
            login_button.place(x=400, y=260, anchor="center")

            # Registreer
            register_button = tk.Button(
                self, text="Registreer", highlightbackground="white smoke", font=(None, 18, 'bold'),
                command=lambda: showinfo("Registreren", "Dit is een dummy"))
            register_button.config(height=3, width=25)
            register_button.place(x=400, y=350, anchor="center")
        else:
            login_button = tk.Button(
                self, text="Login", bg="white smoke", font=(None, 18, 'bold'), command=login)
            login_button.config(height=2, width=20)
            login_button.place(x=400, y=260, anchor="center")

            # Registreer
            register_button = tk.Button(
                self, text="Registreer", bg="white smoke", font=(None, 18, 'bold'),
                command=lambda: showinfo("Registreren", "Dit is een dummy"))
            register_button.config(height=2, width=20)
            register_button.place(x=400, y=375, anchor="center")


class Home(tk.Frame):
    '''Bevat knoppen om te gaan naar: data, instellingen en controlepaneel'''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Titel
        title_label = tk.Label(
            self, text="Homepagina", font=controller.tfont, bg="white smoke")
        title_label.pack(side="top", fill="x")

        divider = tk.Frame(self, height=1, bg="black")
        divider.pack(side="top", fill="x")

        # Huidige temperatuur
        temp_label = tk.Label(
            self, text="Huidige temperatuur: " + str(controller.cur_temp) + " °C", bg="white smoke",
            font=controller.tempfont, fg="grey40")
        temp_label.place(x=120, y=11, anchor="center")

        if platform.system() == "Darwin":
            # Controle paneel button
            controlpanel_button = tk.Button(
                self, text="Controlepaneel", highlightbackground="white smoke",
                font=(None, 18, 'bold'), command=lambda: controller.show_frame(ControlPanel))
            controlpanel_button.config(height=3, width=25)
            controlpanel_button.place(x=400, y=150, anchor="center")

            # Bekijk data button
            data_button = tk.Button(
                self, text="Bekijk data", highlightbackground="white smoke",
                font=(None, 18, 'bold'), command=lambda: controller.show_frame(ViewData))
            data_button.config(height=3, width=25)
            data_button.place(x=400, y=250, anchor="center")

            # Instellingen button
            settings_button = tk.Button(
                self, text="Instellingen", highlightbackground="white smoke",
                font=(None, 18, 'bold'), command=lambda: controller.show_frame(Settings))
            settings_button.config(height=3, width=25)
            settings_button.place(x=400, y=350, anchor="center")

            # Uitloggen button
            logout_button = tk.Button(
                self, text="Uitloggen", highlightbackground="white smoke", command=quit)
            logout_button.place(x=718, y=465)
        else:
            # Controle paneel button
            controlpanel_button = tk.Button(
                self, text="Controlepaneel", bg="white smoke",
                font=(None, 18, 'bold'), command=lambda: controller.show_frame(ControlPanel))
            controlpanel_button.config(height=2, width=20)
            controlpanel_button.place(x=400, y=125, anchor="center")

            # Bekijk data button
            data_button = tk.Button(
                self, text="Bekijk data", bg="white smoke",
                font=(None, 18, 'bold'), command=lambda: controller.show_frame(ViewData))
            data_button.config(height=2, width=20)
            data_button.place(x=400, y=250, anchor="center")

            # Instellingen button
            settings_button = tk.Button(
                self, text="Instellingen", bg="white smoke",
                font=(None, 18, 'bold'), command=lambda: controller.show_frame(Settings))
            settings_button.config(height=2, width=20)
            settings_button.place(x=400, y=375, anchor="center")


class ControlPanel(tk.Frame):
    '''Geeft de mogelijkheid om het scherm op te rollen of uit te rollen'''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Titel
        title_label = tk.Label(self, text="Controlepaneel",
                               font=controller.tfont, bg="white smoke")
        title_label.pack(side="top", fill="x")

        divider = tk.Frame(self, height=1, bg="black")
        divider.pack(side="top", fill="x")

        # Huidige temperatuur
        temp_label = tk.Label(self, text="Huidige temperatuur: " + str(controller.cur_temp) + " °C",
                              bg="white smoke", font=controller.tempfont, fg="grey40")
        temp_label.place(x=120, y=11, anchor="center")

        if platform.system() == "Darwin":
            # Scherm uitrollen
            rollout_button = tk.Button(
                self, text="Scherm uitrollen", highlightbackground="white smoke",
                font=(None, 18, 'bold'), command=lambda: showinfo("Werkt niet", "In de maak"))
            rollout_button.config(height=3, width=25)
            rollout_button.place(x=400, y=180, anchor="center")

            # Scherm oprollen
            pullup_button = tk.Button(
                self, text="Scherm oprollen", highlightbackground="white smoke",
                font=(None, 18, 'bold'), command=lambda: showinfo("Werkt niet", "In de maak"))
            pullup_button.config(height=3, width=25)
            pullup_button.place(x=400, y=330, anchor="center")

            # Terug naar homepagina
            back_button = tk.Button(
                self, text="⬅ Terug naar homepagina", highlightbackground="white smoke",
                command=lambda: controller.show_frame(Home))
            back_button.place(x=15, y=465)

            # Uitloggen button
            logout_button = tk.Button(
                self, text="Uitloggen", highlightbackground="white smoke", command=quit)
            logout_button.place(x=718, y=465)
        else:
            # Scherm uitrollen
            rollout_button = tk.Button(
                self, text="Scherm uitrollen", bg="white smoke",
                font=(None, 18, 'bold'), command=lambda: showinfo("Werkt niet", "In de maak"))
            rollout_button.config(height=2, width=20)
            rollout_button.place(x=400, y=180, anchor="center")

            # Scherm oprollen
            pullup_button = tk.Button(
                self, text="Scherm oprollen", bg="white smoke",
                font=(None, 18, 'bold'), command=lambda: showinfo("Werkt niet", "In de maak"))
            pullup_button.config(height=2, width=20)
            pullup_button.place(x=400, y=355, anchor="center")

            # Terug naar homepagina
            back_button = tk.Button(
                self, text="⬅ Terug naar homepagina", bg="white smoke",
                command=lambda: controller.show_frame(Home))
            back_button.place(x=15, y=465)


class Settings(tk.Frame):
    '''Pas de instellingen aan van het zonnescherm'''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Titel
        title_label = tk.Label(self, text="Instellingen",
                               font=controller.tfont, bg="white smoke")
        title_label.pack(side="top", fill="x")

        divider = tk.Frame(self, height=1, bg="black")
        divider.pack(side="top", fill="x")

        # Huidige temperatuur
        temp_label = tk.Label(
            self, text="Huidige temperatuur: " + str(controller.cur_temp) + " °C",
            bg="white smoke", font=controller.tempfont, fg="grey40")
        temp_label.place(x=120, y=11, anchor="center")

        # Intellingen minimale temperatuur
        min_temp_entry = tk.Entry(self)
        min_temp_entry.place(x=480, y=50)

        min_temp_label = tk.Label(
            self, text="Scherm optrekken bij temperatuur ...",
            font=(None, 12, 'italic'), bg="Azure")
        min_temp_label.place(x=90, y=50)

        # Maximale temperatuur
        max_temp_entry = tk.Entry(self)
        max_temp_entry.place(x=480, y=90)

        max_temp_label = tk.Label(
            self, text="Scherm uitrollen bij temperatuur ...",
            font=(None, 12, 'italic'), bg="Azure")
        max_temp_label.place(x=90, y=90)

        # Minimale lichtintensiteit
        min_light_entry = tk.Entry(self)
        min_light_entry.place(x=480, y=130)

        min_light_label = tk.Label(
            self, text="Scherm optrekken bij lichtintensiteit ...",
            font=(None, 12, 'italic'), bg="Azure")
        min_light_label.place(x=90, y=130)

        # Maximale lichtintensiteit
        max_light_entry = tk.Entry(self)
        max_light_entry.place(x=480, y=170)

        max_light_label = tk.Label(
            self, text="Scherm uitrollen bij lichtintensiteit ...",
            font=(None, 11, 'italic'), bg="Azure")
        max_light_label.place(x=90, y=170)

        # Maximaal uitrollen scherm
        max_rollout_entry = tk.Entry(self)
        max_rollout_entry.place(x=480, y=210)

        max_rollout_label = tk.Label(
            self, text="Hoever mag het zonnescherm uitgerold worden?",
            font=(None, 11, 'italic'), bg="Azure")
        max_rollout_label.place(x=90, y=210)

        if platform.system() == "Darwin":
            # Instellingen opslaan
            save_button = tk.Button(
                self, text="Opslaan", highlightbackground="white smoke",
                font=(None, 18, 'bold'), command=lambda: showinfo("Werkt niet", "In de maak"))
            save_button.config(height=3, width=25)
            save_button.place(x=400, y=360, anchor="center")

            # Terug naar homepagina
            back_button = tk.Button(
                self, text="⬅ Terug naar homepagina", highlightbackground="white smoke",
                command=lambda: controller.show_frame(Home))
            back_button.place(x=15, y=465)

            # Naar Besturings eenheden
            Arduino_button = tk.Button(
                self, text="Besturingseenheden", highlightbackground="white smoke",
                command=lambda: controller.show_frame(ConnectedUnits))
            Arduino_button.place(x=351, y=465)

            # Uitloggen button
            logout_button = tk.Button(
                self, text="Uitloggen", highlightbackground="white smoke", command=quit)
            logout_button.place(x=718, y=465)
        else:
            # Instellingen opslaan
            save_button = tk.Button(
                self, text="Opslaan", highlightbackground="white smoke",
                font=(None, 18, 'bold'), command=lambda: showinfo("Werkt niet", "In de maak"))
            save_button.config(height=2, width=20)
            save_button.place(x=400, y=360, anchor="center")

            # Terug naar homepagina
            back_button = tk.Button(
                self, text="⬅ Terug naar homepagina", highlightbackground="white smoke",
                command=lambda: controller.show_frame(Home))
            back_button.place(x=15, y=465)

            # Naar Besturings eenheden
            Arduino_button = tk.Button(
                self, text="Besturingseenheden", highlightbackground="white smoke",
                command=lambda: controller.show_frame(ConnectedUnits))
            Arduino_button.place(x=351, y=465)

            # Uitloggen button
            logout_button = tk.Button(
                self, text="Uitloggen", highlightbackground="white smoke", command=quit)
            logout_button.place(x=718, y=465)


class ViewData(tk.Frame):
    '''Bevat knoppen die leiden naar verschillende data (grafieken)'''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        title_label = tk.Label(self, text="Bekijk data",
                               font=controller.tfont, bg="white smoke")
        title_label.pack(side="top", fill="x")

        divider = tk.Frame(self, height=1, bg="black")
        divider.pack(side="top", fill="x")

        # Huidige temperatuur
        temp_label = tk.Label(self, text="Huidige temperatuur: " + str(controller.cur_temp) + " °C",
                              bg="white smoke", font=controller.tempfont, fg="grey40")
        temp_label.place(x=120, y=11, anchor="center")

        if platform.system() == "Darwin":
            # Temperatuur bekijken
            temp_button = tk.Button(
                self, text="Temperatuur", font=(None, 18, 'bold'),
                highlightbackground="white smoke",
                command=lambda: controller.show_frame(Temperature))
            temp_button.config(height=3, width=25)
            temp_button.place(x=400, y=150, anchor="center")

            # Lichtintensiteit bekijken
            lightintensity_button = tk.Button(
                self, text="Lichtintensiteit", font=(None, 18, 'bold'),
                highlightbackground="white smoke",
                command=lambda: controller.show_frame(Lightintensity))
            lightintensity_button.config(height=3, width=25)
            lightintensity_button.place(x=400, y=250, anchor="center")

            # Afstand bekijken
            distance_button = tk.Button(
                self, text="Afstand", font=(None, 18, 'bold'), highlightbackground="white smoke",
                command=lambda: controller.show_frame(Distance))
            distance_button.config(height=3, width=25)
            distance_button.place(x=400, y=350, anchor="center")

            # Terug naar homepagina
            back_button = tk.Button(
                self, text="⬅ Terug naar homepagina", highlightbackground="white smoke",
                command=lambda: controller.show_frame(Home))
            back_button.place(x=15, y=465)

            # Uitloggen button
            logout_button = tk.Button(
                self, text="Uitloggen", highlightbackground="white smoke", command=quit)
            logout_button.place(x=718, y=465)
        else:
            # Temperatuur bekijken
            temp_button = tk.Button(
                self, text="Temperatuur", font=(None, 18, 'bold'),
                highlightbackground="white smoke",
                command=lambda: controller.show_frame(Temperature))
            temp_button.config(height=2, width=20)
            temp_button.place(x=400, y=125, anchor="center")

            # Lichtintensiteit bekijken
            lightintensity_button = tk.Button(
                self, text="Lichtintensiteit", font=(None, 18, 'bold'),
                highlightbackground="white smoke",
                command=lambda: controller.show_frame(Lightintensity))
            lightintensity_button.config(height=2, width=20)
            lightintensity_button.place(x=400, y=250, anchor="center")

            # Afstand bekijken
            distance_button = tk.Button(
                self, text="Afstand", font=(None, 18, 'bold'), highlightbackground="white smoke",
                command=lambda: controller.show_frame(Distance))
            distance_button.config(height=2, width=20)
            distance_button.place(x=400, y=375, anchor="center")

            # Terug naar homepagina
            back_button = tk.Button(
                self, text="⬅ Terug naar homepagina", highlightbackground="white smoke",
                command=lambda: controller.show_frame(Home))
            back_button.place(x=15, y=465)

            # Uitloggen button
            logout_button = tk.Button(
                self, text="Uitloggen", highlightbackground="white smoke", command=quit)
            logout_button.place(x=718, y=465)

class Temperature(tk.Frame):
    '''Bevat een grafiek van de gemeten temperatuur data'''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.rollout = controller.temp_rollout
        self.temp = TempList

        self.figure = Figure(figsize=(8, 5), dpi=100)
        self.plt = self.figure.add_subplot(1, 1, 1)

        #De waarden die in de grafiek moeten
        self.x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
        y = self.temp

        #Limit de waarden tot 20 wanneer er meer zijn.
        self.x = self.x[0:20]  # Pak alleen 20 waarden
        y = y[0:20]

        #Set the y-ax
        self.plt.set_ylim([min(TempList) - 1, max(TempList) + 1])

        # Basic plot for when there are no new values
        self.line = self.plt.plot(self.x, y, color="blue", linestyle="-")[0]

        self.canvas = FigureCanvasTkAgg(self.figure, self)

        self.canvas.get_tk_widget().grid(row=0, column=0)

        # Labels
        title = tk.Label(self, text="Gemeten temperatuur", font=(
            None, 18, 'bold'))
        title.place(x=400, y=20, anchor="center")

        blue_line = tk.Label(self, text="Gemeten temperatuur", fg="blue")
        blue_line.place(x=725, y=15, anchor="e")

        #Overbodig?
        #red_line = tk.Label(self, text="Gemiddelde temperatuur", fg="red")
        #red_line.place(x=725, y=40, anchor="e")

        y_label = tk.Label(self, text="Temperatuur")
        y_label.place(x=15, y=15)

        x_label = tk.Label(self, text="Meetmoment")
        x_label.place(x=725, y=485, anchor="e")

        # Homepagina button
        back_button = tk.Button(
            self, text="⬅ Bekijk data", highlightbackground="white smoke",
            command=lambda: controller.show_frame(ViewData))
        back_button.place(x=15, y=465)

        # Refresh button
        refresh_button = tk.Button(self, text="Refresh", highlightbackground="white smoke", command=self.TempRefresh)
        refresh_button.place(x=200, y=10)

    def TempRefresh(self):
        global TempList
        self.temp = TempList
        self.temp = self.temp[0:20]

        self.line.set_ydata(self.temp)
        self.plt.set_ylim([min(TempList) - 1, max(TempList) + 1])

        self.canvas.draw()
        Temperature.update(self)

class Distance(tk.Frame):
    '''Bevat een grafiek van de uitgerolde afstand van het zonnescherm'''

    def __init__(self, parent, controller, Temp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.rollout = controller.temp_rollout
        self.Distance = TempList

        self.figure = Figure(figsize=(8, 5), dpi=100)
        self.plt = self.figure.add_subplot(1, 1, 1)

        #De waarden die in de grafiek moeten
        self.x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
        y = self.Distance

        #Limit de waarden tot 20 wanneer er meer zijn.
        self.x = self.x[0:20]  # Pak alleen 20 waarden
        y = y[0:20]

        #Set the y-ax
        self.plt.set_ylim([min(TempList) - 1, max(TempList) + 1])

        #Basic plot for when there are no new values
        self.line = self.plt.plot(self.x, y, color="blue", linestyle="-")[0]

        self.canvas = FigureCanvasTkAgg(self.figure, self)

        self.canvas.get_tk_widget().grid(row=0, column=0)

        # Labels
        title = tk.Label(self, text="Gemeten temperatuur", font=(
            None, 18, 'bold'))
        title.place(x=400, y=20, anchor="center")

        blue_line = tk.Label(self, text="Gemeten temperatuur", fg="blue")
        blue_line.place(x=725, y=15, anchor="e")

        #Overbodig?
        #red_line = tk.Label(self, text="Gemiddelde temperatuur", fg="red")
        #red_line.place(x=725, y=40, anchor="e")

        y_label = tk.Label(self, text="Temperatuur")
        y_label.place(x=15, y=15)

        x_label = tk.Label(self, text="Meetmoment")
        x_label.place(x=725, y=485, anchor="e")

        # Homepagina button
        back_button = tk.Button(
            self, text="⬅ Bekijk data", highlightbackground="white smoke",
            command=lambda: controller.show_frame(ViewData))
        back_button.place(x=15, y=465)

        # Refresh button
        refresh_button = tk.Button(self, text="Refresh", highlightbackground="white smoke", command=self.DistanceRefresh)
        refresh_button.place(x=200, y=10)

    def DistanceRefresh(self):
        global TempList
        self.Distance = TempList
        self.Distance = self.Distance[0:20]

        self.line.set_ydata(self.Distance)
        self.plt.set_ylim([min(TempList) - 1, max(TempList) + 1])

        self.canvas.draw()
        Temperature.update(self)

class Lightintensity(tk.Frame):
    '''Bevat een grafiek van de gemeten lichtintesiteit data'''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.rollout = controller.temp_rollout
        self.light = TempList

        self.figure = Figure(figsize=(8, 5), dpi=100)
        self.plt = self.figure.add_subplot(1, 1, 1)

        #De waarden die in de grafiek moeten
        self.x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
        y = self.light

        #Basic plot for when there are no new values
        self.line = self.plt.plot(self.x, y, color="blue", linestyle="-")[0]

        #Limit de waarden tot 20 wanneer er meer zijnd.
        self.x = self.x[0:20]  # Pak alleen 20 waarden
        y = y[0:20]

        #Set the y-ax
        self.plt.set_ylim([min(TempList) - 1, max(TempList) + 1])

        self.canvas = FigureCanvasTkAgg(self.figure, self)

        self.canvas.get_tk_widget().grid(row=0, column=0)

        # Labels
        title = tk.Label(self, text="Gemeten Lichtintensiteit", font=(
            None, 18, 'bold'))
        title.place(x=400, y=20, anchor="center")

        blue_line = tk.Label(self, text="Gemeten Lichtintensiteit", fg="blue")
        blue_line.place(x=725, y=15, anchor="e")

        y_label = tk.Label(self, text="Lichtintensiteit")
        y_label.place(x=15, y=15)

        x_label = tk.Label(self, text="Meetmoment")
        x_label.place(x=725, y=485, anchor="e")

        # Homepagina button
        back_button = tk.Button(
            self, text="⬅ Bekijk data", highlightbackground="white smoke",
            command=lambda: controller.show_frame(ViewData))
        back_button.place(x=15, y=465)

        # Refresh button
        refresh_button = tk.Button(self, text="Refresh", highlightbackground="white smoke", command=self.LightRefresh)
        refresh_button.place(x=200, y=10)

    def LightRefresh(self):
        global TempList
        self.light = TempList
        self.light = self.light[0:20]

        self.line.set_ydata(self.light)
        self.plt.set_ylim([min(TempList) - 1, max(TempList) + 1])

        self.canvas.draw()
        Temperature.update(self)

class ConnectedUnits(tk.Frame):
    '''Bevat een tabel met alle aangesloten besturings een heden.'''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg="Azure")
        connectedlabels = []

        title_Unit_Label = tk.Label(self, text="Aangesloten eenheden", font=(
            None, 18, 'bold'), bg="Azure")
        title_Unit_Label.pack(side="top", fill="x")

        canvas = tk.Canvas(self, width=800, height=500, bg="Azure")
        canvas.pack()

        #figure = Figure(figsize=(8, 5), dpi=100)

        for i in range(0, len(getPorts()) + 1):
            if i < len(getPorts()):
                connectedlabels.append(tk.Label(self, text= getPorts()[i], bg= "Azure"))
                connectedlabels[i].place(x=300, y=(180 + (i * 50)))
            else:
                break

        if platform.system() == "Darwin":
            # Homepagina button
            back_button = tk.Button(
                self, text="⬅ Terug naar instellingen", highlightbackground="white smoke",
                command=lambda: controller.show_frame(Settings))
            back_button.place(x=700, y=465, anchor="center")

            # Refresh button
            refresh_button = tk.Button(self, text="Refresh", highlightbackground="white smoke",
                                       command=Temperature.update(self))
            refresh_button.place(x=80, y=465, ancho="center")

        else:
            # Homepagina button
            back_button = tk.Button(
                self, text="⬅ Terug naar instellingen", highlightbackground="white smoke",
                command=lambda: controller.show_frame(Settings))
            back_button.place(x=700, y=465, anchor="center")

            # Refresh button
            refresh_button = tk.Button(self, text="Refresh", highlightbackground="white smoke",
                                       command=Temperature.update(self))
            refresh_button.place(x=80, y=465, anchor="center")

def TempMaker():
    global TempList
    time.sleep(3)
    while 1:
        try:
            time.sleep(1)
            TempList = TempLineData(ser.read(60))
            print(TempList)
        except:
            print("OOF")
            break

def ThreadSetup():
    TempThread = threading.Thread(target=TempMaker, args=(), daemon=True)
    TempThread.start()

if __name__ == "__main__":
    try:
        ser = SetupConnection("Com3", 19200)
        ser.open()
        ser.read(4)
        TempList = TempLineData(ser.read(60))
        ThreadSetup()
    except:
        TempList = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    APP = App()
    APP.title("Zonnescherm Applicatie")
    APP.resizable(0, 0)
    APP.geometry("800x500")
    APP.update()
    APP.mainloop()

    ser.close()