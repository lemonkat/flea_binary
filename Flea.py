class Flea:
  def __init__(self, rules: dict, x: int, y: int, r: int, board, color:str):
    self.rules = rules
    self.x = x % (board.max_x)
    self.y = y % (board.max_y)
    self.r = r
    self.board = board
    self.color = color

  def paint(self):
    if (self.r == 0):
        self.board.display_canvas.create_polygon(
          (self.x) * self.board.cell_size,
          (self.y) * self.board.cell_size,
          (self.x) * self.board.cell_size,
          (self.y + 1) * self.board.cell_size,
          (self.x + 1) * self.board.cell_size,
          (self.y + 0.5) * self.board.cell_size,
          fill=self.color
        )
    elif (self.r == 1):
      self.board.display_canvas.create_polygon(
        (self.x) * self.board.cell_size,
        (self.y) * self.board.cell_size,
        (self.x + 1) * self.board.cell_size,
        (self.y) * self.board.cell_size,
        (self.x + 0.5) * self.board.cell_size,
        (self.y + 1) * self.board.cell_size,
        fill=self.color
      )
    elif (self.r == 2):
      self.board.display_canvas.create_polygon(
        (self.x + 1) * self.board.cell_size,
        (self.y) * self.board.cell_size,
        (self.x + 1) * self.board.cell_size,
        (self.y + 1) * self.board.cell_size,
        (self.x) * self.board.cell_size,
        (self.y + 0.5) * self.board.cell_size,
        fill=self.color
      )
    else:
      self.board.display_canvas.create_polygon(
        (self.x) * self.board.cell_size,
        (self.y + 1) * self.board.cell_size,
        (self.x + 1) * self.board.cell_size,
        (self.y + 1) * self.board.cell_size,
        (self.x + 0.5) * self.board.cell_size,
        (self.y) * self.board.cell_size,
        fill=self.color
      )
  def step(self, times: int = 1):
    for i in range(times):
      if self.board.board[self.y][self.x] in self.rules.keys():
        self.board.updated_coords.append([self.x, self.y])
        current_rules = self.rules[self.board.board[self.y][self.x]]
        self.board.board[self.y][self.x] = current_rules["s"]
        self.r = (self.r + int(current_rules["r"])) % 4
        if self.r == 0:
          if self.x != self.board.max_x - 1:
            self.x += 1
          else:
            self.board.board[self.y][self.x] = " "
        elif self.r == 1:
          if self.y != self.board.max_y - 1:
            self.y += 1
          else:
            self.board.board[self.y][self.x] = " "
        elif self.r == 2:
          if self.x != 0:
            self.x -= 1
          else:
            self.board.board[self.y][self.x] = " "
        else:
          if self.y != 0:
            self.y -= 1
          else:
            self.board.board[self.y][self.x] = " "
      else:
        self.board.dead_fleas.append(self)
