# Author: Jarrod Merriman
# Date Created: 2020-01-20
# Date Modified: 2020-01-23

import random
import tkinter

# Uncomment the below line when testing.
# random.seed(100)

# The object containing the status of the Minesweeper board.
class Minesweeper_Board:

    # Initialize the board.
    def __init__(self, size_y, size_x):
        self.active = 0                                                 # Flag to keep status of the game.
        self.size_y = size_y                                            # Y dimension for the board.
        self.size_x = size_x                                            # X dimension for the board.
        self.bombs = [[0] * self.size_x for y in range(self.size_y)]    # 2D array of bomb locations.
        self.view = [[1] * self.size_x for y in range(self.size_y)]     # 2D array of the user's view with the board.

        # Random assignment of bombs to locations.
        for y in range(self.size_y):
            for x in range(self.size_x):
                bomb = random.randint(1,10)
                if bomb == 1:
                    self.bombs[y][x] = -1
                else:
                    self.bombs[y][x] = 0

        # Calculates the number of bombs next to an empty location.
        for y in range(self.size_y):
            for x in range(self.size_x):
                if self.bombs[y][x] != -1:
                    if x > 0 and y > 0 and self.bombs[y-1][x-1] == -1:                              self.bombs[y][x] += 1 # Top left location
                    if y > 0 and self.bombs[y-1][x] == -1:                                          self.bombs[y][x] += 1 # Top location
                    if x > 0 and y < self.size_y - 1 and self.bombs[y+1][x-1] == -1:                self.bombs[y][x] += 1 # Top right location
                    if x < self.size_x - 1 and self.bombs[y][x+1] == -1:                            self.bombs[y][x] += 1 # Right location
                    if x < self.size_x - 1 and y < self.size_y - 1 and self.bombs[y+1][x+1] == -1:  self.bombs[y][x] += 1 # Bottom Right location
                    if y < self.size_y - 1 and self.bombs[y+1][x] == -1:                            self.bombs[y][x] += 1 # Bottom location
                    if x < self.size_x - 1 and y > 0 and self.bombs[y-1][x+1] == -1:                self.bombs[y][x] += 1 # Bottom Left location
                    if x > 0 and self.bombs[y][x-1] == -1:                                          self.bombs[y][x] += 1 # Left location

    # User marks the location as containing a bomb.
    def SelectBomb(self, y, x):
        self.view[y][x] = -1
        self.IsComplete()

    # User Marks the location as not containing the bomb.
    def SelectSafe(self, y, x):
        if self.bombs[y][x] == -1:  # If there is a bomb.
            self.active = -1        # End board as failure.
        elif self.bombs[y][x] == 0: # If there is no bomb in the location or next to the location.
            self.SetView(y,x)       # Mark the locations with no bombs next to locations with no bombs as viewable by the user.
        else:                       # If there isnt a bomb.
            self.view[y][x] = 0     # Mark location as viewable by the user.
        self.IsComplete()

    # Recursive function to mark the locations with no bombs next to locations with no bombs as viewable by the user.
    # If there is a bomb next to the current location then the current location is marked as viewable.
    # If there is not a bomb next to the location then the function is called with this position.
    def SetView(self, y, x):
        self.view[y][x] = 0     # Mark current location as viewable by the user.
        # Top left location
        if y > 0 and x > 0 and self.view[y-1][x-1] == 1:
            if self.bombs[y-1][x-1] > 0:                                
                self.view[y-1][x-1] = 0
            elif self.bombs[y-1][x-1] == 0:
                self.SetView(y-1,x-1)
        # Top location
        if y > 0 and self.view[y-1][x] == 1:
            if self.bombs[y-1][x] > 0:
                self.view[y-1][x] = 0
            elif self.bombs[y-1][x] == 0:
                self.SetView(y-1,x)
        # Top right location
        if x < self.size_x-1 and y > 0 and self.view[y-1][x+1] == 1:
            if self.bombs[y-1][x+1] > 0:
                self.view[y-1][x+1] = 0
            elif self.bombs[y-1][x+1] == 0:
                self.SetView(y-1,x+1)
        # Right location
        if x < self.size_x-1 and self.view[y][x+1] == 1:
            if self.bombs[y][x+1] > 0:
                self.view[y][x+1] = 0
            elif self.bombs[y][x+1] == 0:
                self.SetView(y,x+1)
        # Bottom right location
        if x < self.size_x-1 and y < self.size_y-1 and self.view[y+1][x+1] == 1:
            if self.bombs[y+1][x+1] > 0:
                self.view[y+1][x+1] = 0
            elif self.bombs[y+1][x+1] == 0:
                self.SetView(y+1,x+1)
        # Bottom location
        if y < self.size_y-1 and self.view[y+1][x] == 1:
            if self.bombs[y+1][x] > 0:
                self.view[y+1][x] = 0
            elif self.bombs[y+1][x] == 0:
                self.SetView(y+1,x)
        # Bottom left location
        if x > 0 and y < self.size_y-1 and self.view[y+1][x-1] == 1:
            if self.bombs[y+1][x-1] > 0:
                self.view[y+1][x-1] = 0
            elif self.bombs[y+1][x-1] == 0:
                self.SetView(y+1,x-1)
        # Left location
        if x > 0 and self.view[y][x-1] == 1:
            if self.bombs[y][x-1] > 0:
                self.view[y][x-1] = 0
            elif self.bombs[y][x-1] == 0:
                self.SetView(y,x-1)
        self.IsComplete()

    def IsComplete(self):
        # Check if all locations have been marked.
        for y in range(self.size_y):
            for x in range(self.size_x):
                if self.view[y][x] != 1:
                    continue
                else:
                    return
        # Check if any locations have been misclassified as bombs.
        for y in range(self.size_y):
            for x in range(self.size_x):
                if self.view[y][x] == -1 and self.bombs[y][x] != -1:
                    return
                else:
                    continue
        # Mark game as successfully completed.
        self.active = 1

# Object containing the user interface that interacts with the Minesweeper board object.
class Minesweeper_GUI:

    # Initialize the GUI.
    def __init__(self, master, size_y, size_x):
        self.size_y = size_y                                                                            # Y dimension for the board.
        self.size_x = size_x                                                                            # X dimension for the board.
        self.board = Minesweeper_Board(self.size_y, self.size_x)                                        # Initialize the Minesweeper board.
        self.master = master
        master.title("Minesweeper")                                                                     # Title of the window.
        self.canvas = tkinter.Canvas(master, bg="white", width=50*self.size_x, height=50*self.size_y)   # Creates the canvas.
        self.canvas.pack(fill="both", expand=True)                                                      # Sets the canvas to fill the window.
        self.canvas.bind("<Configure>", self.Refresh)                                                   # Calls the function Refresh when the window size is changed.
        master.bind("<Button-1>", self.Left_Click)                                                      # Assigns the left mouse button to the function Left_Click.
        master.bind("<Button-3>", self.Right_Click)                                                     # Assigns the right mouse button to the function Right_Click.

    # Selects the location on the board as safe when the user selects the location with a left mouse click.
    def Left_Click(self, event):
        if self.board.active == 0:  # If the game is active.
            x = int(event.x * self.size_x / self.width)
            y = int(event.y * self.size_y / self.height)
            self.board.SelectSafe(y,x)
            self.Refresh_Board()

    # Selects the location on the board as containing a bomb when the user selects the location with a right mouse click.
    def Right_Click(self, event):
        if self.board.active == 0:  # If the game is active.
            x = int(event.x * self.size_x / self.width)
            y = int(event.y * self.size_y / self.height)
            self.board.SelectBomb(y,x)
            self.Refresh_Board()

    # Refreshes the board when the window size is changed.
    def Refresh(self, event):
        self.Refresh_Board()

    # Refreshes the board.
    def Refresh_Board(self):
        self.width = self.master.winfo_width()      # Gets the width of the window.
        self.height = self.master.winfo_height()    # Gets the height of the window.
        self.canvas.delete("all")                   # Clears the canvas.
        font_size = int(self.width / 7)             # Sets a default font size.
        if self.board.active == 0:                  # If the game is active.
            
            # Determines a font size of the numbers that will fit in the window's current size.
            if self.width <= self.height:   font_size = int(self.width / self.size_x - self.size_x)
            elif self.height < self.width:  font_size = int(self.height / self.size_y - self.size_y)

            # Creates the boxes for the locations.
            for y in range(self.size_y):
                self.canvas.create_line(0, self.height / self.size_y * y, self.width, self.height / self.size_y * y)
            for x in range(self.size_x):
                self.canvas.create_line(self.width / self.size_x * x, 0, self.width / self.size_x * x, self.height)

            # Displays an asterisk on an unmarked board location.
            # Displays an exclamation mark on what a user selects as a bomb.
            # Displays the value on bombs next to the location that are viewable to the user.
            for y in range(self.size_y):
                for x in range(self.size_x):
                    if self.board.view[y][x] == 0:
                        value = self.board.bombs[y][x]
                    elif self.board.view[y][x] == -1:
                        value = "!"
                    else:
                        value = "*"
                    self.canvas.create_text(self.width * (x+0.5) / self.size_x, self.height * (y+0.5) / self.size_y, font=("Arial", font_size), text=value)

        elif self.board.active == 1:    # Displays success when the user has successfully completed the board.
            self.canvas.create_text(self.width * 0.5, self.height * 0.5, font=("Arial", font_size), text="SUCCESS")
        elif self.board.active == -1:   # Displays failure when the user has selected a bomb.
            self.canvas.create_text(self.width * 0.5, self.height * 0.5, font=("Arial", font_size), text="FAILURE")
    
if __name__ == "__main__":
    root = tkinter.Tk()
    board = Minesweeper_GUI(root, 15, 30)
    root.mainloop()
