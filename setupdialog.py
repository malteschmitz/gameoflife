from tkinter import *

class SetupDialog(object):
    def __init__(self, parent):
        # neues Fenster erzeugen
        self.top = Toplevel(parent)

        # Validierungskommando für positive Ganzzahlen registrieren
        vcmd = (parent.register(self.validate), '%P')

        # Eingabeelemente erzeugen
        body = Frame(self.top)
        Label(body, text = "Anzahl Zellen\nauf dem Bildschirm:").grid(row = 0, columnspan = 2)
        Label(body, text = "Breite:").grid(row = 1)
        self.width_var = StringVar()
        width_entry = Entry(body, textvariable = self.width_var,
            validate = "all", validatecommand = vcmd)
        width_entry.grid(row = 1, column = 1)
        Label(body, text = "Höhe:").grid(row = 2)
        self.height_var = StringVar()
        Entry(body, textvariable = self.height_var,
            validate = "all", validatecommand = vcmd).grid(row = 2, column = 1)
        Label(body, text = "Anzahl Pixel, die für\neine Zelle verwendet werden:").grid(row = 3,
            columnspan = 2, pady = [10, 0])
        self.pixels_per_cell_var = StringVar()
        Entry(body, textvariable = self.pixels_per_cell_var,
            validate = "all", validatecommand = vcmd).grid(row = 4, columnspan = 2, stick = "we")
        Label(body, text = "Verzögerung für den\nautomatischen Ablauf\nin Millisekunden:").grid(row = 5,
            columnspan = 2, pady = [10, 0])
        self.auto_step_delay_var = StringVar()
        Entry(body, textvariable = self.auto_step_delay_var,
            validate = "all", validatecommand = vcmd).grid(row = 6, columnspan = 2, stick = "we")

        # Buttonleiste erzeugen
        buttons = Frame(self.top)
        okButton = Button(buttons, text = "OK", command = self.ok)
        okButton.grid(row = 0, column = 0)
        cancelButton = Button(buttons, text = "Abbrechen", command = self.cancel)
        cancelButton.grid(row = 0, column = 1)

        # Eingabelemente und Buttonleiste im Hauptfenster anordnen
        body.grid(padx = 10, pady = [10,5])
        buttons.grid(row = 1, padx = 10, pady = [5,10])

        # Größe des Hauptfesnters kann nicht verändert werden
        self.top.resizable(0, 0)

        # modaler Dialog sperrt das Hauptfenster
        self.top.transient(parent)
        self.top.grab_set()
        width_entry.focus_set()

        # Ereignisse abfangen
        self.top.bind("<Return>", self.ok)
        self.top.bind("<Escape>", self.cancel)

    def validate(self, value):
        try:
            val = int(value)
            return val >= 0
        except ValueError:
            return False

    def cancel(self, event = None):
        self.top.destroy()

    def valid_in(self, key, name, min_value, max_value):
        value = int(getattr(self, key + "_var").get())
        if value < min_value or value > max_value:
            messagebox.showinfo(message = name + " muss zwischen " + str(min_value) + 
                " und " + str(max_value) + " liegen.", icon = "warning")
            return False
        return True

    def valid(self):
        return self.valid_in("width", "Breite", 5, 5000) and \
            self.valid_in("height", "Höhe", 5, 5000) and \
            self.valid_in("pixels_per_cell", "Pixel pro Zelle", 5, 30) and \
            self.valid_in("auto_step_delay", "Verzögerung", 25, 2000)

    def ok(self, event = None):
        if self.valid():
            self.cancel()
            self.apply()

    def apply():
        pass