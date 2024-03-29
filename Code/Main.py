"""Python GUI voor het uitlezen en bekijken van data van zonnescherm"""
import tkinter as tk
from tkinter import font as tfont
from tkinter.messagebox import showinfo, showerror
import platform
from Serialportconnection import *
from tempRead import *
import threading
import time
import matplotlib
from lightRead import *
from matplotlib.animation import FuncAnimation
from matplotlib import style
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
plt.rcParams['toolbar'] = 'None'
style.use("ggplot")


global TempPort
global LightPort
global TempList
global ConnectList
global LightList


class App(tk.Tk):
    """App initialisatie"""

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

        self.frames = {}
        for frame_class in (Login, Home, ControlPanel, Settings, ViewData, ConnectedUnits):
            frame = frame_class(container, self)
            self.frames[frame_class] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            frame.config(bg="Azure")

        self.show_frame(Login)

    def show_frame(self, page):
        """Verander van frame in de GUI"""
        frame = self.frames[page]
        frame.tkraise()


class Login(tk.Frame):
    """Bevat het (dummy) login scherm"""

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
            """Bepaal of de opgegeven inlog correct is of niet (zonder DB)"""
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
    """Bevat knoppen om te gaan naar: data, instellingen en controlepaneel"""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Titel
        title_label = tk.Label(
            self, text="Homepagina", font=controller.tfont, bg="white smoke")
        title_label.pack(side="top", fill="x")

        divider = tk.Frame(self, height=1, bg="black")
        divider.pack(side="top", fill="x")

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
    """Geeft de mogelijkheid om het scherm op te rollen of uit te rollen"""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Titel
        title_label = tk.Label(self, text="Controlepaneel",
                               font=controller.tfont, bg="white smoke")
        title_label.pack(side="top", fill="x")

        divider = tk.Frame(self, height=1, bg="black")
        divider.pack(side="top", fill="x")

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
    """Pas de instellingen aan van het zonnescherm"""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Titel
        title_label = tk.Label(self, text="Instellingen",
                               font=controller.tfont, bg="white smoke")
        title_label.pack(side="top", fill="x")

        divider = tk.Frame(self, height=1, bg="black")
        divider.pack(side="top", fill="x")

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
    """Bevat knoppen die leiden naar verschillende data (grafieken)"""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        title_label = tk.Label(self, text="Bekijk data",
                               font=controller.tfont, bg="white smoke")
        title_label.pack(side="top", fill="x")

        divider = tk.Frame(self, height=1, bg="black")
        divider.pack(side="top", fill="x")

        if platform.system() == "Darwin":
            # Temperatuur bekijken
            temp_button = tk.Button(
                self, text="Temperatuur", font=(None, 18, 'bold'),
                highlightbackground="white smoke",
                command=TemperatureGraph)
            temp_button.config(height=3, width=25)
            temp_button.place(x=400, y=180, anchor="center")

            # Lichtintensiteit bekijken
            lightintensity_button = tk.Button(
                self, text="Lichtintensiteit", font=(None, 18, 'bold'),
                highlightbackground="white smoke",
                command=LightGraph)
            lightintensity_button.config(height=3, width=25)
            lightintensity_button.place(x=400, y=330, anchor="center")

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
                command=TemperatureGraph)
            temp_button.config(height=2, width=20)
            temp_button.place(x=400, y=180, anchor="center")

            # Lichtintensiteit bekijken
            lightintensity_button = tk.Button(
                self, text="Lichtintensiteit", font=(None, 18, 'bold'),
                highlightbackground="white smoke",
                command=LightGraph)
            lightintensity_button.config(height=2, width=20)
            lightintensity_button.place(x=400, y=355, anchor="center")

            # Terug naar homepagina
            back_button = tk.Button(
                self, text="⬅ Terug naar homepagina", highlightbackground="white smoke",
                command=lambda: controller.show_frame(Home))
            back_button.place(x=15, y=465)

            # Uitloggen button
            logout_button = tk.Button(
                self, text="Uitloggen", highlightbackground="white smoke", command=quit)
            logout_button.place(x=718, y=465)

    def LowerSCreen(self):
        TempPort.write()

    def RaiseScreen(self):
        TempPort.write(1)


class TemperatureGraph:
    """Schetst een grafiek van de gemeten temperatuur"""

    def __init__(self):
        self.x_axis = [0]
        self.y_axis = [TempList[0]]

        self.animation = FuncAnimation(plt.gcf(), self.animate, interval=1000)
        plt.show()

    def add_y(self, y):
        """Voeg nieuwe y toe"""
        self.x_axis.append(self.x_axis[-1] + 1)
        self.y_axis.append(y)

    def animate(self, _i):
        """Schets de grafiek"""
        self.add_y(int(TempList[-1]))
        x = self.x_axis[-10:]
        y = self.y_axis[-10:]
        plt.cla()  # Clear current axes
        plt.plot(x, y, 'o-')
        plt.title('Gemeten temperatuur')
        plt.gcf().canvas.set_window_title('Temperatuur grafiek')
        plt.ylabel('Temperatuur in °C')
        plt.xlabel('Meetmoment')


class LightGraph:
    """Schetst een grafiek van de gemeten lichtintensiteit"""

    def __init__(self):
        self.x_axis = [0]
        self.y_axis = [LightList[0]]

        self.animation = FuncAnimation(plt.gcf(), self.animate, interval=1000)
        plt.show()

    def add_y(self, y):
        """Voeg nieuwe y toe"""
        self.x_axis.append(self.x_axis[-1] + 1)
        self.y_axis.append(y)

    def animate(self, _i):
        """Schets de grafiek"""
        self.add_y(LightList[-1])
        x = self.x_axis[-10:]
        y = self.y_axis[-10:]
        plt.cla()  # Clear current axes
        plt.plot(x, y, 'o-')
        plt.title('Gemeten lichtintensiteit')
        plt.gcf().canvas.set_window_title('Lichtintensiteit grafiek')
        plt.ylabel('Lichtintensiteit in Lumen')
        plt.xlabel('Meetmoment')


class ConnectedUnits(tk.Frame):
    """Bevat een tabel met alle aangesloten besturings een heden"""

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

        else:
            # Homepagina button
            back_button = tk.Button(
                self, text="⬅ Terug naar instellingen", highlightbackground="white smoke",
                command=lambda: controller.show_frame(Settings))
            back_button.place(x=700, y=465, anchor="center")


def TempMaker():
    global TempList
    time.sleep(3)
    while 1:
        try:
            time.sleep(2)
            TempList = TempLineData(TempPort.read(80))
            print(TempList)
        except:
            print("Temperature detection unit not available")


def LightMaker():
    global LightList
    time.sleep(2)
    while 1:
        try:
            time.sleep(2)
            LightList = LightLineData(LightPort.read(120))
            print(LightList)
        except:
            print("Lightdetection unit not available")


def ThreadSetup():
    TempThread = threading.Thread(target=TempMaker, args=(), daemon=True)
    TempThread.start()

    LightThread = threading.Thread(target=LightMaker, args=(), daemon=True)
    LightThread.start()


def ConnectionSetup():
    global TempPort
    global TempList
    global LightPort
    global ConnectList
    ports = getPorts()
    ConnectList = []
    for port in ports:
        ser = serial.Serial()
        test = str(port).split(" ")
        ser.baudrate = 19200
        ser.port = test[0]
        ConnectList.append(ser)

    for arduino in ConnectList:
        arduino.open()
        Value = arduino.read(15)
        if "t" in str(Value)[2:-1]:
            TempPort = arduino
        if "L" in str(Value)[2:-1]:
            LightPort = arduino


if __name__ == "__main__":
    TempList = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    LightList = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    try:
        ConnectionSetup()
        #TempList = TempLineData(TempPort.read(60))
        ThreadSetup()
    except:
        TempList = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        print("Zero supported devices found")

    APP = App()
    APP.title("Zonnescherm Applicatie")
    APP.resizable(0, 0)
    APP.geometry("800x500")
    APP.update()
    APP.mainloop()

    for arduino in ConnectList:
        arduino.close()
