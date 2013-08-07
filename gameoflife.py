# Conways Spiel des Lebens mit Python 3 und Tk
#
# Dieser Quelltext ist frei unter der MIT-Lizenz.
#
# Copyright (c) 2013 Malte Schmitz
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Anzahl Zellen auf dem Bildschirm
width = 40
height = 30

# Anzahl Pixel, die für eine Zelle verwendet werden
pixels_per_cell = 15

# Verzögerung für den automatischen Ablauf in Millisekunden
auto_step_delay = 200

# An dieser Funktion müssen Änderungen vorgenommen werden.
def step(grid, new_grid):
    '''Diese Funktion führt einen Schritt von Conways Spiel des
       Lebens aus. Der aktuelle Zustand befindet sich dabei in
       grid und der neue Zustand wird in new_grid gesetzt.
       Dabei gelten die folgenden Regeln: Eine Zelle wird
       geboren, wenn es in ihrer Umgebung genau 3 Zellen gibt.
       Eine Zelle überlebt, wenn es in ihrer
       Umgebung genau 2 oder 3 Zellen gibt. Sonst stirbt sie an
       Vereinsamung oder Überbevölkerung. Lebt eine Zelle,
       befindet sich an der Koordinate in grid eine 1, sonst
       eine 0. Die erste Koordinate ist die X-Koordinate,
       die links mit 0 beginnt. Die zweite Koordinate ist die
       Y-Koordinate, die oben mit 0 beginnt.'''
    # Beginn der Lösung
    for x in range(1, width - 1):
        for y in range(1, height - 1):
            # Offset zu den Nachbarzellen
            nachbarschaft = [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]
            # Anzahl Nachbarn der Zelle an Position (x,y) berechnen
            nachbarn = 0
            for dx, dy in nachbarschaft:
                xn, yn = x + dx, y + dy
                nachbarn += grid[xn][yn]
            # Lasse neue Zellen entstehen
            if (grid[x][y] == 1 and nachbarn == 2) or nachbarn == 3:
                new_grid[x][y] = 1
    # Ende der Lösung

#############################################################

# Die folgende Klasse organisiert die GUI und muss nicht mehr angepasst werden.

# Laden der Komponenten für die GUI
from tkinter import *
# Laden des Dialoges für die Einstellungen
from setupdialog import SetupDialog
# Laden des Speichern-Dialoges
from tkinter.filedialog import asksaveasfilename
# Laden des Öffnen-Dialoges
from tkinter.filedialog import askopenfile

class GameOfLife(object):
    def __init__(self):
        self.root = Tk()

        # Verhindern, dass die Fenstergröße angepasst werden kann
        self.root.resizable(0, 0)

        # Initialisierung des Grids
        self.grid = [[0 for y in range(height)] for x in range(width)]

        # Zeichenfläche erzeugen
        self.canvas = Canvas(self.root,
            bd=0, highlightthickness=0, relief='ridge')

        # Die Zeichenfläche soll Tastaturereignisse erhalten
        self.canvas.focus_set()

        # Gitter zeichnen
        self.draw_grid()

        # Glider als Initiale Belegung erzeugen
        self.init_grid = [[0 for y in range(height)] for x in range(width)]
        self.init_grid[3][2] = 1
        self.init_grid[4][3] = 1
        self.init_grid[2][4] = 1
        self.init_grid[3][4] = 1
        self.init_grid[4][4] = 1
        self.handleReset()

        # Größe der Canvas auf ihren Inhalt anpassen
        self.canvas.pack()

        # Menüleiste erzeugen
        menubar = Menu(self.root)

        # Dateimenü erzeugen
        filemenu = Menu(menubar, tearoff = 0)
        filemenu.add_command(label = "Zurücksetzen", command = self.handleReset, accelerator = "R")
        filemenu.add_command(label = "Öffnen...", command = self.handleOpen, accelerator = "O")
        filemenu.add_command(label = "Speichern unter...", command = self.handleSave, accelerator = "S")
        filemenu.add_command(label = "Einstellungen...", command = self.handleSetup, accelerator = "E")
        filemenu.add_separator()
        filemenu.add_command(label = "Beenden", command = self.handleQuit, accelerator = "Q")
        
        # automatisches Weiterschalten ist initial nicht aktiv
        self.auto_step = BooleanVar()
        self.auto_step.set(False)

        # Generationenmenü erzeugen
        generationmenu = Menu(menubar, tearoff = 0)
        generationmenu.add_command(label = "nächste Generation", command = self.handleStep, accelerator = "N")
        generationmenu.add_checkbutton(label = "Play", variable = self.auto_step,
            onvalue = True, offvalue = False, command = self.play, accelerator = "P")

        # Menüleiste zusammensetzen und verwenden
        menubar.add_cascade(label = "Datei", menu = filemenu)
        menubar.add_cascade(label = "Generationen", menu = generationmenu)
        self.root.config(menu = menubar)

        # Abfangen von Ereignissen
        self.canvas.bind("<n>", self.handleStep)
        self.canvas.bind("<Key-space>", self.handleStep)
        self.canvas.bind("<p>", self.handlePlay)
        self.canvas.bind("<q>", self.handleQuit)
        self.canvas.bind("<o>", self.handleOpen)
        self.canvas.bind("<s>", self.handleSave)
        self.canvas.bind("<r>", self.handleReset)
        self.canvas.bind("<e>", self.handleSetup)
        self.canvas.bind("<Button-1>", self.handleClick)

        # Titel des Fenster setzen
        self.root.title("Conways Spiel des Lebens")

    def draw_grid(self):
        # Berechnung der Größe des Fensters
        width_pixels = width * pixels_per_cell - 1
        height_pixels = height * pixels_per_cell - 1
        
        # Setzen der Größe der Canvas
        self.canvas.config(width = width_pixels, height = height_pixels)

        # Löschen aller Elemente der Canvas
        self.canvas.delete(ALL)

        # Feld zum Speichern der Tags der gezeichneten Zellen
        self.circles = [[None for y in range(height)] for x in range(width)]

        # Zeichnen des Hintergrundgitters
        for x in range(1, width):
            self.canvas.create_line(x * pixels_per_cell - 1, 0,
                x * pixels_per_cell - 1, height_pixels - 1, fill = "gray")
        for y in range(1, height):
            self.canvas.create_line(0, y * pixels_per_cell - 1,
                width_pixels - 1, y * pixels_per_cell - 1, fill = "gray")

    def update_gui(self):
        for x in range(width):
            for y in range(height):
                if self.grid[x][y] == 1 and self.circles[x][y] == None:
                    self.circles[x][y] = self.canvas.create_oval(x * pixels_per_cell + 1,
                        y * pixels_per_cell + 1,
                        (x+1) * pixels_per_cell - 3, (y+1) * pixels_per_cell - 3,
                        fill = "lightblue", outline = "black")
                elif self.grid[x][y] == 0 and self.circles[x][y] != None:
                    self.canvas.delete(self.circles[x][y])
                    self.circles[x][y] = None

    def update_grid(self):
        # Anpassen der Größe des Grids
        old = self.grid
        self.grid = [[0 for y in range(height)] for x in range(width)]
        for x in range(min(width, len(old))):
            for y in range(min(height, len(old[0]))):
                self.grid[x][y] = old[x][y]
        # Anpassen der Größe des initialen Grids
        old = self.init_grid
        self.init_grid = [[0 for y in range(height)] for x in range(width)]
        for x in range(min(width, len(old))):
            for y in range(min(height, len(old[0]))):
                self.init_grid[x][y] = old[x][y]

    def handleSetup(self, event = None):
        dialog = SetupDialog(self.root)

        def apply():
            global width, height, pixels_per_cell, auto_step_delay
            width = int(dialog.width_var.get())
            height = int(dialog.height_var.get())
            pixels_per_cell = int(dialog.pixels_per_cell_var.get())
            auto_step_delay = int(dialog.auto_step_delay_var.get())
            self.update_grid()
            self.draw_grid()
            self.update_gui()

        dialog.apply = apply
        dialog.width_var.set(width)
        dialog.height_var.set(height)
        dialog.pixels_per_cell_var.set(pixels_per_cell)
        dialog.auto_step_delay_var.set(auto_step_delay)

    def handleClick(self, event):
        if not self.auto_step.get():
            x = int(event.x / pixels_per_cell)
            y = int(event.y / pixels_per_cell)
            self.grid[x][y] = 1 - self.grid[x][y]
            self.update_gui()

    def performStep(self):
        # Leeres neues Grid erzeugen
        next_grid = [[0 for y in range(height)] for x in range(width)]
        # Schritt berechnen
        step(self.grid, next_grid)
        self.grid = next_grid
        self.update_gui()

    def handleReset(self, event = None):
        for x in range(width):
            for y in range(height):
                self.grid[x][y] = self.init_grid[x][y]
        self.update_gui()

    def handleOpen(self, event = None):
        global width, height

        # Einlesen der Daten
        file = askopenfile(title = "Öffnen...",
            defaultextension = ".cells",
            filetypes = [("Plaintext-Dateien (*.cells)", "*.cells")])
        f = open(file.name, "r")
        content = f.read()
        f.close()
        # Datei in ihre Zeilen zerlegen
        lines = content.strip().split("\n")
        # Whitespace-Zeichen entfernen
        lines = list(map(lambda line: list(line.strip()), lines))
        # Alle Kommentar-Zeilen entfernen, die mit ! beginnen
        data = list(filter(lambda line: line[0] != "!" if len(line) > 0 else True, lines))
        
        # Aktualisieren von Breite und Höhe
        # (Es werden zwei Zellen Rand auf allen Seiten hinzugefügt)
        height = len(data) + 4
        width = max(list(map(lambda line: len(line), data))) + 4
        self.draw_grid()

        # eingelesene Daten übernehmen
        self.grid = [[0 for y in range(height)] for x in range(width)]
        self.init_grid = [[0 for y in range(height)] for x in range(width)]
        for y in range(len(data)):
            for x in range(len(data[y])):
                if data[y][x] != '.':
                    self.init_grid[x+2][y+2] = 1
        self.handleReset()

    def handleSave(self, event = None):
        # Dateiname erfragen
        filename = asksaveasfilename(title = "Speichern unter...",
            defaultextension = ".cells",
            filetypes = [("Plaintext-Dateien (*.cells)", "*.cells")])
        # Dateiformat erzeugen
        # (Es werden zwei Zellen Rand auf allen Seiten ignoriert)
        data = [["." for x in range(width - 4)] for y in range(height - 4)]
        for y in range(len(data)):
            for x in range(len(data[y])):
                if self.grid[x + 2][y + 2] == 1:
                    data[y][x] = "O"
        content = "\n".join(map(lambda line: "".join(line), data))
        # Datei schreiben
        f = open(filename, "w")
        f.write(content)
        f.close()
        # Aktuelle Generation als initiale Generation übernehmen
        self.init_grid = self.grid
        self.handleReset()

    def handleQuit(self, event = None):
        self.root.quit()

    def handleStep(self, event = None):
        if not self.auto_step.get():
            self.performStep()

    def handleTimer(self):
        if self.auto_step.get():
            self.performStep()
            self.root.after(auto_step_delay, self.handleTimer)

    def play(self):
        if self.auto_step.get():
            self.handleTimer()

    def handlePlay(self, event = None):
        self.auto_step.set(not self.auto_step.get())
        self.play()

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = GameOfLife()
    # Bei der Verwendung in interaktiven Systemen wie IDLE muss die folgende
    # Zeile auskommentiert werden. In diesem Fall übernehmen diese Systeme
    # die Ausführung der Mainloop.
    app.run()
