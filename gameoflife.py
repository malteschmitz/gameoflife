# Game of Life in Python

# Für eine Schritt die Taste n oder die Leertaste drücken.
# Zum Starten und Stoppen des automatischen Ablaufs die
# Taste p drücken.

# Anzahl Zellen auf dem Bildschirm
width = 40
height = 30

# Anzahl Pixel, die für eine Zelle verwendet werden
pixels_per_cell = 20

# Verzögerung für den automatischen Ablauf in Millisekunden
auto_step_delay = 200

# An dieser Funktion müssen Änderungen vorgenommen werden.
def step(grid, new_grid):
    '''Diese Funktion führt einen Schritt des Game of Life aus.
       Der aktuelle Zustand befindet sich dabei in grid und der
       neue Zustand wird in new_grid gesetzt. Dabei gelten
       die folgenden Regeln: Eine Zelle wird geboren, wenn es
       in ihrer Umgebung genau 3 Zellen gibt.
       Eine Zelle überlebt, wenn es in ihrer
       Umgebung genau 2 oder 3 Zellen gibt. Sonst stirbt sie an
       Vereinsamung oder Überbevölkerung. Lebt eine Zelle,
       befindet sich an der Koordinate in grid eine 1, sonst
       eine 0. Die erste Koordinate ist die X-Koordinate,
       die links mit 0 beginnt. Die zweite Koordinate ist die
       Y-Koordinate, die oben mit 0 beginnt.'''
    for x in range(width):
        for y in range(height):
            # Anzahl Nachbarn der Zelle an Position (x,y) berechnen
            nachbarn = 0
            for delta_x, delta_y in [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]:
                x_nachbar = x + delta_x
                y_nachbar = y + delta_y
                # Achtung: Am Rand des Feldes existieren nicht alle Nachbarn
                if x_nachbar >= 0 and x_nachbar < width and y_nachbar >= 0 and y_nachbar < height:
                    nachbarn = nachbarn + grid[x_nachbar][y_nachbar]
            # Lasse neue Zellen entstehen
            if (grid[x][y] == 1 and nachbarn == 2) or nachbarn == 3:
                new_grid[x][y] = 1
            else:
                new_grid[x][y] = 0


# An dieser Funktion müssen Änderungen vorgenommen werden.
def init(grid):
    '''Diese Funktion setzt einige Zellen für die
       initiale Belegung auf das Feld.'''
    # Glider
    #grid[2][2] = 1
    #grid[3][3] = 1
    #grid[1][4] = 1
    #grid[2][4] = 1
    #grid[3][4] = 1
    
    # Blinker
    #grid[2][2] = 1
    #grid[2][3] = 1
    #grid[2][4] = 1

    # Glider Gun
    template =   """......................................
                    .........................1............
                    .......................1.1............
                    .............11......11............11.
                    ............1...1....11............11.
                    .11........1.....1...11...............
                    .11........1...1.11....1.1............
                    ...........1.....1.......1............
                    ............1...1.....................
                    .............11.......................
                    ......................................"""
    grid_template = list(map(lambda line: list(line.strip()), template.split("\n")))
    for y in range(len(grid_template)):
        for x in range(len(grid_template[0])):
            if grid_template[y][x] == '1':
                grid[x][y] = 1


#############################################################

# Die folgende Klasse organisiert die GUI und muss nicht mehr angepasst werden.

# Laden der Komponenten für die GUI
from tkinter import *

class GameOfLife():
    def __init__(self):
        self.root = Tk()

        # Initialisierung des Grids
        self.grid = [[0 for y in range(height)] for x in range(width)]

        # Berechnung der Größe des Fensters
        self.width_pixels = width * pixels_per_cell - 1
        self.height_pixels = height * pixels_per_cell - 1

        # Zeichenfläche erzeugen
        self.canvas = Canvas(self.root, width = self.width_pixels,
            height = self.height_pixels,
            bd=0, highlightthickness=0, relief='ridge')

        # Die Zeichenfläche soll Tastaturereignisse erhalten
        self.canvas.focus_set()

        # Gitter zeichnen
        for x in range(1, width):
            self.canvas.create_line(x * pixels_per_cell - 1, 0,
                x * pixels_per_cell - 1, self.height_pixels - 1, fill = "gray")
        for y in range(1, height):
            self.canvas.create_line(0, y * pixels_per_cell - 1,
                self.width_pixels - 1, y * pixels_per_cell - 1, fill = "gray")
        
        # Darstellung der Zellen
        self.circles = [[None for y in range(height)] for x in range(width)]

        # Initiale Belegung erzeugen
        init(self.grid)
        self.update_gui()

        # Abfangen von Ereignissen
        self.canvas.bind("<n>", self.handleStep)
        self.canvas.bind("<Key-space>", self.handleStep)
        self.canvas.bind("<p>", self.handlePlay)

        # Größe der Canvas auf ihren Inhalt anpassen
        self.canvas.pack()

        # automatisches Weiterschalten ist initial nicht aktiv
        self.auto_step = False

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

    def performStep(self):
        # Leeres neues Grid erzeugen
        next_grid = [[0 for y in range(height)] for x in range(width)]
        # Schritt berechnen
        step(self.grid, next_grid)
        self.grid = next_grid
        self.update_gui()

    def handleStep(self, event = None):
        if not self.auto_step:
            self.performStep()

    def handleTimer(self):
        if self.auto_step:
            self.performStep()
            self.root.after(auto_step_delay, self.handleTimer)

    def handlePlay(self, event = None):
        self.auto_step = not self.auto_step
        if self.auto_step:
            self.handleTimer()

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = GameOfLife()
    # Bei der Verwendung in interaktiven Systemen wie IDLE muss die folgende
    # Zeile auskommentiert werden. In diesem Fall übernehmen diese Systeme
    # die Ausführung der Mainloop.
    # app.run()
