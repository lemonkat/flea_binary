from tkinter import Tk, Canvas, Scrollbar, Frame
from Flea import Flea

class Board:

  def __init__(self, max_x: int, max_y: int, cell_size: int, color_profile:dict, y_mult = 1):
    self.root = Tk()
    self.updated_coords = []
    self.container = Frame(self.root)
    self.display_canvas = Canvas(
      self.container,
      scrollregion=(0, 0, max_x * cell_size, max_y * cell_size),
      width=max_x * cell_size,
      height=max_x * cell_size * y_mult
    )
    self.scrollbar = Scrollbar(self.container, orient="vertical", command=self.display_canvas.yview)
    self.display_canvas.config(yscrollcommand=self.scrollbar.set)
    self.max_x = max_x
    self.max_y = max_y
    self.fleas = []
    self.dead_fleas = []
    self.board = []
    self.color_profile = color_profile
    for y in range(max_y):
      row = []
      for x in range(max_x):
        row.append(" ")
      self.board.append(row.copy())
    self.cell_size = cell_size

    self.update()

  def reload(self):
    for y in range(len(self.board)):
      for x in range(len(self.board[0])):
        self.updated_coords.append([x, y])

  def add_flea(self, rules: dict, x: int, y: int, d: int, color:str) -> Flea:
    f = Flea(rules, x, y, d, self, color)
    self.fleas.append(f)
    f.paint()
    return f

  def step(self, times: int = 1):
    for i in range(times):
      for f in self.fleas:
        if not f in self.dead_fleas:
          f.step()
    

  def paint(self, color, x, y):
    self.display_canvas.create_rectangle(
      (x) * self.cell_size,
      (y) * self.cell_size,
      (x + 1) * self.cell_size,
      (y + 1) * self.cell_size,
      fill=self.color_profile[color]
      )
    

  def update(self, follow=False):
    #self.display_canvas.delete("all")
    for pair in self.updated_coords:
      x = pair[0]
      y = pair[1]
      self.paint(self.board[y][x], x, y)
    self.updated_coords = []
    for f in self.fleas:
      if not f in self.dead_fleas:
        f.paint()
    self.scrollbar.pack(side = "right" ,fill = "y")
    self.display_canvas.pack(side = "left",fill = "both" ,expand=True)
    self.container.pack()
    self.root.update_idletasks()
    self.root.update()

  def is_flea_at(self, x:int, y:int) -> bool:
    x = x % self.max_x
    y = y % self.max_y
    for f in self.fleas:
      if f.x == x and f.y == y:
        return True
    return False

