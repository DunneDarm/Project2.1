class Temperature(tk.Frame):
    '''Bevat een grafiek van de gemeten temperatuur data'''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.rollout = controller.temp_rollout

        figure = Figure(figsize=(8, 5), dpi=100)
        plot = figure.add_subplot(1, 1, 1)

        x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        y = [19, 20, 20, 21, 20, 20, 20, 21, 20, 19, 19, 18, 20, 21, 20, 20, 20, 21, 21, 20]
        x = x[0:20]  # Pak alleen 20 waarden
        y = y[0:20]

        avg = round(sum(y) / len(y))

        avg_list = []
        for i in range(20):
            avg_list.append(avg-0.025)

        # Teken de lijnen
        plot.plot(x, y, color="blue",  linestyle="-")
        plot.plot(x, avg_list, color="red", linestyle="-")

        canvas = FigureCanvasTkAgg(figure, self)
        canvas.get_tk_widget().grid(row=0, column=0)

        # Labels
        title = tk.Label(self, text="Gemeten temperatuur", font=(
            None, 18, 'bold'))
        title.place(x=400, y=20, anchor="center")

        blue_line = tk.Label(self, text="Gemeten temperatuur", fg="blue")
        blue_line.place(x=725, y=15, anchor="e")

        red_line = tk.Label(self, text="Gemiddelde temperatuur", fg="red")
        red_line.place(x=725, y=40, anchor="e")

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
        refresh_button = tk.Button(self, text="Refresh", highlightbackground="white smoke", command=Temperature.update)
        refresh_button.place(x=200, y=10)